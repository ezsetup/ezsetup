<template>
  <div class="main">
    <h2 class="title">{{name}}</h2>
    <div class="columns">
      <svg ref="svg" class="column workspace" width="100%" height="700">
        <NetworkLink v-for="el in elements.links" :key="el.id" :el="el" @click="onComponentClick">
        </NetworkLink>
        <NetworkNode v-for="el in elements.networks" :key="el.id" :el="el" @click="onComponentClick">
        </NetworkNode>
        <Instance v-for="el in elements.instances" :key="el.id" :el="el" @click="onComponentClick">
        </Instance>
        <Router v-for="el in elements.routers" :key="el.id" :el="el" @click="onComponentClick">
        </Router>
      </svg>

      <div class="column is-3 property">
        <PropertiesViewer :el="currentElement"></PropertiesViewer>
      </div>
    </div>
  </div>
</template>

<style scoped>
  .main {
    margin-top: 20px;
  }

  .property {
    background-color: #f6f6f6;
    margin-left: 5px;
    margin-bottom: 5px;
  }

  .workspace {
    background-color: #f6f6f6;
    margin-bottom: 5px;
    width: 800px;
  }

  .center {
    width: 60%;
    margin: auto;
  }

</style>

<script>
  import { GETslice } from '@/api'
  import Instance from '@/components/networkelements/Instance.vue'
  import Router from '@/components/networkelements/Router.vue'
  import NetworkNode from '@/components/networkelements/Network.vue'
  import NetworkLink from '@/components/networkelements/Link.vue'
  import PropertiesViewer from '@/components/slices/PropertiesViewer.vue'

  export default {
    name: 'Slice',
    components: {
      Instance,
			Router,
      NetworkLink,
      NetworkNode,
      PropertiesViewer
    },
    data: function () {
      return {
        name: null,
        elements: {
          networks: null,
          instances: null,
          links: null,
					routers: null
        },
        currentElement: null,
        sliceId: null,
        pollingTimeout: 3000
      }
    },
    created: function () {
      this.sliceId = this.$route.params.sliceId
      this.pollSlice()
    },
    methods: {
      pollSlice: function () {
        GETslice(this.sliceId, json => {
          this.status = json.status
          this.name = json.name
          this.elements = {
            instances: json.instances,
            routers: json.routers,
            networks: json.networks,
            links: json.links
          }
          if (this.status === 'deploying') {
            setTimeout(() => {
              this.pollSlice()
            }, this.pollingTimeout)
          }
        })
      },
      onComponentClick: function (element) {
        this.currentElement = element
      }
    }
  }
</script>
