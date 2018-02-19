<template>
  <BasePanel>
    <span slot="title">Link Properties</span>
    <div slot="body">
      <div class="field">
        <label class="label">IP address</label>
        <div class="control">
          <p>{{ link.ip && link.ip.trim() ? link.ip : '(Unknown)' }}</p>
        </div>
      </div>
    </div>
  </BasePanel>
</template>

<script>
  import BasePanel from '@/components/slices/panels/BasePanel.vue'

  export default {
    name: "LinkPropertiesPanel",
    props: ['link'],
    components: {
      BasePanel
    },
    data() {
      return {
      }
    }
  }
</script>
