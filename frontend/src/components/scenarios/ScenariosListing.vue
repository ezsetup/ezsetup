<template>
  <table class="table is-striped">
    <thead>
      <tr>
        <th>#</th>
        <th>Name</th>
        <th>Description</th>
        <th>Networks</th>
        <th>Instances</th>
        <th>Routers</th>
        <th>Action</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(scenario, i) in scenarios" track-by="$index">
        <td>{{ i + 1 }}</td>
        <td><router-link :to="{ name: 'ScenarioEditor', params: { id: scenario.id } }">{{ scenario.name }}</router-link></td>
        <td>{{ scenario.description }}</td>
        <td>{{ scenario.topo.networks.length }}</td>
        <td>{{ scenario.topo.instances.length }}</td>
        <td>{{ scenario.topo.routers.length }}</td>
        <td><router-link class="button is-small" :to="{ name: 'ScenarioEditor', params: { id: scenario.id } }">Edit</router-link></td>
      </tr>
    </tbody>
  </table>
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
    LISTscenarios(null, json => {
      this.scenarios = json
    })
  }
}
</script>
