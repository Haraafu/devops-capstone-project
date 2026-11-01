**As a** service provider  
**I need** my service to use security headers and CORS policies  
**So that** my web site is not vulnerable to CORS attacks

### Assumptions
* Use Flask-Talisman for security headers.
* Use Flask-Cors to establish CORS policies.
* Only explicitly configured origins receive CORS permission; credentials are disabled.

### Acceptance Criteria
```gherkin
Given the site is secured
When a REST API request is made
Then secure headers and the configured CORS policy should be returned
And an untrusted origin receives no Access-Control-Allow-Origin header
```
