<template>
  <div class="center">
    <div class="field">
      <label for="fullname">Full name</label>
      <p class="control">
        <input class="input" v-model="fullname" type="text" id="fullname" name="fullname" placeholder="Full Name">
      </p>
    </div>
    <div class="field">
      <label for="email">Email address</label>
      <p class="control">
        <input type="email" v-model="email" class="input" id="email" aria-describedby="emailHelp" placeholder="Enter email">
      </p>
      <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>
    </div>
    <div class="field">
      <label for="password1">Password</label>
      <p class="control">
        <input type="password" class="input" v-model="password1" id="password1" placeholder="Password">
      </p>
    </div>
    <div class="field">
      <label for="password2">Retype Password</label>
      <p class="control">
        <input type="password" v-model="password2" id="password2" class="input" placeholder="Retype Password">
      </p>
    </div>
    <div class="field">
      <label for="role">Role</label>
      <p class="control">
        <span class="select">
        <select id="role" v-model="role">
          <option value="lab manager">Lab manager</option>
          <option value="user">User</option>
        </select>
        </span>
      </p>
    </div>
    <button v-if="password1 !== null && password1 === password2" v-on:click="onSignupBtn" type="submit" class="button is-primary">SIGN UP</button>
    <button v-else disabled type="submit" class="button is-primary">SIGN UP</button>
    <p v-if="error" class="is-danger">{{error}}</p>
  </div>
</template>

<script>
  import {API_SERVER} from '@/api'
  import Cookies from 'js-cookie'
  export default {
    name: 'signup',
    data: function () {
      return {
        fullname: null,
        email: null,
        password1: null,
        password2: null,
        role: 'user',
        error: null
      }
    },
    methods: {
      onSignupBtn: function () {
        this.error = null
        let options = {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({
            'fullname': this.fullname,
            'email': this.email,
            'password': this.password1,
            'role': this.role
          })
        }

        fetch(API_SERVER + '/auth/users/', options)
          .then(response => {
            if (response.ok) {
              response.json().then(json => {
                this.$store.commit('login', {
                  email: this.email,
                  role: this.role,
                  token: json.token
                })
                Cookies.set('auth', {
                  email: this.email,
                  role: this.role,
                  token: json.token
                }, {
                  expires: 1
                })
                this.$router.push({
                  path: '/'
                })
              })
            } else {
              response.json().then(json => {
                this.error = json.error
              })
            }
          })
          .catch((error) => {
            this.error = error.message
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
