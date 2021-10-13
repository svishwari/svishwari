<template>
  <svg-as-component
    :src="`assets/icons/${type}`"
    :width="size"
    :height="size"
    :color="color"
    :variant="variant"
    :fill-opacity="fillOpacity"
  />
</template>

<script>
import svgAsComponent from "./SVG"

export default {
  name: "Icon",

  components: {
    svgAsComponent,
  },

  props: {
    type: {
      type: String,
      required: true,
    },

    size: {
      type: Number,
      required: false,
      default: 60,
    },

    color: {
      type: String,
      required: false,
    },

    variant: {
      type: String,
      required: false,
    },

    fillOpacity: {
      type: Number,
      required: false,
      default: 1,
    },
  },
}
</script>
