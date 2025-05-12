from flask import Blueprint, request, jsonify
from app import db
from app.models import Request, MCQ, Option
from app.utils.mcq_generator import generate_mcq_with_gemini
from app.utils.parse_gemini_response import parse_gemini_response

# Creating a Blueprint for API routes
api_bp = Blueprint('api', __name__)

# Define the API route to generate MCQ based on a topic and SOLO level
@api_bp.route('/generate_mcq')
def generate_mcq_api():
    # Retrievig the query parameters from the request
    topic = request.args.get('topic')
    solo_level = request.args.get('solo_level')

    # basic error handling for API calls and invalid inputs.
    if not topic or not solo_level:
        return jsonify({'error': 'Missing parameters'}), 400
    if solo_level not in ['Unistructural', 'Multistructural']:
        return jsonify({'error': 'Invalid SOLO level'}), 400

    try:
        # Step 1: Generate MCQ using Gemini API based on topic and SOLO level
        response = generate_mcq_with_gemini(topic, solo_level)
        # Step 2: Parse the Gemini API response into structured format
        parsed = parse_gemini_response(response)

        # Step 3: Store request info (topic and SOLO level) in the database
        new_request = Request(topic=topic, solo_level=solo_level)
        db.session.add(new_request)
        db.session.commit()

        # Step 4: Create an MCQ entry linked to the request
        new_mcq = MCQ(question_text=parsed['question_text'], request_id=new_request.id)
        db.session.add(new_mcq)
        db.session.commit()

        # Step 5: Add options for the MCQ, marking the correct one
        # Getting correct index by subtracting ASCII value of the correct option with A
        correct_index = ord(parsed['correct_answer']) - ord('A')
        for i, opt in enumerate(parsed['options']):
            db.session.add(Option(mcq_id=new_mcq.id, option_text=opt, is_correct=(i == correct_index)))
        db.session.commit()

        # Step 6: Return the parsed MCQ as JSON response
        return jsonify(parsed)
    except Exception as e:
        # Rollback any DB changes if an error occurs, and return error message
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
