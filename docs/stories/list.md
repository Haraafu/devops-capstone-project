**As a** customer account manager  
**I need** to list all accounts  
**So that** I can review registered customers

### Assumptions
* GET /accounts returns a JSON array.
* An empty database returns an empty array.

### Acceptance Criteria
```gherkin
Given accounts have been created
When I send GET /accounts
Then I receive status 200 and all accounts
And an empty database returns []
```
