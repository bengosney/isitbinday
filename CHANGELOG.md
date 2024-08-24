## 0.2.0 (2024-08-24)

### Feat

- **models**: context manager that calls save on exit
- **books**: encrypt sync passwords
- **books**: setup the sync to run once an hour
- **books**: make the settings id for couch sync optional
- **books**: api endpoint for the sync settings
- **books**: service to sync book with couchdb
- **tasks**: api view for the task actions
- **task**: remove the archive state and give it it's own field

### Fix

- **books**: make the tests folder a module so it can actualy run tests
- **books**: handle missing doc
- **books**: rate limit requests to couch
- **books**: set the owner on create
- **tasks**: suppress transition errors when auto archiving
- **books**: explicitly raise from a previous error
- **books**: make the password write only in the api
- **books**: apply missing migration
- **books**: tmp cover can not be null
- **books**: sync in transactions, log and set cover correctly
- **types**: "fix" some type issues with third party code
- **recipes**: if you can't parse the time, return 0 timedelta
- **deps**: update all the dependacies
- **static-files**: correct static file configuration
- **books**: create missing migration
- **recipes**: handle missing data
- **rollbar**: remove rollbar, the api doesn't work and because of that it was clogging up the error even worse
- **rollbar**: update the config for the new rollbar style

### Refactor

- **save-context-manager**: simplify the __exit__ function
- **tests**: use the save context manager
- **tasks**: make better use of the fixtures
- **task**: move the fixtures
- **tasks**: remove the loop in the test
- **books**: reduce duplicate code and complexity
- **tests**: swap to pytest-mock for mocking
- **tests**: use pytest-check to get the all the errors when checking the object
- **tasks**: split the tests into seperate files
- **books**: remove debug print
- **book**: move some boiler plate into a fixture
- **books**: expand the function to be more explicit
- **books**: break out the document to book function
- **books**: published date is not synced so make it blank and remove it from the admin list

## 0.1.4 (2024-05-25)

### Refactor

- **circleci**: update ci config to use python 3.10
- **isb**: automatic sorting of classes and update to python 3.10 syntax
