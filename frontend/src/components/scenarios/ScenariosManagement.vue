<template>
  <div>
    <div class="columns">
      <div class="column">
        <h1 class="title">Scenarios</h1>
      </div>
      <div class="column is-narrow">
		    <router-link :to="{ name: 'NewScenario' }" class="button is-success">Create Scenario</router-link>
      </div>
    </div>
    <div class="columns">
      <div class="column">
        <ScenariosListing></ScenariosListing>
      </div>
    </div>
  </div>
</template>

<script>
  import ScenariosListing from '@/components/scenarios/ScenariosListing.vue'

  export default {
    name: 'ScenariosManagement',
    components: {
      ScenariosListing
    },
    data: function () {
      return {
      }
    },
    methods: {
    }
  }
</script>
