**As a** customer account manager  
**I need** to update an account  
**So that** I can keep customer information current

### Assumptions
* PUT /accounts/{id} replaces editable fields without changing the id.
* Validate JSON before changing persisted data.

### Acceptance Criteria
```gherkin
Given an account exists
When I send a valid JSON PUT request
Then I receive status 200 and the persisted updated account
And invalid input returns 400 without changing the account
And an unknown id returns 404
```
