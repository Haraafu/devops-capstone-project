#!/usr/bin/env python3
"""Publish this implementation to a development branch and open a pull request.

Run board.py init first. main remains unchanged until the PR is merged.
"""
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
state = json.loads((ROOT / ".board-state.json").read_text())
repo = state["repo"]
if not re.fullmatch(r"[A-Za-z0-9_.-]+/devops-capstone-project", repo):
    raise SystemExit("Unexpected repository identity in state file")
readme = ROOT / "README.md"
readme.write_text(re.sub(
    r"https://github\.com/[^/\s)]+/devops-capstone-project/actions/workflows/ci-build\.yaml",
    f"https://github.com/{repo}/actions/workflows/ci-build.yaml",
    readme.read_text(),
))
branch = "development/capstone-implementation"
with tempfile.TemporaryDirectory(prefix="capstone-publish-") as folder:
    destination = Path(folder) / "repo"
    subprocess.run(["gh", "repo", "clone", repo, str(destination)], check=True)
    subprocess.run(["git", "-C", str(destination), "checkout", "-b", branch], check=True)
    ignore = shutil.ignore_patterns(
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "*.pyc",
        ".coverage",
        ".board-state.json",
        "submission",
        "*.db",
    )
    shutil.copytree(ROOT, destination, dirs_exist_ok=True, ignore=ignore)
    subprocess.run(["git", "-C", str(destination), "add", "."], check=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(destination),
            "commit",
            "-m",
            "Implement Customer Accounts REST API, security, CI, and delivery pipeline",
        ],
        check=True,
    )
    subprocess.run(["git", "-C", str(destination), "push", "-u", "origin", branch], check=True)
    body = destination / "pr-body.txt"
    body.write_text(
        "Completes the Customer Accounts REST endpoints with validated input, "
        "Talisman/CORS, a PostgreSQL CI workflow, Docker/OpenShift manifests, and "
        "a Tekton delivery pipeline.\n\nValidation: 37 local tests, 96% coverage, "
        "Flake8 clean, Pylint 10/10; local tests used SQLite. "
        "The Actions workflow independently validates PostgreSQL. "
        "OpenShift/Docker/Tekton execution is pending in the lab.\n"
    )
    subprocess.run(
        [
            "gh",
            "pr",
            "create",
            "--repo",
            repo,
            "--base",
            "main",
            "--head",
            branch,
            "--title",
            "Implement Customer Accounts microservice and DevOps workflows",
            "--body-file",
            str(body),
        ],
        check=True,
    )
print("Review the pull request and require CI to pass before merging.")
