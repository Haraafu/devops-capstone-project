# Evidence provenance

Updated 2 November 2026 (Asia/Jakarta). Artifact capture metadata uses UTC ISO timestamps.

## GitHub Actions / PostgreSQL / Docker

- Successful run: https://github.com/Haraafu/devops-capstone-project/actions/runs/41335295847
- Source main commit: `27de1adbe48ea8da0184992066771142932dd87f`
- `ci-workflow-done`: complete real workflow logs, prefixed with run URL and commit.
- `security-headers-done`: complete passing nosetests output downloaded from that run; 38 tests, 96% service coverage, Python 3.9, actual PostgreSQL service.
- `ci-coverage.xml`: actual coverage artifact from the same run.
- `rest-create-done`, `rest-list-done`, `rest-read-done`, `rest-update-done`, `rest-delete-done`: exact curl commands and HTTP responses against the Dockerized Gunicorn service at localhost:8080 on the GitHub runner, backed by its isolated PostgreSQL container. The demonstration account is deleted by the capture script.
- `kube-images`: actual `docker images --digests --no-trunc accounts:latest` table from that runner. The rubric filename does not make it Kubernetes evidence.
- `docker-build.txt`, `docker-image-inspect.json`, `docker-validation.txt`, `docker-app.log`, `docker-postgres.log`: real image build, configured UID, runtime identity, PostgreSQL version, health response and container logs. Build/run success does not establish an IBM registry push.
- `ci-provenance.json`: run status/URL/head SHA and the matching main SHA when captured. Refresh after subsequent main changes.
- `submission-urls.txt` and `.json`: six verified public GitHub paths on main.

## Live planning screenshots

Fourteen PNGs capture the real public GitHub Project at https://github.com/users/Haraafu/projects/1. No image generation, mock board, DOM changes or image editing was used. The initial seven-story image was visually inspected. Later captures compare the rendered cards/columns/labels/points/sprints with authoritative live API data before saving. Sidecar metadata records the source URL, UTC timestamp, SHA-256 and compared card state; sidecar text records the rendered page text.

GitHub initially served stale anonymous views. Invalid captures were replaced with current verified views before proceeding. Triage and labels screenshots show the same valid triaged/labeled state. All sprint states were performed on 2 November 2026; the three weekly iteration assignments do not represent a fabricated three-week work history.

## Historical local evidence

Original 30 October 2026 SQLite outputs and their original provenance/validation notes are preserved under `historical-local/`. `tdd-sprint1-red.txt` and `tdd-sprint2-red.txt` retain the earlier local failing-test sequence. `local-flake8.txt` and `local-pylint.txt` retain the earlier local results; the current quality gates are in the real CI logs.

`tooling-validation.txt` records offline board-resume regression checks, pipeline source/BuildConfig isolation checks and shell syntax checks. These do not establish OpenShift schema/admission or Tekton runtime success.

## Not executed

The local Docker Desktop engine failed startup; the Docker evidence instead comes from real GitHub-hosted Docker execution. No IBM Cloud registry push, OpenShift deployment or Tekton PipelineRun was executed. No assigned lab link/session was available. Items 26, 28, 31, 32 and 33 remain missing, and the associated Kubernetes/CD stories remain pending.
