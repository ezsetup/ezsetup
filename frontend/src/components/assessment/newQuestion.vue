<template>
  <div>
    <div>
      <button class="button is-success" v-if="!newQuestion" @click="addQuestion">Create New Question</button>
    </div>
    <div v-if="newQuestion">
      Question Type
      <br>
      <select v-model="qtype">
        <option value="text">Text</option>
        <option value="checkbox">Multiple Choice</option>
      </select>
      <br>
      <br>
      <div v-if="qtype === 'text'">
        Title
        <br>
        <input v-model="qtitle" type="text" size=64 placeholder="Enter a title to reuse this question">
        <br><br>
        Question
        <br>
        <textarea v-model="question" rows=2 cols=80 placeholder="Enter the question text here"></textarea>
        <br><br>
        Feedback
        <br>
        <textarea v-model="feedback" rows=2 cols=80 placeholder="Enter feedback for the student here"></textarea>
        <br><br>
        Correct Answer(s)
        <br>
        <textarea v-model="correct" rows=2 cols=80 placeholder="Enter potential correct answer strings separated by commas"></textarea>
      </div>
      <div v-else-if="qtype === 'checkbox'">
        Title
        <br>
        <input v-model="qtitle" type="text" size=64 placeholder="Enter a title to reuse this question">
        <br><br>
        Question
        <br>
        <textarea v-model="question" rows=2 cols=80 placeholder="Enter the question text here"></textarea>
        <br><br>
        <table>
          <tr>
            <td>
              Answer 1
              <br>
              <textarea v-model="answers[0]" rows=2 cols=64 placeholder="Enter the question text here"></textarea> Correct Answer <input type="checkbox" v-model="correct[0]" value=1>
              <br><br>
            </td>
            <td>
              Answer 2
              <br>
              <textarea v-model="answers[1]" rows=2 cols=64 placeholder="Enter the question text here"></textarea>Correct Answer <input type="checkbox" v-model="correct[1]" value=2>
              <br><br>
            </td>
          </tr>
          <tr>
            <td>
              Answer 3
              <br>
              <textarea v-model="answers[2]" rows=2 cols=64 placeholder="Enter the question text here"></textarea>Correct Answer <input type="checkbox" v-model="correct[2]" value=3>
              <br><br>
            </td>
            <td>
              Answer 4
              <br>
              <textarea v-model="answers[3]" rows=2 cols=64 placeholder="Enter the question text here"></textarea>Correct Answer <input type="checkbox" v-model="correct[3]" value=4>
              <br><br>
            </td>
          </tr>
        </table>
        Feedback
        <br>
        <textarea v-model="feedback" rows=2 cols=80 placeholder="Enter feedback for the student here"></textarea>
      </div>
    <button class="button is-success" type="button" @click="onSubmitBtn">Save Question</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'newQuestion',
  data: function () {
    return {
    newQuestion: false,
	  qtype: '',
	  qtitle: '',
	  question: '',
	  answers: [],
	  correct: [],
	  feedback: ''
	}
  },
  methods: {
	onSubmitBtn: function() {
      this.isLoading = true
      POSTQuestion(this.qtitle, this.question, this.answers, this.correct, this.feedback, json => {
        this.$router.push('/questions')
        this.newQuestion = false
        this.isLoading = false
      })
    },
    addQuestion: function () {
	    if(!this.newQuestion) {
        return this.newQuestion=true
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
