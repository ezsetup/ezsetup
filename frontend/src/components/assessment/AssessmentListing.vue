<template>
  <table class="table is-striped">
    <thead>
      <tr>
        <th>#</th>
        <th>Title</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(assessment, i) in assessments" track-by="$index">
        <td>{{ i + 1 }}</td>
        <td>{{ assessment.atitle }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import {LISTAssessments} from "@/api"
export default {
  name: 'AssessmentListing',
  data: function () {
    return {
      assessments: []
    }
  },
  created: function () {
    LISTAssessments (json => {
      this.assessments = json
    })
  }
}
</script>
<style scoped>
.main {
  margin-top: 20px;
}

.center {
  width: 60%;
  margin: auto;
}
</style>
