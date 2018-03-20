<template>
  <table class="table is-striped">
    <thead>
      <tr>
        <th>#</th>
        <th>User</th>
        <th>Lab</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(report, i) in reports" track-by="$index">
        <td>{{ i + 1 }}</td>
        <td>{{ report.user }}</td>
        <td>{{ report.lab }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
  import {LISTReports} from '@/api'

  export default {
    name: "ReportsListing",
    data: function () {
      return {
        reports: []
      }
    },
    created: function () {
      LISTReports (json => {
        this.reports = json
      })
    }
  }
</script>

<style scoped>

</style>
