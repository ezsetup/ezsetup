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
    <div class="columns" v-for="(question, i) in displayQuestions" track-by="$index">
      <div class="column is-half">
        <div>
          <strong>{{ i + 1 }}. &nbsp; {{ question.qtext }}</strong>
        </div>
        <br>
        <div class="columns" v-for="(answer, x) in question.answers" track-by="$index">
          <div v-if="question.correct[x] === 'true'" class="column is-narrow" style="padding-top: 0; padding-bottom: 0;">
            &#9745;
          </div>
          <div v-else class="column is-narrow" style="visibility:hidden; padding-top: 0; padding-bottom: 0;">
            &#9745;
          </div>
          <div class="column is-narrow" style="padding-top: 0; padding-bottom: 0;">
            {{ answer }}
          </div>
        </div>
        <div>
          Feedback:<br>
          {{ question.feedback }}
        </div>
      </div>
      <div class="column is-2">
        Point value: <input class="input" type="number" v-model="scores[i]">
      </div>
    </div>
    <div class="columns">
      <div class="column is-narrow">
        <div class="field has-addons">
          <div class="control">
            <div class="select is-success">
              <select v-model="currentQuestion">
                <option v-for="question in allQuestions" track-by="$index" :value="question">{{ question.qtitle }}</option>
              </select>
            </div>
          </div>
          <div class="control">
            <button class="button is-success is-outlined" @click="addQuestion">Add Question</button>
          </div>
        </div>
      </div>
      <div class="column is-narrow">
        <button class="button is-success" v-if="!addingQuestion" @click="checkQuestion">Create New Question</button>
      </div>
    </div>

    <div v-if="addingQuestion">
      Question Type
      <br>
      <select class="select is-success" v-model="question.qkind">
        <option value="textbox">Short Answer</option>
        <option value="checkbox">Multiple Choice</option>
      </select>
      <br>
      <br>
      <div v-if="question.qkind === 'textbox'">
        Title
        <br>
        <input class="input" v-model="question.qtitle" type="text" size=64 placeholder="Enter a title to reuse this question">
        <br><br>
        Question
        <br>
        <textarea class="textarea" v-model="question.qtext" rows=2 cols=80 placeholder="Enter the question text here"></textarea>
        <br><br>
        Correct Answer(s)
        <br>
        <textarea class="textarea" v-model="question.answers[0]" rows=2 cols=80 placeholder="Enter potential correct answer strings separated by commas"></textarea>
        <br><br>
        Feedback
        <br>
        <textarea class="textarea" v-model="question.feedback" rows=2 cols=80 placeholder="Enter feedback for the student here"></textarea>
        <br><br>
      </div>
      <div v-else-if="question.qkind === 'checkbox'">
        Title
        <br>
        <input class="input" v-model="question.qtitle" type="text" size=64 placeholder="Enter a title to reuse this question">
        <br><br>
        Question
        <br>
        <textarea class="textarea" v-model="question.qtext" rows=2 cols=80 placeholder="Enter the question text here"></textarea>
        <br><br>
        <table>
          <tr>
            <td>
              Answer 1
              <br>
              <textarea class="textarea" v-model="question.answers[0]" rows=2 cols=64 placeholder="Enter the question text here"></textarea> Correct Answer <input type="checkbox" v-model="question.correct[0]">
              <br><br>
            </td>
            <td>
              Answer 2
              <br>
              <textarea class="textarea" v-model="question.answers[1]" rows=2 cols=64 placeholder="Enter the question text here"></textarea>Correct Answer <input type="checkbox" v-model="question.correct[1]">
              <br><br>
            </td>
          </tr>
          <tr>
            <td>
              Answer 3
              <br>
              <textarea class="textarea" v-model="question.answers[2]" rows=2 cols=64 placeholder="Enter the question text here"></textarea>Correct Answer <input type="checkbox" v-model="question.correct[2]">
              <br><br>
            </td>
            <td>
              Answer 4
              <br>
              <textarea class="textarea" v-model="question.answers[3]" rows=2 cols=64 placeholder="Enter the question text here"></textarea>Correct Answer <input type="checkbox" v-model="question.correct[3]">
              <br><br>
            </td>
          </tr>
        </table>
        Feedback
        <br>
        <textarea class="textarea" v-model="question.feedback" rows=2 cols=80 placeholder="Enter feedback for the student here"></textarea>
      </div>
      <button v-if="isLoading" type="submit" class="button is-primary is-loading" @click="submitQuestion">Save Question</button>
      <button v-else type="submit" class="button is-primary" @click="submitQuestion">Save Question</button>
    </div>
    <br>
    <button v-if="isLoading" type="submit" class="button is-primary is-loading" @click="submitAssessment">Save Assessment</button>
    <button v-else type="submit" class="button is-primary" @click="submitAssessment">Save Assessment</button>
  </div>
</template>

<script>
import {POSTAssessment,
        LISTQuestions,
        POSTQuestion} from '@/api'
export default {
  name: 'newAssessment',
  data: function () {
    return {
      title: '',
      description: '',
      questions: [],
      displayQuestions: [],
      scores: [],
      newQuestion: false,
      isLoading: false,
      allQuestions: [],
      currentQuestion: '',
      createdQuestion: null,
      addingQuestion: false,
      question: {
        qkind: '',
        qtitle: '',
        qtext: '',
        answers: [],
        correct: [],
        feedback: ''
      }
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
      this.questions.push(this.currentQuestion.id)
      this.displayQuestions.push(this.currentQuestion)
      this.$router.push('/assessment/new')
    },
    submitQuestion: function() {
      this.isLoading = true
      if (this.question.qkind === "checkbox") {
        for (var i = 0; i < this.question.correct.length; i++) {
          if (this.question.correct[i] != true) {
            this.question.correct[i] = false
          }
        }
        for (var i = this.question.correct.length; i < 4; i++) {
          this.question.correct.push(false)
        }
      }
      POSTQuestion(this.question.qkind,
                   this.question.qtitle,
                   this.question.qtext,
                   this.question.answers,
                   this.question.correct,
                   this.question.feedback, json => {
        this.question.qkind = ''
        this.question.qtitle = ''
        this.question.qtext = ''
        this.question.answers = []
        this.question.correct = []
        this.question.feedback = ''
        this.addingQuestion = false
        this.isLoading = false
        LISTQuestions (json => {
          this.allQuestions = json
        })
      })

    },
    checkQuestion: function () {
	    if(!this.addingQuestion) {
        return this.addingQuestion=true
	    }
	    else {
	      return this.addingQuestion=false
	    }
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
