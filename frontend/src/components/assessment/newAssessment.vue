<template>
  <div>
    Title
    <br>
    <input class="input" type="text" v-model="title" size=80 placeholder="Enter a title for the assessment">
    <br><br>
    Description
    <br>
    <textarea class="textarea" v-model="description" cols=80 rows=4 placeholder="Enter a description and instructions for the assessment"></textarea>
    <br><br>
    <div v-for="(question, i) in questions" track-by="$index">
      <strong>{{ i + 1 }}. &nbsp; {{ question.qtitle }}</strong>
      <br>
      {{ question.qtext }}
      <br>
      <table>
        <tbody>
          <tr v-for="(answer, x) in question.answers" track-by="$index">
            <td><p v-if="question.correct[x]">&#9745;</p></td><td>{{ answer }}</td>
          </tr>
        </tbody>
      </table>
      {{ question.feedback }}
    </div>
    <select v-model="currentQuestion">
      <option v-for="question in allQuestions" track-by="$index" :value="question">{{ question.qtitle }}</option>
    </select>
    <button class="button is-success" @click="addQuestion">Add Question</button>
    <br>
    <new-question></new-question>
    <br>
    <button v-if="isLoading" type="submit" class="button is-primary is-loading" @click="submitAssessment">Save Assessment</button>
    <button v-else type="submit" class="button is-primary" @click="submitAssessment">Save Assessment</button>
  </div>
</template>

<script>
import {POSTAssessment} from '@/api'
import {LISTQuestions} from '@/api'
import newQuestion from '@/components/assessment/newQuestion.vue'
export default {
  name: 'newAssessment',
  components: {
    newQuestion
  },
  data: function () {
    return {
    title: '',
	  description: '',
    questions: [],
    scores: [],
	  newQuestion: false,
    isLoading: false,
    allQuestions: [],
    nextQuestion: 0,
    currentQuestion: ''
	}
  },
  created: function () {
    LISTQuestions (json => {
      this.allQuestions = json
    })
  },
  methods: {
    submitAssessment: function() {
      this.isLoading = true
      POSTAssessment(this.title, this.description, this.questions, this.scores, json => {
        this.$router.push('/assessment')})
        this.isLoading = false
    },
    addQuestion: function() {
      this.questions[this.nextQuestion] = this.currentQuestion
      this.nextQuestion += 1
      this.$router.push('/assessment/new')
    }
  }
}
</script>

<style>
#assessment {
  text-align: left;
  padding: 0 10px 0 10px;
}
</style>
