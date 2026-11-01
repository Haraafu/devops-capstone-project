# AI-Graded Final Checklist — all 33 items

This is an honest status inventory, not a claim that all submission evidence exists. Source implementation is prepared. Six local outputs have been captured from real runs. Public GitHub file URLs, real board screenshots, Actions logs, and Docker/OpenShift/Tekton results require execution in the authenticated environments.

Put screenshots and output files in `evidence/`. Screenshots must be `.png` or `.jpeg`; use the exact base names below. Do not submit a mock board or invented successful output. Planning screenshots must be captured **before** progressing to the next board state.

| # | Requirement | Artifact | Points | Current status |
|---|---|---|---:|---|
| 1 | README.md public GitHub URL with passing badge | `README.md` | 2 | needs github |
| 2 | User story template public GitHub URL | `user-story.md` | 1 | needs github |
| 3 | Seven original stories in New issues | `Planning-userstories-done.png / .jpeg` | 1 | needs github |
| 4 | Triage showing Docker/Kubernetes in Icebox | `planning-productbacklog-done.png / .jpeg` | 1 | needs github |
| 5 | Technical debt and enhancement labels visible | `planning-labels-done.png / .jpeg` | 1 | needs github |
| 6 | Five Sprint 1 stories in Sprint backlog | `planning-kanban-done.png / .jpeg` | 1 | needs github |
| 7 | setup.cfg public GitHub URL | `setup.cfg` | 1 | needs github |
| 8 | Development environment story in Done | `rest-techdebt-done.png / .jpeg` | 1 | needs github |
| 9 | Read story in Done | `read-accounts.png / .jpeg` | 1 | needs github |
| 10 | List story in Done | `list-accounts.png / .jpeg` | 1 | needs github |
| 11 | Update story in Done | `update-accounts.png / .jpeg` | 1 | needs github |
| 12 | Delete story in Done | `delete-accounts.png / .jpeg` | 1 | needs github |
| 13 | CREATE curl command and response | `rest-create-done` | 2 | captured local sqlite |
| 14 | LIST curl command and response | `rest-list-done` | 2 | captured local sqlite |
| 15 | READ curl command and response | `rest-read-done` | 2 | captured local sqlite |
| 16 | UPDATE curl command and response | `rest-update-done` | 2 | captured local sqlite |
| 17 | DELETE curl command and response | `rest-delete-done` | 2 | captured local sqlite |
| 18 | Two Sprint 2 stories in Sprint backlog | `sprint2-plan.png / .jpeg` | 1 | needs github |
| 19 | Successful GitHub Actions complete workflow logs | `ci-workflow-done` | 2 | needs github run |
| 20 | CI automation story in Done | `ci-kanban-done.png / .jpeg` | 1 | needs github |
| 21 | ci-build.yaml public GitHub URL | `ci-build.yaml` | 4 | needs github |
| 22 | Talisman configuration public GitHub URL | `__init__.py` | 1 | needs github |
| 23 | Complete passing nosetests security output | `security-headers-done` | 1 | captured local sqlite |
| 24 | Security story in Done | `security-kanban-done.png / .jpeg` | 1 | needs github |
| 25 | Three Sprint 3 stories assigned and ranked | `sprint3-plan.png / .jpeg` | 1 | needs github |
| 26 | Deployed application JSON from port 8080 | `kube-app-output` | 1 | needs openshift run |
| 27 | Docker story in Done | `kube-docker-done.png / .jpeg` | 1 | needs github and docker |
| 28 | Kubernetes story in Done | `kube-kubernetes-done.png / .jpeg` | 1 | needs github and openshift |
| 29 | Dockerfile public GitHub URL | `Dockerfile` | 2 | needs github |
| 30 | Docker image table with name/tag/id/time/size | `kube-images` | 2 | needs docker run |
| 31 | Deployment/pod/replicaset/service details | `kube-deploy-accounts` | 2 | needs openshift run |
| 32 | Complete successful Tekton pipeline logs | `pipelinerun.txt` | 5 | needs tekton run |
| 33 | CD pipeline story in Done | `cd-pipeline-done.png / .jpeg` | 1 | needs github and tekton |

Total rubric points: **50**.

## File URL mapping

After a passing main-branch workflow, `python scripts/capture-ci.py` writes `evidence/submission-urls.txt` and `.json`, checks the repository is public, and verifies these files exist on main:

| Checklist item | Repository path |
|---|---|
| 1 | `README.md` |
| 2 | `.github/ISSUE_TEMPLATE/user-story.md` |
| 7 | `setup.cfg` |
| 21 | `.github/workflows/ci-build.yaml` |
| 22 | `service/__init__.py` |
| 29 | `Dockerfile` |

The checklist says “init.py”; the actual Python package initialization file is **`service/__init__.py`**. Submit its public URL, where Talisman and CORS are configured.

## Capture commands

| Evidence | Command / action |
|---|---|
| Initial planning | `board.py init`, `triage`, `refine`, `sprint1`, capturing each stage |
| Sprint 2 / 3 plans | `board.py sprint2` / `board.py sprint3` |
| Done screenshots | Move the verified story with `board.py status KEY Done`, then capture the real board |
| Five curl outputs | `python scripts/capture-rest.py --base-url http://localhost:8080` |
| Security output | `bash scripts/test.sh` against a disposable PostgreSQL DB; CI also uploads it |
| CI logs and six URLs | `python scripts/capture-ci.py` after merging and passing main CI |
| Image table, cluster state, app JSON | `bash scripts/capture-cluster.sh` after build/deploy and port forwarding |
| Tekton logs | `bash scripts/run-pipeline.sh` |
| Missing-evidence audit | `python scripts/validate-submission.py` |

Local output provenance and limitations are recorded in `evidence/PROVENANCE.md`. When running in the lab, replace the relevant output files by capturing fresh real results. Never rename a local smoke-test result into cluster evidence.
