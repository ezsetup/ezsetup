<template>
  <BasePanel @confirm="confirm" @cancel="$emit('cancel')">
    <span slot="title">Scenario Properties</span>
    <div slot="body">
      <div class="field">
        <label class="label">Name</label>
        <p class="control">
          <input class="input" type="text" v-model="name">
        </p>
        <p class="help is-danger" v-if="error.name">{{ error.name }}</p>
      </div>
      <div class="field">
        <label class="label">Description</label>
        <p class="control is-expanded">
          <textarea class="textarea" v-model="description"></textarea>
        </p>
      </div>
      <div class="field">
        <label class="label">
          Security Group Rules
          <span @click="securityGroupTip = true">
            <i class="far fa-question-circle"></i>
          </span>
        </label>
        <div class="field" v-for="(rule, i) in securityGroupRules" track-by="$index">
          <div class="field has-addons">
            <div class="control is-expanded">
              <input class="input" type="text" v-model="rule.value" placeholder="e.g.: ingress ipv4 tcp 8080 0.0.0.0/0">
            </div>
            <div class="control">
              <button class="button is-danger" @click="deleteSecurityGroupRule(rule)">
                <span class="icon">
                  <i class="fa fa-trash-alt"></i>
                </span>
              </button>
            </div>
          </div>
          <p class="help is-danger" v-if="error.securityGroupRules.hasOwnProperty(i)">
            {{ error.securityGroupRules[i] }}
          </p>
        </div>
        <button class="button is-primary" @click="addSecurityGroupRule">Add Rule</button>
      </div>
      <div class="field">
        <label class="label">Publicly available</label>
        <p class="control">
          <label class="radio">
            <input type="radio" value=true v-model="isPublic"> Yes
          </label>
          <label class="radio">
            <input type="radio" value=false v-model="isPublic"> No
          </label>
        </p>
      </div>
    </div>
    <div v-if="securityGroupTip" class="modal" slot="body">
      <div class="modal-background" @click="securityGroupTip = false"></div>
      <div class="modal-content">
        <div class="box">
          <h4 class="title is-4">Available security group rule format</h4>
          <ol>
            <li>ingress/egress ipv4/ipv6 protocol port number/range(e.g. 8000-9000) IP/CIDR</li>
            <li>ingress/egress ipv4/ipv6 protocol port number/range(e.g. 8000-9000)</li>
            <li>ingress/egress ipv4/ipv6 protocol IP/CIDR</li>
            <li>ingress/egress ipv4/ipv6 protocol</li>
          </ol>
        </div>
      </div>
      <button class="modal-close is-large" @click="securityGroupTip = false"></button>
    </div>
  </BasePanel>
</template>

<script>
  import BasePanel from '@/components/scenarios/panels/BasePanel.vue'

  export default {
    name: "ScenarioMetaPanel",
    props: ['scenario'],
    components: {
      BasePanel,
    },
    data() {
      return {
        name: null,
        description: null,
        securityGroupRules: null,
        isPublic: null,

        securityGroupTip: false,

        error: {
          name: '',
          securityGroupRules: {}
        }
      }
    },
    created() {
      this.update();
    },
    watch: {
      scenario() {
        this.update();
      }
    },
    methods: {
      update() {
        this.name = this.scenario.name ? this.scenario.name : '';
        this.description = this.scenario.description ? this.scenario.description : '';
        this.securityGroupRules = Array.isArray(this.scenario.securityGroupRules) ?
          this.scenario.securityGroupRules.map(rule => ({ value: rule })) : [];
        this.isPublic = !!this.scenario.isPublic;
      },
      addSecurityGroupRule() {
        let length = this.securityGroupRules.length;
        if (length === 0 || this.securityGroupRules[length - 1].value.trim() !== '') {
          this.securityGroupRules.push({ value: '' });
        }
      },
      deleteSecurityGroupRule(rule) {
        let index = this.securityGroupRules.indexOf(rule);
        if (index > -1) {
          this.securityGroupRules.splice(index, 1);
        }
      },
      validate() {
        let passed = true;
        this.name.trim() === '' ? (this.error.name = 'Scenario name cannot be empty', passed = false) : this.error.name = '';

        this.error.securityGroupRules = {};
        this.securityGroupRules.forEach((rule, i) => {
          const SG_RULE_PATTERN = /(ingress|egress)\s+(ipv4|ipv6)\s+([a-z]+)\s*(?:(\d+(?:-\d+)?)?(?:\s|$)+)?(?:((?:(?:(?:[0-9A-Fa-f]{1,4}:){7}(?:[0-9A-Fa-f]{1,4}|:))|(?:(?:[0-9A-Fa-f]{1,4}:){6}(?::[0-9A-Fa-f]{1,4}|(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(?:(?:[0-9A-Fa-f]{1,4}:){5}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,2})|:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(?:(?:[0-9A-Fa-f]{1,4}:){4}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,3})|(?:(?::[0-9A-Fa-f]{1,4})?:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?:(?:[0-9A-Fa-f]{1,4}:){3}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,4})|(?:(?::[0-9A-Fa-f]{1,4}){0,2}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?:(?:[0-9A-Fa-f]{1,4}:){2}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,5})|(?:(?::[0-9A-Fa-f]{1,4}){0,3}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?:(?:[0-9A-Fa-f]{1,4}:){1}(?:(?:(?::[0-9A-Fa-f]{1,4}){1,6})|(?:(?::[0-9A-Fa-f]{1,4}){0,4}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?::(?:(?:(?::[0-9A-Fa-f]{1,4}){1,7})|(?:(?::[0-9A-Fa-f]{1,4}){0,5}:(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?:\/[0-9]{1,2})?(\s|$)))*/;
          !SG_RULE_PATTERN.test(rule.value.trim()) ? (this.error.securityGroupRules[i] = 'Security group rule format error', passed = false) : null;
        });
        return passed;
      },
      confirm() {
        if (!this.validate()) {
          return;
        }
        this.$emit('confirm', {
          name: this.name,
          description: this.description,
          securityGroupRules: [...this.securityGroupRules],
          isPublic: this.isPublic,
        });
      }
    }
  }
</script>

<style scoped>
  .modal {
    display: flex;
  }
</style>
