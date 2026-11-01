**As a** customer account manager  
**I need** to delete an account  
**So that** I can remove accounts that are no longer needed

### Assumptions
* DELETE /accounts/{id} is idempotent.
* A successful or repeated deletion returns 204 with no body.

### Acceptance Criteria
```gherkin
Given an account exists
When I send DELETE /accounts/{id}
Then I receive status 204 and the account is removed
And reading the deleted account returns 404
```
