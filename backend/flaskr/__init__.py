import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    @app.route('/categories')
    def retrieve_categories():
        all_categories = {
            category.id: category.type for category in Category.query.order_by(Category.id).all()}

        if len(all_categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': all_categories,
            'total_categories': len(all_categories)
        })

    @app.route('/questions')
    def retrieve_questions():
        all_categories = {
            category.id: category.type for category in Category.query.order_by(Category.id).all()}
        all_questions = Question.query.order_by(Question.id).all()

        questions_page = paginate_questions(request, all_questions)
        current_categories = list(
            set([question['category'] for question in questions_page]))

        if len(questions_page) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': questions_page,
            'total_questions': len(all_questions),
            'categories': all_categories,
            'current_category': current_categories
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id,
            })

        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        if not new_question or not new_answer or not new_category or not new_difficulty or Question.query.filter(Question.question == new_question).one_or_none():
            abort(422)

        try:
            question = Question(question=new_question, answer=new_answer,
                                category=new_category, difficulty=new_difficulty)
            print(question.format())
            question.insert()

            return jsonify({
                'success': True,
                'created': question.id
            }), 201

        except:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def retrieve_questions_based_on_search():
        body = request.get_json()

        search_term = body.get('searchTerm', None)

        if not search_term:
            abort(422)

        search_results = Question.query.order_by(Question.id).filter(
            Question.question.ilike(f'%{search_term}%')).all()

        if len(search_results) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'current_category': None,
            'questions': paginate_questions(request, search_results),
            'total_question': len(search_results)
        })

    @app.route('/categories/<int:category_id>/questions')
    def retrieve_questions_based_on_category(category_id):
        questions_for_category = Question.query.order_by(Question.id).join(
            Category, Category.id == Question.category).filter(Question.category == category_id).all()

        if len(questions_for_category) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': paginate_questions(request, questions_for_category),
            'total_questions': len(questions_for_category),
            'current_category': category_id
        })

    @app.route('/quizzes', methods=['Post'])
    def start_quizz():
        body = request.get_json()
        category_info = body.get('quiz_category', None)
        previous_questions = body.get('previous_questions', None)

        try:
            categories = [category.id for category in Category.query.all()]
            if int(category_info['id']) not in categories:
                selection = Question.query.order_by(Question.id).filter(
                    ~Question.id.in_(previous_questions)).all()
            else:
                selection = Question.query.order_by(Question.id).join(Category, Category.id == Question.category).filter(
                    Question.category == category_info['id'], ~Question.id.in_(previous_questions)).all()

            return jsonify({
                'success': True,
                'question':  random.choice(selection).format()
            })

        except Exception as err:
            print(err)
            abort(422)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    return app
