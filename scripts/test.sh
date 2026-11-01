#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
: "${DATABASE_URI:?Set DATABASE_URI to a disposable test database}"
mkdir -p evidence
flake8 service tests --count --show-source --statistics | tee evidence/local-flake8.txt
pylint service --fail-under=8 2>&1 | tee evidence/local-pylint.txt
nosetests 2>&1 | tee evidence/security-headers-done
coverage report --fail-under=95
