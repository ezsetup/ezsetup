<template>
  <div class="main">
    <LabsListing></LabsListing>
    <br>
    <router-link to="/labs/new" class="button">New lab</router-link>
  </div>
</template>

<style scoped>
  .main {
    margin-top: 20px;
  }
  .center {
    text-align: center;
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
