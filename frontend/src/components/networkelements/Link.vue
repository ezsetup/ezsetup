/*
 * A Link is just a line that connects:
 *  - network: always a network node
 *  - target: a instance node or a router node
 */
<template>
  <svg>
    <defs>
      <filter :id="`linkSofGlow${el.gid}`" height="300%" width="300%" x="-75%" y="-75%">
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
    <line :filter="filter" @mouseover="onMouseOver" @mouseout="onMouseOut" @click="onClick"
          :x1="el.network.x" :y1="el.network.y" :x2="el.target.x" :y2="el.target.y" stroke-width="3" stroke="#555555" />
  </svg>
</template>

<script>
  export default {
    name: 'link-element',
    props: ['el'],
    data: function () {
      return {
        filter: null
      }
    },
    methods: {
      onMouseOver: function () {
        this.filter = `url(#linkSofGlow${this.el.gid})`
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
