#!/usr/bin/env python3
"""Capture real curl commands and responses; only deletes its own test account."""
import argparse
import json
from pathlib import Path
import shlex
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--base-url", default="http://localhost:8080")
parser.add_argument("--output", default="evidence")
args = parser.parse_args()
base = args.base_url.rstrip("/")
out = Path(args.output)
out.mkdir(parents=True, exist_ok=True)


def curl(name, method, path, expected, data=None):
    command = [
        "curl",
        "--silent",
        "--show-error",
        "--fail-with-body",
        "--include",
        "--request",
        method,
        base + path,
    ]
    if data is not None:
        command += ["--header", "Content-Type: application/json", "--data", json.dumps(data)]
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    output = result.stdout.replace("\r\n", "\n")
    headers, _, body = output.partition("\n\n")
    status = int(headers.splitlines()[0].split()[1])
    if status != expected:
        raise RuntimeError(f"{name}: expected {expected}, got {status}")
    (out / name).write_text("$ " + shlex.join(command) + "\n" + output + "\n")
    return json.loads(body) if body.strip() else None


data = {
    "name": "Capstone Demo Customer",
    "email": "demo@example.test",
    "address": "Jakarta, Indonesia",
    "phone_number": "+62-21-555-0100",
    "date_joined": "2026-10-30",
}
created = curl("rest-create-done", "POST", "/accounts", 201, data)
account_id = created["id"]
curl("rest-list-done", "GET", "/accounts", 200)
curl("rest-read-done", "GET", f"/accounts/{account_id}", 200)
data["address"] = "Depok, Indonesia"
updated = curl("rest-update-done", "PUT", f"/accounts/{account_id}", 200, data)
assert updated["address"] == data["address"]
curl("rest-delete-done", "DELETE", f"/accounts/{account_id}", 204)
print(f"Captured five REST operations in {out}")
