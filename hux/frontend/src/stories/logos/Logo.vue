<template>
  <svg-as-component
    v-if="type"
    :src="`assets/newLogos/${type}`"
    :width="size"
    :height="size"
  />
</template>

<script>
import svgAsComponent from "@/components/common/SVG.vue"

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
