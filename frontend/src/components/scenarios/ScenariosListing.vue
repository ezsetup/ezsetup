<template>
  <div>
    <div v-for="(scenario, index) in scenarios" v-bind:key="index" class="columns">
      <div class="column is-2">
        <span>{{index + 1}}.</span>
        <span>{{scenario.name}}</span>
      </div>
      <p class="column is-4">{{scenario.description}}</p>
      <router-link class="button is-info" :to="{name: 'ScenarioEditor', params: {id: scenario.id}}">Edit</router-link>
    </div>
  </div>
</template>

<script>
import {LISTscenarios} from '@/api'
export default {
  name: "ScenariosListing",
  data: function () {
    return {
      scenarios: []
    }
  },
  created: function () {
    LISTscenarios('?privateOnly=true', json => {
      this.scenarios = json
    })
  }
}
</script>