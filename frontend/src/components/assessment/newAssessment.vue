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
    <table class="table is-striped">
    <tbody>
      <tr v-for="(question, i) in questions" track-by="$index">
        <td>{{ i + 1 }}</td>
        <td>{{ question.title }}</td>
        <td><input class="text" type="textbox" v-bind="scores[i-1]"></td>
      </tr>
    </tbody>
  </table>
    <new-question></new-question>
    <button v-if="isLoading" type="submit" class="button is-primary is-loading" @click="onSubmitBtn">SUBMIT</button>
    <button v-else type="submit" class="button is-primary" @click="onSubmitBtn">SUBMIT</button>
  </div>
</template>

<script>
import {POSTAssessment} from "@/api"
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
    isLoading: false
	}
  },
  methods: {
    onSubmitBtn: function() {
      this.isLoading = true
      POSTAssessment(this.title, this.description, this.questions, this.scores, json => {
        this.$router.push('/assessments')
        this.isLoading = false
      })
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
