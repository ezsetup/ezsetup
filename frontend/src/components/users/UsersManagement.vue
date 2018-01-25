<template>
  <div class="main">
    <router-link class="button" to="users/new">New User</router-link>
    <UserListing></UserListing>
  </div>
</template>

<style scoped>
.main {
  margin-top: 20px;
}

.center {
  text-align: center;
}
</style>

<script>
import UserListing from '@/components/users/UserListing.vue'
export default {
  name: 'LabManagement',
  components: {
    UserListing
  },
  data: function () {
    return {
    }
  },
  methods: {
  }
}
</script>
