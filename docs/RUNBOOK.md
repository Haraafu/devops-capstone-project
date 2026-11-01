# Execution and submission runbook

This runbook creates real evidence in chronological order. All commands run from the repository root. Use Python 3.9 and a disposable test database. Command blocks use bash (the Skills Network lab or WSL works on Windows).

## 1. GitHub repository and initial planning

Install GitHub CLI (`gh`) and authenticate on your own machine or lab terminal. Enable project access:

```bash
gh auth login
gh auth refresh -s project
python3 scripts/board.py init --start YYYY-MM-DD
```

Replace YYYY-MM-DD with your actual Sprint 1 start date. The script creates a **public**, template-based `devops-capstone-project` in your personal account; it refuses to overwrite an existing repository. It creates a GitHub Project with eight Status values (the seven required columns plus Closed), an iteration field with three one-week sprints, a Story Points field, three milestones, and seven original issues.

The GitHub API automation is prepared but has not been live-tested against your account. If a command reports an API/scope error, fix the stated permission/schema problem before continuing. `.board-state.json` stores the exact created identifiers; preserve it. If init stops partway, do not delete the repository or keep repeating create commands: resume/fix the partially created board using its saved IDs.

Open the printed project URL. Change the layout to **Board**, group by **Status**, and show **Labels**, **Story Points**, and **Sprint**. Save the view. Make the column width/zoom sufficient to show all seven initial story titles in New issues. Capture the actual browser board as `evidence/Planning-userstories-done.png`.

```bash
python3 scripts/board.py triage
# Capture planning-productbacklog-done.png: five Product backlog, two Icebox.
python3 scripts/board.py refine
# Capture planning-labels-done.png: labels visible.
python3 scripts/board.py sprint1
# Filter Sprint 1; capture planning-kanban-done.png.
```

Do not close GitHub issues during planning. Capture each screenshot before moving to the next state. The screenshot names match the final AI checklist; its first screenshot uses an uppercase P.

## 2. Publish the implementation through a pull request

```bash
python3 scripts/publish.py
```

This updates the badge to your actual account, copies the implementation onto a `development/capstone-implementation` branch in your own template-based repository, pushes it, and opens a PR to main. It does not automatically merge or claim the work was performed across three historical remote sprints. The included red-test logs document the local TDD sequence. If your course additionally checks separate sprint PR histories, create and review sprint-specific branches while you perform the labs; do not fabricate backdated history.

Open the PR, wait for all checks, and address any PostgreSQL/CI failures. Review the changes and merge when checks pass. Then wait for the main-branch CI run to pass. This confirms the README badge is actually passing on main.

```bash
python3 scripts/capture-ci.py
```

This captures the **latest successful run matching current main**, saves complete logs as `ci-workflow-done`, downloads the actual PostgreSQL test output as `security-headers-done`, and records/verifies all six public file URLs in `submission-urls.txt`/`.json`.

For ongoing lab development, use separate sprint branches and normal PR review, for example `git checkout -b sprint2/security` followed by commit/push/PR. Do not skip failing tests to merge.

## 3. Sprint 1 Done screenshots and REST outputs

Once the corresponding implementation and tests are verified, move each story through the working states:

```bash
python3 scripts/board.py status setup 'In progress'
python3 scripts/board.py status setup 'Review/QA'
python3 scripts/board.py status setup Done
# Capture rest-techdebt-done.png showing this story in Done.
```

Repeat for the verified `read`, `list`, `update`, and `delete` stories and capture respectively `read-accounts.png`, `list-accounts.png`, `update-accounts.png`, and `delete-accounts.png`. Keep the story title and Done column visible. After capturing, `python3 scripts/board.py close KEY` closes that issue and moves it to Closed. This prevents completed Sprint 1 work from cluttering later sprint screenshots.

In the lab, activate the virtual environment and point the app at PostgreSQL:

```bash
pip install -r requirements.txt
# Use the PostgreSQL credentials provided by your lab (do not commit them).
export DATABASE_URI='postgresql://USER:PASSWORD@HOST:5432/DATABASE'
# Use a separate disposable DB for nosetests, which clear the accounts table.
gunicorn --bind 0.0.0.0:8080 service:app
```

In another terminal with the app running:

```bash
python3 scripts/capture-rest.py --base-url http://localhost:8080
```

The script saves the exact five curl commands and their actual HTTP outputs. It only removes the demonstration account it creates. Use freshly captured lab outputs for submission. Run `bash scripts/test.sh` against the disposable **test** DB to refresh complete test/coverage output.

## 4. Sprint 2 planning and completion

```bash
python3 scripts/board.py sprint2
```

Filter Sprint = Sprint 2. Capture `sprint2-plan.png` with CI first and security second under Sprint backlog, labels/points visible. Verify CI executes successfully and security tests pass; move the corresponding issues through In progress and Review/QA to Done and capture:

| Story key | Done screenshot |
|---|---|
| ci | `ci-kanban-done.png` |
| security | `security-kanban-done.png` |

Then close them after saving the screenshots. The real CI workflow file is `.github/workflows/ci-build.yaml`; Talisman and CORS are in `service/__init__.py`.

## 5. Sprint 3 planning

```bash
python3 scripts/board.py sprint3
```

Filter Sprint = Sprint 3. Capture `sprint3-plan.png` with Docker first, Kubernetes second, and CD third in Sprint backlog. All three must show Sprint 3. These are not Done until their actual execution succeeds.

## 6. Build and push to IBM Cloud Container Registry

Use the Skills Network lab's Docker, IBM CLI credentials, registry namespace, and assigned cluster. Do not create paid cloud resources or log into a different cluster for this project. Fill in your own values:

```bash
export ICR_REGION=us-south
export ICR_HOST=us.icr.io
export ICR_NAMESPACE=YOUR_ASSIGNED_NAMESPACE
export IMAGE="$ICR_HOST/$ICR_NAMESPACE/accounts:v1"
ibmcloud cr region-set "$ICR_REGION"
ibmcloud cr login
docker build --tag accounts:latest --tag "$IMAGE" .
docker push "$IMAGE"
```

The lab must provide a Docker daemon and permission to push to the namespace. Match ICR_HOST to the assigned region. Run `docker run --rm accounts:latest id` is **not** appropriate because the Dockerfile has a Gunicorn entrypoint; inspect the configured user using `docker image inspect accounts:latest --format '{{.Config.User}}'` (expected 1001).

Run the built image against a reachable PostgreSQL instance and confirm port 8080. `docker compose up --build` is one local option; PostgreSQL must be ready before starting the accounts process. After verifying it works, mark `docker` Done and capture `kube-docker-done.png`.

## 7. Create cluster secrets and deploy manually

Confirm the selected identity and **assigned lab namespace**:

```bash
oc whoami
oc project -q
python3 scripts/create-db-secret.py
```

Create the registry Secret using the lab-provided ICR API key. The following prompts locally without echoing the key, then passes a JSON secret to oc over stdin (no key in command arguments or a committed file):

```bash
python3 - <<'PY'
import base64, getpass, json, os, subprocess
host = os.environ['ICR_HOST']
key = getpass.getpass('Lab ICR API key: ')
auth = base64.b64encode(('iamapikey:' + key).encode()).decode()
config = json.dumps({'auths': {host: {'username': 'iamapikey', 'password': key, 'auth': auth}}})
secret = {'apiVersion': 'v1', 'kind': 'Secret', 'metadata': {'name': 'ibm-registry'},
          'type': 'kubernetes.io/dockerconfigjson',
          'data': {'.dockerconfigjson': base64.b64encode(config.encode()).decode()}}
subprocess.run(['oc', 'apply', '-f', '-'], input=json.dumps(secret), text=True, check=True)
PY
oc secrets link builder ibm-registry --for=mount
IMAGE="$IMAGE" bash scripts/deploy.sh
```

`create-db-secret.py` preserves an existing accounts-db Secret to avoid breaking the persisted PostgreSQL database. If the Secret is missing after a DB has already initialized, recover the original credentials rather than generating a different password for that PVC. The manifests need an available default StorageClass and quota for two 1Gi claims (database and pipeline), PostgreSQL, the app, and build/task pods.

The script creates persistent PostgreSQL, waits for it, renders and applies the accounts deployment/service, waits for rollout, and creates an edge-TLS HTTPS Route. The lab's registry key must support both pull and push for the CD build.

In a separate terminal:

```bash
oc port-forward service/accounts 8080:8080
```

With forwarding active:

```bash
IMAGE="$IMAGE" bash scripts/capture-cluster.sh
```

This saves actual port-8080 root JSON as `kube-app-output`, the full Docker image table as `kube-images`, and deployment/pod/replicaset/service details as `kube-deploy-accounts`. Check each output and the app. Mark `kubernetes` Done and capture `kube-kubernetes-done.png`.

## 8. Run Tekton CD and capture logs

Prerequisites: Tekton/OpenShift Pipelines installed; `oc` and `tkn` in PATH; namespace rights to create Tasks/Pipelines/RBAC/PVCs; cluster OpenShift Docker builds enabled; outbound access to GitHub/PyPI/container registries; successful manual deployment; registry push/pull Secret present. No privileged container is requested by these Tekton tasks; OpenShift's build controller handles the Docker build. A cluster with only Kubernetes and no OpenShift Build API needs a different build task.

```bash
export REPO_URL='https://github.com/YOUR_GITHUB_USERNAME/devops-capstone-project'
export IMAGE="$ICR_HOST/$ICR_NAMESPACE/accounts:cd-v1"
bash scripts/run-pipeline.sh
```

Use a **fresh image tag per pipeline run**; the deploy task also restarts the workload to ensure it pulls the newly built image. The script applies resources, performs server-side manifest validation, starts the pipeline under its scoped service account, saves all task logs as `pipelinerun.txt`, waits for success, and appends the run details. The stages run in order: clone → lint → test (isolated PostgreSQL sidecar) → build/push → deploy. A failing stage stops downstream work.

Confirm the rollout and the live API after CD, then mark `cd` Done and capture `cd-pipeline-done.png`. Refresh `kube-deploy-accounts` after this rollout if desired. If the pipeline fails, preserve the error, fix it, re-run and capture the complete successful run; do not edit logs to hide failures.

## 9. Final audit

```bash
python3 scripts/validate-submission.py
```

It must report 33/33 artifacts present. Inspect every screenshot for actual required content; presence checks cannot determine correct board states or grader acceptance. Inspect pipeline logs for all five successful stages. Submit the six URLs from `submission-urls.txt` and the exact screenshot/output files listed in `docs/AI_GRADED_CHECKLIST.md`. Do not upload the ZIP in place of the grader's individual fields unless the submission form explicitly accepts a ZIP.

The automation scripts do not delete cloud resources. Follow the lab's cleanup instructions after submission and after saving your evidence.
