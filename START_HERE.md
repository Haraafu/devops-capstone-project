# Start here

The Customer Accounts service is implemented and locally tested. This package includes all code, ten sprint-ready stories, GitHub planning automation, Docker/OpenShift/Tekton configuration, and capture scripts for the complete 33-item rubric.

**The submission is not complete yet.** Local tests pass, but the real GitHub board, public URLs, hosted CI run, Docker build, OpenShift deployment, and Tekton logs require your authenticated GitHub and Skills Network environments. See `docs/AI_GRADED_CHECKLIST.md` for the exact item-by-item status.

## Fast path

1. Extract this ZIP and open a terminal in `devops-capstone-project`.
2. In your GitHub-capable environment, install/sign in to `gh` and grant Project access: `gh auth login` then `gh auth refresh -s project`. Never paste a token into chat or commit credentials.
3. Run `python3 scripts/board.py init --start YYYY-MM-DD`, using the date you start Sprint 1. This creates your public repository from the IBM template, the board, three weekly iterations, and seven initial stories. It intentionally stops at the first screenshot state.
4. Follow `docs/RUNBOOK.md` in order to capture the planning screenshots, publish the implementation through a pull request, run CI, and deploy in the Skills Network lab.
5. Put screenshots in `evidence/` with the required names. Run `python3 scripts/validate-submission.py` before submitting. The initial audit correctly reports 6/33 artifacts present and 27 still missing.

The initial local outputs use SQLite. The prepared GitHub CI workflow uses PostgreSQL (`postgres:alpine`) and enforces 95% coverage. Refresh the local outputs from the lab before final submission.

## Included implementation

- REST create/read/update/delete/list operations with input validation and JSON errors.
- Flask-Talisman security headers and an explicit Flask-CORS policy.
- 37 tests; 96% local coverage; clean Flake8; Pylint 10/10.
- CI on pull requests to main and pushes to main, with a README build badge.
- Non-root Python 3.9 Docker image with Gunicorn on port 8080.
- PostgreSQL and accounts Kubernetes manifests plus HTTPS OpenShift Route.
- Tekton clone/lint/test/build/deploy pipeline using an OpenShift Docker BuildConfig.

`requirements.lock.txt` records all installed package versions from local validation. `requirements.txt` remains the course-facing direct dependency list.
