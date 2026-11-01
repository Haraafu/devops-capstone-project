**As a** developer  
**I need** to create a CD pipeline to automate deployment to Kubernetes  
**So that** the developers are not wasting their time doing it manually

### Assumptions
* Use Tekton to define the pipeline.
* Clone, lint, test, build, and deploy the service.
* Deployment should be to OpenShift.
* A manual trigger is sufficient for this MVP.
* Reuse the Dockerfile and Kubernetes manifests; push the image to IBM ICR.
* Use OpenShift Docker builds from the Tekton build task.

### Acceptance Criteria
```gherkin
Given the CD pipeline has been created
When I trigger the pipeline run
Then I should see the accounts service deployed to OpenShift
And all five pipeline stages succeed
```
