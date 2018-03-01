<template>
  <div class="my-main">
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
        <li v-if="permissionGroups.includes('labs')" :class="{'is-active': this.$route.path.includes('/assessment')}">
          <router-link to="/assessment">Assessment</router-link>
        </li>
      </ul>
    </div>
    <router-view></router-view>
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
      permissionGroups: null
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
