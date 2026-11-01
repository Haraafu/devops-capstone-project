# AI-Graded Final Checklist — all 33 items

Current evidence inventory: **28/33 artifacts present and reviewed; five assigned-lab items missing**. Presence does not guarantee grader acceptance.

See [CURRENT_STATUS.md](CURRENT_STATUS.md) for validation and [RESUME_LAB.md](RESUME_LAB.md) for the remaining work. Screenshots are real GitHub Project captures; terminal outputs retain their execution provenance.

| # | Requirement | Artifact | Points | Current status |
|---|---|---|---:|---|
| 1 | README.md public GitHub URL with passing badge | `README.md` | 2 | verified public main |
| 2 | User story template public GitHub URL | `user-story.md` | 1 | verified public main |
| 3 | Seven original stories in New issues | `Planning-userstories-done.png` | 1 | captured live github |
| 4 | Triage showing Docker/Kubernetes in Icebox | `planning-productbacklog-done.png` | 1 | captured live github |
| 5 | Technical debt and enhancement labels visible | `planning-labels-done.png` | 1 | captured live github |
| 6 | Five Sprint 1 stories in Sprint backlog | `planning-kanban-done.png` | 1 | captured live github |
| 7 | setup.cfg public GitHub URL | `setup.cfg` | 1 | verified public main |
| 8 | Development environment story in Done | `rest-techdebt-done.png` | 1 | captured live github |
| 9 | Read story in Done | `read-accounts.png` | 1 | captured live github |
| 10 | List story in Done | `list-accounts.png` | 1 | captured live github |
| 11 | Update story in Done | `update-accounts.png` | 1 | captured live github |
| 12 | Delete story in Done | `delete-accounts.png` | 1 | captured live github |
| 13 | CREATE curl command and response | `rest-create-done` | 2 | captured ci postgresql container |
| 14 | LIST curl command and response | `rest-list-done` | 2 | captured ci postgresql container |
| 15 | READ curl command and response | `rest-read-done` | 2 | captured ci postgresql container |
| 16 | UPDATE curl command and response | `rest-update-done` | 2 | captured ci postgresql container |
| 17 | DELETE curl command and response | `rest-delete-done` | 2 | captured ci postgresql container |
| 18 | Two Sprint 2 stories in Sprint backlog | `sprint2-plan.png` | 1 | captured live github |
| 19 | Successful GitHub Actions complete workflow logs | `ci-workflow-done` | 2 | captured github actions |
| 20 | CI automation story in Done | `ci-kanban-done.png` | 1 | captured live github |
| 21 | ci-build.yaml public GitHub URL | `ci-build.yaml` | 4 | verified public main |
| 22 | Talisman configuration public GitHub URL | `__init__.py` | 1 | verified public main |
| 23 | Complete passing nosetests security output | `security-headers-done` | 1 | captured ci postgresql |
| 24 | Security story in Done | `security-kanban-done.png` | 1 | captured live github |
| 25 | Three Sprint 3 stories assigned and ranked | `sprint3-plan.png` | 1 | captured live github |
| 26 | Deployed application JSON from port 8080 | `kube-app-output` | 1 | needs assigned lab |
| 27 | Docker story in Done | `kube-docker-done.png` | 1 | captured live github |
| 28 | Kubernetes story in Done | `kube-kubernetes-done.png` | 1 | needs assigned lab |
| 29 | Dockerfile public GitHub URL | `Dockerfile` | 2 | verified public main |
| 30 | Docker image table with name/tag/id/time/size | `kube-images` | 2 | captured ci docker |
| 31 | Deployment/pod/replicaset/service details | `kube-deploy-accounts` | 2 | needs assigned lab |
| 32 | Complete successful Tekton pipeline logs | `pipelinerun.txt` | 5 | needs assigned lab |
| 33 | CD pipeline story in Done | `cd-pipeline-done.png` | 1 | needs assigned lab |

Total rubric points: **50**. Present artifacts represent **40** points; five pending items represent **10** points.

Six public file URLs are in `evidence/submission-urls.txt` and `.json`. The Talisman package file is `service/__init__.py`. The Docker image table is genuine output from the successful GitHub Actions Docker build; it does not prove cluster deployment.

Run `python scripts/capture-ci.py` only after successful current-main CI. It downloads complete workflow logs, PostgreSQL test/coverage output, Docker build/runtime/image evidence, REST transcripts and verified public file URLs.

Run `python scripts/validate-submission.py` to refresh both audit formats. Missing lab artifacts must remain absent until their real execution succeeds.
