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
                'student': report.student,
                'labname': report.labname,
                'assessmentid': report.assessmentid,
                'answers': report.answers,
                'starttime': report.starttime,
                'endtime': report.endtime,
                'attemptNum': report.attempt_num
            })
        return jsonify(sorted(ret, key=lambda i: i['id'], reverse=True))

    def get(self, id):
        rep = Report.fetchone(id=id)
        return jsonify({
            'id': rep.id,
            'student': rep.student,
            'labname': rep.labname,
            'assessmentid': rep.assessmentid,
            'answers': rep.answers,
            'starttime': rep.starttime,
            'endtime': rep.endtime,
            'attemptNum': rep.attempt_num
        })

    def post(self):
        """Create new report"""
        student = request.get_json()['student']
        labname = request.get_json()['labname']
        assessmentid = request.get_json()['assessmentid']
        answers = request.get_json()['answers']
        starttime = request.get_json()['starttime']
        endtime = request.get_json()['endtime']
        attempt_num = request.get_json()['attemptNum']
        new_report = Report(student=student, labname=labname, assessmentid=assessmentid, answers=answers,
                                starttime=starttime, endtime=endtime, attempt_num=attempt_num)
        try:
            new_report.save()
        except UniqueViolatedError:
            return jsonify(error=""), 409
        return jsonify(message="ok")

