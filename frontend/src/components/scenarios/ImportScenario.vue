<template>
  <div v-if="!Boolean(loadedScenario)" class="center">
      <div class="field">
        <label for="inputFile" class="label">Scenario file</label>
        <p class="control">
          <input class="input" type="file" id="inputFile" accept=".json" name="inputFile" placeholder="EZSetup scenario file" ref="inputFile">
        </p>
      </div>
      <button type="submit" @click="onImportBtn" class="button is-primary">IMPORT</button>
      <p>{{loadFileError}}</p>
  </div>
  <ScenarioEditor v-else :propContent="loadedScenario">
  </ScenarioEditor>
</template>

<script>
  import ScenarioEditor from '@/components/scenarios/ScenarioEditor'

  export default {
    name: 'ImportScenario',
    components: {
      ScenarioEditor,
    },
    data: function () {
      return {
        loadFileError: null,
        loadedScenario: null
      }
    },
    methods: {
      onImportBtn: function() {
        let file = null
        if (file = this.$refs.inputFile.files[0]) {
          this.loadFileError = null
          let filereader = new FileReader()
          filereader.onload = e => {
            let raw = e.target.result
            this.loadedScenario = JSON.parse(raw)
          }
          filereader.readAsText(file)
        } else {
          this.loadFileError = "Please select a file from your machine"
        }
      }
    }
  }
</script>
