import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_user = os.environ['DB_USER']
        self.database_password = os.environ['DB_PASSWORD']
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            self.database_user, self.database_password, 'localhost:5432', self.database_name
        )
        setup_db(self.app, self.database_path)

        self.all_questions = [question.format() for question in  Question.query.all()]
        self.total_questions = len(self.all_questions)

        self.all_categories = {
            "1": "Science", 
            "2": "Art", 
            "3": "Geography", 
            "4": "History", 
            "5": "Entertainment", 
            "6": "Sports"
        }

        # to test for creating new question
        self.new_question = {
            'answer': 'Muhammed Buhari',
            'category': 4,
            'difficulty': 2,
            'question': 'Who is the current Nigerian president'
        }

        # to test for searching questions
        self.search_term = 'title'
        self.search_questions = [
            question.format()
            for question in Question.query.filter(Question.question.ilike(f'%{self.search_term}%')).order_by(Question.id).all()
        ]

        self.art_questions = [
            question.format()
            for question in Question.query.filter_by(category=2).order_by(Question.id).all()
        ]

        # to test for getting quiz questions
        self.previous_questions = [9, 12, 23,]
        self.quiz_category = {
            'type': 'History',
            'id': '4'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass


    def test_get_all_categories_success(self):
        res = self.client().get('/categories')
        result = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(result['categories'])
        for key in result['categories'].keys():
            self.assertEqual(result['categories'][key], self.all_categories[key]) 

    def test_get_all_categories_error(self):
        res = self.client().post('/categories', json={'id':7, 'type': 'General'})
        result = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(result['success'], False)
        self.assertEqual(result['message'], 'method not allowed')

    def test_get_all_questions_success(self):
        res = self.client().get('/questions')
        result = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(result['success'], True)
        self.assertLessEqual(len(result['questions']), 10)
        self.assertEqual(result['total_questions'], self.total_questions)
        self.assertTrue(result['total_questions'])
        self.assertTrue(result['categories'])
        self.assertTrue(result['current_category'])
        
        for key in result['categories'].keys():
                self.assertEqual(result['categories'][key], self.all_categories[key]) 

    def test_get_all_questions_error1(self):
        """
            Test for none availability of questions due to large page number relative to the number of questions in the database
        """
        res = self.client().get('/questions?page=6')
        result = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(result['success'], False)
        self.assertEqual(result['message'], 'resource not found')
    
    def test_get_all_questions_error2(self):
        """
            Test for invalid page number (number <=0)
        """
        res = self.client().get('/questions?page=-4')
        result = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(result['success'], False)
        self.assertEqual(result['message'], 'request is unprocessable')

    def test_delete_question_success(self):
        """
            Test for successful deletion of question from the database
        """
        res = self.client().delete('/questions/26')
        result = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(result['success'], True)
        self.assertEqual(result['deleted'], 26)
    
    def test_delete_question_error(self):
        """
            Test for deleting non existing question
        """

        res = self.client().delete('/questions/194')
        result = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(result['success'], False)
        self.assertEqual(result['message'], 'resource not found')

    def test_create_new_question_success(self):
        """
            Test for creating a new question successfully
        """
        res = self.client().post('/questions', json=self.new_question)
        result = json.loads(res.data)

        self.assertEqual(result['success'], True)
        self.assertTrue(res.status_code, 200)
        self.assertTrue(self.total_questions, 19)

    def test_create_new_question_error(self):

        """
            Failure test for creating new question
        """
        res = self.client().post('/questions', json={
            'question': '',
            'answer': '',
            'difficulty': '',
            'category': ''
        })
        result = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(result['success'], False)
        self.assertEqual(result['message'], 'Bad Request')


    def test_search_for_questions_success(self):
        """
            Test for searching searhing questions successfully
        """

        res = self.client().post('/searched_questions', json={'searchTerm':self.search_term})
        result = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(result['success'])
        self.assertTrue(result['current_category'])
        self.assertEqual(result['total_questions'], len(self.search_questions))

        for i in range(0, len(result['questions'])): # comparing search results with query results
            self.assertEqual(result['questions'][i], self.search_questions[i])

    def test_search_for_questions_error(self):
        """
            Failure test for searching qustions
        """ 
        res = self.client().get('/searched_questions')
        result = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(result['success'], False)
        self.assertEqual(result['message'], 'method not allowed')

    def test_questions_by_category_success(self):
        """
            Test for getting questions by category successfully
        """
        res = self.client().get('/categories/2/questions')
        result = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(result['success'])
        self.assertEqual(result['current_category'], 'Art')
        self.assertEqual(result['total_questions'], len(self.art_questions))

        for i in range(0, len(result['questions'])): # comparing returned results with query results
            self.assertEqual(result['questions'][i], self.art_questions[i])

    def test_questions_by_category_error(self):
        """
            Test for getting questions by category that does not exist in the database
        """
        res = self.client().get('/categories/21/questions')
        result = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(result['success'], False)
        self.assertEqual(result['message'], 'resource not found')

    def test_quiz_question_success(self):
        """
            Test for getting test question
        """
        res = self.client().post('/quizzes', json={
            'previous_questions': self.previous_questions, 
            'quiz_category': self.quiz_category
        })
        result = json.loads(res.data)

        self.assertTrue(result['question'])
        self.assertEqual(res.status_code, 200)
        self.assertEqual(result['question']['category'], int(self.quiz_category['id']))

        for id in self.previous_questions:
            self.assertNotEqual(id, result['question']['id'])

    def test_quiz_question_error(self):

        """
            Failure test for getting quiz question by sending get request instead for the only allowed post request
        """
        res = self.client().get('/quizzes')
        result = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(result['success'], False)
        self.assertEqual(result['message'], 'method not allowed')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()