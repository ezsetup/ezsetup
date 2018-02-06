<template>
  <div class="main">
    <div class="columns">
      <div class="column">
        <h1 class="title">Labs</h1>
      </div>
      <div class="column is-narrow">
		    <router-link :to="{ name: 'NewLab' }" class="button is-success">Create Lab</router-link>
      </div>
    </div>
    <div class="columns">
      <div class="column">
        <LabsListing></LabsListing>
      </div>
    </div>
  </div>
</template>

<style scoped>
  .main {
    margin-top: 20px;
  }
</style>

<script>
  import LabsListing from '@/components/labs/LabsListing.vue'

  export default {
    name: 'LabsManagement',
    components: {
      LabsListing
    },
    data: function () {
      return {
      }
    },
    methods: {
    }
  }
</script>
