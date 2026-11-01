#!/usr/bin/env bash
# Requires a logged-in oc CLI in the correct lab namespace.
set -euo pipefail
cd "$(dirname "$0")/.."
: "${IMAGE:?Set IMAGE to the full IBM Cloud registry image reference}"
if [[ ! "$IMAGE" =~ ^[a-zA-Z0-9._:/@-]+$ ]]; then
  echo 'Invalid image reference' >&2; exit 1
fi
oc whoami
oc project -q
oc get secret accounts-db ibm-registry >/dev/null
oc apply -f deploy/configmap.yaml
oc apply -f deploy/postgresql.yaml
oc rollout status deployment/postgresql --timeout=300s
sed "s|IMAGE_PLACEHOLDER|$IMAGE|g" deploy/deployment.yaml | oc apply -f -
oc rollout status deployment/accounts --timeout=300s
oc apply -f deploy/route.yaml
mkdir -p evidence
{ printf '$ oc get deployments,pods,replicasets,services -o wide\n';
  oc get deployments,pods,replicasets,services -o wide;
  printf '\n$ oc describe deployment accounts\n';
  oc describe deployment accounts;
} > evidence/kube-deploy-accounts
printf 'Deployment ready. Use oc port-forward service/accounts 8080:8080 for the port-8080 evidence.\n'
