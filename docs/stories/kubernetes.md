**As a** service provider  
**I need** my service to run on Kubernetes  
**So that** I can easily scale and manage the service

### Assumptions
* Kubernetes manifests will be created in YAML format.
* These manifests will be reused by the CD pipeline.
* The actual deployment will be to OpenShift.
* Provision PostgreSQL and a registry pull secret.

### Acceptance Criteria
```gherkin
Given the Kubernetes manifests have been created
When I use the oc command to apply the manifests
Then the service should be deployed and run in Kubernetes
```
