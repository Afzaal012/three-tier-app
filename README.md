# Three-Tier Student App — Docker Compose + Jenkins

Nginx frontend -> Flask API -> MySQL database. Only the frontend is published to the host; API and database use a private Docker network.

## Requirements
- Docker Engine + Docker Compose plugin (or Docker Desktop)
- Git
- Jenkins with Git and Pipeline plugins
- Jenkins service account allowed to use Docker on the lab host. Docker group membership effectively grants root-level access; use a controlled lab instance.

## Run locally
Copy `.env.example` to `.env`, then run from the project root:

```bash
docker compose up --build -d
docker compose ps
curl http://localhost:8081/api/health
curl http://localhost:8081/api/students
```

Open http://localhost:8081 and click **Load Students**.

View logs with `docker compose logs`. Stop services with `docker compose down`. To also delete the local database volume (destructive), use `docker compose down --volumes`.

## Push to GitHub
Create an empty repository named `three-tier-app`, then:

```bash
git init
git add .
git commit -m "Add three-tier Docker app and Jenkins pipelines"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/three-tier-app.git
git push -u origin main
```

Replace `YOUR_GITHUB_USERNAME` in the remote and all three Jenkinsfiles.

## Jenkins: create three Pipeline jobs
For each job select **Pipeline script from SCM**, SCM **Git**, your GitHub URL, branch `*/main`, and no credentials if the repository is public.

| Job | Script Path | Purpose |
|---|---|---|
| `01-Docker-Build` | `Jenkinsfile.build` | Validate and build images |
| `02-Docker-Test` | `Jenkinsfile.test` | Run isolated integration tests |
| `03-Docker-Deploy` | `Jenkinsfile.deploy` | Deploy stack on port 8081 |

Configure Job 1 to trigger Job 2 only if stable. Configure Job 2 to trigger Job 3 only if stable. Start by building Job 1 manually.

All jobs assume the same EC2 host and Docker daemon. If using different agents/hosts, push images to a registry such as ECR or Docker Hub.

## EC2 security group
Allow TCP 8080 from your IP for Jenkins and TCP 8081 from your IP for the app. Restrict SSH 22 to your IP. Do not publish MySQL 3306.

App URL: `http://EC2_PUBLIC_IP:8081`

## Security and data notes
- The default passwords are for disposable lab practice only. Replace them before real use and keep secrets out of Git.
- The test job removes only its `three-tier-test` project and volume, not the production project.
- Do not run tests against production data.
- `database/init.sql` runs only when MySQL initializes a fresh data directory. Changes to it do not automatically migrate an existing database.
- This is a learning example, not a zero-downtime or rollback-ready production deployment.
