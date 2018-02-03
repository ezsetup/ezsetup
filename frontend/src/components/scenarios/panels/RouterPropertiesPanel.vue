<template>
  <BasePanel @confirm="confirm" @cancel="$emit('cancel')">
    <span slot="title">Router Properties</span>
    <div slot="body">
      <div class="field">
        <label class="label">Name</label>
        <div class="control">
          <input class="input" type="text" v-model="name">
        </div>
        <p class="help is-danger" v-if="error.name">{{ error.name }}</p>
      </div>
      <div class="field">
        <label class="label">Image name</label>
        <div class="control">
          <input class="input" type="text" v-model="image">
        </div>
        <p class="help is-danger" v-if="error.image">{{ error.image }}</p>
      </div>
      <div class="field">
        <label class="label">Flavor
          <span @click="flavorTip = true">
            <i class="far fa-question-circle"></i>
          </span>
        </label>
        <div class="control">
          <div class="select">
            <select v-model="flavor">
              <option v-for="f in flavors" :value="f" :selected="f.name === flavor.name">{{ f.name }}</option>
            </select>
          </div>
        </div>
        <p class="help is-danger" v-if="error.flavor">{{ error.flavor }}</p>
      </div>
      <div class="field">
        <label class="label">Additional configurations</label>
        <div class="control" v-for="c in routerConfigurations">
          <label class="checkbox">
            <input type="checkbox" :checked="hasConfig(c)" @change="onConfigChanged($event, c)"> {{ c }}
          </label>
        </div>
      </div>
    </div>
    <div v-if="flavorTip" class="modal" slot="body">
      <div class="modal-background" @click="flavorTip = false"></div>
      <div class="modal-content">
        <div class="box">
          <h4 class="title is-4">Available flavors</h4>
          <ol>
            <li>Small: 1024MB RAM</li>
            <li>Medium: 2048MB RAM</li>
            <li>Large: 4096MB RAM</li>
            <li>XLarge: 8192MB RAM</li>
          </ol>
        </div>
      </div>
      <button class="modal-close is-large" @click="flavorTip = false"></button>
    </div>
  </BasePanel>
</template>

<script>
  import BasePanel from '@/components/scenarios/panels/BasePanel.vue'

  export default {
    name: "RouterPropertiesPanel",
    props: ['router', 'flavors', 'routerConfigurations'],
    components: {
      BasePanel,
    },
    data() {
      return {
        name: null,
        image: null,
        flavor: null,
        configurations: null,

        flavorTip: false,

        error: {
          name: '',
          image: '',
          flavor: ''
        }
      }
    },
    created() {
      this.update();
    },
    watch: {
      router() {
        this.update();
      }
    },
    methods: {
      update() {
        this.name = this.router.name ? this.router.name : '';
        this.image = this.router.image ? this.router.image : '';
        this.flavor = this.router.flavor ? this.router.flavor : { name: '' };
        this.configurations = Array.isArray(this.router.configurations) ? [...this.router.configurations] : [];
      },
      hasConfig(conf) {
        return this.configurations.includes(conf);
      },
      onConfigChanged(event, conf) {
        const checked = event.target.checked;
        const index = this.configurations.indexOf(conf);
        if (!checked && index > -1) {
          this.configurations.splice(index, 1);
        } else if (checked && index === -1) {
          this.configurations.push(conf);
        }
      },
      validate() {
        let passed = true;
        this.name.trim() === '' ? (this.error.name = 'Router name cannot be empty', passed = false) : this.error.name = '';
        this.image.trim() === '' ? (this.error.image = 'Image name cannot be empty', passed = false) : this.error.image = '';
        this.flavor.name.trim() === '' ? (this.error.flavor = 'Must choose a flavor for the router', passed = false) :
          this.error.flavor = '';
        return passed;
      },
      confirm() {
        if (!this.validate()) {
          return;
        }
        this.$emit('confirm', {
          name: this.name,
          image: this.image,
          flavor: this.flavor,
          configurations: [...this.configurations]
        });
      }
    }
  }
</script>

<style scoped>
  select, .select {
    width: 100%;
  }

  .modal {
    display: flex;
  }
</style>
