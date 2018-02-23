<template>
  <div class="main">
    <div class="columns">
      <div class="column">
        <h1 class="title">{{ meta.name }}</h1>
      </div>
    </div>

    <div class="columns">
      <div class="column is-narrow">
        <Toolbar :toggle="true" :initialTool="currentTool" :tools="primaryTools" @toolClick="onPrimaryToolClick"></Toolbar>
      </div>
      <div class="column is-narrow">
        <Toolbar :toggle="false" :tools="secondaryTools" @toolClick="onSecondaryToolClick"></Toolbar>
      </div>
      <div class="column is-narrow">
        <Toolbar :toggle="false" :tools="publishTools" @toolClick="onPublishToolClick"></Toolbar>
      </div>
    </div>

    <div class="columns">
      <div class="column panel-container">
        <svg ref="svg" class="workspace" width="100%" height="700" @click.self.stop="onMainSVGClick" @mousemove="onMouseMove">
          <NetworkLink v-for="el in links" :key="el.gid" :el="el" @click="onLinkClick"></NetworkLink>
          <NetworkNode v-for="el in networks" :key="el.gid" :el="el" @click="onNetworkClick"></NetworkNode>
          <Instance v-for="el in instances" :key="el.gid" :el="el" @click="onInstanceClick"></Instance>
          <Router v-for="el in routers" :key="el.gid" :el="el" @click="onRouterClick"></Router>
          <TempLink v-if="tempLink !== null" :tempLink="tempLink"></TempLink>
        </svg>

      <LinkPropertiesPanel v-if="selectionType === 'link'"
        :link="selectedElement"
        @confirm="updateLink"
        @cancel="selectionType = ''"></LinkPropertiesPanel>

      <InstancePropertiesPanel v-if="selectionType === 'instance'"
        :flavors="flavors"
        :instance="selectedElement"
        :instanceConfigurations="instanceConfigurations"
        @confirm="updateInstance"
        @cancel="selectionType = ''"></InstancePropertiesPanel>

      <RouterPropertiesPanel v-if="selectionType === 'router'"
        :flavors="flavors"
        :router="selectedElement"
        :routerConfigurations="routerConfigurations"
        @confirm="updateRouter"
        @cancel="selectionType = ''"></RouterPropertiesPanel>

      <NetworkPropertiesPanel v-if="selectionType === 'network'"
        :network="selectedElement"
        @confirm="updateNetwork"
        @cancel="selectionType = ''"></NetworkPropertiesPanel>

      <ScenarioMetaPanel v-if="selectionType === 'scenario'"
        :scenario="selectedElement"
        @confirm="updateScenarioMeta"
        @cancel="selectionType = ''"></ScenarioMetaPanel>

      </div>
    </div>

    <article v-if="errors.length > 0" class="message is-danger">
      <div class="message-header">
        <p>Error</p>
        <button class="delete" @click="errors = []"></button>
      </div>
      <div class="message-body">
        {{ errors }}
      </div>
    </article>
  </div>
</template>

<script>
import Toolbar from '@/components/scenarios/Toolbar.vue'

import Instance from '@/components/networkelements/Instance.vue'
import Router from '@/components/networkelements/Router.vue'
import NetworkNode from '@/components/networkelements/Network.vue'
import NetworkLink from '@/components/networkelements/Link.vue'
import TempLink from '@/components/networkelements/TempLink.vue'

import LinkPropertiesPanel from '@/components/scenarios/panels/LinkPropertiesPanel.vue'
import InstancePropertiesPanel from '@/components/scenarios/panels/InstancePropertiesPanel.vue'
import RouterPropertiesPanel from '@/components/scenarios/panels/RouterPropertiesPanel.vue'
import NetworkPropertiesPanel from '@/components/scenarios/panels/NetworkPropertiesPanel.vue'
import ScenarioMetaPanel from '@/components/scenarios/panels/ScenarioMetaPanel.vue'

import {
  PATCHscenario,
  POSTscenario,
  GETscenario,
  LISTInstanceConfigurations,
  LISTRouterConfigurations,
  LISTFlavors
} from '@/api'

const uuidv1 = require('uuid/v1')

export default {
  name: "ScenarioEditor",
  components: {
    Toolbar,

    Instance,
    Router,
    NetworkNode,
    NetworkLink,
    TempLink,

    LinkPropertiesPanel,
    InstancePropertiesPanel,
    RouterPropertiesPanel,
    NetworkPropertiesPanel,
    ScenarioMetaPanel
  },
  data: function () {
    return {
      isNewScenario: false,

      meta: {
        name: 'Untitled Scenario',
        description: '',
        securityGroupRules: [],
        isPublic: false,
      },

      currentTool: 'select',
      primaryTools: [
        { name: 'select', icon: 'mouse-pointer', title: '' },
        { name: 'instance', icon: 'server', title: 'Instance' },
        { name: 'router', icon: 'cube', title: 'Router' },
        { name: 'network', icon: 'cloud', title: 'Network' },
        { name: 'link', icon: 'link', title: 'Link' },
        { name: 'delete', icon: 'trash-alt', title: '' }
      ],
      secondaryTools: [
        { name: 'import', icon: 'upload', title: 'Import', disabled: true },
        { name: 'export', icon: 'download', title: 'Export' }
      ],
      publishTools: [
        { name: 'save', icon: 'save', title: '', theme: 'is-success' },
        { name: 'delete', icon: 'trash-alt', title: 'Delete Scenario', hidden: true, disabled: true },
      ],

      selectionType: '',
      selectedElement: null, // the element is selected on the screen using select tool

      tempLink: null,
      networks: [],
      instances: [],
      routers: [],
      links: [],

      instanceConfigurations: [],
      routerConfigurations: [],

      flavors: [],

      errors: []
    }
  },

  beforeRouteEnter: function (to, from, next) {
    if (to.name === "ScenarioEditor") {
      GETscenario(to.params.id, json => {
        next(vm => vm.setData(json))
      });
    } else {
      next();
    }
  },

  created: function () {
    switch (this.$route.name) {
      case "ScenarioEditor":
        this.isNewScenario = false;
        this.publishTools.find(tool => tool.name === 'save').title = 'Update';
        this.publishTools.find(tool => tool.name === 'delete').hidden = false;
        break;
      case "NewScenario":
        this.isNewScenario = true;
        this.publishTools.find(tool => tool.name === 'save').title = 'Create';
        this.publishTools.find(tool => tool.name === 'delete').hidden = true;
        this.selectionType = 'scenario';
        this.selectedElement = this.meta;
        break;
    }

    LISTInstanceConfigurations(json => {
      this.instanceConfigurations = json
    });

    LISTRouterConfigurations(json => {
      this.routerConfigurations = json
    });

    LISTFlavors(json => {
      this.flavors = json
    });
  },

  computed: {
    topo() {
      return {
        networks: this.networks,
        instances: this.instances,
        routers: this.routers,
        links: this.links
      }
    }
  },

  methods: {
    setData: function (json) {
      this.meta = {
        name: json.name ? json.name : '',
        description: json.description ? json.description : '',
        isPublic: !!json.isPublic,
        securityGroupRules: Array.isArray(json.sgRules) ? json.sgRules : [],
      };
      this.instances = json.topo.hasOwnProperty('instances') ? json.topo.instances : [];
      this.networks = json.topo.hasOwnProperty('networks') ? json.topo.networks : [];
      this.routers = json.topo.hasOwnProperty('routers') ? json.topo.routers : [];
      this.links = json.topo.hasOwnProperty('links') ? json.topo.links : [];
      this.selectionType = 'scenario';
      this.selectedElement = this.meta;
    },

    /**
     * Event handler when user select a new tool in ToolBox
     */
    onPrimaryToolClick (name) {
      this.currentTool = name;
      this.tempLink = null;
    },

    onSecondaryToolClick(name) {
      switch (name) {
        case 'import':
          break;
        case 'export':
          this.download();
          break;
      }
    },

    onPublishToolClick(name) {
      switch (name) {
        case 'save':
          let button = this.publishTools.find(tool => tool.name === 'save');
          button.theme += ' is-loading';
          button.disabled = true;
          let onSuccess = () => this.$router.push('/scenarios/');
          let onFailed = json => {
            button.theme = 'is-success';
            button.disabled = false;
            if (json && json.errors) {
              this.errors = json.errors;
            }
          };
          if (this.isNewScenario) {
            POSTscenario(this.meta.name, this.meta.description, this.meta.securityGroupRules, this.meta.isPublic, this.topo, onSuccess, onFailed);
          } else {
            PATCHscenario(this.meta.name, this.meta.description, this.meta.securityGroupRules, this.meta.isPublic, this.topo,
              this.$route.params.id, onSuccess, onFailed);
          }
          break;
        case 'delete':
          break;
      }
    },

    /**
     * Event handler when main svg is clicked.
     */
    onMainSVGClick: function (e) {
      let svg = this.$refs.svg
      let pt = svg.createSVGPoint()
      pt.x = e.clientX
      pt.y = e.clientY
      let realPt = pt.matrixTransform(svg.getScreenCTM().inverse())

      switch (this.currentTool) {
        case 'network':
          {
            let newNetwork = {
              gid: uuidv1(),
              type: 'NetworkNode',
              name: 'Network' + this.networks.length,
              x: realPt.x,
              y: realPt.y,
              cidr: null
            }
            this.networks.push(newNetwork)
            break
          }
        case 'instance':
          {
            let newInstance = {
              gid: uuidv1(),
              type: 'Instance',
              name: 'Instance' + this.instances.length,
              x: realPt.x,
              y: realPt.y,
              image: null,
              status: null,
              configurations: []
            }
            this.instances.push(newInstance)
            break
          }
        case 'router':
          {
            let newRouter = {
              gid: uuidv1(),
              type: 'Router',
              name: 'Router' + this.routers.length,
              x: realPt.x,
              y: realPt.y,
              status: null,
              configurations: []
            }
            this.routers.push(newRouter)
            break
          }
        default:
          this.selectedElement = this.meta;
          this.selectionType = 'scenario';
      }
    },

    onMouseMove: function (e) {
      let svg = this.$refs.svg
      let pt = svg.createSVGPoint()
      pt.x = e.clientX
      pt.y = e.clientY

      let realPt = pt.matrixTransform(svg.getScreenCTM().inverse())

      if (this.tempLink !== null) {
        let deltaX = 5
        let deltaY = 5
        if (realPt.x < this.tempLink.x1) {
          deltaX = -5
        }
        if (realPt.y < this.tempLink.y1) {
          deltaY = -5
        }
        this.tempLink.x2 = realPt.x - deltaX // to prevent the templine become clickable
        this.tempLink.y2 = realPt.y - deltaY // to prevent the templine become clickable
      }
    },

    onNetworkClick: function(element) {
      switch (this.currentTool) {
        case 'select':
          this.selectedElement = element;
          this.selectionType = 'network';
          break;
        case 'delete':
          if (this.selectedElement === element || (this.selectionType === 'link'
              && this.selectedElement.network.gid === element.gid)) {
            this.selectedElement = null;
            this.selectionType = '';
          }
          this.networks = this.networks.filter(network => network.gid !== element.gid);
          this.links = this.links.filter(link => link.network.gid !== element.gid);
          break;
        case 'link':
          if (this.tempLink === null) {
            this.tempLink = {
              network: element,
              x1: element.x,
              y1: element.y,
              x2: element.x,
              y2: element.y,
              target: null
            }
          } else {
            // a link is drawn from an instance or router
            if (this.tempLink.network === null) {
              let network = element
              let target = this.tempLink.target
              let newLink = {
                gid: uuidv1(),
                name: `${network.name}_${target.name}`,
                type: 'NetworkLink',
                network: network,
                target: target,
                ip: null
              }
              if (this.links.find(el => el.network == network && el.target == target) === undefined) { // not duplicated link)
                  this.links.push(newLink)
                  this.tempLink = null
              }
            }
          }
        break
      }
    },

    onRouterClick: function(element) {
      switch (this.currentTool) {
        case 'select':
          this.selectedElement = element;
          this.selectionType = 'router';
          break;
        case 'delete':
          if (this.selectedElement === element || (this.selectionType === 'link'
              && this.selectedElement.target.gid === element.gid)) {
            this.selectedElement = null;
            this.selectionType = '';
          }
          this.routers = this.routers.filter(router => router.gid !== element.gid);
          this.links = this.links.filter(link => link.target.gid !== element.gid);
          break;
        case 'link': {
          if (this.tempLink === null){
            this.tempLink = {
              network: null,
              target: element,
              x1: element.x,
              y1: element.y,
              x2: element.x,
              y2: element.y
            }
          } else {
            if (this.tempLink.target === null) {
              let network = this.tempLink.network
              let target = element
              let newLink = {
                gid: uuidv1(),
                name: `${network.name}_${target.name}`,
                type: 'NetworkLink',
                network: network,
                target: target,
                ip: null
              }
              if (this.links.find(el => el.network == network && el.target == target) === undefined) { // not duplicated link)
                  this.links.push(newLink)
                  this.tempLink = null
              }
            }
          }
          break;
        }
      }
    },

    onInstanceClick: function(element) {
      switch (this.currentTool) {
        case 'select':
          this.selectedElement = element;
          this.selectionType = 'instance';
          break;
        case 'delete':
          if (this.selectedElement === element || (this.selectionType === 'link'
              && this.selectedElement.target.gid === element.gid)) {
            this.selectedElement = null;
            this.selectionType = '';
          }
          this.instances = this.instances.filter(instance => instance.gid !== element.gid);
          this.links = this.links.filter(link => link.target.gid !== element.gid);
          break;
        case 'link':
          if (this.tempLink === null){
            this.tempLink = {
              network: null,
              target: element,
              x1: element.x,
              y1: element.y,
              x2: element.x,
              y2: element.y
            }
          } else {
            if (this.tempLink.target === null) {
              let network = this.tempLink.network
              let target = element
              let newLink = {
                name: `${network.name}_${target.name}`,
                gid: uuidv1(),
                type: 'NetworkLink',
                network: network,
                target: target,
                ip: null
              }
              if (this.links.find(el => el.network == network && el.target == target) === undefined) { // not duplicated link)
                  this.links.push(newLink)
                  this.tempLink = null
              }
            }
          }
        break
      }
    },

    onLinkClick: function(element) {
      switch (this.currentTool) {
        case 'select':
          this.selectionType = 'link';
          this.selectedElement = element;
          break;
        case 'delete':
          if (this.selectedElement === element) {
            this.selectedElement = null;
            this.selectionType = '';
          }
          this.links = this.links.filter(link => link.gid !== element.gid);
          break;
      }
    },

    updateLink(link) {
      this.selectedElement.ip = link.ip;
      this.selectedElement.allowedAddressPairs = link.allowedAddressPairs;
      this.selectedElement = null;
      this.selectionType = '';
    },

    updateInstance(instance) {
      this.selectedElement.name = instance.name;
      this.selectedElement.image = instance.image;
      this.selectedElement.flavor = instance.flavor;
      this.selectedElement.configurations = instance.configurations;
      this.selectedElement = null;
      this.selectionType = '';
    },

    updateRouter(router) {
      this.selectedElement.name = router.name;
      this.selectedElement.image = router.image;
      this.selectedElement.flavor = router.flavor;
      this.selectedElement.configurations = router.configurations;
      this.selectedElement = null;
      this.selectionType = '';
    },

    updateNetwork(network) {
      this.selectedElement.name = network.name;
      this.selectedElement.cidr = network.cidr;
      this.selectedElement = null;
      this.selectionType = '';
    },

    updateScenarioMeta(scenario) {
      this.meta = {
        name: scenario.name,
        description: scenario.description,
        securityGroupRules: scenario.securityGroupRules,
        isPublic: scenario.isPublic
      };
      this.selectedElement = null;
      this.selectionType = '';
    },

    download() {
      const element = document.createElement('a');
      const json = JSON.stringify(this.topo);
      const blob = new Blob([json], {type: "application/json"});

      element.setAttribute('href', URL.createObjectURL(blob));
      element.setAttribute('download', [this.meta.name, new Date().toISOString().slice(0, 10), 'export.json']
        .filter(i => !!i.trim()).join("_"));
      element.style.display = 'none';
      document.body.appendChild(element);
      element.click();

      document.body.removeChild(element);
    }
  }
}
</script>

<style scoped>
  .main {
    position: relative;
  }

  .panel-container {
    position: relative;
  }

  .workspace {
    background-color: #f6f6f6;
    border-radius: 5px;
    border: 1px solid rgba(0,0,0,0.1);
  }

  .message {
    position: absolute;
    z-index: 100;
    top: 0;
    right: 0;
    max-width: 400px;
  }
</style>
