<template>
  <table class="table is-striped">
    <thead>
      <tr>
        <th>#</th>
        <th>Name</th>
        <th>Description</th>
        <th>Status</th>
        <th>Action</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(slice, i) in slices" track-by="$index">
        <td>{{ i + 1 }}</td>
        <td><router-link :to="{ name: 'Slice', params: { sliceId: slice.id } }">{{ slice.lab.name }}</router-link></td>
        <td>{{ slice.lab.description }}</td>
        <td>
          <status-indicator :status="slice.status"></status-indicator>
        </td>
        <td>
          <router-link :to="{ name: 'Slice', params: { sliceId: slice.id } }">View</router-link>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
  import { LISTslices } from '@/api'
  import StatusIndicator from '@/components/common/StatusIndicator'

  export default {
    name: 'WorkSpace',
    components: { StatusIndicator },
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

