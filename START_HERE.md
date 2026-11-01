# Start here

The Customer Accounts capstone is published at https://github.com/Haraafu/devops-capstone-project. The real board is at https://github.com/users/Haraafu/projects/1.

**Current audit: 28/33 artifacts present; five assigned-lab items are still missing.** Read [docs/CURRENT_STATUS.md](docs/CURRENT_STATUS.md) for verified results and [docs/RESUME_LAB.md](docs/RESUME_LAB.md) for the remaining deployment and Tekton steps.

The service passed 38 PostgreSQL tests with 96% coverage, clean Flake8 and Pylint 10/10. GitHub Actions built the actual Dockerfile, checked UID 1001, started Gunicorn on port 8080, and captured five real CRUD responses backed by PostgreSQL. See `evidence/ci-provenance.json` for the exact successful run and source commit.

Planning and completion screenshots are real browser captures of the live GitHub Project. Sprint 1 and Sprint 2 are closed after capture; Sprint 3 has Docker Done and Kubernetes/CD in Sprint backlog. Preserve `.board-state.json`; do not recreate the board or replay the initial stages.

Remaining items are 26, 28, 31, 32 and 33. They require the assigned Skills Network OpenShift/Tekton environment. No cluster evidence has been substituted with local or GitHub-runner output.

Run `python scripts/validate-submission.py` to refresh both audit formats. It deliberately exits with status 1 while evidence is missing. After future changes to main, run `python scripts/capture-ci.py` after the new workflow succeeds.
