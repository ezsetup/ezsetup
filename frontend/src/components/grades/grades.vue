<template>
  <div class="main">
    <div class="columns">
      <div class="column">
        <h1 class="title">Grades: {{ userInfo.fullname }}</h1>
      </div>
    </div>
    <div class="columns">
      <div class="column">
        <GradesListing v-bind:userInfo="userInfo"></GradesListing>
      </div>
    </div>
  </div>
</template>

<script>
  import GradesListing from '@/components/grades/GradesListing.vue'
  import {GETUserSelf,
          GETUser,
          SEARCHuser} from '@/api'

  export default {
    name: "Grades",
    components: {
      GradesListing
    },
    data: function () {
      return {
        userInfo: null
      }
    },
    created: function () {
      GETUserSelf(json => {
        SEARCHuser(json.email, json => {
            this.userInfo = json[0]
        })
      })
    }
  }
</script>

<style scoped>

</style>
