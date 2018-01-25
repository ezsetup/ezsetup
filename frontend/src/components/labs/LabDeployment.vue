<template>
  <div class="main">
    <div class="center">
      <h4 class="title">Deployment</h4>
      <div class="field">
        <label class="label">Add users</label>
        <div v-for="(user, index) in users" :key="index" class="columns is-7">
          <p class="column is-1">{{index + 1}}</p>
          <p class="column is-5">{{user.fullname}}</p>
          <p class="column is-5">{{user.email}}</p>
        </div>
        <div class="field has-addons">
          <p class="control">
            <input class="input" type="text" placeholder="Find a user" 
              v-model="searchTerm" @keypress.enter="searchUser"
              @keypress.esc="()=>{searchResults = []}" >
          </p>
          <p class="control"
            <button class="button is-info" @click="searchUser">
              Search
            </button>
          </p>
        </div>
        <div v-if="searchResults.length > 0" class="box column is-7">
        <div v-for="user in addableUsers" :key="user.id" class="columns">
          <p class="column is-5">{{user.fullname}}</p>
          <p class="column is-5">{{user.email}}</p>
          <div class="column is-2">
            <button @click="addUser(user)" class="button is-small">Add</button>
            </div>
        </div>
        </div>
        <hr>
  
        <div class="field">
          <label for="cloudProvider" class="label">Cloud provider</label>
          <p class="control">
            <span class="select">
              <select id="cloudProvider" name="cloudProvider" v-model="cloudProvider">
                <option value="Openstack">Openstack</option>
                <option value="AWS">AWS</option>
              </select>
            </span>
          </p>
        </div>
  
        <div v-if="cloudProvider === 'Openstack'">
          <div class="field">
            <label for="openstackAuthURL" class="label">Auth URL</label>
            <p class="control">
              <input class="input" v-model="openstackAuthURL" id="openstackAuthURL" name="openstackAuthURL" type="url" placeholder="Openstack authenication URL">
            </p>
          </div>
          <div class="field">
            <label for="openstackUser" class="label">User</label>
            <p class="control">
              <input class="input" v-model="openstackUser" id="openstackUser" name="openstackUser" placeholder="Openstack username">
            </p>
          </div>
          <div class="field">
            <label for="openstackPassword" class="label">Password</label>
            <p class="control">
              <input class="input" v-model="openstackPassword" type="password" id="openstackPassword" name="openstackPassword" placeholder="Openstack password">
            </p>
          </div>
          <div class="field">
            <label for="openstackProject" class="label">Project</label>
            <p class="control">
              <input class="input" v-model="openstackProject" id="openstackProject" name="openstackProject" placeholder="Openstack project">
            </p>
          </div>
        </div>
  
        <div v-else-if="cloudProvider === 'AWS'">
          <div class="field">
            <label for="awsAccessKeyId" class="label">Access Key ID</label>
            <p class="control">
              <input class="input" v-model="awsAccessKeyId" id="awsAccessKeyId" name="awsAccessKeyId" placeholder="AWS access key id">
            </p>
          </div>
          <div class="field">
            <label for="awsSecretAccessKey" class="label">Secret Access Key</label>
            <p class="control">
              <input class="input" v-model="awsSecretAccessKey" id="awsSecretAccessKey" name="awsSecretAccessKey" placeholder="AWS secret access key">
            </p>
          </div>
          <div class="field">
            <label for="awsRegion" class="label">Region</label>
            <p class="control">
              <span class="select">
                <select id="awsRegion" name="awsRegion" v-model="awsRegion">
                  <option value="us-west-2">us-west-2</option>
                </select>
              </span>
            </p>
          </div>
        </div>
  
        <br>
        <div class="field">
          <button v-if="state !== null" type="submit" class="button is-primary is-loading"></button>
          <button v-else type="submit" v-on:click="onDeployBtn" class="button is-primary">{{buttonTitle}}</button>
          <p v-if="error" class="help is-danger">{{error}}</p>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
  import {POSTcloudconfig, DEPLOYlab, SEARCHuser} from '@/api'
  const State = Object.freeze({
    UPLOADING: 'Uploading cloud config',
    DEPLOYING: 'Deploying'
  })
  export default {
    name: 'LabDeployment',
    data: function () {
      return {
        cloudConfigId: null,
        cloudProvider: 'Openstack',
        openstackAuthURL: 'http://keystone.maas:5000/v2.0', // TODO: change me to null
        openstackUser: null,
        openstackPassword: null,
        openstackProject: null,
        awsAccessKeyId: null,
        awsSecretAccessKey: null,
        awsRegion: 'us-west-2',
        error: null,
        state: null,
        users: [],
        searchTerm: null,
        searchResults: []
      }
    },
    computed: {
      buttonTitle: function () {
        if (this.state === null) {
          return 'DEPLOY'
        }
      },
      addableUsers: function () {
        return this.searchResults.filter( (element) =>
          !this.users.map(user=>user.id).includes(element.id)
        )
      }
    },
    methods: {
      onDeployBtn: function () {
        this.error = null
        this.postCloudConfig()
      },
      postCloudConfig: function () {
        this.state = State.UPLOADING
        let cloudDetail
        switch (this.cloudProvider) {
          case 'Openstack':
            cloudDetail = {
              openstackAuthURL: this.openstackAuthURL,
              openstackUser: this.openstackUser,
              openstackPassword: this.openstackPassword,
              openstackProject: this.openstackProject
            }
            break
          case 'AWS':
            cloudDetail = {
              awsAccessKeyId: this.awsAccessKeyId,
              awsSecretAccessKey: this.awsSecretAccessKey,
              awsRegion: this.awsRegion
            }
            break
        }

        POSTcloudconfig(cloudDetail, this.cloudProvider, this.$route.params.id, 
          json => {
            this.cloudConfigId = json.id
            this.deployLab()
          },
          json => {
            this.error = json.message
            this.state = null
          })
      },
      deployLab: function () {
        if (this.users.length === 0) {
          this.error = "No users have been added to the lab. You need at least one user to deploy"
          this.state = null
        } else {
          this.error = null
          this.state = State.UPLOADING
          DEPLOYlab(this.$route.params.id, this.cloudConfigId, this.users, json => {
            this.$emit('deploying')
          })
        }
      },
      searchUser: function () {
        SEARCHuser(this.searchTerm, json => {
          this.searchResults = json
        })
      },
      addUser: function(user) {
        this.users.push(user)
      }
    }
  }
</script>

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