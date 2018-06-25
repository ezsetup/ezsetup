<template>
  <div class="center">
    <h4 class="title">Creating a new lab</h4>
    <div class="field">
      <label for="name" class="label">Name</label>
      <p class="control">
        <input class="input" v-model="name" placeholder="Lab name" />
      </p>
    </div>

    <div class="field">
      <label for="description" class="label">Description</label>
      <p class="control">
        <textarea class="textarea" v-model="description" placeholder="Lab description"></textarea>
      </p>
    </div>

    <div class="field">
      <label for="scenarioType" class="label">Scenario type</label>
      <p class="control">
        <span class="select">
          <select id="scenarioType" v-model="scenarioId" name="scenarioType">
            <option v-for="scenario in scenarios" :value="scenario.id" :key="scenario.id">{{scenario.name}}</option>
          </select>
        </span>
		    <router-link :to="{ name: 'NewScenario' }" class="button">Create Scenario</router-link>
      </p>
    </div>

    <div class="columns">
      <div class="column is-narrow">
        <div class="field">
          <label for="preAssessment" class="label">Pre-Assessment</label>
          <p class="control">
            <span class="select">
              <select id="preAssessment" v-model="preassessmentId" name="scenarioType">
                <option v-for="assessment in assessments" :value="assessment.id" :key="assessment.id">{{assessment.atitle}}</option>
              </select>
            </span>
            <router-link :to="{ name: 'newAssessment' }" class="button">Create Assessment</router-link>
          </p>
        </div>
      </div>
      <div class="column is-narrow">
        <div class="field">
          <label for="preAssessmentAttempts" class="label">Attempts Allowed</label>
          <p class="control">
            <input class="input" v-model="preAssessmentAttempts" placeholder="1" />
          </p>
        </div>
      </div>
      <div class="column"></div>
    </div>

    <div class="columns">
      <div class="column is-narrow">
        <div class="field">
          <label for="postAssessment" class="label">Post Assessment</label>
          <p class="control">
            <span class="select">
              <select id="postAssessment" v-model="postassessmentId" name="scenarioType">
                <option v-for="assessment in assessments" :value="assessment.id" :key="assessment.id">{{assessment.atitle}}</option>
              </select>
            </span>
            <router-link :to="{ name: 'newAssessment' }" class="button">Create Assessment</router-link>
          </p>
        </div>
      </div>
      <div class="column is-narrow">
        <label for="postAssessmentAttempts" class="label">Attempts Allowed</label>
        <p class="control">
          <input class="input" v-model="postAssessmentAttempts" placeholder="1"/>
        </p>
      </div>
      <div class="column"></div>
    </div>

    <div class="field">
      <button v-if="isLoading" type="submit" v-on:click="onCreateBtn" class="button is-primary is-loading">CREATE</button>
      <button v-else type="submit" v-on:click="onCreateBtn" class="button is-primary">CREATE</button>
      <p v-if="error" class="is-danger">{{error}}</p>
    </div>
  </div>
</template>

<style scoped>
  .center {
    width: 60%;
    margin: auto;
  }
</style>

<script>
import {LISTscenarios, POSTlab, LISTAssessments} from '@/api'
export default {
  name: 'NewLab',
  data: function () {
    return {
        name: null,
        description: null,
        scenarioId: null,
        scenarios: null,
        error: null,
        isLoading: false,
        preassessmentId: null,
        postassessmentId: null,
        assessments: null,
        preAssessmentAttempts: 1,
        postAssessmentAttempts: 1
    }
  },
  created: function () {
    LISTAssessments (json => {
      this.assessments = json
    })
  },
  beforeRouteEnter: function (to, from, next) {
    LISTscenarios(null, json => {
      next(vm => vm.setData(json))
    })
  },
  computed: {
    attempts: function () {
      var attemptArray = [1, 1]
      attemptArray[0] = parseInt(this.preAssessmentAttempts)
      attemptArray[1] = parseInt(this.postAssessmentAttempts)
      return attemptArray
    }
  },
  methods: {
    setData: function (json) {
      this.scenarios = json
    },
    onCreateBtn: function () {
      this.isLoading = true
      POSTlab(this.name, this.description, this.scenarioId, this.preassessmentId, this.postassessmentId, this.attempts, json => {
        this.isLoading = false
        this.$router.push('/labs')
      })
    }
  }
}
</script>
