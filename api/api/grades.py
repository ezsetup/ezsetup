from flask import jsonify, g, request
from flask_classful import route, FlaskView
from models import Grade
from auth.decorators import login_required
from api import permission_required
from postgrespy import UniqueViolatedError
from postgrespy.queries import Select


class Grades(FlaskView):
    decorators = [login_required, permission_required]

    def index(self):
        grades = Grade.fetchall()
        ret = []
        for grade in grades:
            ret.append({
                'id': grade.id,
                'student': grade.student,
                'reportid': grade.reportid,
                'points': grade.points,
                'feedback': grade.feedback,
                'needsgrading': grade.needsgrading
            })
        return jsonify(sorted(ret, key=lambda i: i['id'], reverse=True))

    def get(self, reportid):
        repid = int(reportid)
        grade = Grade.fetchone(reportid=repid)
        try:
            return jsonify({
                'id': grade.id,
                'student': grade.student,
                'reportid': grade.reportid,
                'points': grade.points,
                'feedback': grade.feedback,
                'needsgrading': grade.needsgrading
            })
        except:
            return jsonify("None")

    def post(self):
        """Create new grade"""
        student = request.get_json()['student']
        reportid = request.get_json()['reportid']
        points = request.get_json()['points']
        feedback = request.get_json()['feedback']
        needsgrading = request.get_json()['needsgrading']
        new_grade = Grade(student=student, reportid=reportid, points=points,
                                feedback=feedback, needsgrading=needsgrading)
        try:
            new_grade.save()
        except UniqueViolatedError:
            return jsonify(error="Grade for this report already exists"), 409
        return jsonify(message="ok")

    def patch(self, id):
        grade = Grade.fetchone(id=id)
        grade.student = request.get_json()['student']
        grade.reportid = request.get_json()['reportid']
        grade.points = request.get_json()['points']
        grade.feedback = request.get_json()['feedback']
        grade.needsgrading = request.get_json()['needsgrading']
        try:
            grade.save()
        except UniqueViolatedError:
            return jsonify(errors=["Duplicated email address"]), 409
        return jsonify(message='ok')