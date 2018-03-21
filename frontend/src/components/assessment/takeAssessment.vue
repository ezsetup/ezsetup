<template>
  <div class="main">
    <div class="columns">
      <div class="column">
        Select Assessment:
        <select v-model="currentAssessment">
          <option v-for="assessment in allAssessments" track-by="$index" :value="assessment">{{ assessment.atitle }}</option>
        </select>
      </div>
    </div>
    <div class="columns">
      <div class="column">
        <h1 class="title">{{ currentAssessment.atitle }}</h1>
        <p>{{ currentAssessment.adescription }}</p>
        <div v-for="(question, i) in currentAssessment.questions">
          {{ question.qtext }}
          <div v-if="question.qkind === 'textbox'">
            <input class="input" type="text" v-model="answers[i]">
          </div>
          <div v-else-if="question.qkind === 'checkbox'">
            <div>
              {{ question.answers[0] }}
              <br>
              {{ questions.answers[1] }}
              <br>
              {{ questions.answers[2] }}
              <br>
              {{ questions.answers[3] }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import {POSTReports} from "@/api"
  import {LISTAssessments} from "@/api"
  import {GETAssessment} from "@/api";

  export default {
    name: "TakeAssessment",
    data: function () {
      return {
        currentAssessment: [],
        allAssessments: [],
        student: '',
        labname: '',
        answers: [],
        points: [],
        starttime:'',
        endtime: '',
        isLoading: false
      }
    },
    created: function () {
      LISTAssessments(json => {
        this.allAssessments = json
      })
    },
    methods: {
      submitReport: function () {
        this.endtime = Date.now()
        this.isLoading = true
        POSTReports(this.student, this.labname, this.answers, this.points, this.starttime, this.endtime, json => {
          this.$router.push('/reports')
        })
        this.isLoading = false
      }
    }
  }
</script>

<style scoped>

</style>
