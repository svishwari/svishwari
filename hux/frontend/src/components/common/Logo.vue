<template>
  <svg-as-component
    v-if="type"
    :src="`assets/logos/${type}`"
    :width="size"
    :height="size"
  />
</template>

<script>
import svgAsComponent from "./SVG"

export default {
  name: "Logo",

  components: {
    svgAsComponent,
  },

  props: {
    type: {
      type: String,
      required: false,
    },

    size: {
      type: Number,
      required: false,
      default: 24,
    },
  },
}
</script>
