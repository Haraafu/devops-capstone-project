**As a** Developer  
**I need** automation to build and test every pull request  
**So that** I do not have to rely on manual testing of each request, which is time-consuming

### Assumptions
* GitHub Actions will be used for the automation workflow.
* The workflow must include code linting and testing.
* The database Docker image must be postgres:alpine.
* Add a GitHub Actions badge to README.md to reflect the build status.
* Run for pull requests to main and pushes to main; enforce at least 95% coverage.

### Acceptance Criteria
```gherkin
Given code is ready to be merged
When a pull request is created
Then GitHub Actions should run linting and unit tests
And the badge should show that the build is passing
```
