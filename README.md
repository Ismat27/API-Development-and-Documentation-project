## API Reference

### Getting Started
- Base URL: Currently the app is hosted locally at `http://127.0.0.1:5000/` which is set as a proxy in the frontend configuration.
- Authentication: The current version of the app does not require any form of authentication.

### Error Handling
Errors are formatted and returned as JSON objects. A typical error object is as below:
```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```
The API will return any of the errors below depending on the corresponding failed request:
- 400: Bad Request
- 404: Resource not found
- 405: Method not allowed
- 422 Request not processable

### Endpoints
#### GET /categories
- General:
    - Returns an object of question categories and success value
- Sample: `curl http://127.0.0.1:5000/categories `

```
{
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
#### GET /questions
- General:
    - Returns a list of question objects, number of total questions, object of question categories, current category and success value.
    - Results are paginated in groups of 10. Include a request argument (page) which defaults to 1 to choose page number, starting from 1. 
- Smaple `curl http://127.0.0.1:5000/questions`

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "ALL", 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
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
  "total_questions": 21
}
```

#### DELETE /questions/{question_id}
- General: Delete the question of the given id if it existed and returns the id of the deleted question and success value.
- Sample `curl -X DELETE http://127.0.0.1:5000/questions/16`

```
{
    'deleted': 16,
    'success': true
}
```

#### POST /questions
- General: Create a new question in the database with the submitted data if successful and return success value.
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{'answer': 'Benjamin Nnamdi Azikwe', 'category': 4, 'difficulty': 2, 'question': 'Who is the first Nigerian civilian president'}'`

```
{
    'success': true
}
```

#### POST /searched_questions
- General: Receive a search keyword, search for questions which their question text consist of the search keyword. Return list of matched question objects, total number of questions matched, current category and success value.
- Sample: `curl http://127.0.0.1:5000/searched_questions -X POST -H "Content-Type: application/json" -d '{'searchTerm': 'title'}'`

```
{
    "current_category": "ALL",
    "questions": [
        {
            "answer": "Edward Scissorhands", 
            "category": 5, 
            "difficulty": 3, 
            "id": 6, 
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }
    ],
    "success": true,
    "total_questions": 1
}
```
#### GET /categories/{category_id}/questions
- General: Get all the questions of a given category indicated by the id of the category. Returns similar result to getting questions
- Smaple `curl http://127.0.0.1:5000/categories/6/questions`

```
{
  "current_category": "Sports", 
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
#### POST /quizzes
- General: Accept a list of previous questions user has answered if any and the quiz category then return a succes value and a **random** question not among the previous ones the user has answered if any or an empty string if none.
- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{'previous_questions': [9, 12, 23], quiz_category': {'id': '4', 'type': 'History'} }'`

```
{
    "answer": "Benjamin Nnamdi Azikwe", 
    "category": 4, 
    "difficulty": 2, 
    "id": 24, 
    "question": "Who is the first Nigerian civilian president"
}
```
