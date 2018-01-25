<template>
  <nav class="nav has-shadow">
    <div class="nav-left">
      <a class="nav-item is-tab" :class="{ 'is-active': $route.name ==='index' }" href="/">EZSetUp</a>
    </div>
    <div v-if='$store.getters.authenticated' class="nav-right">
      <a class="nav-item is-tab">{{email}}</a>
      <a class="nav-item is-tab" v-on:click="onLogoutBtn">Log Out</a>
    </div>
    <div v-else class="nav-right">
      <a class="nav-item is-tab" :class="{ 'is-active': $route.name ==='login' }" href="/login">Log in</a>
    </div>
  </nav>
</template>

<script>
  import {
    mapState
  } from 'vuex'
  import Cookies from 'js-cookie'

  export default {
    name: 'nav',
    computed: mapState({
      email: state => state.auth.email
    }),
    methods: {
      onLogoutBtn: function () {
        Cookies.remove('auth')
        this.$store.commit('logout')
        this.$router.push('/login')
      }
    }
  }
</script>
