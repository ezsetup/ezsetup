<template>
  <BasePanel @confirm="confirm" @cancel="$emit('cancel')">
    <span slot="title">Network Properties</span>
    <div slot="body">
      <div class="field">
        <label class="label">Name</label>
        <div class="control">
          <input class="input" type="text" v-model="name">
        </div>
        <p class="help is-danger" v-if="error.name">{{ error.name }}</p>
      </div>
      <div class="field">
        <label class="label">CIDR</label>
        <div class="control">
          <input class="input" type="text" v-model="cidr">
        </div>
        <p class="help is-danger" v-if="error.cidr">{{ error.cidr }}</p>
      </div>
    </div>
  </BasePanel>
</template>

<script>
  import { CIDR_PATTERN } from '@/common/index'
  import BasePanel from '@/components/scenarios/panels/BasePanel.vue'

  export default {
    name: "NetworkPropertiesPanel",
    props: ['network'],
    components: {
      BasePanel,
    },
    data() {
      return {
        name: null,
        cidr: null,
        error: {
          name: '',
          cidr: ''
        }
      }
    },
    created() {
      this.update();
    },
    watch: {
      network() {
        this.update();
      }
    },
    methods: {
      update() {
        this.name = this.network.name;
        this.cidr = this.network.cidr;
      },
      validate() {
        let passed = true;
        !CIDR_PATTERN.test(this.cidr) ? (this.error.cidr = 'CIDR is invalid', passed = false) : this.error.cidr = '';
        this.name.trim() === '' ? (this.error.name = 'Network name cannot be empty', passed = false) : this.error.name = '';
        return passed;
      },
      confirm() {
        if (!this.validate()) {
          return;
        }
        this.$emit('confirm', {
          name: this.name,
          cidr: this.cidr
        });
      }
    }
  }
</script>
