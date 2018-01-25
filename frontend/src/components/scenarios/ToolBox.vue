<template>
  <div>
    <h5 class="title is-5 has-text-centered">Tools</h5>
    <div>
      <button v-on:click="onToolClick('select')" :class="getCSSClasses('select')">Select</button>
    </div>
    <div>
      <button v-on:click="onToolClick('instance')" :class="getCSSClasses('instance')">Instance</button>
    </div>
    <div>
			<button v-on:click="onToolClick('router')" :class="getCSSClasses('router')">Router</button>
    </div>
    <div>
      <button v-on:click="onToolClick('network')" :class="getCSSClasses('network')">Network</button>
    </div>
    <div>
      <button v-on:click="onToolClick('link')" :class="getCSSClasses('link')">Link</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ToolBox',
  props: ['currentTool'],
  methods: {
    onToolClick: function(tool) {
      let newCurrentTool = null
      if (this.currentTool !== tool) {
        newCurrentTool = tool
      }
      this.$emit("currentToolChange", newCurrentTool)
    },
    getCSSClasses: function(name) {
      if (name === this.currentTool) {
        return "button is-small is-fullwidth is-focused"
      } else {
        return "button is-small is-fullwidth"
      }
    }
  }
}
</script>

<style scoped>
</style>
