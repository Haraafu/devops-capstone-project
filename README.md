# devops-capstone-project

[![CI Build](https://github.com/Haraafu/devops-capstone-project/actions/workflows/ci-build.yaml/badge.svg?branch=main)](https://github.com/Haraafu/devops-capstone-project/actions/workflows/ci-build.yaml)

Customer Accounts microservice for the IBM DevOps and Software Engineering Capstone. A Flask REST API manages customer names, email addresses, postal addresses, phone numbers, and joining dates in PostgreSQL. The project includes TDD tests, security headers, CORS policy, GitHub Actions CI, Docker packaging, OpenShift deployment, and a Tekton CD pipeline.

**Start with [START_HERE.md](START_HERE.md).** The full [33-item submission checklist](docs/AI_GRADED_CHECKLIST.md) distinguishes implemented source from evidence still requiring GitHub or a running cluster. The repository is public and real CI has passed; see the current status and provenance for the exact run. OpenShift/Tekton lab execution is still pending.

## Run locally

Python 3.9 matches the required lab runtime. Use the IBM Skills Network lab for the prescribed Python version and OpenShift environment. These legacy versions are retained for course compatibility; this is a course MVP, with no authentication or authorization added beyond the assignment's security headers and CORS requirements.

```bash
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Start a disposable PostgreSQL database, e.g. with Docker:
docker run -d --name accounts-postgres -p 5432:5432 \
  -e POSTGRES_USER=accounts -e POSTGRES_PASSWORD=localdev \
  -e POSTGRES_DB=accounts postgres:alpine
export DATABASE_URI=postgresql://accounts:localdev@localhost:5432/accounts
# Wait for pg_isready before importing the service.
gunicorn --bind 0.0.0.0:8080 service:app
```

Or run `docker compose up --build` to start the service and PostgreSQL together. This uses disposable local credentials; OpenShift credentials are generated separately as Secrets.

For quick local smoke tests without PostgreSQL, explicitly set `DATABASE_URI=sqlite:////tmp/accounts.db`. SQLite runs are identified in the evidence notes and do not establish PostgreSQL or cluster success.

## API

| Method | Path | Result |
|---|---|---|
| GET | `/` | Service information, 200 |
| GET | `/health` | `{"status":"OK"}`, 200 |
| POST | `/accounts` | Create, 201 and resource Location |
| GET | `/accounts` | List, 200 JSON array |
| GET | `/accounts/{id}` | Read, 200 or 404 |
| PUT | `/accounts/{id}` | Replace editable fields, 200 or 404 |
| DELETE | `/accounts/{id}` | Idempotent delete, 204 |

Example input:
```json
{
  "name": "Ada Lovelace",
  "email": "ada@example.test",
  "address": "Jakarta, Indonesia",
  "phone_number": "+62-21-555-0100",
  "date_joined": "2026-10-30"
}
```

`name`, `email`, and `address` must be non-empty strings within their database length limits. `phone_number` and `date_joined` are optional; the date defaults to today and must use YYYY-MM-DD when present. The server controls IDs. PUT validates the full replacement before mutating the account. JSON errors use status 400, 404, 405, or 415 as appropriate.

## Test and quality gates

Use a **disposable test database**, because the tests clear its accounts table.

```bash
export DATABASE_URI=postgresql://accounts:localdev@localhost:5432/testdb
bash scripts/test.sh
```

`nosetests` enforces 95% coverage through `setup.cfg`. CI also runs Flake8, Pylint with a minimum score of 8, and coverage reporting. The CI database is `postgres:alpine`, as required by the lab. The complete local output and TDD failing-test output are in `evidence/`.

## Security

Flask-Talisman configures CSP, frame protection, content-type protection, referrer policy, and HTTPS HSTS. Flask-CORS permits the exact origins in the comma-separated `CORS_ORIGINS` variable (default `http://localhost:3000`) for the accounts API. Untrusted origins receive no allow-origin header. CORS governs browser access; it does not authenticate callers.

HTTPS redirect enforcement is handled by the OpenShift edge Route. Talisman uses `force_https=False` so the service and health probes remain accessible over internal HTTP and lab port forwarding. Secrets are injected through Kubernetes Secrets, never committed in YAML.

## Delivery

`Dockerfile` uses `python:3.9-slim`, installs requirements, runs as an unprivileged user, and starts Gunicorn on port 8080. `deploy/` provisions the accounts service, persistent PostgreSQL, and an HTTPS OpenShift route. The PostgreSQL cluster image supports OpenShift's arbitrary UID policy.

`tekton/` defines clone → lint → test → build → deploy. Tests use a separate PostgreSQL sidecar. The build task invokes an OpenShift Docker BuildConfig, which pushes the image to IBM Cloud Container Registry; it does not require a Docker daemon inside a Tekton step. Deployment reuses the manual deployment manifests and waits for rollout success. See [the runbook](docs/RUNBOOK.md) for prerequisites and capture commands.

## Planning and submission

- [Ten user stories](docs/stories.json) with roles, assumptions, Gherkin criteria, labels, points, and sprint assignments.
- [Sprint plan](docs/SPRINT_PLAN.md) with three one-week sprints.
- [GitHub automation](scripts/board.py) creates the real board in evidence stages.
- [Evidence checklist](docs/AI_GRADED_CHECKLIST.md) maps all 33 requirements to exact filenames and URLs.
- `python scripts/validate-submission.py` reports absent evidence; it never creates substitute screenshots or logs.

## Attribution and license

Based on [IBM's DevOps Capstone template](https://github.com/ibm-developer-skills-network/aolwx-devops-capstone-template), starter commit `cc3a90911a8ba9d1b06a2b7114f17386d43464c2`. Original source and notices are retained under the Apache-2.0 license in `LICENSE`.
