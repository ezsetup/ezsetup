<template>
  <div class="main">
    <div class="columns">
      <div class="column">
        <h1 class="title">Reports</h1>
      </div>
    </div>
    <div class="columns">
      <div class="column">
        <ReportsListing></ReportsListing>
      </div>
    </div>
  </div>
</template>

<script>
  import ReportsListing from '@/components/reports/ReportsListing.vue'
    export default {
        name: "Reports",
        components: {
          ReportsListing
        }
    }
</script>

<style scoped>

</style>
