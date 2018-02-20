<template>
  <div>
    <LabDeployment v-if="status==='inactive'" @deploying="onStartDeploying" :name="name"></LabDeployment>
    <LabViewer v-else-if="status!=='inactive'" @destroying="onStartDestroying" :name="name" :slices="slices" :status="status"></LabViewer>
  </div>
</template>

<script>
  import { GETlab } from '@/api'
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
        GETlab(this.labId, json => {
          this.status = json.status
          this.name = json.name
          this.slices = json.slices
          if (this.status === 'deploying' || this.status === 'destroying') {
            this.timeoutId = setTimeout(() => {
              this.pollLab()
            }, this.pollingTimeout)
          }
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
