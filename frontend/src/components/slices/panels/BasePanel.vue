<template>
  <div class="card">
    <header class="card-header">
      <p class="card-header-title">
        <slot name="title">Panel Title</slot>
      </p>
    </header>
    <div class="card-content">
      <div class="content">
        <slot name="body">Panel Content</slot>
      </div>
    </div>
  </div>
</template>

<script>
    export default {
        name: "BasePanel"
    }
</script>

<style scoped>
  .card {
    position: absolute;
    top: 30px;
    right: 30px;
    min-width: 340px;
  }

  .card-header {
    background: #f7f7f7;
  }

  .card-content {
    max-height: 570px;
    overflow-y: auto;
  }
</style>
