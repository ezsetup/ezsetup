<template>
  <BasePanel>
    <span slot="title">Instance Properties</span>
    <div slot="body">
      <div class="field">
        <label class="label">Name</label>
        <div class="control">
          <p>{{ instance.name }}</p>
        </div>
      </div>
      <div class="field">
        <label class="label">Public IP address</label>
        <div class="control">
          <p>{{ instance.public_ip && instance.public_ip.trim() ? instance.public_ip : '(Unknown)' }}</p>
        </div>
      </div>
      <div class="field" v-if="instance.configurations && instance.configurations.map(el => el.name).includes('Enable password authentication')">
        <label class="label">Username</label>
        <div class="control">
          <p>{{ instance.password && instance.password.trim() ? 'Ubuntu' : '(Unknown)' }}</p>
        </div>
      </div>
      <div class="field" v-if="instance.configurations && instance.configurations.map(el => el.name).includes('Enable password authentication')">
        <label class="label">Password</label>
        <div class="control">
          <p>{{ instance.password && instance.password.trim() ? (showPassword ? instance.password : '********') : '(Unknown)' }}
            <button class="button is-small" title="Show" v-if="!showPassword" @click="showPassword = true" :key="1"><i class="fas fa-eye"></i></button>
            <button class="button is-small" title="Hide" v-if="showPassword" @click="showPassword = false" :key="2"><i class="fas fa-eye-slash"></i></button>
            <button class="button is-small" title="Copy to clipboard" @click="copy"><i class="fas fa-copy"></i></button>
          </p>
          <input name="password_copy" id="password_copy" type="hidden" :value="instance.password.trim()">
        </div>
      </div>
      <div class="field" v-if="instance.configurations && instance.configurations.map(el => el.name).includes('noVNC')">
        <label class="label">VNC connection</label>
        <div class="control">
          <p><a target="_blank" :href="'http://'+ instance.public_ip + ':6080/vnc.html'">Open</a></p>
        </div>
      </div>
      <div class="field">
        <label class="label">Status</label>
        <div class="control">
          <p><status-indicator :status="instance.status" class="is-small"></status-indicator></p>
        </div>
      </div>
    </div>
  </BasePanel>
</template>

<style scoped>
  .control .button {
    height: auto;
  }
</style>

<script>
  import BasePanel from '@/components/slices/panels/BasePanel.vue'
  import StatusIndicator from '@/components/common/StatusIndicator'

  export default {
    name: "InstancePropertiesPanel",
    props: ['instance'],
    components: {
      BasePanel,
      StatusIndicator
    },
    data() {
      return {
        showPassword: false
      }
    },
    mounted: function() {
      this.showPassword = false;
    },
    methods: {
      copy() {
        let passwordInput = document.querySelector('#password_copy');
        if (!passwordInput) {
          return;
        }
        passwordInput.setAttribute('type', 'text');
        passwordInput.focus();
        passwordInput.select();
        try {
          document.execCommand('copy');
        } catch (err) {
          // TODO: tell user to copy it himself if failed
        } finally {
          passwordInput.setAttribute('type', 'hidden');
        }
      }
    }
  }
</script>
