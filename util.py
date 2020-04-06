import json

def load_questions():
    as_json = {}
    with open('questions.json', 'r') as questions:
        as_json = json.loads(questions.read())
    return as_json