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
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', 'Selem_2018', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question_01 = {
            'question': 'test question 01 ?',
            'answer': 'test answer 01',
            'category': 1,
            'difficulty': 1}

        self.new_question_02 = {
            'question': 'test question 02 ?',
            'answer': 'test answer 02',
            'category': 1,
            'difficulty': 1}
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total_categories'])

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['total_questions'])

    def test_get_questions_unvalid_pages(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_question(self):
        res = self.client().delete('/questions/23')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 23).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 23)
        self.assertEqual(question, None)

    def test_delete_question_not_exist(self):
        res = self.client().delete('/questions/1000')  # id for not existing question
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_question(self):
        res = self.client().post('/questions',
                                 json=self.new_question_01)
        data = json.loads(res.data)
        new_question = Question.query.filter(
            Question.id == data['created']).one_or_none()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(new_question, None)

    # def test_create_question_duplicate(self):
    #     res = self.client().post('/questions',
    #                              json=self.new_question_01)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')

    def test_create_question_not_allowed(self):
        res = self.client().post('/questions/1000',
                                 json={'question': 'test question ?', 'answer': 'test answer', 'category': 1, 'difficulty': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_create_question_unvalid_parameters(self):
        res = self.client().post('/questions',
                                 json={'answer': 'test answer', 'category': 1, 'difficulty': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_retrieve_questions_on_search(self):
        res = self.client().post('/questions/search',
                                 json={'searchTerm':'question'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']),1)
        self.assertEqual(data['total_question'],1)

    def test_retrieve_questions_on_search_unvalid_parameters(self):
        res = self.client().post('/questions/search',
                                 json={'search': 'question'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")

    def test_retrieve_questions_on_search_not_found(self):
        res = self.client().post('/questions/search',
                                 json={'searchTerm': 'XXXX'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")

    def test_retrieve_questions_per_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], 1)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])

    def test_retrieve_questions_per_category_unvalid(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_start_quizz(self):
        res = self.client().post('/quizzes',
                                 json={
                                     "quiz_category": {
                                         "id": 1,
                                         "type": "blabla"
                                     },
                                     "previous_questions": [20, 21, 22]
                                 })
        data = json.loads(res.data)
        

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_start_quizz_unvalid_parameters(self):
        res = self.client().post('/quizzes',
                                 json={
                                     "previous_questions": [20, 21, 22]
                                 })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")

    def test_start_quizz_no_questions_remain(self):
        res = self.client().post('/quizzes',
                                 json={
                                     "quiz_category": {
                                         "id": 1,
                                         "type": "blabla"
                                     },
                                     "previous_questions": [20, 21, 22,27]
                                 })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "unprocessable")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
