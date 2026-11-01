# Remaining assigned-lab work

Open your enrolled [Coursera DevOps Capstone course](https://www.coursera.org/learn/devops-capstone-project) and launch its Skills Network lab. [IBM's starter repository](https://github.com/ibm-developer-skills-network/aolwx-devops-capstone-template) directs learners to those course-provided lab links. A public course URL is not a running authenticated lab session.

Repository: https://github.com/Haraafu/devops-capstone-project

Project: https://github.com/users/Haraafu/projects/1

Preserve `.board-state.json` in the original local project folder. It contains the real issue/project identifiers. Do not run `board.py init` or replay completed planning stages.

Five checklist items need real lab execution:

| Item | Artifact | Required execution |
|---|---|---|
| 26 | `evidence/kube-app-output` | JSON from the OpenShift-deployed service, forwarded to port 8080 |
| 28 | `evidence/kube-kubernetes-done.png` | Actual Kubernetes story in Done after successful rollout |
| 31 | `evidence/kube-deploy-accounts` | Actual deployment/pod/replicaset/service state |
| 32 | `evidence/pipelinerun.txt` | Complete successful clone, lint, test, build/push, deploy logs |
| 33 | `evidence/cd-pipeline-done.png` | Actual CD story in Done after the successful pipeline |

Docker build, non-root execution, PostgreSQL integration, and the five REST operations have also been exercised on a GitHub Actions runner. Those logs do not establish IBM registry push or an OpenShift/Tekton deployment.

## Prepare the assigned environment

In the lab terminal:

```bash
git clone https://github.com/Haraafu/devops-capstone-project.git
cd devops-capstone-project
oc whoami
oc project -q
```

Use only the namespace and registry credentials assigned by the course. Follow [RUNBOOK.md sections 6 and 7](RUNBOOK.md#6-build-and-push-to-ibm-cloud-container-registry) to build and push the image, create the database/registry Secrets, and deploy. `scripts/create-db-secret.py` preserves any existing database Secret. Keep API keys in the lab's local prompts; do not commit or paste them into chat.

## Capture the manual deployment

Once the rollout is healthy, keep this running in a second lab terminal:

```bash
oc port-forward service/accounts 8080:8080
```

In the first terminal, with `IMAGE` still set to the image built/pushed in the lab:

```bash
bash scripts/capture-cluster.sh
```

Inspect the JSON and deployment details. In the original local folder, move `kubernetes` through In progress, Review/QA, and Done using `scripts/board.py status`. Save a screenshot of the actual Sprint 3 board as `evidence/kube-kubernetes-done.png` before closing the issue.

## Execute Tekton

In the lab, choose a fresh image tag and run:

```bash
export REPO_URL=https://github.com/Haraafu/devops-capstone-project
export IMAGE="$ICR_HOST/$ICR_NAMESPACE/accounts:cd-$(date -u +%Y%m%d%H%M%S)"
bash scripts/run-pipeline.sh
```

The source directory and OpenShift BuildConfig are isolated per run. The deployment is shared, so run delivery sequentially for this course service. Each run leaves its source directory and BuildConfig for inspection; follow lab cleanup instructions after preserving evidence.

Verify that all five stages succeeded, that `oc rollout status deployment/accounts` succeeds, and that the forwarded API still responds. Move `cd` through the working states to Done and capture `evidence/cd-pipeline-done.png`.

Copy the real lab artifacts back into the original project's `evidence/` folder and run:

```bash
python scripts/validate-submission.py
```

It must report 33/33 files present. Presence alone does not establish screenshot content or grader acceptance. Inspect every remaining artifact before submitting the individual fields.
