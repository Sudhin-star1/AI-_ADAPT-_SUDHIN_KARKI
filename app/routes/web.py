from flask import Blueprint, request, render_template
from app import db
from app.models import Request, MCQ, Option
from app.utils.mcq_generator import generate_mcq_with_gemini
from app.utils.parse_gemini_response import parse_gemini_response

# Creating a blueprint for web routes
web_bp = Blueprint('web', __name__)

@web_bp.route('/generate_mcq')
def generate_mcq_web():
    topic = request.args.get('topic')
    solo_level = request.args.get('solo_level')

    if not topic or not solo_level:
        return "Missing topic or solo_level parameters", 400
    if solo_level not in ['Unistructural', 'Multistructural']:
        return "Invalid solo_level. Must be Unistructural or Multistructural", 400

    try:
        # Get response from Gemini
        gemini_response = generate_mcq_with_gemini(topic, solo_level)
        parsed_data = parse_gemini_response(gemini_response)

        # basic Error handling
        if not parsed_data['question_text'] or not parsed_data['options'] or not parsed_data['correct_answer']:
            raise ValueError("Failed to parse Gemini response")

        # save new requests
        new_request = Request(topic=topic, solo_level=solo_level)
        db.session.add(new_request)
        db.session.commit()

        # save generated quesitons
        new_mcq = MCQ(question_text=parsed_data['question_text'], request_id=new_request.id)
        db.session.add(new_mcq)
        db.session.commit()

        # Store the options and mark the correct one
        correct_index = ord(parsed_data['correct_answer']) - ord('A')
        for i, option_text in enumerate(parsed_data['options']):
            is_correct = (i == correct_index)
            new_option = Option(
                mcq_id=new_mcq.id,
                option_text=option_text,
                is_correct=is_correct
            )
            print("new_option",new_option)
            db.session.add(new_option)
        db.session.commit()
        print("Okay")

        # Render the result in an HTML template
        return render_template('mcq.html', 
                             question=parsed_data['question_text'],
                             options=parsed_data['options'],
                             correct_answer=parsed_data['correct_answer'])
    except Exception as e:
        # Rollback on any failure
        db.session.rollback()
        return f"An error occurred: {str(e)}", 500
