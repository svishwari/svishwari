<template>
  <svg-as-component
    :src="`assets/logos/${type}`"
    :width="size"
    :height="size"
    v-if="type"
  />
</template>

<script>
import svgAsComponent from "./SVG"

export default {
  name: "logo",

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
