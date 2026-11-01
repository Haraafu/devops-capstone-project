**As a** developer  
**I need** to containerize my microservice using Docker  
**So that** I can deploy it easily with all of its dependencies

### Assumptions
* Create a Dockerfile for repeatable builds.
* Use python:3.9-slim as the base, as required by the lab.
* Install all Python requirements.
* Do not run as root.
* Use gunicorn as the WSGI entry point.

### Acceptance Criteria
```gherkin
Given the Docker image named accounts has been created and a database is configured
When I use docker run accounts with DATABASE_URI and port mapping
Then I should see the accounts service running in Docker on port 8080
```
