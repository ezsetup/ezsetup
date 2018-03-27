<template>
  <div class="columns">
    <div class="column is-8 is-offset-2">
      <h1 class="title">Edit User {{fullname}}</h1>
      <div class="field">
        <label class="label" for="inputFullname">Full name</label>
        <p class="control">
          <input class="input" v-model="inputFullname" type="text" id="inputFullname" name="inputFullname" placeholder="Full Name">
        </p>
      </div>
      <div class="field">
        <label class="label" for="inputEmail">Email address</label>
        <p class="control">
          <input type="email" v-model="inputEmail" class="input" id="inputEmail" aria-describedby="emailHelp" placeholder="Enter email">
        </p>
      </div>
      <div class="field">
        <label class="label" for="inputPassword">Password</label>
        <p class="control">
          <input class="input" v-model="inputPassword" id="inputPassword" placeholder="Keep this field empty if you don't want to change the password" type="password">
        </p>
      </div>
      <div v-if="permissionGroups && permissionGroups.includes('permissions')" class="field">
        <label class="label">Permissions</label>
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
      <div class="field">
        <p class="control">
          <button v-if="isLoading" type="submit" class="button is-primary is-loading" @click="onSubmitBtn">UPDATE</button>
          <button v-else type="submit" class="button is-primary" @click="onSubmitBtn">UPDATE</button>
          <button class="button is-primary is-danger" @click="onDeleteBtn">DELETE</button>
        </p>
        <p v-if="errors" class="is-danger">{{errors}}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>

<script>
  import {mapState} from 'vuex'
  import {PATCHUser, GETUser, DELETEUser} from '@/api'
  export default {
    name: 'User',
    components: {
    },
    data: function () {
      return {
        inputFullname: null,
        inputEmail: null,
        inputPassword: null,
        errors: null,
        allowLabsManagement: false,
        allowScenariosManagement: false,
        allowUsersManagement: false,
        isLoading: false,
        fullname: null
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
        PATCHUser(this.$route.params.id, this.inputFullname, this.inputEmail, this.inputPassword, this.inputPermissionGroups,
          json => {
            this.$router.push('/users')
            this.isLoading = false
          },
          json => {
            this.errors = json.errors
          }
        )
      },
      onDeleteBtn: function() {
        DELETEUser(this.$route.params.id, json => {
          this.$router.push('/users')
        })
      }
    },
    created: function () {
      GETUser(this.$route.params.id, json => {
        this.fullname = json['fullname']
        this.inputFullname = json['fullname']
        this.inputEmail = json['email']
        this.allowUsersManagement = json['permission_groups'].includes('users')
        this.allowScenariosManagement = json['permission_groups'].includes('scenarios')
        this.allowLabsManagement = json['permission_groups'].includes('labs')
      })
    },
  }
</script>
