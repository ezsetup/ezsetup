<template>
  <div>
    <AppNav/>
    <section class="section">
      <div class="container">
        <router-view></router-view>
      </div>
    </section>
    <div v-if="this.$store.getters.authenticated && !this.$store.state.userConsent" class="modal is-active">
      <div class="modal-background"></div>
      <div class="modal-content">
        <div class="box">
          <h3 class="title is-3">User Agreement</h3>
          <p>TODO: add text here</p>
          <div class="field">
            <label class="label">Your name:</label>
            <div class="control">
              <input class="input" type="text" placeholder="Enter your name here to accept these terms above" v-model="consentUserName">
            </div>
          </div>
          <button v-if="consentUserName" class="button" @click="()=>this.$store.commit('setUserConsent', true)">Accept</button>
          <button v-else disabled class="button">Accept</button>
          <button class="button" @click="()=>{this.$store.commit('logout'); this.$router.push('/login');}">Decline</button>
        </div>
      </div>
    </div>
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
    data() {
      return {
        consentUserName: null
      }
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
