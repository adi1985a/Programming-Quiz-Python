import random

class Quiz:
    def __init__(self, questions, user=None):
        self.questions = questions  # List of dicts: {'question', 'type', 'options', 'answer', 'hint'}
        self.current_question = 0
        self.points = 0
        self.user = user
        self.lifelines = {
            'fifty_fifty': True,
            'hint': True,
            'skip': True
        }
        self.used_lifelines = []

    def next_question(self):
        self.current_question += 1

    def check_answer(self, user_answer):
        q = self.questions[self.current_question]
        correct = q['answer']
        if q['type'] == 'single':
            return user_answer == correct
        elif q['type'] == 'multiple':
            return set(user_answer) == set(correct)
        elif q['type'] == 'open':
            # Check if at least 2 key words from answer are present
            user_answer = user_answer.lower()
            correct_answer = correct.lower()
            key_words = [word for word in correct_answer.split() if len(word) > 3][:5]
            matches = sum(1 for word in key_words if word in user_answer)
            return matches >= 2
        return False

    def use_fifty_fifty(self):
        q = self.questions[self.current_question]
        if q['type'] not in ['single', 'multiple']:
            return []
        correct = q['answer'] if isinstance(q['answer'], list) else [q['answer']]
        options = q['options'][:]
        to_remove = [opt for opt in options if opt not in correct]
        if len(to_remove) > 1:
            remove = random.sample(to_remove, len(to_remove)-1)
            return [opt for opt in options if opt not in remove]
        return options

    def use_hint(self):
        q = self.questions[self.current_question]
        return q.get('hint', 'No hint available for this question.')

    def use_skip(self):
        self.current_question += 1

    def get_progress(self):
        return self.current_question, len(self.questions) 