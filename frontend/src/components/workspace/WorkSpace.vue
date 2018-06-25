<template>
  <div>
    <div v-for="(slice, i) in slices" :key="slice.id" class="columns">
      <div class="column is-2">
        <p><strong>{{slice.labName}}</strong></p>
      </div>
      <div class="column is-2">
        <div style="padding-bottom: 0.5em;">
          <div class="columns">
            <div class="column is-narrow">
              <router-link v-if="checkpreattempts(i, slice.allowedAttempts[0])" class="button is-info is-outlined"
                       :to="{name: 'TakeAssessment', params: {id: slice.preassessment, type: 'pre', labname: slice.labName}}">
                       Pre-Assessment</router-link>
              <button v-else disabled class="button is-info is-outlined">Pre-Assessment</button>
            </div>
            <div class="column is-narrow">
              Attempts remaining: {{ slice.allowedAttempts[0] - preattempts[i] }}
            </div>
          </div>
        </div>
        <div style="padding-bottom: 0.5em;">
          <router-link class="button is-info" :to="{name: 'Slice', params: {sliceId: slice.id}}">View Lab</router-link> &nbsp;
        </div>
        <div style="padding-bottom: 1em;">
          <div class="columns">
            <div class="column is-narrow">
              <router-link v-if="checkpostattempts(i, slice.allowedAttempts[1])" class="button is-info is-outlined"
                       :to="{name: 'TakeAssessment', params: {id: slice.postassessment, type: 'post', labname: slice.labName}}">
                       Post-Assessment</router-link>
              <button v-else disabled class="button is-info is-outlined">Post-Assessment</button>
            </div>
            <div class="column is-narrow">
              Attempts remaining: {{ slice.allowedAttempts[1] - postattempts[i] }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {LISTslices,
        GETAssessment,
        LISTReports,
        LISTAssessments,
        GETUserSelf,
        SEARCHuser} from '@/api'
export default {
  name: 'WorkSpace',
  data: function () {
    return {
      slices: [],
      preattempts: [],
      postattempts: [],
      student: null
    }
  },
  beforeRouteEnter: function (to, from, next) {
    LISTslices(json => {
      next (vm => vm.setData(json))
    })
  },
  methods: {
    setData: function (slices) {
      var student = ''
      var preattempts = []
      var postattempts = []
      GETUserSelf(json => {
          SEARCHuser(json.email, json => {
            student = json[0].fullname
            LISTReports(json => {
              for (var i=0; i < slices.length; i++) {
                preattempts.push(0)
                postattempts.push(0)
                for (var x=0; x < json.length; x++) {
                  if (slices[i].preassessment === parseInt(json[x].assessmentid)) {
                    if (slices[i].labName === json[x].labname) {
                      if (json[x].student === student) {
                        if (json[x].attemptNum > preattempts[i]) {
                          preattempts[i] = json[x].attemptNum
                        }
                      }
                    }
                  }
                  else if (slices[i].postassessment === parseInt(json[x].assessmentid)) {
                    if (slices[i].labName === json[x].labname) {
                      if (json[x].student === student) {
                        if (json[x].attemptNum > postattempts[i]) {
                          postattempts[i] = json[x].attemptNum
                        }
                      }
                    }
                  }
                }
              }
              this.slices = slices
              this.student = student
              this.preattempts = preattempts
              this.postattempts = postattempts
            })
          })
        })

    },
    checkpreattempts: function(i, attempts) {
      if (this.preattempts[i] < attempts) {
        return true
      }
      else {
        return false
      }
    },
    checkpostattempts: function(i, attempts) {
      if (this.postattempts[i] < attempts) {
        return true
      }
      else {
        return false
      }
    }
  }
}
</script>

