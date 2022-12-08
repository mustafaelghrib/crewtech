const CircleCI = require('@circleci/circleci-config-sdk');
const fs = require('fs');
const argv = require('minimist')(process.argv.slice(2));

const project = "crewtech"
const env = "production"

const ubuntu = new CircleCI.executors.MachineExecutor("medium", "ubuntu-2204:2022.10.1")

const circleci_config = new CircleCI.Config()

const deploy_workflow = new CircleCI.Workflow("deploy_to_aws_ec2")
circleci_config.addWorkflow(deploy_workflow)

const run_unit_tests = () => {

    const env_vars = {
        "DATABASE_NAME": "$POSTGRES_DB",
        "DATABASE_USER": "$POSTGRES_USER",
        "DATABASE_PASSWORD": "$POSTGRES_PASSWORD",
        "DATABASE_HOST": "$POSTGRES_HOST",
        "DATABASE_PORT": "$POSTGRES_PORT",
    }

    const postgres_image = new CircleCI.types.executors.docker.DockerImage(
        "cimg/postgres:13.8",
        undefined,
        undefined,
        undefined,
        undefined,
        env_vars
    )

    const docker_python = new CircleCI.executors.DockerExecutor("cimg/python:3.10", "medium")
    docker_python.addServiceImage(postgres_image)

    const job = new CircleCI.Job("run_unit_tests", docker_python)
    circleci_config.addJob(job)

    job.addStep(new CircleCI.commands.Checkout())
    job.addStep(new CircleCI.commands.Run({
        name: "Install Packages",
        working_directory: "backend",
        command:
            "python3 -m venv venv;\n" +
            ". venv/bin/activate;\n" +
            "python -m pip install --upgrade pip;\n" +
            "pip install poetry;\n" +
            "poetry config virtualenvs.create false --local;\n" +
            "poetry install;",
    }))
    job.addStep(new CircleCI.commands.Run({
        name: "Run Pytest",
        working_directory: "backend",
        command: `venv/bin/pytest`
    }))

    deploy_workflow.addJob(job, {
        context: [`${project}-common-context`],
        filters: {branches: {only: ["main"]}},
    })

}

const build_and_push_docker_image = () => {

    const job = new CircleCI.Job("build_and_push_docker_image", ubuntu)
    circleci_config.addJob(job)

    job.addStep(new CircleCI.commands.Checkout())
    job.addStep(new CircleCI.commands.Run({
        name: "Setup AWS ECR",
        command: "sh scripts/install_aws_cli.sh -C $AWS_ACCESS_KEY -S $AWS_SECRET_KEY -R $AWS_REGION -A $AWS_ACCOUNT_ID"
    }))
    job.addStep(new CircleCI.commands.Run({
        name: "Build a Docker Image",
        command: "docker build -t $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$DOCKER_IMAGE:latest -f backend/Dockerfile backend --build-arg ENVIRONMENT=production"
    }))
    job.addStep(new CircleCI.commands.Run({
        name: "Push to AWS ECR",
        command: "docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$DOCKER_IMAGE:latest"
    }))

    deploy_workflow.addJob(job, {
        context: [`${project}-common-context`],
        filters: {branches: {only: ["main"]}},
        requires: ['run_unit_tests']
    })

}

const deploy_to_production_server = () => {

    const job = new CircleCI.Job("deploy_to_production_server", ubuntu)
    circleci_config.addJob(job)

    job.addStep(new CircleCI.commands.Checkout())
    job.addStep(new CircleCI.commands.Run({
        name: "Get the environment variables from CircleCI",
        command: `python3 scripts/get_circleci_env.py --env=${env} --token=$CIRCLE_TOKEN --owner=$CIRCLE_OWNER_ID`
    }))
    job.addStep(new CircleCI.commands.Run({
        name: "Append server env vars to env file",
        command:
            `echo "AWS_ACCOUNT_ID=$AWS_ACCOUNT_ID" >> .env.${env};\n` +
            `echo "AWS_REGION=$AWS_REGION" >> .env.${env};\n` +
            `echo "DOCKER_IMAGE=$DOCKER_IMAGE" >> .env.${env};`
    }))
    job.addStep(new CircleCI.commands.Run({
        name: "Copy the env file and the run script to the server",
        command: `rsync .env.${env} scripts/run_backend.py $EC2_INSTANCE:/home/ubuntu`
    }))
    job.addStep(new CircleCI.commands.Run({
        name: "Run the script",
        command: `ssh $EC2_INSTANCE 'source .env.${env} && python3 run_backend.py --env=.env.${env} --image=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$DOCKER_IMAGE:latest'`
    }))

    deploy_workflow.addJob(job, {
        context: [`${project}-common-context`, `${project}-${env}-context`],
        filters: {branches: {only: ["main"]}},
        requires: ['run_unit_tests', 'build_and_push_docker_image']
    })
}

run_unit_tests()
build_and_push_docker_image()
deploy_to_production_server()

const yml_config = circleci_config.stringify();

fs.writeFileSync(argv.f, yml_config, {flag: 'w'});
fs.readFileSync(argv.f, 'utf-8');

