import json
import random

def load_questions():
    as_json = {}
    with open('questions.json', 'r') as questions:
        as_json = json.loads(questions.read())
    return as_json

def get_random_question():
    questions = load_questions()
    return questions[random.randint(0, len(questions) - 1)]
