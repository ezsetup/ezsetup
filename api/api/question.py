from flask import jsonify, g, request
from flask_classful import route, FlaskView
from models import Question
from auth.decorators import login_required
from api import permission_required
from postgrespy import UniqueViolatedError
from postgrespy.queries import Select


class Questions(FlaskView):
    decorators = [login_required, permission_required]

    def index(self):
        questions = Question.fetchall()
        ret = []
        for question in questions:
            ret.append({
                'id': question.id,
                'qkind': question.qkind,
                'qtitle': question.qtitle,
                'qtext': question.qtext,
                'answers': question.answers,
                'correct': question.correct,
                'feedback': question.feedback
            })
        return jsonify(sorted(ret, key=lambda i: i['id'], reverse=True))

    def get(self, id):
        return "Get question"

    def post(self):
        """Create new question"""
        qkind = request.get_json()['qkind']
        qtitle = request.get_json()['qtitle']
        qtext = request.get_json()['qtext']
        answers = request.get_json()['answers']
        correct = request.get_json()['correct']
        feedback = request.get_json()['feedback']
        new_question = Question(qkind=qkind, qtitle=qtitle, qtext=qtext,
                        answers=answers, correct=correct, feedback=feedback)
        try:
            new_question.save()
        except UniqueViolatedError:
            return jsonify(error="Duplicated question title"), 409
        return jsonify(message="ok")

