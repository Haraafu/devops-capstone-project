#!/usr/bin/env bash
# Execute after the image is built and the OpenShift deployment is healthy.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p evidence
: "${IMAGE:?Set IMAGE to the Docker image reference you built and pushed}"
{
  printf '$ docker images --digests --no-trunc\n'
  docker images --digests --no-trunc "$IMAGE"
} > evidence/kube-images
# Fail if docker knows no such image rather than submitting an empty table.
docker image inspect "$IMAGE" >/dev/null
oc rollout status deployment/accounts --timeout=300s
{
  printf '$ oc get deployments,pods,replicasets,services -o wide\n'
  oc get deployments,pods,replicasets,services -o wide
  printf '\n$ oc describe deployment accounts\n'
  oc describe deployment accounts
} > evidence/kube-deploy-accounts
# Port forwarding must already be active: oc port-forward service/accounts 8080:8080
curl --silent --show-error --fail http://localhost:8080/ > evidence/kube-app-output
python3 -m json.tool evidence/kube-app-output >/dev/null
printf 'Captured image table, deployment details, and port-8080 JSON output.\n'
