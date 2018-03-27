<template>
  <table class="table is-striped">
    <thead>
      <tr>
        <th>#</th>
        <th>Name</th>
        <th>Description</th>
        <th>Slices</th>
        <th>Status</th>
        <th>Action</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(lab, i) in labs" track-by="$index">
        <td>{{ i + 1 }}</td>
        <td><router-link :to="{ name: 'Lab', params: { id: lab.id } }">{{ lab.name }}</router-link></td>
        <td>{{ lab.description }}</td>
        <td>{{ lab.slices }}</td>
        <td>
          <status-indicator :status="lab.status"></status-indicator>
        </td>
        <td>
          <router-link class="button is-small" :to="{ name: 'Lab', params: { id: lab.id } }">
            Manage
          </router-link>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
  import { LISTlabs } from '@/api'
  import StatusIndicator from '@/components/common/StatusIndicator'

  export default {
    components: { StatusIndicator },
    name: 'LabsListing',
    data: function () {
      return {
        labs: []
      }
    },
    created: function () {
      LISTlabs(json => {
        this.labs = json
      })
    }
  }
</script>
