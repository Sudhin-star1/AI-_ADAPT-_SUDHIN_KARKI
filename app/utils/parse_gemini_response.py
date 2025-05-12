def parse_gemini_response(response_text):
    lines = [line.strip() for line in response_text.split('\n') if line.strip()]
    question = None
    options = []
    correct_answer = None

    for line in lines:
        if line.startswith('Question:'):
            question = line.replace('Question:', '').strip()
        elif line.startswith(('A)', 'B)', 'C)', 'D)')):
            option_text = line[3:].strip()
            options.append(option_text)
        elif line.startswith('Correct Answer:'):
            correct_answer = line.split(':')[-1].strip().upper()

    return {
        'question_text': question,
        'options': options,
        'correct_answer': correct_answer
    }