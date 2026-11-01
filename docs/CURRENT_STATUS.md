# DevOps capstone status — 2 November 2026

**28/33 required artifacts are present and reviewed. Five assigned-lab items remain.** The present artifacts represent 40/50 rubric points; this is an evidence inventory, not a predicted grade.

- [Public repository](https://github.com/Haraafu/devops-capstone-project)
- [Live GitHub board](https://github.com/users/Haraafu/projects/1)
- [Merged implementation PR](https://github.com/Haraafu/devops-capstone-project/pull/9)
- [Successful current-main workflow](https://github.com/Haraafu/devops-capstone-project/actions/runs/41335295847)
- Verified main commit: `27de1adbe48ea8da0184992066771142932dd87f`

Validation: **38 PostgreSQL-backed tests passed, 96% service coverage, Flake8 clean, Pylint 10/10**. The actual Dockerfile built successfully, ran as UID 1001 with Gunicorn on port 8080, and passed all five CRUD captures against PostgreSQL. The GitGuardian check passed on the implementation PR.

Fourteen screenshots show the real GitHub Project at the required planning and Done stages. Screenshots were captured from the live public board without DOM or image edits. Cache-busting and API-to-render comparisons prevented stale board captures; the first seven-story screenshot was visually verified. Screenshot metadata includes URLs, capture times, and hashes. The triage and label captures show the same valid board state with labels visible.

Sprint 1 and Sprint 2 stories are closed after their Done captures. Sprint 3 is assigned and ranked; Docker is Done. Kubernetes and CD remain in Sprint backlog. These sprint states were performed on 2 November, not backdated across three historical weeks.

## Remaining five items

| Item | Required evidence | Blocker |
|---|---|---|
| 26 | `kube-app-output` | Deploy to assigned OpenShift lab; capture forwarded port-8080 JSON |
| 28 | `kube-kubernetes-done.png` | Verified rollout, then actual board Done screenshot |
| 31 | `kube-deploy-accounts` | Real deployment/pod/replicaset/service details |
| 32 | `pipelinerun.txt` | Successful actual Tekton clone/lint/test/build/deploy logs |
| 33 | `cd-pipeline-done.png` | Verified successful CD, then actual board Done screenshot |

The assigned Skills Network lab was unavailable in this session. No IBM registry push, OpenShift rollout, or Tekton run is claimed. Use [the lab continuation steps](RESUME_LAB.md) after launching the lab through the enrolled Coursera course. No paid or substitute cluster was created.

## Submission files

Use the six URLs in `evidence/submission-urls.txt` and upload each exact artifact listed in `docs/AI_GRADED_CHECKLIST.md`. `evidence/submission-audit.json` and `.txt` agree on the five missing items. The ZIP is a convenience bundle, not a substitute for the grader's individual fields.

CI logs and artifacts identify their source run and commit. Refresh them with `python scripts/capture-ci.py` after any later main-branch change. Original 30 October SQLite outputs are preserved under `evidence/historical-local/`. Failing TDD logs remain historical supporting evidence.
