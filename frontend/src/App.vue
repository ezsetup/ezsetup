<template>
  <div id="app" class="container main">
    <AppNav class="my-nav"/>
    <router-view></router-view>
  </div>
</template>

<script>
  import AppNav from '@/components/AppNav.vue'
  export default {
    name: 'app',
    components: {
      AppNav: AppNav
    }
  }
</script>

<style>
  #app {
    margin-top: 60px;
  }
  th {
    font-weight: 600;
  }
</style>
