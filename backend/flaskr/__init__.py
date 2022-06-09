import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from sqlalchemy import except_all

from models import setup_db,db, Question, Category

QUESTIONS_PER_PAGE = 10
def get_all_categories():
    categories = Category.query.order_by(Category.id).all()
    return_categories = {}
    formatted_categories = [category.format() for category in categories]
    for category in formatted_categories:
        return_categories[str(category['id'])] = category['type']
    return return_categories

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route('/categories', methods=['GET'])
    def categories():
        try:
            return jsonify({
                'categories': get_all_categories(),
                'success': True
            })
        except:
            abort(422)

    @app.route('/questions', methods=['GET'])
    def questions():
        page = request.args.get('page', 1, type=int)
        if page <= 0:
            abort(422)

        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = Question.query.order_by(Question.id).all()
        formated_questions = [question.format() for question in questions]
        total_questions = len(formated_questions)

        if len(formated_questions[start:end]) == 0:
            abort(404)
        try:

            return jsonify({
                'questions': formated_questions[start:end],
                'total_questions': total_questions,
                'categories': get_all_categories(),
                'current_category': 'ALL',
                'success': True
        })

        except:
            abort(422)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        """
            Route for deleting question of a given id
        """
        question = Question.query.get(question_id)
        if not question:
            abort(404)
        try:
            question.delete()
        except:
            db.session.rollback()
            db.session.close()
            abort(422)
        return jsonify({
            'success': True,
            'deleted': question_id
        })

    @app.route('/questions', methods=['POST'])
    def create_new_question():
        """
            Route for creating new question
        """
        data = request.get_json()

        question = data['question']
        answer = data['answer']
        difficulty = data['difficulty']
        category = data['category']

        new_question = Question(
            question=question,
            answer=answer,
            difficulty=difficulty,
            category=category
        )
        try:
            new_question.insert()
            return jsonify({
                'success': True
            })
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    @app.route('/searched_questions', methods=['POST'])
    def search_questions():
        """
            Route for getting result of searching for questions
        """
        try:
            search_term = request.get_json()['searchTerm']
            questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).order_by(Question.id).all()
            formated_questions = [question.format() for question in questions]
            total_questions = len(formated_questions)

            return jsonify({
                'questions': formated_questions,
                'total_questions': total_questions,
                'current_category': 'ALL',
                'success': True,

            })

        except:
            abort(422)


    @app.route('/categories/<int:category_id>/questions')
    def category_questions(category_id):
        """
            Route to get questions of a given category of id category_id
        """
        category = Category.query.get(category_id)
        if not category:
            abort(404)
        questions = Question.query.filter_by(category=category_id).order_by(Question.id).all()
        formated_questions = [question.format() for question in questions]
        total_questions = len(formated_questions)

        try:
            return jsonify({
                'questions': formated_questions,
                'total_questions': total_questions,
                'current_category': category.format()['type'],
                'success': True
            })
        
        except:
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def quiz_question():

        """
            Route for getting quiz question
        """
        data = request.get_json()
        previous_questions = data['previous_questions']
        quiz_category = data['quiz_category']
        if quiz_category['id'] != 0:
                category_id = int(quiz_category['id'])
                questions = Question.query.filter_by(category=category_id).order_by(Question.id)
                # ids = [question.id for question in questions.all()]
                # print(ids, len(ids))
        else:
            questions = Question.query.order_by(Question.id)
        available_questions = [question.format() for question in questions if question.id not in previous_questions]
        
        if len(available_questions) == 0:
            return jsonify({
            'success': True,
            'question': ''
        })
        return jsonify({
            'success': True,
            'question': random.choice(available_questions)
        })

   # ERRORS HANDLERS

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'message': 'Bad Request',
            'error': 400
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'resource not found',
            'error': 404
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'message': 'method not allowed',
            'error': 405
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'message': 'request is unprocessable',
            'error': 422
        }), 422

    return app

