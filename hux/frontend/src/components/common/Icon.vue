<template>
  <svg-as-component
    :src="`assets/icons/${type}`"
    :width="enableCustomSize ? customSize.width : size"
    :height="enableCustomSize ? customSize.height : size"
    :color="color"
    :variant="variant"
    :fill-opacity="fillOpacity"
    :stroke="stroke"
    :stroke-opacity="strokeOpacity"
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
      type: [Number, String],
      required: false,
      default: 60,
    },

    enableCustomSize: {
      type: Boolean,
      required: false,
      default: false,
    },

    customSize: {
      type: Object,
      required: false,
      default() {
        return {
          width: 0,
          height: 0,
        }
      },
    },

    color: {
      type: String,
      required: false,
    },

    variant: {
      type: String,
      required: false,
    },

    stroke: {
      type: String,
      required: false,
    },

    fillOpacity: {
      type: Number,
      required: false,
      default: 1,
    },

    strokeOpacity: {
      type: Number,
      required: false,
      default: 1,
    },
  },
}
</script>
