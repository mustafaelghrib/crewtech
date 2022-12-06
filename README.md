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

**Run Terraform Commands:**

- terraform init
  ```shell
  docker compose -f infrastructure/.docker-compose.yml run --rm terraform init -backend-config=.backend.hcl
  ```
- terraform plan
  ```shell
  docker compose -f infrastructure/.docker-compose.yml run --rm terraform plan
  ```
- terraform apply
  ```shell
  docker compose -f infrastructure/.docker-compose.yml run --rm terraform apply --auto-approve
  ```
- terraform destroy
  ```shell
  docker compose -f infrastructure/.docker-compose.yml run --rm terraform destroy --auto-approve
  ```

---

