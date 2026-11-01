**As a** customer account manager  
**I need** to read an account by its id  
**So that** I can view the customer details

### Assumptions
* GET /accounts/{id} returns the serialized account.
* Missing accounts return a JSON 404 response.

### Acceptance Criteria
```gherkin
Given an account exists
When I send GET /accounts/{id}
Then I receive status 200 and the account details
And an unknown id returns status 404
```
