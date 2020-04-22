import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
# pagination
def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  questions = [question.format() for question in selection]
  current_questions = questions[start:end]
  return current_questions

def get_category_list():
  categories = {}
  for category in Category.query.all():
    categories[category.id] = category.type
  return categories

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r'/*': {'origins':'*'}}, supports_credentials=True)

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def retrieve_categories():
    categories = Category.query.order_by(Category.id).all()
    if len(categories) == 0:
      abort(404)
    
    category_list = {}
    for category in categories:
      category_list[category.id] = category.type
    
    return jsonify({
      'success': True,
      'categories': category_list,
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def retrieve_questions():
    question_list = Question.query.order_by(Question.id).all()
    current_questions = paginate_questions(request, question_list)
    if len(current_questions) == 0:
      abort(404)
        
    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(Question.query.all()),
      'categories': get_category_list(),
      'currentCategory': None
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()
      if question is None:
        abort(404)
      
      question.delete()
      question_list = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request, question_list)
      
      return jsonify({

        'success': True,
        'deleted': question_id,
        'question': current_questions,
        'total_questions': len(Question.query.all())
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_category = body.get('category', None)
    new_difficulty = body.get('difficulty', None)
    search = body.get('searchTerm','')

    try:
      if search:
        question_list =  Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search)))
        current_questions = paginate_questions(request, question_list)

        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': len(question_list.all())
        })
      else:
        question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
        question.insert()
        question_list = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, question_list)
        
        return jsonify({
          'success': True,
          'created': question.id,
          'questions': current_questions,
          'total_questions': len(Question.query.all())
        })
    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  ''' 
  
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):   
    category = Category.query.filter(Category.id == category_id).first()
    
    if category is None:
      abort(404)

    try:
        question_list = Question.query.filter_by(category=category_id).all()
        current_questions = paginate_questions(request, question_list)
        if len(current_questions) == 0:
            abort(404)
    
        return jsonify({   
          'success': True,       
          'current_category': category.type,
          'questions': current_questions,
          'total_questions': len(question_list)
        })
    except:
        abort(404)

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def get_question_for_quiz():
    body = request.get_json()
    quiz_category_id = body['quiz_category']['id']
    previous_questions = body['previous_questions']

    try:
      questions_query = Question.query.filter_by(category=quiz_category_id).filter(
                                  Question.id.notin_(previous_questions)).all()
      length_of_available_question = len(questions_query)
      if length_of_available_question > 0:
        result = {
                      "success": True,
                      "question": Question.format(questions_query[random.randrange(0,length_of_available_question)])
                   }
      else:
          result = {
                      "success": True,
                      "question": None
                   }
      return jsonify(result)
    except:
      abort(404)
    
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  #Handle error 400
  @app.errorhandler(400)
  def not_found(error):
      return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request'
      }), 400

  #Handle 404 error
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
      }), 404

  #Handle error 405
  @app.errorhandler(405)
  def not_found(error):
      return jsonify({
         'success': False,
          'error': 405,
          'message': 'Method not allowed'
      }), 405

  #Handle 422 error
  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable'
      }), 422


  return app

    