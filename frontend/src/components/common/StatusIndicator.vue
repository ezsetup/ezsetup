<template>
  <span>
    <span v-if="status === 'inactive'"><i class="fas fa-question-circle"></i> Not deployed</span>
    <span v-if="status === 'deploying'"><i class="fas fa-spinner fa-pulse"></i> Deploying</span>
    <span v-if="status === 'deployfailed'"><i class="fas fa-times-circle has-text-danger"></i> Deploy failed</span>
    <span v-if="status === 'active'"><i class="fas fa-check-circle has-text-success"></i> Active</span>
    <span v-if="status === 'destroying'"><i class="fas fa-spinner fa-pulse"></i> Destroying</span>
    <span v-if="status === 'destroyfailed'"><i class="fas fa-times-circle has-text-danger"></i> Destroy failed</span>
  </span>
</template>

<script>
    export default {
      name: "StatusIndicator",
      props: [ 'status' ]
    }
</script>
