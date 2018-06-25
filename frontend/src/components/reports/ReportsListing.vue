<template>
  <table class="table is-striped">
    <thead>
      <tr>
        <th>Lab</th>
        <th>Student</th>
        <th>Date Submitted</th>
        <th>Time taken</th>
        <th>Grade</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="report in reports">
        <td>{{ report.labname }}</td>
        <td>{{ report.student }}</td>
        <td>{{ dateDisplay(report.endtime) }}</td>
        <td>{{ duration(report.starttime, report.endtime) }}</td>
        <td>{{ gradeDisplay(report.id) }}</td>
        <td><router-link class="button is-small" :to="{ name: 'ManageReports', params: { id: report.id } }">Grade Details</router-link></td>
      </tr>
    </tbody>
  </table>
</template>

<script>
  import {LISTReports,
          LISTGrades,
          LISTAssessments,
          GETAssessment} from '@/api'
  export default {
    name: "ReportsListing",
    data: function () {
      return {
        reports: [],
        grades: [],
        assessments: [],
        total: null,
        score: null
      }
    },
    created: function () {
      LISTReports (json => {
        this.reports = json
        LISTGrades (json => {
          this.grades = json
          LISTAssessments (json => {
            this.assessments = json
            var pointsTotal = {}
            var scoreTotal = {}
            for (var x = 0; x < this.reports.length; x++) {
              var points = 0
              for (var y = 0; y < this.assessments.length; y++) {
                if (this.assessments[y].id === parseInt(this.reports[x].assessmentid)) {
                  for (var i = 0; i < this.assessments[y].scores.length; i++) {
                    points += parseInt(this.assessments[y].scores[i])
                  }
                }
              }
              var score = 0
              for (var y = 0; y < this.grades.length; y++) {
                if (parseInt(this.grades[y].reportid) === this.reports[x].id) {
                  if (this.grades[y].needsgrading === "false") {
                    for (var i = 0; i < this.grades[y].points.length; i++) {
                      score += parseInt(this.grades[y].points[i])
                    }
                  }
                }
              }
              var currentId = this.reports[x].id
              pointsTotal[currentId] = points
              scoreTotal[currentId] = score
            }
            this.total = pointsTotal
            this.score = scoreTotal
          })
        })
      })
    },
    computed: {

    },
    methods: {
      gradeDisplay: function(id) {
        for (var i = 0; i < this.grades.length; i++) {
          if (parseInt(this.grades[i].reportid) === id) {
            if (this.grades[i].needsgrading === "false"){
              return ((this.score[id] / this.total[id] * 100) + "% (" + this.score[id] + " out of " + this.total[id] + ")")
            }
          }
        }
        return "Needs Grading"
      },
      dateDisplay: function(ts) {
        var submitDate = new Date(ts)
        var month = ''
        var hour = ''
        var ampm = ''
        var minute = ''
        switch(submitDate.getUTCMonth()) {
          case 1:
            month = 'Jan';
            break;
          case 2:
            month = 'Feb';
            break;
          case 3:
            month = 'Mar';
            break;
          case 4:
            month = 'Apr';
            break;
          case 5:
            month = 'May';
            break;
          case 6:
            month = 'Jun';
            break;
          case 7:
            month = 'Jul';
            break;
          case 8:
            month = 'Aug';
            break;
          case 9:
            month = 'Sep';
            break;
          case 10:
            month = 'Oct';
            break;
          case 11:
            month = 'Nov';
            break;
          case 12:
            month = 'Dec';
            break;
        }
        if (submitDate.getUTCHours() > 12) {
          hour = submitDate.getUTCHours() - 12
          ampm = 'pm'
        }
        else {
          hour = submitDate.getUTCHours()
          ampm = 'am'
        }
        if (submitDate.getUTCMinutes() < 10) {
          minute = '0' + submitDate.getUTCMinutes()
        }
        else {
          minute = submitDate.getUTCMinutes()
        }
        return submitDate.getUTCDate() + " " + month
                                       + " " + submitDate.getUTCFullYear()
                                       + ", " + hour
                                       + ":" + submitDate.getUTCMinutes()
                                       + " " + ampm
      },
      duration: function (st, et) {
        var time = new Date(et - st)
        var minute = time.getUTCMinutes()
        var seconds = time.getUTCSeconds()
        if (time.getUTCMinutes() < 10) {
          minute = '0' + time.getUTCMinutes()
        }
        else {
          minute = time.getUTCMinutes()
        }
        if (time.getUTCSeconds() < 10) {
          seconds = '0' + time.getUTCSeconds()
        }
        else {
          seconds = time.getUTCSeconds()
        }
        return (time.getUTCHours() + ':' + minute + ':' + seconds)
      }
    }
  }
</script>

<style scoped>

</style>
