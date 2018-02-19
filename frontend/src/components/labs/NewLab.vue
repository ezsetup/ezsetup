<template>
  <div class="columns">
    <div class="column is-8 is-offset-2">
      <h1 class="title">Create Lab</h1>
      <div class="field">
        <label for="name" class="label">Name</label>
        <p class="control">
          <input class="input" id="name" v-model="name" placeholder="Lab name" />
        </p>
      </div>

      <div class="field">
        <label for="description" class="label">Description</label>
        <p class="control">
          <textarea class="textarea" id="description" v-model="description" placeholder="Lab description"></textarea>
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

      <div class="field">
        <button v-if="isLoading" type="submit" v-on:click="onCreateBtn" class="button is-primary is-loading">CREATE</button>
        <button v-else type="submit" v-on:click="onCreateBtn" class="button is-primary">CREATE</button>
        <p v-if="error" class="is-danger">{{error}}</p>
      </div>
    </div>
  </div>
</template>

<script>
import {LISTscenarios, POSTlab} from '@/api'
export default {
  name: 'NewLab',
  data: function () {
    return {
        name: null,
        description: null,
        scenarioId: null,
        scenarios: null,
        error: null,
        isLoading: false
    }
  },
  beforeRouteEnter: function (to, from, next) {
    LISTscenarios(null, json => {
      next(vm => vm.setData(json))
    })
  },
  methods: {
    setData: function (json) {
      this.scenarios = json
    },
    onCreateBtn: function () {
      this.isLoading = true
      POSTlab(this.name, this.description, this.scenarioId, json => {
        this.isLoading = false
        this.$router.push('/labs')
      })
    }
  }
}
</script>
