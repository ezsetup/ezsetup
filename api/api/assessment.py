from flask import jsonify, g, request
from flask_classful import route, FlaskView
from models import Assessments
from auth.decorators import login_required
from api import permission_required
from postgrespy import UniqueViolatedError
from postgrespy.queries import Select


class Assessments(FlaskView):
    decorators = [login_required, permission_required]

    def index(self):
        assessments = Assessments.fetchall()
        ret = []
        for assessment in assessments:
            ret.append({
                'id': assessment.id,
                'atitle': assessment.atitle,
                'adescription': assessment.adescription,
                'questions': assessment.questions,
                'scores': assessment.scores
            })
        return jsonify(sorted(ret, key=lambda i: i['id'], reverse=True))

    def get(self, id):
        return "Get assessment"

    def post(self):
        """Create new assessment"""
        atitle = request.get_json()['atitle']
        adescription = request.get_json()['adescription']
        questions = request.get_json()['questions']
        scores = request.get_json()['scores']
        new_assessment = Assessments(atitle=atitle, adescription=adescription,
                        questions=questions, scores=scores)
        try:
            new_assessment.save()
        except UniqueViolatedError:
            return jsonify(error="Duplicated assessment title"), 409
        return jsonify(message="ok")

