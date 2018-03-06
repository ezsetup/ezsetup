<template>
  <div>
    <div>
      <button class="button is-success" v-if="!addQuestion" @click="checkQuestion">Create New Question</button>
    </div>
    <div v-if="addQuestion">
      Question Type
      <br>
      <select v-model="qkind">
        <option value="textbox">Short Answer</option>
        <option value="checkbox">Multiple Choice</option>
      </select>
      <br>
      <br>
      <div v-if="qkind === 'textbox'">
        Title
        <br>
        <input class="input" v-model="qtitle" type="text" size=64 placeholder="Enter a title to reuse this question">
        <br><br>
        Question
        <br>
        <textarea class="textarea" v-model="qtext" rows=2 cols=80 placeholder="Enter the question text here"></textarea>
        <br><br>
        Correct Answer(s)
        <br>
        <textarea class="textarea" v-model="answers[0]" rows=2 cols=80 placeholder="Enter potential correct answer strings separated by commas"></textarea>
        <br><br>
        Feedback
        <br>
        <textarea class="textarea" v-model="feedback" rows=2 cols=80 placeholder="Enter feedback for the student here"></textarea>
        <br><br>
      </div>
      <div v-else-if="qkind === 'checkbox'">
        Title
        <br>
        <input class="input" v-model="qtitle" type="text" size=64 placeholder="Enter a title to reuse this question">
        <br><br>
        Question
        <br>
        <textarea class="textarea" v-model="qtext" rows=2 cols=80 placeholder="Enter the question text here"></textarea>
        <br><br>
        <table>
          <tr>
            <td>
              Answer 1
              <br>
              <textarea class="textarea" v-model="answers[0]" rows=2 cols=64 placeholder="Enter the question text here"></textarea> Correct Answer <input type="checkbox" v-model="correct[0]" value=1>
              <br><br>
            </td>
            <td>
              Answer 2
              <br>
              <textarea class="textarea" v-model="answers[1]" rows=2 cols=64 placeholder="Enter the question text here"></textarea>Correct Answer <input type="checkbox" v-model="correct[1]" value=2>
              <br><br>
            </td>
          </tr>
          <tr>
            <td>
              Answer 3
              <br>
              <textarea class="textarea" v-model="answers[2]" rows=2 cols=64 placeholder="Enter the question text here"></textarea>Correct Answer <input type="checkbox" v-model="correct[2]" value=3>
              <br><br>
            </td>
            <td>
              Answer 4
              <br>
              <textarea class="textarea" v-model="answers[3]" rows=2 cols=64 placeholder="Enter the question text here"></textarea>Correct Answer <input type="checkbox" v-model="correct[3]" value=4>
              <br><br>
            </td>
          </tr>
        </table>
        Feedback
        <br>
        <textarea class="textarea" v-model="feedback" rows=2 cols=80 placeholder="Enter feedback for the student here"></textarea>
      </div>
      <button v-if="isLoading" type="submit" class="button is-primary is-loading" @click="submitQuestion">Save Question</button>
      <button v-else type="submit" class="button is-primary" @click="submitQuestion">Save Question</button>
    </div>
  </div>
</template>

<script>
import {POSTQuestion} from '@/api'
export default {
  name: 'newQuestion',
  data: function () {
    return {
    addQuestion: false,
	  qkind: '',
	  qtitle: '',
	  qtext: '',
	  answers: [],
	  correct: [],
	  feedback: '',
    isLoading: false,
	}
  },
  methods: {
	  submitQuestion: function() {
      this.isLoading = true
      POSTQuestion(this.qkind, this.qtitle, this.qtext, this.answers, this.correct, this.feedback, json => {
        this.$router.push('/questions')})
        this.addQuestion = false
        this.isLoading = false
    },
    checkQuestion: function () {
	    if(!this.addQuestion) {
        return this.addQuestion=true
	    }
	    else {
	      return this.newQuestion=false
	    }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#Question {
  text-align: left;
  padding: 0 10px 0 10px;
}

table {
  width: 80%;
}

td {
  padding-right: 10px;
}
</style>
