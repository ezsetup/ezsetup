<template>
  <table class="table is-striped">
    <thead>
      <tr>
        <th>#</th>
        <th>Name</th>
        <th>Email</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(user, i) in users" track-by="$index">
        <td>{{ i + 1 }}</td>
        <td>{{ user.fullname }}</td>
        <td>{{ user.email }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import {LISTusers} from '@/api'
export default {
  name: 'UserListing',
  data: function () {
    return {
      users: []
    }
  },
  created: function () {
    LISTusers (json => {
      this.users = json
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
