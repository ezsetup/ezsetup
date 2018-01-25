<template>
  <div class="main">
    <ScenariosListing></ScenariosListing>
    <br>
		<router-link :to="{name: 'NewScenario'}" class="button">New scenario</router-link>
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
