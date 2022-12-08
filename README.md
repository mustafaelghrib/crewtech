## Crewtech
A full production backend API built with these tech stacks:
- REST API: _Django and Django REST Framework_.
- Database: _PostgresSQL_.
- Unit Testing: _Pytest_.
- Packaging Management: _Poetry_.
- Containerization: _Docker and Docker Compose_.
- Cloud Provider: _AWS: VPC, EC2, RDS, S3, ECR_.
- Infrastructure as Code: _Terraform_.
- CI/CD: _CircleCI_.

---

### Backend:

**Set the environment variables:**
- Copy `backend/.env.sample/` folder and rename it to `backend/.env/`.

**Run the base environment locally:**
- Update the `backend/.env/.env.base` file.
- Run Docker Compose:
  ```shell
  docker compose -f backend/.docker-compose/base.yml up -d --build
  ```
- Run Pytest:
  ```shell
  docker exec -it crewtech_base_django /bin/bash -c "/opt/venv/bin/pytest"
  ```

**Run the production environment locally:**
- Get the environment variables from the infrastructure:
  ```shell
  python scripts/get_infra_output.py --c=infrastructure/docker-compose.yml --m=aws --f=env
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

-
- terraform apply all
  ```shell
  docker compose -f infrastructure/.docker-compose.yml run --rm terraform apply --auto-approve
  ```
- terraform apply aws
  ```shell
  docker compose -f infrastructure/.docker-compose.yml run --rm terraform apply -target="module.aws" --auto-approve
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

- 
- terraform output aws
  ```shell
  docker compose -f infrastructure/.docker-compose.yml run --rm terraform output aws
  ```

---

