<template>
  <div>
    <div class="columns">
      <div class="column is-8 is-offset-2">
        <h4 class="title">Deploy {{ name }}</h4>

        <div class="field">
          <label class="label">Assign to</label>
          <multiselect v-model="users" :options="userOptions" :multiple="true" placeholder="Select users" label="fullname" track-by="fullname">
            <template slot="tag" slot-scope="props">
              <span class="tag is-primary">
                {{ props.option.fullname }}
                <button class="delete is-small" @keydown.enter.prevent="props.remove(option)"  @mousedown.prevent="props.remove(props.option)"></button>
              </span>
            </template>
            <template slot="option" slot-scope="props">
              <div class="option__desc">
                <span class="option__title">{{ props.option.fullname }}</span>&nbsp;
                <span class="option__small">({{ props.option.email }})</span>
              </div>
            </template>
          </multiselect>
        </div>

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

        <div class="field" v-if="cloudProvider === 'Openstack'">
          <div class="field">
            <label for="openstackAuthURL" class="label">Auth URL</label>
            <p class="control">
              <input class="input" v-model="openstackAuthURL" id="openstackAuthURL" name="openstackAuthURL" type="url" placeholder="Openstack authenication URL">
            </p>
          </div>
          <div class="field">
            <label class="label">Credentials</label>
            <div class="field is-horizontal">
              <div class="field-body">
                <div class="field">
                  <p class="control">
                    <input class="input" v-model="openstackUser" id="openstackUser" name="openstackUser" placeholder="Openstack username">
                  </p>
                </div>
                <div class="field">
                  <p class="control">
                    <input class="input" v-model="openstackPassword" type="password" id="openstackPassword" name="openstackPassword" placeholder="Openstack password">
                  </p>
                </div>
              </div>
            </div>
          </div>
          <div class="field">
            <label for="openstackProject" class="label">Project</label>
            <p class="control">
              <input class="input" v-model="openstackProject" id="openstackProject" name="openstackProject" placeholder="Openstack project">
            </p>
          </div>
        </div>

        <div class="field" v-else-if="cloudProvider === 'AWS'">
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

        <div class="field">
          <p class="control">
            <button v-if="state !== null" type="submit" class="button is-primary is-loading"></button>
            <button v-else type="submit" v-on:click="onDeployBtn" class="button is-primary">{{buttonTitle}}</button>
          </p>
          <p v-if="error" class="help is-danger">{{error}}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style scoped>
  .multiselect__tags .tag {
    margin-right: 8px;
  }
</style>

<script>
  import Multiselect from 'vue-multiselect'
  import { POSTcloudconfig, DEPLOYlab, LISTusers } from '@/api'

  const State = Object.freeze({
    UPLOADING: 'Uploading cloud config',
    DEPLOYING: 'Deploying'
  })
  export default {
    name: 'LabDeployment',
    props: [ 'name' ],
    components: { Multiselect },
    data: function () {
      return {
        lab: null,
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
        userOptions: []
      }
    },
    computed: {
      buttonTitle: function () {
        if (this.state === null) {
          return 'DEPLOY'
        }
      }
    },
    created: function () {
      LISTusers(json => {
        this.userOptions = json
      })
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
      }
    }
  }
</script>
