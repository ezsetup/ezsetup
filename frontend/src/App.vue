<template>
  <div>
    <AppNav/>
    <section class="section">
      <div class="container">
        <router-view></router-view>
      </div>
    </section>
  </div>
</template>

<script>
  import {
    GETUserSelf
  } from '@/api'
  import AppNav from '@/components/AppNav.vue'

  export default {
    name: 'app',
    components: {
      AppNav: AppNav
    },
    beforeCreate() {
      if (this.$store.getters.authenticated) {
        GETUserSelf(json => {
          this.$store.commit('setUserInfo', json)
        })
      }
    }
  }
</script>
