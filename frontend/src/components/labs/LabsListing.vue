<template>
  <div v-if="labs.length">
    <h4 class="title">Labs</h4>
    <div v-for="(l, index) in labs" v-bind:key="index" class="columns">
      <div class="column is-2">
        <span>{{index + 1}}.</span>
        <span>{{l.name}}</span>
      </div>
      <p class="column is-4">{{l.description}}</p>
      <router-link :to="{name: 'Lab', params: {id: l.id}}" class="button is-info">Manage</router-link>
    </div>
  </div>
</template>

<script>
import {LISTlabs} from '@/api'
export default {
  name: 'LabsListing',
  data: function () {
    return {
      labs: []
    }
  },
  created: function () {
    LISTlabs(json => {
      this.labs = json
    })
  }
}
</script>