from flask import Blueprint, request, jsonify
from app import db
from app.models import Request, MCQ, Option
from app.utils.mcq_generator import generate_mcq_with_gemini
from app.utils.parse_gemini_response import parse_gemini_response

api_bp = Blueprint('api', __name__)

@api_bp.route('/generate_mcq')
def generate_mcq_api():
    topic = request.args.get('topic')
    solo_level = request.args.get('solo_level')

    if not topic or not solo_level:
        return jsonify({'error': 'Missing parameters'}), 400
    if solo_level not in ['Unistructural', 'Multistructural']:
        return jsonify({'error': 'Invalid SOLO level'}), 400

    try:
        response = generate_mcq_with_gemini(topic, solo_level)
        parsed = parse_gemini_response(response)

        new_request = Request(topic=topic, solo_level=solo_level)
        db.session.add(new_request)
        db.session.commit()

        new_mcq = MCQ(question_text=parsed['question_text'], request_id=new_request.id)
        db.session.add(new_mcq)
        db.session.commit()

        correct_index = ord(parsed['correct_answer']) - ord('A')
        for i, opt in enumerate(parsed['options']):
            db.session.add(Option(mcq_id=new_mcq.id, option_text=opt, is_correct=(i == correct_index)))
        db.session.commit()

        return jsonify(parsed)
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
