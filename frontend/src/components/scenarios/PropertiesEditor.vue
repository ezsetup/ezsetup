<template>
  <div>
    <h5 class="title is-5 has-text-centered">Properties</h5>
    <div v-if="el !== null">

      <div class="modal is-active" v-if="showFlavorModal">
        <div class="modal-background" @click="showFlavorModal=false"></div>
        <div class="modal-content">
          <div class="box">
            <h3 class="title is-3">List of flavors:</h3>
            <p v-for="flavor in flavors">{{flavor.name}}: {{flavor.ram}}MB RAM</p>
          </div>
        </div>
        <button class="modal-close is-large" aria-label="close" @click="showFlavorModal=false"></button>
      </div>

      <div v-if="isNetwork">
        <div class="field">
        <label>Name: </label>
        <input class="input" id="name" name="name" v-model="el.name">
        </div>
        <br>
        <div class="field">
        <label>CIDR: </label>
        <input class="input" id="cidr" name="cidr" v-model="el.cidr">
        </div>
      </div>

      <div v-else-if="isInstance">
        <div class="field">
          <label>Name: </label>
          <input class="input" id="name" name="name" v-model="el.name">
        </div>

        <div class="field">
          <label>Image: </label>
          <input class="input" id="image" name="image" v-model="el.image">
        </div>

        <div class="field">
          <label>Configurations: </label>
          <div v-for="conf in instanceConfigurations">
            <label class="checkbox">
              <input type="checkbox" :checked="checkConfig(el, conf)" @change="onConfigChecked($event, conf)"> {{conf}}
            </label>
          </div>
        </div>

        <div class="field">
          <label>Flavor: </label> <a @click="showFlavorModal=true">?</a> <br>
          <select v-model="el.flavor">
            <option v-for="flavor in flavors" :value="flavor">{{flavor.name}}</option>
          </select>
        </div>
      </div>

      <div v-else-if="isRouter">
        <div class="field">
          <label>Name: </label>
          <input class="input" id="name" name="name" v-model="el.name">
        </div>

        <div class="field">
          <label>Image: </label>
          <input class="input" id="image" name="image" v-model="el.image">
        </div>

        <div class="field">
          <label>Configurations: </label>
          <div v-for="conf in routerConfigurations">
          <label class="checkbox">
            <input type="checkbox" :checked="checkConfig(el, conf)" @change="onConfigChecked($event, conf)"> {{conf}}
          </label>
          </div>
        </div>

        <div class="field">
          <label>Flavor: </label> <a @click="showFlavorModal=true">?</a> <br>
          <select v-model="el.flavor">
            <option v-for="flavor in flavors" :value="flavor">{{flavor.name}}</option>
          </select>
        </div>
      </div>
      <div v-else-if="isLink">
        <label>IP address: </label>
        <input class="input" id="ip" name="ip" v-model="el.ip">
      </div>

      <button class="button is-danger deleteBtn" @click="onDeleteBtn(el.gid)">Delete</button>
    </div>
  </div>
</template>

<script>
export default {
  data: function () {
    return {
      showFlavorModal: false
    }
  },
  props: ['el', 'instanceConfigurations', 'routerConfigurations', 'flavors'],
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
    onDeleteBtn: function (elementId) {
      this.$emit('delete', elementId)
    },
    onConfigChecked: function (event, name) {
      let checked = event.target.checked
      if (checked) {
        this.el.configurations.push(name)
      } else {
        this.el.configurations = this.el.configurations.filter(e => e !== name)
      }
    },
    checkConfig: function (el, conf) {
      return el.configurations.includes(conf)
    }
  }
}
</script>

<style scoped>
.deleteBtn {
  margin-top: 10px;
}
</style>
