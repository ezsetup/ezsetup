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
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #222222;
  margin-top: 60px;
}
</style>
