from flask import jsonify, g, request
from flask_classful import route, FlaskView
from models import Assessments
from auth.decorators import login_required
from api import permission_required
from postgrespy import UniqueViolatedError
from postgrespy.queries import Select


class Questions(FlaskView):
    decorators = [login_required, permission_required]

    def index(self):
        questions = Questions.fetchall()
        ret = []
        for question in questions:
            ret.append({
                'id': question.id,
                'qtitle': question.qtitle,
                'question': question.question,
                'answers': question.answers,
                'correct': question.correct,
                'feedback': question.feedback
            })
        return jsonify(sorted(ret, key=lambda i: i['id'], reverse=True))

    def get(self, id):
        return "Get question"

    def post(self):
        """Create new question"""
        qtitle = request.get_json()['qtitle']
        question = request.get_json()['question']
        answers = request.get_json()['answers']
        correct = request.get_json()['correct']
        feedback = request.get_json()['feedback']
        new_question = Questions(qtitle=qtitle, question=question,
                        answers=answers, correct=correct, feedback=feedback)
        try:
            new_question.save()
        except UniqueViolatedError:
            return jsonify(error="Duplicated assessment title"), 409
        return jsonify(message="ok")

