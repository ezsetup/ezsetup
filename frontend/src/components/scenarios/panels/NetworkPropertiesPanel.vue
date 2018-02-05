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
        const CIDR_PATTERN = /^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))\/[0-9]{1,2}$/;
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
