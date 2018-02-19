<template>
  <BasePanel>
    <span slot="title">Network Properties</span>
    <div slot="body">
      <div class="field">
        <label class="label">Name</label>
        <div class="control">
          <p>{{ network.name }}</p>
        </div>
      </div>
      <div class="field">
        <label class="label">CIDR</label>
        <div class="control">
          <p>{{ network.cidr && network.cidr.trim() ? network.cidr : '(Unknown)' }}</p>
        </div>
      </div>
    </div>
  </BasePanel>
</template>

<script>
  import BasePanel from '@/components/slices/panels/BasePanel.vue'

  export default {
    name: "NetworkPropertiesPanel",
    props: ['network'],
    components: {
      BasePanel
    },
    data() {
      return {
      }
    }
  }
</script>
