<template>
  <div>
    <h5 class="title is-5 has-text-centered">Properties</h5>
    <div v-if="el !== null">

      <div v-if="isInstance">
        <div class="columns">
          <label class="column is-4">Name: </label>
          <p id="name" name="name" class="value column">{{el.name}}</p>
        </div>
        <div class="columns">
          <label class="column is-4">Public IP:</label>
          <p class="value column" id="public-ip" name="public-ip">{{el.public_ip}}</p>
        </div>
        <div v-if="el.configurations.map(el => el.name).includes('noVNC')" class="columns">
          <label class="column is-4">VNC:</label>
          <a class="value column" target="_blank" id="console-url" name="console-url" :href="'http://'+ el.public_ip + ':6080/vnc.html'">
            Open
          </a>
        </div>

        <div v-if="el.password" class="columns">
          <label class="column is-4">Password</label>
          <div v-if="showPassword" class="column">
            <label>{{el.password}}</label>
            <button class="button is-small" @click="toggleShowPassword">Hide</button>
          </div>
          <div v-else class="column">
            <button class="button is-small" @click="toggleShowPassword">Show</button>
          </div>
        </div>

        <div class="columns">
          <label class="column is-4">Status:</label>
          <p class="value column" id="instance-status" name="instance-status">{{el.status}}</p>
        </div>
      </div>

      <div v-if="isRouter">
        <div class="columns">
          <label class="column is-4">Name: </label>
          <p id="name" name="name" class="value column">{{el.name}}</p>
        </div>

        <div class="columns">
          <label class="column is-4">Public IP:</label>
          <p class="value column" id="public-ip" name="public-ip">{{el.public_ip}}</p>
        </div>

        <div class="columns">
          <label class="column is-4">VNC:</label>
          <a class="value column" target="_blank" id="console-url" name="console-url" :href="'http://'+ el.public_ip + ':6080/vnc.html'">
            Open
          </a>
        </div>

        <div v-if="el.password" class="columns">
          <label class="column is-4">Password</label>
          <div v-if="showPassword" class="column">
            <label>{{el.password}}</label>
            <button class="button is-small" @click="toggleShowPassword">Hide</button>
          </div>
          <div v-else class="column">
            <button class="button is-small" @click="toggleShowPassword">Show</button>
          </div>
        </div>

        <div class="columns">
          <label class="column is-4">Status:</label>
          <p class="value column" id="instance-status" name="instance-status">{{el.status}}</p>
        </div>
      </div>

      <div v-if="isNetwork">
        <div class="columns">
          <label class="column is-4">Name: </label>
          <p id="name" name="name" class="value column">{{el.name}}</p>
        </div>
        <div class="columns">
          <label class="column is-4">CIDR: </label>
          <p class="value column" id="cidr" name="cidr">{{el.cidr}}</p>
        </div>
      </div>

      <div v-if="isLink">
        <div class="columns">
          <label class="column is-4">IP address: </label>
          <p class="value column" id ="ip" name="ip">{{el.ip}}</p>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
  .deleteBtn {
    margin-top: 10px;
  }
  .value {
    font-style: italic
  }
</style>

<script>
  export default {
    name: 'propertiesviewer',
    data: function () {
      return {
        showPassword: false
      }
    },
    props: ['el'],
    computed: {
      isNetwork: function () {
        return this.el.type === 'NetworkNode'
      },
      isInstance: function () {
        return this.el.type === 'Instance'
      },
			isRouter: function () {
				return this.el.type === 'Router'
			},
      isLink: function () {
        return this.el.type === 'NetworkLink'
      }
    },
    methods: {
      toggleShowPassword: function () {
        this.showPassword = !this.showPassword
      }
    }
  }
</script>
