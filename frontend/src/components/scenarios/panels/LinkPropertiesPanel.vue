<template>
  <BasePanel @confirm="confirm" @cancel="$emit('cancel')">
    <span slot="title">Link Properties</span>
    <div slot="body">
      <div class="field">
        <label class="label">IP address</label>
        <div class="control">
          <input class="input" type="text" v-model="ip">
        </div>
        <p class="help is-danger" v-if="error.ip">{{ error.ip }}</p>
      </div>
      <div class="field">
        <label class="label">Allowed address pairs</label>
        <div class="field" v-for="(pair, i) in allowedAddressPairs" track-by="$index">
          <div class="field has-addons">
            <div class="control is-expanded">
              <input class="input" type="text" v-model="pair.value" placeholder="e.g.: 1b:10:84:ff:c9:39,10.0.2.0/16">
            </div>
            <div class="control">
              <button class="button is-danger" @click="deleteAllowedAddressPair(pair)">
                <span class="icon">
                  <i class="fa fa-trash-alt"></i>
                </span>
              </button>
            </div>
          </div>
          <p class="help is-danger" v-if="error.allowedAddressPairs.hasOwnProperty(i)">
            {{ error.allowedAddressPairs[i] }}
          </p>
        </div>
        <button class="button is-primary" @click="addAllowedAddressPair">Add address pair</button>
      </div>
    </div>
  </BasePanel>
</template>

<script>
  import { IP_PATTERN, MAC_PATTERN, CIDR_PATTERN } from '@/common/index'
  import BasePanel from '@/components/scenarios/panels/BasePanel.vue'

  export default {
    name: "LinkPropertiesPanel",
    props: ['link'],
    components: {
      BasePanel,
    },
    data() {
      return {
        ip: null,
        allowedAddressPairs: [],
        error: {
          ip: '',
          allowedAddressPairs: {}
        }
      }
    },
    created() {
      this.update();
    },
    watch: {
      link() {
        this.update();
      }
    },
    methods: {
      update() {
        this.ip = this.link.ip;
        this.allowedAddressPairs = Array.isArray(this.link.allowedAddressPairs) ?
          this.link.allowedAddressPairs.map(pair => ({ value: pair })) : [];
      },
      addAllowedAddressPair() {
        let length = this.allowedAddressPairs.length;
        if (length === 0 || this.allowedAddressPairs[length - 1].value.trim() !== '') {
          this.allowedAddressPairs.push({ value: '' });
        }
      },
      deleteAllowedAddressPair(pair) {
        let index = this.allowedAddressPairs.indexOf(pair);
        if (index > -1) {
          this.allowedAddressPairs.splice(index, 1);
        }
      },
      validate() {
        let passed = true;
        !IP_PATTERN.test(this.ip) ? (this.error.ip = 'IP address is invalid', passed = false) : this.error.ip = '';

        this.error.allowedAddressPairs = {};
        this.allowedAddressPairs.forEach((pair, i) => {
          const [ mac, ip ] = pair.value.trim().split(',');
          if (!MAC_PATTERN.test(mac.trim()) || !(IP_PATTERN.test(ip.trim()) || CIDR_PATTERN.test(ip.trim()))) {
            this.error.allowedAddressPairs[i] = 'Allowed address pair is invalid';
            passed = false;
          }
        });
        return passed;
      },
      confirm() {
        if (!this.validate()) {
          return;
        }
        this.$emit('confirm', {
          ip: this.ip,
          allowedAddressPairs: this.allowedAddressPairs.map(pair => pair.value).filter(pair => pair !== ''),
        });
      }
    }
  }
</script>
