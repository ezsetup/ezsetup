<template>
  <div class="main">
    <div class="columns">
      <div class="column">
        <h1 class="title">Users</h1>
      </div>
      <div class="column is-narrow">
		    <router-link :to="{ name: 'NewUser' }" class="button is-success">Create User</router-link>
      </div>
    </div>
    <div class="columns">
      <div class="column">
        <UserListing></UserListing>
      </div>
    </div>
  </div>
</template>

<style scoped>
  .main {
    margin-top: 20px;
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
