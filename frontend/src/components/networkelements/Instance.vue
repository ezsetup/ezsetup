<template>
  <svg>
    <defs>
      <filter :id="`instanceSofGlow${el.gid}`" height="300%" width="300%" x="-75%" y="-75%">
        <!-- Thicken out the original shape -->
        <feMorphology operator="dilate" radius="2" in="SourceAlpha" result="thicken" />

        <!-- Use a gaussian blur to create the soft blurriness of the glow -->
        <feGaussianBlur in="thicken" stdDeviation="5" result="blurred" />

        <!-- Change the colour -->
        <feFlood flood-color="rgb(64,224,208)" result="glowColor" />

        <!-- Color in the glows -->
        <feComposite in="glowColor" in2="blurred" operator="in" result="softGlow_colored" />

        <!--	Layer the effects together -->
        <feMerge>
          <feMergeNode in="softGlow_colored" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>

      </filter>
    </defs>
    <text :x="el.x" :y="el.y-30" text-anchor="middle" font-size="14">{{el.name}}</text>
    <svg :filter="filter" @mouseover="onMouseOver" @mouseout="onMouseOut" @click="onClick" height="60" width="60" :x="el.x-30" :y="el.y-30" viewBox="0 0 506 415" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41421;">
      <path d="M72.651,0C48.798,0 37.044,20.739 29.439,43.348L6.212,111.949C1.857,124.948 0,136.677 0,150.436L0,288.718C0,312.572 19.425,331.931 43.349,331.931L461.84,331.931C485.694,331.931 505.188,312.572 505.188,288.718L505.188,150.436C505.188,136.677 503.197,124.948 498.842,111.949L475.749,43.348C468.144,20.739 456.325,0 432.402,0L72.651,0ZM47.804,140.173L457.249,140.173C465.269,140.173 471.698,146.671 471.698,154.623L471.698,284.127C471.698,292.078 465.269,298.576 457.249,298.576L214.58,298.576L214.58,219.442L192.704,219.442L192.704,298.576L173.392,298.576L173.392,219.442L151.382,219.442L151.382,298.576L132.205,298.576L132.205,219.442L110.193,219.442L110.193,298.576L91.153,298.576L91.153,219.442L69.141,219.442L69.141,298.576L47.804,298.576C39.854,298.576 33.355,292.078 33.355,284.127L33.355,154.622C33.355,146.671 39.854,140.173 47.804,140.173ZM426.595,191.354C411.176,191.354 398.642,203.955 398.642,219.442C398.642,234.93 411.176,247.396 426.595,247.396C442.013,247.396 454.683,234.861 454.683,219.442C454.683,204.024 442.013,191.354 426.595,191.354Z" :style="generalStyle" />
      <g transform="matrix(1.0709,0,0,1.15328,-14.1907,-34.2993)">
        <path d="M454,163.878C454,157.322 448.268,152 441.209,152L57.791,152C50.732,152 45,157.322 45,163.878L45,277.122C45,283.678 50.732,289 57.791,289L441.209,289C448.268,289 454,283.678 454,277.122L454,163.878Z" style="fill:rgb(235,235,235);" />
      </g>
      <g transform="matrix(1,0,0,1,-20,-3)">
        <circle cx="430" cy="223" r="29" :style="lightStyle" />
      </g>
      <g transform="matrix(1,0,0,1,0,1)">
        <rect x="69" y="220" width="22" height="78" :style="generalStyle" />
      </g>
      <g transform="matrix(1,0,0,1,41,1)">
        <rect x="69" y="220" width="22" height="78" :style="generalStyle" />
      </g>
      <g transform="matrix(1,0,0,1,83,1)">
        <rect x="69" y="220" width="22" height="78" :style="generalStyle" />
      </g>
      <g transform="matrix(1,0,0,1,124,1)">
        <rect x="69" y="220" width="22" height="78" :style="generalStyle" />
      </g>
    </svg>
  </svg>
</template>

<script>
  export default {
    name: 'instance-element',
    props: ['el'],
    data: function () {
      return {
        filter: null
      }
    },
    computed: {
      lightStyle: function () {
        if (this.el.status == 'active') {
          return "fill:rgb(4,255,0);"
        } else if (this.el.status == 'inactive') {
          return "fill:rgb(115,115,115);"
        } else {
          return null
        }
      },
      generalStyle: function () {
        if (this.el.status == 'inactive') {
          return "fill:rgb(115,115,115);"
        } else {
          return null
        }
      }
    },
    methods: {
      onMouseOver: function () {
        this.filter = `url(#instanceSofGlow${this.el.gid})`
      },
      onMouseOut: function () {
        this.filter = null
      },
      onClick: function () {
        this.$emit('click', this.el)
      }
    }
  }
</script>

<style scoped>
</style>
