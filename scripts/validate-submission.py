#!/usr/bin/env python3
"""Inventory 33 artifacts. Presence is not a grading or provenance guarantee."""
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"


def output_valid(artifact, content):
    """Detect empty and obviously wrong terminal outputs."""
    if artifact.startswith("rest-"):
        return "$ curl " in content and "HTTP/" in content
    if artifact == "security-headers-done":
        return bool(re.search(r"Ran \d+ tests", content) and re.search(r"^OK\s*$", content, re.M))
    if artifact == "kube-app-output":
        try:
            return isinstance(json.loads(content), dict)
        except json.JSONDecodeError:
            return False
    if artifact == "kube-images":
        return "REPOSITORY" in content and "IMAGE ID" in content and len(content.splitlines()) >= 3
    if artifact == "pipelinerun.txt":
        return "Succeeded" in content and all(
            stage in content for stage in ["clone", "lint", "test", "build", "deploy"]
        )
    return True


def check_item(item, urls):
    """Return a file-level presence check and its detail."""
    artifact = item["artifact"]
    if item["kind"] == "url":
        value = urls.get(artifact, "")
        ready = (
            bool(
                re.fullmatch(
                    r"https://github\.com/[^/]+/devops-capstone-project/blob/main/.+", value
                )
            )
            and "YOUR_GITHUB_USERNAME" not in value
        )
        return ready, value or "public URL not captured"
    if item["kind"] == "screenshot":
        for ext in [".png", ".jpeg"]:
            path = EVIDENCE / (artifact + ext)
            if path.exists() and path.stat().st_size > 100:
                header = path.read_bytes()[:8]
                ready = header.startswith(b"\x89PNG\r\n\x1a\n") or header.startswith(
                    b"\xff\xd8\xff"
                )
                return ready, str(path.relative_to(ROOT))
        return False, ""
    path = EVIDENCE / artifact
    if not path.exists() or not path.stat().st_size:
        return False, ""
    return output_valid(artifact, path.read_text(errors="replace")), str(path.relative_to(ROOT))


def main():
    items = json.loads((ROOT / "docs/checklist.json").read_text())
    urls_path = EVIDENCE / "submission-urls.json"
    urls = json.loads(urls_path.read_text()) if urls_path.exists() else {}
    missing = []
    for item in items:
        ready, detail = check_item(item, urls)
        item["file_check"] = "PRESENT_REVIEW" if ready else "MISSING_OR_INVALID"
        if not ready:
            missing.append(item["number"])
        print(f"{item['number']:02} {item['file_check']:18} {item['artifact']} {detail}")
    report = {
        "artifact_count": 33,
        "present": 33 - len(missing),
        "missing": missing,
        "warning": "Presence does not establish provenance, external execution, or screenshot content.",
        "items": items,
    }
    (EVIDENCE / "submission-audit.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"\nPresent: {33-len(missing)}/33. Missing or invalid: {len(missing)}.")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
