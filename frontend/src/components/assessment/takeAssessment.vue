<template>
  <div class="main">
    <div class="columns">
      <div class="column is-half is-offset-one-quarter">
        <h1 class="title">{{ currentAssessment.atitle }}</h1>
        <h3 class="subtitle is-4">{{ currentAssessment.adescription }}</h3>
        <template v-for="(question, i) in allQuestions">
          <div style="padding-bottom: 1em;">
            <div>
              <strong>{{ i+1 }}. {{ question.qtext }}</strong>
            </div>
            <div style="padding-left: 1em;" v-if="question.qkind === 'textbox'">
              <input class="input" type="text" v-model="answers[i]">
            </div>
            <div style="padding-left: 1em;" v-else-if="question.qkind === 'checkbox'">
              <div><input type="checkbox" id="0" v-model="multChoiceAns[0+(i*4)]"> {{ question.answers[0] }}</div>
              <div><input type="checkbox" id="1" v-model="multChoiceAns[1+(i*4)]"> {{ question.answers[1] }}</div>
              <div><input type="checkbox" id="2" v-model="multChoiceAns[2+(i*4)]"> {{ question.answers[2] }}</div>
              <div><input type="checkbox" id="3" v-model="multChoiceAns[3+(i*4)]"> {{ question.answers[3] }}</div>
            </div>
          </div>
        </template>
        <input type="submit" class="button is-primary" @click="submitReport()">
      </div>
    </div>
  </div>
</template>

<script>
  import {GETUserSelf,
          SEARCHuser,
          POSTReports,
          GETAssessment,
          LISTAssessments,
          LISTQuestions,
          GETQuestion,
          LISTReports,
          POSTGrade} from '@/api'

  export default {
    name: "TakeAssessment",
    data: function () {
      return {
        currentAssessment: null,
        assessmentID: this.$route.params.id,
        allQuestions: [],
        searchResults: [],
        email: '',
        student: '',
        labname: this.$route.params.labname,
        answers: [],
        multChoiceAns: [],
        starttime: null,
        endtime: null,
        attempt: 1,
        isLoading: false,
        scores: []
      }
    },
    beforeRouteEnter: function (to, from, next) {
      GETAssessment(to.params.id, json => {
        next(vm => vm.setData(json))
      })
    },
    methods: {
      setData: function (assess) {
        this.currentAssessment = assess
        for (var i = 0; i < assess.questions.length; i++) {
          GETQuestion(assess.questions[i], json => {
            this.allQuestions.push(json)
          })
        }
        for (var i=0; i < (assess.questions.length  * 4); i++) {
          this.multChoiceAns[i] = false
        }
        GETUserSelf(json => {
          this.email = json.email
          SEARCHuser(this.email, json => {
            this.searchResults = json
            this.starttime = Date.now()
          })
        })
      },
      submitReport: function () {
        this.isLoading = true
        this.endtime = Date.now()
        this.assessmentID = this.currentAssessment.id
        for (var i = 0; i < this.searchResults.length; i++) {
            if (this.searchResults[i].email === this.email) {
              this.student = this.searchResults[i].fullname
            }
          }
        for (var i = 0; i < this.allQuestions.length; i++) {
          if (this.allQuestions[i].qkind === 'checkbox') {
            var mcArray = [this.multChoiceAns[0+(i*4)],
                           this.multChoiceAns[1+(i*4)],
                           this.multChoiceAns[2+(i*4)],
                           this.multChoiceAns[3+(i*4)]]
            var needed = 0
            var correct = 0
            for (var x = 0; x < mcArray.length; x++) {
              if (this.allQuestions[i].correct[x] === "true") {
                needed++
                if (mcArray[x] === true) {
                  correct++
                }
              }
              else if (this.allQuestions[i].correct[x] === "false") {
                if (mcArray[x] === true) {
                  correct--
                }
              }
            }
            if (correct < 0) {
              correct = 0
            }
            this.scores[i] = (this.currentAssessment.scores[i] * (correct / needed))
            mcArray = mcArray.toString()
            this.answers[i] = mcArray
          }
          else {
            this.scores[i] = null
          }
        }
        LISTReports(json => {
          for (var i=0; i < json.length; i++) {
            if (parseInt(json[i].assessmentid) === this.assessmentID) {
              if (json[i].student === this.student) {
                if (json[i].labname === this.labname) {
                  if(json[i].attemptNum >= this.attempt) {
                    this.attempt = json[i].attemptNum + 1
                  }
                }
              }
            }
          }
          POSTReports(this.student, this.labname, this.assessmentID, this.answers, this.starttime, this.endtime, this.attempt, json => {
            LISTReports(json => {
              var repID = 0
              for (var i = 0; i < json.length; i++) {
                if (json[i].id > repID) {
                  if (json[i].student === this.student) {
                    if (parseInt(json[i].assessmentid) === this.assessmentID) {
                      repID = json[i].id
                    }
                  }
                }
              }
              POSTGrade(this.student, repID, this.scores, [], 'true', json => {
                this.isLoading = false
                this.$router.push('/workspace')
              })
            })

          })
        })
      }
    }
  }
</script>

<style scoped>

</style>
