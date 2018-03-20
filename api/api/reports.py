from flask import jsonify, g, request
from flask_classful import route, FlaskView
from models import Report
from auth.decorators import login_required
from api import permission_required
from postgrespy import UniqueViolatedError
from postgrespy.queries import Select


class Reports(FlaskView):
    decorators = [login_required, permission_required]

    def index(self):
        reports = Report.fetchall()
        ret = []
        for report in reports:
            ret.append({
                'id': report.id,
                'user': report.user,
                'lab': report.lab,
                'answers': report.answers,
                'points': report.points,
                'starttime': report.starttime,
                'endtime': report.endtime
            })
        return jsonify(sorted(ret, key=lambda i: i['id'], reverse=True))

    def get(self, id):
        return "Get report"

    def post(self):
        """Create new report"""
        user = request.get_json()['user']
        lab = request.get_json()['lab']
        answers = request.get_json()['answers']
        points = request.get_json()['points']
        starttime = request.get_json()['starttime']
        endtime = request.get_json()['endtime']
        new_report = Report(user=user, lab=lab, answers=answers,
                                points=points, starttime=starttime, endtime=endtime)
        try:
            new_report.save()
        except UniqueViolatedError:
            return jsonify(error="Duplicated question title"), 409
        return jsonify(message="ok")

