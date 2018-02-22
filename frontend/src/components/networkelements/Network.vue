<template>
  <svg :x="el.x - 75" :y="el.y - 50">
    <defs>
      <filter :id="`networkSofGlow${ el.gid }`" height="300%" width="300%" x="-75%" y="-75%">
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
    <text :x="75" :y="15" text-anchor="middle" font-size="14">{{ el.name }}</text>
    <svg :filter="filter" @click="onClick" @mouseout="onMouseOut" @mouseover="onMouseOver" x="0" y="-25" height="150" width="150" viewBox="-25 -25 150 150">
      <g transform="matrix(0.958333,0,0,0.927273,-1.91667,-19.4727)">
          <path d="m 81.269208,99.136136 -54.372628,0 c -12.627886,0 -22.150428,-7.547511 -22.150428,-17.555573 0,-9.490687 4.8903402,-14.718253 13.770283,-14.718253 0.31416,0 0.630516,0.0022 0.950168,0.0066 0.708506,-5.650473 4.338913,-11.004363 12.81023,-11.004363 1.027059,0 1.900334,0.197723 2.601151,0.429497 2.495699,-5.189121 7.752925,-10.535321 18.81331,-10.535321 7.652964,0 13.773578,2.845009 17.827991,8.253822 1.81795,-0.94138 3.790783,-1.432391 5.804258,-1.432391 6.150273,0 11.469012,4.45535 13.367149,11.008757 3.462343,0.639304 6.662155,2.522063 8.949142,5.307755 2.232066,2.719784 4.698106,7.576072 3.765516,15.272975 -1.11713,9.231451 -9.598329,14.966505 -22.136142,14.966505 z" style="fill:#777777;stroke:#000000;stroke-width:5px" />
      </g>
    </svg>
    <text :x="75" :y="90" text-anchor="middle" font-size="14">{{ el.cidr }}</text>
  </svg>
</template>

<script>
  export default {
    name: 'network-element',
    props: ['el'],
    data: function () {
      return {
        filter: null
      }
    },
    methods: {
      onMouseOver: function () {
        this.filter = `url(#networkSofGlow${this.el.gid})`
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
