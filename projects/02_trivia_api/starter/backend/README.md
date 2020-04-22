# Trivia API

This API follows the RESTFUL API principles in creating a webpage to manage the trivia app and play the game.

Current available features are as follows:-
1. Display questions - both all questions and by category. Questions shows the question, category and difficulty rating by default and can show/hide the answer. 
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Frontend was complete. Backend code was done as part of this project.

All backend code follows PEP8 style guidelines.

## Getting Started

#### Pre-requisites and Local Development
To use this application you need Python3, pip and node installed on your local machine.

### Backend
Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.

#### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```
#### Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```
These commands put the application in development and directs our application to use 
the __init__.py file in our flaskr folder. Working in development mode shows an interactive 
debugger in the console and restarts the server whenever changes are made. 
If running locally on Windows, look for the commands in the Flask documentation.

The application is run on http://127.0.0.1:5000/ by default and is a proxy in the frontend 
configuration.

### Frontend

Installing Node and NPM

This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

Installing project dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```
Running Your Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

```bash
npm start
```
By default, the frontend will run on localhost:3000.

### Testing

In order to run tests navigate to the backend folder and run the following commands:

dropdb trivia_test    
createdb trivia_test  
psql trivia_test < trivia.psql   
python test_flaskr.py

The first time you run the tests, omit the dropdb command.
All tests are kept in the file (test_flaskr.py) and should be maintained as updates are made to app functionality.

## API Reference

Getting started
Base URL: At the present this app can only be run locally and is not hosted. The backend app is hosted at http://127.0.0.1:5000/  
Authentication: This version of the application does not  require authentication or API keys.

### Error Handling
Errors are returned as JSON objects in the following format:
```
{  
    'success': False,  
    'error': 404,  
    'message': "resource not found"  
}
```
The API will return four error types when requests fail:

400: Bad Request  
404: resource not found  
405: Method not allowed  
422: unprocessable  
500: internal server error  

### Endpoints

#### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
```
"categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```
#### GET '/questions'
- Fetches a list of questions, paginated in group of 10 questions
- Request Arguments: page number (starting with 1)
- Returns: list of questions, categories, current_category, and total number of questions
```
"categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": null,
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```
#### GET '/categories/<int:category_id>/questions'
- Fetches a list a questions based on a category
- Request Arguments: category id
- Returns: total questions in the category
```
 "current_category": "Geography",
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```
#### DELETE '/questions/<int:question_id>'
 - Deletes the question if it exists
 - Request Arguments: question id
 - Returns: Deleted question id and total number of questions
```
{
  'success': true,
  'deleted': 2,
  'total_questions': 18
}
``` 
#### POST '/questions'
- Creates a new question and will require the question and answer text, category, and difficulty score.
- Returns the total number of questions
```
{
  'success': true,
  'total_questions': 19
}
```
#### POST '/questions'
- Fetches questions based on a search term. It returns any questions for which the search term is a substring of the question. 
- Returns: search term matched questions and total questions in the search result.
```
"questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```
#### POST '/quizzes'
- Fetches random questions to play the quiz
- Request Arguments: category and previous question
- Returns: random questions within the given category, if provided, and that is not one of the previous questions

## Author

Bindu Jacob