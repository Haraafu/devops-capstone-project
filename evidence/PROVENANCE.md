# Evidence provenance

Captured on 30 October 2026 from the actual implementation in this package.

- `tdd-sprint1-red.txt`: failing route/validation tests run before implementing missing REST operations. SQLite test database; 32 tests, expected failures.
- `tdd-sprint2-red.txt`: failing header/CORS tests run after REST implementation but before configuring Talisman and CORS. SQLite; 37 tests, expected security failures.
- `security-headers-done`: complete successful local nosetests output. Python 3.9.25, SQLite, 37 passing tests, 96% reported service coverage.
- `rest-create-done`, `rest-list-done`, `rest-read-done`, `rest-update-done`, `rest-delete-done`: actual curl commands and HTTP responses against Gunicorn on local port 8080 using SQLite. The capture script creates, updates, and removes its own demonstration account.
- `local-flake8.txt` and `local-pylint.txt`: actual local quality checks.
- `local-validation.txt`: final local source, schema, and quality verification summary.

No GitHub Actions, Docker build, OpenShift deployment, or Tekton execution occurred in this workspace. No Kanban screenshots or public repository URLs have been fabricated. The host has no Docker/oc/tkn CLIs or logged-in GitHub integration. PostgreSQL is configured in the CI and cluster files, but its execution must still be verified in those environments.

The six local rubric output files are genuine, but they do not prove the full prescribed PostgreSQL/Skills Network lab workflow. Re-run the supplied capture scripts in the lab to refresh them. `capture-ci.py` replaces security output with the real PostgreSQL CI artifact after a successful current-main run.
