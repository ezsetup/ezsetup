<template>
  <div class="center">
      <div class="field">
        <label for="inputEmail" class="label">Email</label>
        <p class="control">
          <input class="input" v-model="inputEmail" @keyup.enter="onLoginBtn"  id="inputEmail" name="inputEmail" placeholder="Enter email address">
        </p>
        <p v-if="error.emailErr" class="help is-danger">{{error.emailErr}}</p>
      </div>
      <div class="field">
        <label for="inputPassword" class="label">Password</label>
        <p class="control">
          <input type="password" v-model="inputPassword" @keyup.enter="onLoginBtn"  class="input" id="inputPassword" name="inputPassword" placeholder="Password">
        </p>
        <p v-if="error.passwordErr" class="help is-danger">{{error.passwordErr}}</p>
      </div>
      <button v-if="isLoading" type="submit" @click="onLoginBtn" class="button is-primary is-loading">SIGN IN</button>
      <button v-else type="submit" @click="onLoginBtn" class="button is-primary">SIGN IN</button>
      <p v-if="error.generalErr" class="help is-danger">{{error.generalErr}}</p>
  </div>
</template>

<script>
  import { login, GETUserSelf } from '@/api'

  export default {
    name: 'login',
    data: function () {
      return {
        inputEmail: '',
        inputPassword: '',
        error: {
          passwordErr: null,
          emailErr: null,
          generalErr: null
        },
        isLoading: false
      }
    },
    methods: {
      onLoginBtn: function () {
        this.isLoading = true
        this.error = {
          emailErr: null,
          passwordErr: null,
          generalErr: null
        }
        login(this.inputEmail, this.inputPassword)
          .then((response) => {
            this.isLoading = false
            if (response.ok) {
              response.json().then((json) => {
                this.$store.commit('setAuth', json)
                GETUserSelf(json => {
                  this.$store.commit('setUserInfo', json)
                  this.$router.push('/')
                })
              })
            } else {
              if (response.status === 401) {
                response.json().then(json => {
                  if (json.error === 'email address does not exist') {
                    this.error.emailErr = 'email address does not exist'
                  } else {
                    this.error.passwordErr = json.error
                  }
                })
              } else {
                response.json().then(json => {
                  this.error.generalErr = json.error
                })
              }
            }
          })
          .catch((error) => {
            this.isLoading = false
            this.error.generalErr = error.message
          })
      }
    }
  }
</script>

<style scoped>
  .center {
    width: 60%;
    margin: auto;
  }
</style>
