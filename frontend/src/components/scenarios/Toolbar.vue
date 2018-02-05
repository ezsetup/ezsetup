<template>
  <div class="field has-addons">
    <p class="control" v-for="tool in tools.filter(t => typeof(t.hidden) === 'undefined' || !t.hidden)">
      <button @click="click(tool)" :class="getCssClasses(tool)"
              :disabled="typeof(tool.disabled) !== 'undefined' && tool.disabled">
        <span class="icon is-small">
          <i :class="'fa fa-' + tool.icon"></i>
        </span>
        <span v-if="typeof(tool.title) !== 'undefined' && tool.title">{{ tool.title }}</span>
      </button>
    </p>
  </div>
</template>

<script>
  export default {
    name: 'ToolBox',
    props: ['initialTool', 'tools', 'toggle'],
    data() {
      return {
        selection: this.initialTool
      };
    },
    methods: {
      click(tool) {
        if (!this.toggle || tool !== this.selection) {
          this.$emit('toolClick', tool.name);
          this.selection = tool.name;
        }
      },
      getCssClasses(tool) {
        return 'button' + (this.toggle && tool.name === this.selection ? ' is-primary' : '') +
          (tool.theme ? ' ' + tool.theme : '');
      }
    }
  }
</script>
