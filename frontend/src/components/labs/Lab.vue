<template>
  <div>
    <LabDeployment v-if="status==='inactive'" @deploying="onStartDeploying"></LabDeployment>
    <LabViewer v-else-if="status!=='inactive'" @destroying="onStartDestroying" :name="name" :slices="slices" :status="status"></LabViewer>
  </div>
</template>

<style scoped>


</style>

<script>
  import {
    optionsGET
  } from '@/common'
  import {
    API_SERVER
  } from '@/config'
  import LabDeployment from '@/components/labs/LabDeployment'
  import LabViewer from '@/components/labs/LabViewer'

  export default {
    name: 'lab',
    components: {
      LabDeployment,
      LabViewer
    },
    data: function () {
      return {
        status: null,
        name: null,
        slices: [],
        pollingTimeout: 3000,
        timeoutId: null,
        labId: null
      }
    },
    created: function () {
      this.labId = this.$route.params.id
      this.pollLab()
    },
    methods: {
      pollLab: function () {
        let options = optionsGET()
        fetch(API_SERVER + '/api/labs/' + this.labId + '/', options)
          .then(response => {
            if (response.ok) {
              response.json().then(json => {
                this.status = json.status
                this.name = json.name
                this.slices = json.slices
                if (this.status === 'deploying' || this.status === 'destroying') {
                  this.timeoutId = setTimeout(() => {
                    this.pollLab()
                  }, this.pollingTimeout)
                }
              })
            } else {
              console.log(response);
              this.$router.push('/')
            }
          })
          .catch(err => {
            console.log(err)
          })
      },
      onStartDeploying: function () {
        this.status = 'deploying'
        // NOTE: temporary fix for 'always loading' bug
        // TODO: use state machine to ensure what is next state must be. After that, just this.pollLab() is enough
        this.timeoutId = setTimeout(() => {
          this.pollLab()
        }, this.pollingTimeout)
      },
      onStartDestroying: function () {
        this.status = 'destroying'
        // NOTE: temporary fix for 'always loading' bug
        // TODO: use state machine to ensure what is next state must be. After that, just this.pollLab() is enough
        this.timeoutId = setTimeout(() => {
          this.pollLab()
        }, this.pollingTimeout)
      }
    },
    destroyed: function () {
      clearTimeout(this.timeoutId)
    }
  }
</script>
