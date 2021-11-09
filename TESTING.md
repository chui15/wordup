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

### Test 2
Use case name: Verify signup with valid user name and password

Description: Test the signup page

Pre-conditions: User has valid name at least 5 characters long and password at least 3 characters long

Test steps:
- Navigate to login page (should be the home page upon app startup)
- Navigate to signup page
- User enters username less than 5 characters
- User enters password less than 3 characters
- Click "Sign Up" button

Expected result: Error messages show up for the incorrect input field (either username or password or both)

Actual result: Error messages show up for the incorrect input field (either username or password or both)

Status: Pass

Notes: Once DB is connected to Flask front-end, the form will query our backend DB for existing user name and password.

Post-conditions: User is validated with DB and successfully logged into their account.

### Test 3
Use case name: Test database table creation

Description: Test database table creation

Pre-conditions: Database hasn't been created yet and following dependencies have been installed:
```
Package                 Version
----------------------- -------
asn1crypto              1.4.0
greenlet                1.1.2
pg8000                  1.22.0
pip                     21.3.1
psycopg2-binary         2.9.1
scramp                  1.4.1
setuptools              57.4.0
SQLAlchemy              1.4.26
testing.common.database 2.0.3
testing.postgresql      1.3.0
```

Test steps:
- Create a PostgreSQL DB instance
- Run a "CREATE TABLE" query
- Run a "INSERT" query to insert dummy data into table
- Run a "SELECT" query and test its output against expected output
- Destroys test DB

Expected result: "SELECT" query output matches expected output

Actual result: "SELECT" query output matches expected output

Status: Pass

Notes: Real DB will contain actual user data.

Post-conditions: Real DB will contain actual user data and will be hosted on Heroku.