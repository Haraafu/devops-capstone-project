# Sprint plan

Three sprints, each seven days long. `board.py init --start YYYY-MM-DD` creates real iteration dates and milestones from the selected Sprint 1 start date. Story-point estimates use 3/5/8/13 = S/M/L/XL.

| Sprint | Rank | Story key | Title | Label | Points |
|---|---:|---|---|---|---:|
| 1 | 1 | setup | Setting up the development environment | technical debt | 3 |
| 1 | 2 | read | Read an account from the service | enhancement | 3 |
| 1 | 3 | list | List all accounts in the service | enhancement | 3 |
| 1 | 4 | update | Update an account in the service | enhancement | 5 |
| 1 | 5 | delete | Delete an account from the service | enhancement | 3 |
| 2 | 1 | ci | Need the ability to automate continuous integration checks | technical debt | 5 |
| 2 | 2 | security | Need to add security headers and CORS policies | enhancement | 5 |
| 3 | 1 | docker | Containerize your microservice using Docker | technical debt | 5 |
| 3 | 2 | kubernetes | Deploy your Docker image to Kubernetes | enhancement | 5 |
| 3 | 3 | cd | Create a CD pipeline to automate deployment to Kubernetes | technical debt | 8 |

Sprint totals: 17, 10, and 18 points. These are planning estimates, not reported effort.

The original seven stories first go to **New issues**. Triage the five Sprint 1 stories to **Product backlog**, and Docker/Kubernetes to **Icebox**. Add labels and estimates, then select the five Sprint 1 stories into **Sprint backlog** in the order above. Create the CI/security stories when planning Sprint 2; add the CD story when planning Sprint 3 and bring Docker/Kubernetes out of Icebox.

Required board columns: New issues, Icebox, Product backlog, Sprint backlog, In progress, Review/QA, Done. An extra Closed column supports the later capstone lifecycle: capture Done evidence, merge/verify, then close the issue and move it to Closed. “Close the current story” in the planning lab means closing the story's detail pane, not marking unfinished work complete.

Definition of Done: acceptance criteria pass; relevant tests, coverage, and lint gates pass; implementation is reviewed and merged; required output and Done screenshot are captured. Deployment and CD stories additionally need an actual successful cluster run. Never move an unverified deployment story to Done just to populate a screenshot.
