<template>
  <nav class="navbar has-shadow">
    <div class="container">
      <div class="navbar-brand">
        <a class="navbar-item" :class="{ 'is-active': $route.name ==='index' }" href="/"
           style="font-family: 'Montserrat', sans-serif; font-size: 23px;">
          <span style="color: #23d160">ez</span>setup
        </a>
      </div>
      <div class="navbar-menu">
        <div v-if='$store.getters.authenticated' class="navbar-start">
          <router-link v-if="$store.getters.permissionGroups.includes('labs')"
                       :class="{ 'is-active': this.$route.path.startsWith('/labs'), 'navbar-item': true }"
                       to="/labs">Labs</router-link>
          <router-link v-if="$store.getters.permissionGroups.includes('scenarios')"
                       :class="{ 'is-active': this.$route.path.startsWith('/scenarios'), 'navbar-item': true }"
                       to="/scenarios">Scenarios</router-link>
          <router-link v-if="$store.getters.permissionGroups.includes('users')"
                       :class="{ 'is-active': this.$route.path.startsWith('/users'), 'navbar-item': true }"
                       to="/users">Users</router-link>
          <router-link v-if="!$store.getters.isRoot"
                       :class="{ 'is-active': this.$route.path.startsWith('/workspace'), 'navbar-item': true }"
                       to="/workspace">Workspace</router-link>
        </div>
        <div class="navbar-end">
          <div v-if='$store.getters.authenticated' class="navbar-item has-dropdown is-hoverable is-right">
            <a class="navbar-link">{{ email }}</a>
            <div class="navbar-dropdown">
              <a class="navbar-item" v-on:click="logout">Log Out</a>
            </div>
          </div>
          <a v-else class="navbar-item" :class="{ 'is-active': $route.name ==='login' }" href="/login">Log in</a>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
  import {
    mapState
  } from 'vuex'
  import Cookies from 'js-cookie'

  export default {
    name: 'AppNav',
    computed: mapState({
      email: state => state.auth.email
    }),
    methods: {
      logout: function () {
        Cookies.remove('auth')
        this.$store.commit('logout')
        this.$router.push('/login')
      }
    }
  }
</script>

<style scoped>
  .container > .navbar-brand {
    margin-left: -16px;
  }
  .container > .navbar-menu {
    margin-right: -16px;
  }
  .navbar-item.has-dropdown.is-right .navbar-dropdown {
      left: auto;
      right: 0;
  }
  .navbar-link.is-active, a.navbar-item.is-active {
    color: #00d1b2;
  }
</style>
