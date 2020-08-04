# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## APIs

**GET**  `/categories` 
- *Description* : Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- *Request Arguments* : None
- *Returns* : An object with 
    - success : [True/Flase] if false the error code and message will be provided
    - categories : contains a object of id: category_string key:value pairs.
    - total_categories : total number of categories retrieved

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
}
```

**GET**  `/questions?page=<page_number>` 
- *Description* : Fetches all questions in pages of ten questions per page
- *Request Arguments* : (optional)page
- *Returns* : An object with 
    - success : [True/Flase] if false the error code and message will be provided
    - questions : questions retrieved for the required page
    - categories : contains a object of id: category_string key:value pairs.
    - total_questions : total number of questions retrieved

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "<answer>",
      "category": "<category id>",
      "difficulty": "<difficulty level>",
      "id": "<question id>",
      "question": "<question>"
    },
    ... etc
  ],
  "success": true,
  "total_questions": 19
}
```

**DELETE**  `/questions/<question_id>` 
- *Description* : delete the question with provided id
- *Request Arguments* : question_id
- *Returns* : An object with 
    - success : [True/Flase] if false the error code and message will be provided
    - deleted : the id of the deleted question

```json
{
  "deleted": "<question_id>",
  "success": true
}
```

**POST**  `/questions` 
- *Description* : Add question with provided details to questions
- *Request body* : 
```json
{
    "question": "<Question>",
    "answer": "<Answer>",
    "category": "<Category Id>",
    "difficulty": "<difficulty level>"
}
```
- *Returns* : An object with 
    - success : [True/Flase] if false the error code and message will be provided
    - created : the id of the created question

```json
{
  "created": "<question_id>",
  "success": true
}
```

**POST**  `/questions/search` 
- *Description* : search for questions contains the provided searchTerm in the questions
- *Request body* : 
```json
{
    "searchTerm": "<search term>"
}
```
- *Returns* : An object with 
    - success : [True/Flase] if false the error code and message will be provided
    - current_category : the current category id
    - questions : paginated list of  questions matchs the serach term
    - total_question : total number of questions matchs the search term 

```json
{
  "current_category": null,
  "questions": [
    {
      "answer": "<answer>",
      "category": "<category id>",
      "difficulty": "<difficulty level>",
      "id": "<question id>",
      "question": "<question>"
    }
  ],
  "success": true,
  "total_question": 1
}
```

**GET**  `/categories/<category_id>/questions` 
- *Description* : Fetches all questions for provided category id 
- *Request Arguments* : category_id
- *Returns* : An object with 
    - success : [True/Flase] if false the error code and message will be provided
    - current_category : the provided category id
    - questions : paginated list of questions retrived for the provided category id
    - total_questions : total number of questions in the provideed category

```json
{
  "current_category": "<category_id>",
  "questions": [
    {
      "answer": "<answer>",
      "category": "<category id>",
      "difficulty": "<difficulty level>",
      "id": "<question id>",
      "question": "<question>"
    },
    ...etc
  ],
  "success": true,
  "total_questions": 5
}
```
**POST**  `/quizzes` 
- *Description* : Fetches random question for specific category and exclude the list provided for previous questions 
- *Request body* : 
```json
{
    "quiz_category": {
        "id": "<category id>",
        "type": "<category type>"
    },
    "previous_questions":[20,21]
}
```
- *Returns* : An object with 
    - success : [True/Flase] if false the error code and message will be provided
    - question : random question in the same category provided and not match with any of previous questions provided

```json
{
  "question": {
      "answer": "<answer>",
      "category": "<category id>",
      "difficulty": "<difficulty level>",
      "id": "<question id>",
      "question": "<question>"
    },
  "success": true
}
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```