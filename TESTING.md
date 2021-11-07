# WordUp

![logo](app/static/images/logo.png)

Group Project for CSPB3308

## Team Members

Claudia Hidrogo, Raul Ramos, Christie Hui

## Automated Test Cases

### Test 1
Use case name: Verify login with valid user name and password

Description: Test the login page

Pre-conditions: User has valid name and password

Test steps:
- Navigate to login page (should be the home page upon app startup)
- Provide valid user name (please use 'admin')
- Provide valid password (please use 'admin')
- Click "Log In" button

Expected result: User should be redirected to the index page of the app (i.e. '/index')

Actual result: User is navigated to index page upon successful login

Status: Pass

Notes: Once DB is connected to Flask front-end, the form will query our backend DB for existing user name and password.

Post-conditions: User is validated with DB and successfully logged into their account.

