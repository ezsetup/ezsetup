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
          <span v-if="lab.status === 'inactive'"><i class="fas fa-question-circle"></i> Not deployed</span>
          <span v-if="lab.status === 'deploying'"><i class="fas fa-spinner fa-pulse"></i> Deploying</span>
          <span v-if="lab.status === 'deployfailed'"><i class="fas fa-times-circle has-text-danger"></i> Deploy failed</span>
          <span v-if="lab.status === 'active'"><i class="fas fa-check-circle has-text-success"></i> Active</span>
          <span v-if="lab.status === 'destroying'"><i class="fas fa-spinner fa-pulse"></i> Destroying</span>
          <span v-if="lab.status === 'destroyfailed'"><i class="fas fa-times-circle has-text-danger"></i> Destroy failed</span>
        </td>
        <td><router-link class="button is-small" :to="{ name: 'Lab', params: { id: lab.id } }">Manage</router-link></td>
      </tr>
    </tbody>
  </table>
</template>

<script>
  import {LISTlabs} from '@/api'

  export default {
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
