**As a** developer  
**I need** a configured development environment  
**So that** I can build and test the accounts microservice

### Assumptions
* Use the provided IBM Flask/PostgreSQL starter template.
* Install the Python dependencies and configure nosetests, coverage, Flake8 and Pylint.
* Use a disposable PostgreSQL database for tests; maintain at least 95% coverage.

### Acceptance Criteria
```gherkin
Given the repository has been cloned
When I install requirements and run linting and nosetests
Then the environment runs the tests and reports at least 95% coverage
```
