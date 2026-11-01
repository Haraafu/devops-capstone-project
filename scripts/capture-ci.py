#!/usr/bin/env python3
"""Save complete logs from a real successful main-branch GitHub Actions run."""
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
state = json.loads((ROOT / ".board-state.json").read_text())
repo = state["repo"]
result = subprocess.run(
    [
        "gh",
        "run",
        "list",
        "--repo",
        repo,
        "--workflow",
        "ci-build.yaml",
        "--branch",
        "main",
        "--limit",
        "1",
        "--json",
        "databaseId,conclusion,status,url,headSha",
    ],
    check=True,
    capture_output=True,
    text=True,
)
runs = json.loads(result.stdout)
if not runs or runs[0]["conclusion"] != "success":
    raise SystemExit(
        "The latest main CI run has not succeeded. Fix or wait for it; do not submit stale logs."
    )
run = runs[0]
head = subprocess.check_output(
    ["gh", "api", f"repos/{repo}/commits/main", "--jq", ".sha"], text=True
).strip()
if run["headSha"] != head:
    raise SystemExit(
        "CI success does not match the current main commit. Run CI on current main first."
    )
out = ROOT / "evidence"
out.mkdir(exist_ok=True)
with (out / "ci-workflow-done").open("w") as stream:
    stream.write(f"Run: {run['url']}\nCommit: {head}\n\n")
    subprocess.run(
        ["gh", "run", "view", str(run["databaseId"]), "--repo", repo, "--log"],
        stdout=stream,
        stderr=subprocess.STDOUT,
        check=True,
    )
# This replaces the local test output with the real PostgreSQL CI test output.
with tempfile.TemporaryDirectory(prefix="capstone-ci-") as folder:
    downloaded = Path(folder)
    for artifact in ["test-evidence", "docker-evidence"]:
        subprocess.run(
            ["gh", "run", "download", str(run["databaseId"]), "--repo", repo,
             "--name", artifact, "--dir", str(downloaded / artifact)],
            check=True,
        )
    expected = [
        "security-headers-done", "kube-images", "docker-build.txt",
        "docker-image-inspect.json", "docker-validation.txt",
        "docker-app.log", "docker-postgres.log",
        "rest-create-done", "rest-list-done", "rest-read-done",
        "rest-update-done", "rest-delete-done",
    ]
    for name in expected:
        files = list(downloaded.rglob(name))
        if len(files) != 1:
            raise SystemExit(f"Expected exactly one captured artifact: {name}")
        (out / name).write_bytes(files[0].read_bytes())
    coverage_files = list(downloaded.rglob("coverage.xml"))
    if len(coverage_files) == 1:
        (out / "ci-coverage.xml").write_bytes(coverage_files[0].read_bytes())
paths = {
    "README.md": "README.md",
    "user-story.md": ".github/ISSUE_TEMPLATE/user-story.md",
    "setup.cfg": "setup.cfg",
    "ci-build.yaml": ".github/workflows/ci-build.yaml",
    "__init__.py": "service/__init__.py",
    "Dockerfile": "Dockerfile",
}
repository = json.loads(subprocess.check_output(["gh", "api", f"repos/{repo}"], text=True))
if repository["private"]:
    raise SystemExit("The repository must be public for the AI grader")
urls = {name: f"https://github.com/{repo}/blob/main/{path}" for name, path in paths.items()}
for path in paths.values():
    subprocess.run(
        ["gh", "api", f"repos/{repo}/contents/{path}?ref=main"],
        stdout=subprocess.DEVNULL,
        check=True,
    )
(out / "submission-urls.json").write_text(json.dumps(urls, indent=2) + "\n")
(out / "submission-urls.txt").write_text(
    "\n".join(f"{name}: {url}" for name, url in urls.items()) + "\n"
)
(out / "ci-provenance.json").write_text(json.dumps({
    "repository": repo, "run": run, "main_commit": head,
    "database": "PostgreSQL in GitHub Actions",
    "container": "Actual Dockerfile built and exercised on the GitHub runner",
    "cluster_deployment": False,
}, indent=2) + "\n")
print("Captured successful CI logs, PostgreSQL tests, Docker/REST evidence, and six public file URLs.")
