#!/usr/bin/env python3
"""Create a random lab DB credential without printing it or storing it in git."""
import base64
import json
import secrets
import subprocess

# Do not rotate an existing password: it may already protect an initialized PVC.
exists = subprocess.run(["oc", "get", "secret", "accounts-db"], capture_output=True)
if exists.returncode == 0:
    raise SystemExit("accounts-db already exists; preserving existing credentials.")
password = secrets.token_hex(24)
values = {
    "username": "accounts",
    "password": password,
    "uri": f"postgresql://accounts:{password}@postgresql:5432/accounts",
}
manifest = {
    "apiVersion": "v1",
    "kind": "Secret",
    "metadata": {"name": "accounts-db"},
    "type": "Opaque",
    "data": {k: base64.b64encode(v.encode()).decode() for k, v in values.items()},
}
subprocess.run(["oc", "create", "-f", "-"], input=json.dumps(manifest), text=True, check=True)
