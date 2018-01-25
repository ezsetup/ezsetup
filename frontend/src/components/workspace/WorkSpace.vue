<template>
  <div>
    <div v-for="slice in slices" :key="slice.id" class="columns">
      <div class="column is-2">
        <p>{{slice.labName}}</p>
      </div>
      <router-link class="button is-info" :to="{name: 'Slice', params: {sliceId: slice.id}}">View</router-link>
    </div>
  </div>
</template>

<script>
import {LISTslices} from '@/api'
export default {
  name: 'WorkSpace',
  data: function () {
    return {
      slices: []
    }
  },
  beforeRouteEnter: function (to, from, next) {
    LISTslices(json => {
      next (vm => vm.setData(json))
    })
  },
  methods: {
    setData: function (json) {
      this.slices = json
    }
  }
}
</script>

