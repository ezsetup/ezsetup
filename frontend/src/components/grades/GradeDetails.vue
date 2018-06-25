<template>
  <div class="main" v-if="!isLoading">
    <h1 class="title">{{ report.student }}</h1>
    <h3 class="subtitle is-4">{{ report.labname }}: {{ assessment.atitle }}</h3>

    <template v-for="(question, i) in questions">
      <div class="columns is-1">
        <div class="column is-2" style="text-align: right;">
          <strong>{{ i+1 }}.</strong>
        </div>
        <div class="column">
          <strong>{{ question.qtext }}</strong>
        </div>
      </div>

      <div v-if="question.qkind === 'textbox'">
        <div class="columns is-1">
          <div class="column is-2" style="text-align: right;">
            Student Response:
          </div>
          <div class="column">
            {{ answers[i] }}
          </div>
        </div>

        <div class="columns is-1">
          <div class="column is-2" style="text-align: right;">
            Correct Response:
          </div>
          <div class="column">
            <em>{{ question.answers[0] }}</em>
          </div>
        </div>
      </div>

      <div v-else-if="question.qkind === 'checkbox'">
        <div class="columns is-1">
          <div class="column is-2" style="text-align: right;">
            Student Response:
          </div>
          <div class="column">
            <div v-for="(answer, y) in answers[i]" v-if="answer === 'true'">
              {{ question.answers[y] }}
            </div>
          </div>
        </div>

        <div class="columns is-1">
          <div class="column is-2" style="text-align: right;">
            Correct Response:
          </div>
          <div class="column">
            <div v-for="(correct, x) in question.correct" v-if="correct === 'true'">
              <em>{{ question.answers[x] }}</em>
            </div>
          </div>
        </div>
      </div>
      <div class="columns is-1">
        <div class="column is-2" style="text-align: right;">
          Points:
        </div>
        <div class="column is-1">
          {{ scores[i] }} / {{ assessment.scores[i] }}
        </div>
      </div>
      <div class="columns is-1">
        <div class="column is-2" style="text-align: right;">
          Feedback:
        </div>
        <div class="column"><em>{{ question.feedback }}</em></div>
      </div>

      <div v-if="feedback[i] != null" class="columns is-1">
        <div class="column is-2" style="text-align: right;">
          Additional comments:
        </div>
        <div class="column is-half">{{ feedback[i] }}</div>
      </div>
    </template>
    <div>
      Score: {{ totalPoints }} / {{ totalPossible }}
      <br>
      Average: {{ average }}%
    </div>
  </div>
</template>

<script>
  import {GETReport,
          GETAssessment,
          GETQuestion,
          POSTGrade,
          LISTGrades,
          PATCHGrade} from '@/api'

  export default {
    name: "GradeDetails",
    data: function () {
      return {
        report: null,
        assessment: null,
        questions: [],
        scores: [],
        feedback: [],
        isLoading: false,
        gradeid: null
      }
    },
    beforeRouteEnter: function (to, from, next) {
      var report = {}
      var assessment = {}
      GETReport(to.params.id, json => {
        report = json
        GETAssessment(report.assessmentid, json => {
          assessment = json
          next(vm => vm.setData(report, assessment))
        })
      })
    },
    computed: {
      answers: function () {
        var multChoice = []
        for (var i = 0; i < this.questions.length; i++) {
          if (this.questions[i].qkind === 'checkbox') {
            multChoice.push(this.report.answers[i].split(','))
          }
          else if (this.questions[i].qkind === 'textbox') {
            multChoice.push(this.report.answers[i])
          }
        }
        return multChoice
      },
      totalPoints: function () {
        var total = 0
        for (var i = 0; i < this.scores.length; i++) {
          total += parseInt(this.scores[i])
        }
        return total
      },
      totalPossible: function () {
        var tot = 0
        for (var i = 0; i < this.assessment.scores.length; i++) {
          tot += parseInt(this.assessment.scores[i])
        }
        return tot
      },
      average: function () {
        return (this.totalPoints / this.totalPossible * 100)
      }
    },
    methods: {
      setData: function (report, assessment) {
        this.isLoading = true
        this.report = report
        this.assessment = assessment
        for (var i = 0; i < assessment.questions.length; i++) {
            GETQuestion(assessment.questions[i], json => {
              this.questions.push(json)
            })
          }
        LISTGrades(json => {
          for (var i = 0; i < json.length; i++) {
            if (json[i].reportid === report.id) {
              this.gradeid = json[i].id
              for (var x = 0; x < assessment.questions.length; x++) {
                this.scores.push(json[i].points[x])
                this.feedback.push(json[i].feedback[x])
              }
            }
          }
          if (this.gradeid === null) {
            for (var i = 0; i < assessment.questions.length; i++) {
              this.scores.push('0')
              this.feedback.push('')
            }
          }
        })
        this.isLoading = false
      },
      submitGrade: function () {
        if (this.gradeid != null) {
          PATCHGrade(this.gradeid, this.report.student, this.report.id, this.scores, this.feedback, "false", json => {
            this.$router.push('/reports')
          })
        }
        else {
          POSTGrade(this.report.student, this.report.id, this.scores, this.feedback, "false", json => {
            this.$router.push('/reports')
          })
        }
      }
    }
  }
</script>

<style scoped>

</style>
