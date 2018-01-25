<template>
  <div>
    <div v-for="user in users" :key="user.id" class="columns">
      <p class="column is-5">{{user.fullname}}</p>
      <p class="column is-5">{{user.email}}</p>
    </div>
  </div>
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