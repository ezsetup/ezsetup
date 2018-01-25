<template>
    <line :x1="tempLink.x1" :y1="tempLink.y1" :x2="tempLink.x2" :y2="tempLink.y2" stroke-width="5" stroke="black" />
</template>

<script>
  export default {
    name: 'TempLink',
    props: ['tempLink']
  }
</script>
