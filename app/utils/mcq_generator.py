import google.generativeai as genai
from flask import current_app

content_snippet = "Photosynthesis is the process by which plants use sunlight, water, and carbon dioxide to create glucose and oxygen. Chlorophyll absorbs sunlight."


def generate_mcq_with_gemini(topic, solo_level):
    genai.configure(api_key=current_app.config["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    Given the following content about photosynthesis: {content_snippet}

    Generate a single multiple-choice question (MCQ) that aligns with the topic '{topic}' and targets the '{solo_level}' SOLO taxonomy level. 

    The question should have 3-4 plausible answer options, with one correct answer. 

    Format your response as follows:

    Question: [Your question here]
    Options:
    A) [Option A]
    B) [Option B]
    C) [Option C]
    D) [Option D]
    Correct Answer: [Letter of the correct option, e.g., A, B, C, or D]

    For the SOLO level:
    - Unistructural: Focus on recalling a single piece of information.
    - Multistructural: Focus on recalling several pieces of information or listing multiple aspects.
    - Relational: Focus on comparing and explaining the relationsips.
    - Extended Abstract: Focus on hypothesis beyond the context.
    """
    response = model.generate_content(prompt)
    return response.text
