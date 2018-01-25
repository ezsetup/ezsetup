<template>
  <div class="main">
    <div class="center">
      <h2 class="title is-2">Lab: {{name}}</h2>
      <div class="columns">
        <div class="column" v-for="sl in slices" v-bind:key="sl.id">
          <router-link class="box" :to="{name: 'Slice', params:{sliceId: sl.id}}">
            <p>{{sl.name}}</p>
            <p>{{sl.status}}</p>
            <button v-if="sl.status ==='deploying'" class="button is-loading"></button>
          </router-link>
        </div>
      </div>
      <div class="field">
        <button v-if="status==='deploying'" type="submit" class="button is-primary is-loading"></button>
        <button v-else-if="status==='destroying'" type="submit" class="button is-danger is-loading"></button>
        <button v-else-if="status==='active'" type="submit" v-on:click="onDestroyBtn" class="button is-primary is-danger">DESTROY</button>
        <p v-if="error" class="is-danger">{{error}}</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
  .main {
    margin-top: 20px;
  }

  .property {
    background-color: #f6f6f6;
    margin-left: 5px;
    margin-bottom: 5px;
  }

  .workspace {
    background-color: #f6f6f6;
    margin-bottom: 5px;
    width: 800px;
  }

  .center {
    text-align: center;
  }

</style>

<script>
  import {DESTROYlab} from '@/api'
  export default {
    name: 'LabViewer',
    props: ['name', 'slices', 'status'],
    data: function () {
      return {
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
