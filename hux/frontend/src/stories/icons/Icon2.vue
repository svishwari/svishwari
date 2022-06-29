<template>
  <svg-as-component
    :src="`assets/newIcons/${type}`"
    :width="size"
    :height="size"
    :color="color"
    :fill-opacity="fillOpacity"
    :stroke="stroke"
    :stroke-opacity="strokeOpacity"
    :style="style"
    :bg-color="bgColor"
  />
</template>

<script>
import svgAsComponent from "./SVG.vue"

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

    color: {
      type: String,
      required: false,
      default: "primary-base",
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

    outline: {
      type: Boolean,
      required: false,
      default: false,
    },

    borderColor: {
      type: String,
      required: false,
      default: "primary-base",
    },

    bgColor: {
      type: String,
      required: false,
      default: "white-base",
    },
  },

  computed: {
    style() {
      let style = {}
      if (this.outline) {
        style["border-width"] = parseInt(this.size) < 20 ? "0.5px" : "1px"
        style["border-color"] = `var(--v-${this.borderColor})`
        style["border-style"] = "solid"
        style["border-radius"] = `${parseInt(this.size) / 2}px`
      }
      return style
    },
  },
}
</script>
