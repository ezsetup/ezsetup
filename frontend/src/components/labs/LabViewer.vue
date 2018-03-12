<template>
  <div>
    <div class="columns">
      <div class="column">
        <h1 class="title">{{name}}</h1>
      </div>
      <div class="column is-narrow">
        <button v-if="status==='deploying'" class="button is-primary is-loading">Deploying</button>
        <button v-else-if="status==='destroying'" class="button is-danger is-loading">Destroying</button>
        <button v-if="status!=='destroying'" v-on:click="onDestroyBtn" class="button is-primary is-danger">DESTROY</button>
        <p v-if="error" class="is-danger">{{error}}</p>
      </div>
    </div>
    <div class="columns">
      <div class="column is-3" v-for="sl in slices" v-bind:key="sl.id">
        <router-link class="box" :to="{name: 'Slice', params:{sliceId: sl.id}}">
          <p>{{ sl.name }}</p>
          <p>{{ sl.username }}</p>
          <status-indicator :status="sl.status" class="is-small"></status-indicator>
        </router-link>
      </div>
    </div>
    <div>
      <p v-for="err in errors">{{err}}</p>
    </div>
  </div>
</template>
<style scoped>
  .box {
    color: inherit;
  }
  .is-small {
    font-size: 0.8rem;
  }
</style>
<script>
  import { DESTROYlab, LISTusers } from '@/api'
  import StatusIndicator from '@/components/common/StatusIndicator'

  export default {
    name: 'LabViewer',
    props: ['name', 'slices', 'status', 'errors'],
    components: { StatusIndicator },
    data: function () {
      return {
        users: {},
        error: null
      }
    },
    methods: {
      onDestroyBtn: function () {
        this.$emit('destroying')
        DESTROYlab(this.$route.params.id, json => {})
      }
    }
  }
</script>
