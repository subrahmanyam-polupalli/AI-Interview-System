# ai_engine/question_generator.py

import random

def generate_questions():

    questions = [

        "Tell me about yourself",

        "What are your strengths?",

        "What are your weaknesses?",

        "Why should we hire you?",

        "Where do you see yourself in five years?",

        "Describe a challenging situation you faced.",

        "Why do you want to work at our company?",

        "How do you handle pressure or stress?",

        "Tell me about a time you worked in a team.",

        "What motivates you to do your best work?"

    ]

    # Randomize questions
    random.shuffle(questions)

    # Return first 5 questions
    return questions[:5]