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

