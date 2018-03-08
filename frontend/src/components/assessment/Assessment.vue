<template>
  <div class="main">
    <div class="columns">
      <div class="column">
        <h1 class="title">Assessment</h1>
      </div>
      <div class="column is-narrow">
        <router-link :to="{ name: 'newAssessment' }" class="button is-success">Create Assessment</router-link>
      </div>
    </div>
    <div class="columns">
      <div class="column">
        <AssessmentListing></AssessmentListing>
      </div>
    </div>
  </div>
</template>

<script>
import AssessmentListing from '@/components/assessment/AssessmentListing.vue'
export default {
  name: 'Assessment',
  components: {
    AssessmentListing
  },
  data: function () {
    return {
	  title: '',
	  description: '',
	  newQ: false
	}
  },
  methods: {
    addQuestion: function () {
	  if(!this.newQ) {
        return this.newQ=true
	  }
	  else {
	    return this.newQ=false
	  }
    }
  }
}
</script>

<style>
#assessment {
  text-align: left;
  padding: 0 10px 0 10px;
}
</style>
