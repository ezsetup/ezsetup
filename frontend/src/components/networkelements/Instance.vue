<template>
  <svg :x="el.x - 50" :y="el.y - 50">
    <defs>
      <filter :id="`instanceSofGlow${ el.gid }`" height="300%" width="300%" x="-75%" y="-75%">
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
    <text x="50" y="90" text-anchor="middle" font-size="14">{{ el.name }}</text>
    <svg x="0" y="0" width="100" height="100" viewBox="-25 -25 150 150"
         style="clip-rule:evenodd;fill-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:1.41420996"
         @mouseover="onMouseOver" @mouseout="onMouseOut" @click="onClick" :filter="filter">
      <g transform="matrix(0.19794611,0,0,0.19794611,0,16.29555)" >
        <path :style="generalStyle" d="M 72.651,0 C 48.798,0 37.044,20.739 29.439,43.348 L 6.212,111.949 C 1.857,124.948 0,136.677 0,150.436 l 0,138.282 c 0,23.854 19.425,43.213 43.349,43.213 l 418.491,0 c 23.854,0 43.348,-19.359 43.348,-43.213 l 0,-138.282 c 0,-13.759 -1.991,-25.488 -6.346,-38.487 L 475.749,43.348 C 468.144,20.739 456.325,0 432.402,0 L 72.651,0 Z m -24.847,140.173 409.445,0 c 8.02,0 14.449,6.498 14.449,14.45 l 0,129.504 c 0,7.951 -6.429,14.449 -14.449,14.449 l -242.669,0 0,-79.134 -21.876,0 0,79.134 -19.312,0 0,-79.134 -22.01,0 0,79.134 -19.177,0 0,-79.134 -22.012,0 0,79.134 -19.04,0 0,-79.134 -22.012,0 0,79.134 -21.337,0 c -7.95,0 -14.449,-6.498 -14.449,-14.449 l 0,-129.505 c 0,-7.951 6.499,-14.449 14.449,-14.449 z m 378.791,51.181 c -15.419,0 -27.953,12.601 -27.953,28.088 0,15.488 12.534,27.954 27.953,27.954 15.418,0 28.088,-12.535 28.088,-27.954 0,-15.418 -12.67,-28.088 -28.088,-28.088 z" />
      </g>
      <g transform="matrix(0.21198049,0,0,0.22828729,-2.8089939,9.3081896)" >
        <path d="M 454,163.878 C 454,157.322 448.268,152 441.209,152 L 57.791,152 C 50.732,152 45,157.322 45,163.878 l 0,113.244 C 45,283.678 50.732,289 57.791,289 l 383.418,0 C 448.268,289 454,283.678 454,277.122 l 0,-113.244 z" style="fill:#ebebeb" />
      </g>
      <g transform="matrix(0.19794611,0,0,0.19794611,-3.9589222,15.50376)" >
        <circle :style="lightStyle" cx="430" cy="223" r="29" />
      </g>
      <g transform="matrix(0.19794611,0,0,0.19794611,0,16.29555)" >
        <rect :style="generalStyle" x="69" y="220" width="22" height="78" />
      </g>
      <g transform="matrix(0.19794611,0,0,0.19794611,8.1157906,16.29555)" >
        <rect :style="generalStyle" x="69" y="220" width="22" height="78" />
      </g>
      <g transform="matrix(0.19794611,0,0,0.19794611,16.429527,16.29555)" >
        <rect :style="generalStyle" x="69" y="220" width="22" height="78" />
      </g>
      <g transform="matrix(0.19794611,0,0,0.19794611,24.545318,16.29555)" >
        <rect :style="generalStyle" x="69" y="220" width="22" height="78" />
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
        if (this.el.status === 'active') {
          return "fill:rgb(4,255,0);"
        } else if (this.el.status === 'inactive') {
          return "fill:rgb(115,115,115);"
        } else {
          return null
        }
      },
      generalStyle: function () {
        if (this.el.status === 'inactive') {
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
