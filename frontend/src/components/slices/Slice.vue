<template>
  <div>
    <div class="columns">
      <div class="column">
        <h1 class="title">{{name}}</h1>
        <p><status-indicator :status="status" class="is-small"></status-indicator><span><i class="far fa-user"></i> {{ username }}</span></p>
      </div>
    </div>
    <div class="columns">
      <div class="column panel-container">
        <svg ref="svg" class="workspace" width="100%" height="700">
          <NetworkLink v-for="el in elements.links" :key="el.id" :el="el" @click="onComponentClick"></NetworkLink>
          <NetworkNode v-for="el in elements.networks" :key="el.id" :el="el" @click="onComponentClick"></NetworkNode>
          <Instance v-for="el in elements.instances" :key="el.id" :el="el" @click="onComponentClick"></Instance>
          <Router v-for="el in elements.routers" :key="el.id" :el="el" @click="onComponentClick"></Router>
        </svg>

        <InstancePropertiesPanel v-if="currentElement && currentElement.type === 'Instance'" :instance="currentElement"></InstancePropertiesPanel>
        <RouterPropertiesPanel v-if="currentElement && currentElement.type === 'Router'" :router="currentElement"></RouterPropertiesPanel>
        <LinkPropertiesPanel v-if="currentElement && currentElement.type === 'NetworkLink'" :link="currentElement"></LinkPropertiesPanel>
        <NetworkPropertiesPanel v-if="currentElement && currentElement.type === 'NetworkNode'" :network="currentElement"></NetworkPropertiesPanel>
      </div>
    </div>
  </div>
</template>

<style scoped>
  .title {
    margin-bottom: 0.5rem;
  }

  .title + p > span {
    margin-right: 0.5rem;
  }

  .panel-container {
    position: relative;
  }

  .workspace {
    background-color: #f6f6f6;
    border-radius: 5px;
    border: 1px solid rgba(0,0,0,0.1);
  }
</style>

<script>
  import { GETslice } from '@/api'
  import Instance from '@/components/networkelements/Instance.vue'
  import Router from '@/components/networkelements/Router.vue'
  import NetworkNode from '@/components/networkelements/Network.vue'
  import NetworkLink from '@/components/networkelements/Link.vue'
  import StatusIndicator from '@/components/common/StatusIndicator'
  import InstancePropertiesPanel from '@/components/slices/panels/InstancePropertiesPanel.vue'
  import RouterPropertiesPanel from '@/components/slices/panels/RouterPropertiesPanel.vue'
  import LinkPropertiesPanel from '@/components/slices/panels/LinkPropertiesPanel.vue'
  import NetworkPropertiesPanel from '@/components/slices/panels/NetworkPropertiesPanel.vue'

  export default {
    name: 'Slice',
    components: {
      Instance,
			Router,
      NetworkLink,
      NetworkNode,
      StatusIndicator,
      InstancePropertiesPanel,
      RouterPropertiesPanel,
      LinkPropertiesPanel,
      NetworkPropertiesPanel
    },
    data: function () {
      return {
        name: null,
        username: null,
        status: null,
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
          this.username = json.username
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
