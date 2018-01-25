<template>
  <div class="main">
    <div class="center">
      <div class="field">
        <label for="inputFullname">Full name</label>
        <p class="control">
          <input class="input" v-model="inputFullname" type="text" id="inputFullname" name="inputFullname" placeholder="Full Name">
        </p>
      </div>
      <div class="field">
        <label for="inputEmail">Email address</label>
        <p class="control">
          <input type="email" v-model="inputEmail" class="input" id="inputEmail" aria-describedby="emailHelp" placeholder="Enter email">
        </p>
      </div>
      <div class="field">
        <label for="inputPassword">Password</label>
        <p class="control">
          <input type="inputPassword" class="input" v-model="inputPassword" id="inputPassword" placeholder="Password">
        </p>
      </div>
      <div v-if="permissionGroups && permissionGroups.includes('permissions')" class="field">
        <label>Permissions</label>
        <p class="control">
          <label class="checkbox">
          <input type="checkbox" v-model="allowLabsManagement"> Labs management
          </label>
        </p>
        <p class="control">
          <label class="checkbox">
          <input type="checkbox" v-model="allowScenariosManagement"> Scenarios management
          </label>
        </p>
        <p class="control">
          <label class="checkbox">
          <input type="checkbox" v-model="allowUsersManagement"> Users management
          </label>
        </p>
      </div>
      <button v-if="isLoading" type="submit" class="button is-primary is-loading" @click="onSubmitBtn">SUBMIT</button>
      <button v-else type="submit" class="button is-primary" @click="onSubmitBtn">SUBMIT</button>
      <p v-if="error" class="is-danger">{{error}}</p>
    </div>
  </div>
</template>

<style scoped>
.main {
  margin-top: 20px;
}

.center {
  width: 60%;
  margin: auto;
}
</style>

<script>
import {mapState} from 'vuex'
import {POSTUser} from '@/api'
export default {
  name: 'UserCreation',
  data: function () {
    return {
      inputFullname: null,
      inputEmail: null,
      inputPassword: null,
      error: null,
      allowLabsManagement: false, 
      allowScenariosManagement: false, 
      allowUsersManagement: false,
      isLoading: false
    }
  },
  computed: {
    inputPermissionGroups: function() {
      let ret = []
      if (this.allowLabsManagement) {
        ret.push("labs")
      }
      if (this.allowScenariosManagement) {
        ret.push("scenarios")
      }
      if (this.allowUsersManagement) {
        ret.push("users")
      }
      return ret
    },
    ...mapState({
      permissionGroups: state => state.userInfo.permissionGroups
    }),
  },
  methods: {
    onSubmitBtn: function() {
      this.isLoading = true
      POSTUser(this.inputEmail, this.inputPassword, this.inputFullname, this.inputPermissionGroups, json => {
        this.$router.push('/users')
        this.isLoading = false
      })
    }
  }
}
</script>
