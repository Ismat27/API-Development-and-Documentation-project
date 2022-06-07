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
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('ismail', 'Smart 5441', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.all_categories = {
            "1": "Science", 
            "2": "Art", 
            "3": "Geography", 
            "4": "History", 
            "5": "Entertainment", 
            "6": "Sports"
        }

        self.new_book = {
            'answer': 'Benjamin Nnamdi Azikwe',
            'category': 4,
            'difficulty': 2,
            'id': 23,
            'question': 'Who is the first Nigerian civilian president'
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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
# Make the tests conveniently executable

    # test for succesful operaton on </categories> route
    def test_get_all_categories_success(self):
        res = self.client().get('/categories')
        result = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(result['categories'])
        for key in result['categories'].keys():
            self.assertEqual(result['categories'][key], self.all_categories[key]) 

    # test for unsuccesful operaton on </categories> route
    def test_get_all_categories_error(self):
        res = self.client().post('/categories', json={'id':7, 'type': 'General'})
        result = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(result['success'], False)
        self.assertEqual(result['message'], 'method not allowed')

    # test for succesful operaton on </quetionss> route
    def test_get_all_questions_success(self):
        res = self.client().get('/questions')
        result = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(result['success'], True)
        self.assertLessEqual(len(result['questions']), 10)
        self.assertEqual(result['total_questions'], 19)
        self.assertTrue(result['total_questions'])
        self.assertTrue(result['categories'])
        self.assertTrue(result['current_category'])
        
        for key in result['categories'].keys():
                self.assertEqual(result['categories'][key], self.all_categories[key]) 

    # def test_get_all_questions_error1(self):
    #     """
    #         Test for none availability of questions due to large page number relative to the number of questions in the database
    #     """
    #     res = self.client().get('/questions?page=6')
    #     result = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(result['success'], False)
    #     self.assertEqual(result['message'], 'resource not found')
    
    # def test_get_all_questions_error2(self):
    #     """
    #         Test for invalid page number (number <=0)
    #     """
    #     res = self.client().get('/questions?page=-4')
    #     result = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(result['success'], False)
    #     self.assertEqual(result['message'], 'request is unprocessable')
    

if __name__ == "__main__":
    unittest.main()