<template>
  <div v-if="this.$store.state.userConsent" class="my-main">
    <div v-if="permissionGroups" class="tabs">
      <ul>
        <li v-if="permissionGroups.includes('labs')" :class="{'is-active': this.$route.path.includes('/labs')}">
          <router-link to="/labs">Labs</router-link>
        </li>
        <li v-if="permissionGroups.includes('scenarios')" :class="{'is-active': this.$route.path.includes('/scenarios')}">
          <router-link to="/scenarios">Scenarios</router-link>
        </li>
        <li v-if="permissionGroups.includes('users')" :class="{'is-active': this.$route.path.includes('/users')}">
          <router-link to="/users">Users</router-link>
        </li>
        <li v-if="!this.$store.state.auth.is_root" :class="{'is-active': this.$route.path.includes('/workspace')}">
          <router-link to="/workspace">Workspace</router-link>
        </li>
      </ul>
    </div>
    <router-view></router-view>
  </div>
  <div v-else class="modal is-active"> 
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
  mapState
} from 'vuex'
import {
  GETUserSelf
} from '@/api'
import Cookies from 'js-cookie'

export default {
  name: 'index',
  components: {},
  data: function () {
    return {
      permissionGroups: null,
      consentUserName: null,
    }
  },
  beforeRouteEnter: (to, from, next) => {
    GETUserSelf(json => {
      next(vm => {
        vm.setUserInfo(json)
      })
    })
  },
  methods: {
    setUserInfo(json){
      this.permissionGroups = json.permissionGroups
      this.$store.commit('setUserInfo', json)
    }
  }
}
</script>

<style scoped>
.my-main {
  margin-top: 20px;
}
</style>
