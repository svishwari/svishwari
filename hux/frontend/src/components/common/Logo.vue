<template>
  <component :is="svg" :style="style" />
</template>

<script>
export default {
  name: "logo",

  props: {
    type: {
      type: String,
      required: true,
      default: null,
    },

    size: {
      type: Number,
      required: false,
      default: 24,
    },
  },

  computed: {
    svg() {
      return () => import(`../../assets/logos/${this.type}.svg`)
    },

    style() {
      return {
        width: `${this.size}px`,
        height: `${this.size}px`,
      }
    },
  },
}
</script>
