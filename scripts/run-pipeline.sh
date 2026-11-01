#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
: "${REPO_URL:?Set REPO_URL to your public GitHub repository URL}"
: "${IMAGE:?Set IMAGE to a fresh tagged IBM Cloud registry image reference}"
oc get secret accounts-db ibm-registry >/dev/null
oc apply -f tekton/rbac.yaml -f tekton/pvc.yaml -f tekton/tasks.yaml -f tekton/pipeline.yaml
# Server-side schema and admission validation before execution.
oc apply --dry-run=server -f tekton/tasks.yaml -f tekton/pipeline.yaml >/dev/null
RUN=$(tkn pipeline start cd-pipeline \
  --serviceaccount accounts-pipeline \
  -p "repo-url=$REPO_URL" -p branch=main -p "image=$IMAGE" \
  -w name=pipeline-workspace,claimName=pipelinerun-pvc --output name)
mkdir -p evidence
printf '%s\n' "$RUN" > evidence/pipelinerun-name.txt
tkn pipelinerun logs "$RUN" --all --follow 2>&1 | tee evidence/pipelinerun.txt
oc wait --for=condition=Succeeded "pipelinerun/$RUN" --timeout=1200s
tkn pipelinerun describe "$RUN" >> evidence/pipelinerun.txt
