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
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', 'bjjv','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            'question': 'What movie earned Tom Hanks his third straight Oscar nomination, in 1996',
            'answer': 'Apollo 13',
            'category': '5',
            'difficulty': '4'
        }

        self.valid_quiz_query = {
            'quiz_category': { 'id': '3','type': 'Geography'},
            'previous_questions': []
        }

        self.invalid_quiz_query = {
            'quiz_category': { 'id': '10','type': 'Current Affairs'},
            'previous_questions': []
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    #Test 1
    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    #Test 2
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    #Test 3 
    def test_404_sent_requesting_questions_beyond_valid_page(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    #Test 4
    def test_get_question_search_with_results(self):
        res = self.client().post('/questions', json={'searchTerm':'World'}) 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']),2 )  

    #Test 5
    def test_get_question_search_without_results(self):
        res = self.client().post('/questions', json={'searchTerm':'applejacks'}) 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)

    #Test 6
    def test_get_questions_based_on_valid_category(self):
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']),3)

    #Test 7
    def test_404_get_questions_based_on_invalid_category(self):
        res = self.client().get('/categories/0/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    #Test 8
    def test_delete_question(self):
        res = self.client().delete('/questions/35')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 35).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 35)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['question']))
        self.assertEqual(question, None)

    #Test 9
    def test_422_if_question_does_not_exist(self):
        res = self.client().delete('/questions/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
    
    #Test 10
    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))

    #Test 11
    def test_405_if_question_creation_not_allowed(self):
        res = self.client().post('/questions/45', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')
    
    #Test 12
    def test_quiz_question(self):
        res = self.client().post('/quizzes', json=self.valid_quiz_query)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #Test 13
    def test_quiz_question_not_found(self):
        res = self.client().post('/quizzes', json=self.invalid_quiz_query)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
       
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()


