## Crewtech
A full production backend API built with these tech stacks:
- REST API: _Django and Django REST Framework_.
- Database: _PostgresSQL_.
- Unit Testing: _Pytest_.
- Packaging Management: _Poetry_.
- Containerization: _Docker and Docker Compose_.
- Cloud Provider: _AWS: EC2, RDS, S3, ECR_.
- Infrastructure as Code: _Terraform_.
- CI/CD: _CircleCI_.
- Version Control: _Git and GitHub_.

---

### Backend:

**Set the environment variables:**
- Copy `backend/.env.sample/` folder and rename it to `backend/.env/`.

**Run the development environment locally:**
- Update the `backend/.env/.env.development` file.
- Run Docker Compose:
  ```shell
  docker compose -f backend/.docker-compose/development.yml up -d --build
  ```
- Run Pytest:
  ```shell
  docker exec -it crewtech_development_django /bin/bash -c "/opt/venv/bin/pytest"
  ```

**Run the production environment locally:**
- Get the environment variables from the infrastructure:
  ```shell
  python scripts/get_infra_output.py --c=infrastructure/.docker-compose.yml --m=aws --f=env
  ```
- Update the `backend/.env/.env.production` file.
- Run Docker Compose:
  ```shell
  docker compose -f backend/.docker-compose/production.yml up -d --build
  ```

---

### Infrastructure:

**Setup Terraform Backend:**
- Create a bucket on AWS S3.
  ```shell
  aws s3api create-bucket --bucket crewtech-terraform-backend --region us-east-1
  ```
- Create a file and name it to `.backend.hcl` under `infrastructure` folder.
- Copy the content of file `.backend.hcl.sample` inside it and fill the values.

**Setup Secrets:**
- Create a file with the name `.secrets.auto.tfvars` under `infrastructure` folder.
- Copy the contents of file `.secrets.auto.tfvars.sample` inside it and fill the values.

**Setup SSH:**
- Generate an SSH Key.
- Create a folder with the name `.ssh` under `infrastructure` folder.
- Copy `id_rsa.pub` and `id_rsa` file to `infrastructure/.ssh`.

**Run Terraform Commands:**

- terraform init
  ```shell
  docker compose -f infrastructure/.docker-compose.yml run --rm terraform init -backend-config=.backend.hcl
  ```

-
- terraform plan all
  ```shell
  docker compose -f infrastructure/.docker-compose.yml run --rm terraform plan
  ```
- terraform plan aws
  ```shell
  docker compose -f infrastructure/.docker-compose.yml run --rm terraform plan -target="module.aws"
  ```
- terraform plan circleci
  ```shell
  docker compose -f infrastructure/.docker-compose.yml run --rm terraform plan -target="module.circleci" --auto-approve
  ```

-
- terraform apply all
  ```shell
  docker compose -f infrastructure/.docker-compose.yml run --rm terraform apply --auto-approve
  ```
- terraform apply aws
  ```shell
  docker compose -f infrastructure/.docker-compose.yml run --rm terraform apply -target="module.aws" --auto-approve
  ```
- terraform apply circleci
  ```shell
  docker compose -f infrastructure/.docker-compose.yml run --rm terraform apply -target="module.circleci" --auto-approve
  ```

- 
- terraform destroy all
  ```shell
  docker compose -f infrastructure/.docker-compose.yml run --rm terraform destroy --auto-approve
  ```
- terraform destroy aws
  ```shell
  docker compose -f infrastructure/.docker-compose.yml run --rm terraform destroy -target="module.aws" --auto-approve
  ```
- terraform destroy circleci
  ```shell
  docker compose -f infrastructure/.docker-compose.yml run --rm terraform destroy -target="module.circleci" --auto-approve
  ```

- 
- terraform output aws
  ```shell
  docker compose -f infrastructure/.docker-compose.yml run --rm terraform output aws
  ```

---

### Deployment:

#### Deploy Manually:
- Read the infrastructure section and create the resources on AWS.
- Export values and change them according to your infrastructure:
  ```shell
  export ENVIRONMENT=production;
  
  export AWS_REGION=<YOUR_AWS_REGION>;
  export AWS_ACCOUNT_ID=<YOUR_AWS_ACCOUNT_ID>;
  
  export DOCKER_IMG=<YOUR_DOCKER_IMG_NAME>;
  export DOCKER_TAG=<YOUR_DOCKER_IMG_TAG>;
  
  export ECR_REPO=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com;
  
  export FINAL_IMAGE=$ECR_REPO/$DOCKER_IMG:$DOCKER_TAG;
  
  export INSTANCE_USER=<YOUR_INSTANCE_USER>;
  export INSTANCE_IP=<YOUR_INSTANCE_IP>;
  ```
- Login to AWS ECR:
  ```shell
  aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REPO
  ```
- Build Docker Image:
  ```shell
  docker build -t $FINAL_IMAGE -f backend/Dockerfile backend --build-arg ENVIRONMENT=$ENVIRONMENT
  ```
- Push to AWS ECR:
  ```shell
  docker push $FINAL_IMAGE
  ```

- Copy the env file and the run script to the server:
  ```shell
  rsync backend/.env/.env.$ENVIRONMENT scripts/run_backend.py $INSTANCE_USER@$INSTANCE_IP:/home/$INSTANCE_USER
  ```

- Run Docker image on the server:
  ```shell
  ssh $INSTANCE_USER@$INSTANCE_IP "python3 run_backend.py --env=.env.$ENVIRONMENT --image=$FINAL_IMAGE"
  ```

#### Deploy with CircleCI:
- Get the environment variables from the infrastructure:
  ```shell
  python scripts/get_infra_output.py --c=infrastructure/.docker-compose.yml --m=aws --f=circleci
  ```
- Store environment variables using CircleCI module in the infrastructure folder.
- Create a CircleCI config file using `scripts/generate_circleci_config` script.

---

