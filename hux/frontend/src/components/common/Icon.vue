<template>
  <svg-as-component
    :src="`assets/icons/${type}`"
    :width="size"
    :height="size"
    :color="theme[color]"
    :fill-opacity="fillOpacity"
  />
</template>

<script>
import svgAsComponent from "./SVG"
import theme from "@/plugins/theme"

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
      default: "primary",
    },

    fillOpacity: {
      type: Number,
      required: false,
      default: 1,
    },
  },

  data: () => ({
    theme: theme,
  }),
}
</script>
