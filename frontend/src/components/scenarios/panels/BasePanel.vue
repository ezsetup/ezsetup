<template>
  <div class="card">
    <header class="card-header">
      <p class="card-header-title">
        <slot name="title">Dialog Title</slot>
      </p>
    </header>
    <div class="card-content">
      <div class="content">
        <slot name="body">Dialog Content</slot>
      </div>
    </div>
    <footer class="card-footer">
      <a class="card-footer-item" @click="confirm">Save</a>
      <a class="card-footer-item cancel" @click="cancel">Cancel</a>
    </footer>
  </div>
</template>

<script>
  export default {
    name: "BasePanel",
    methods: {
      confirm() {
        this.$emit('confirm');
      },
      cancel() {
        this.$emit('cancel');
      }
    }
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
  .cancel {
    color: #363636;
  }
</style>
