# survey
API service on DRF where client part can CRUD Questions/Options with a sent email to admin when new one added.

# How to run
1. Install everything from the requirements.txt file: `pip install -r requirements.txt`
2. Migrate database: `python manage.py migrate`
3. Populate the database: `python populate_db.py`
4. Start server: `python manage.py runserver`

# Endpoints for http://127.0.0.1:8000
1. http://127.0.0.1:30001/ - Swagger documentation
2. /questions/
  - GET(READ) - list of all questions with options
  - POST(CREATE) - create new question
3. /questions/<int:id>/
  - GET(READ) - detail information of question
  - PUT(UPDATE) - update information of question
  - DELETE - delete question
4. /questions/<int:id>/options/
  - GET(READ) - list of all options for question
  - POST(CREATE) - create new option for question
5. /questions/<int:id>/options/<int:id>/
  - GET(READ) - detail information of option
  - PUT(UPDATE) - update information of option
  - DELETE - delete option
