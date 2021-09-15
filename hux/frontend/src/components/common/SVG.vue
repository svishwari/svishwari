<template>
  <component :is="svg" :style="style" />
</template>

<script>
export default {
  name: "SvgAsComponent",

  props: {
    src: {
      type: String,
      required: true,
    },

    width: {
      type: Number,
      required: false,
    },

    height: {
      type: Number,
      required: false,
    },

    color: {
      type: String,
      required: false,
    },

    fillOpacity: {
      type: Number,
      required: false,
      default: 1,
    },
  },

  data() {
    return {
      svg: null,
    }
  },

  computed: {
    style() {
      let style = {}

      if (this.width) style.width = `${this.width}px`
      if (this.height) style.height = `${this.height}px`
      if (this.color) style.fill = `var(--v-${this.color}-base)`
      if (this.fillOpacity) style.fillOpacity = `${this.fillOpacity}`

      return style
    },
  },

  watch: {
    src: function (newSrc) {
      import(`../../${newSrc}.svg`).then((svg) => (this.svg = svg))
    },
  },

  /**
   * We are using a loader to leverage SVG files as Vue components.
   * This component helps dynamically import SVGs as components given src.
   * This can be used in other components as:
   *
   * <svg-as-component
   *   src="path/to/file"
   *   width="100"
   *   height="60"
   * />
   *
   * Read more on the loader here: https://vue-svg-loader.js.org
   */
  mounted() {
    import(`../../${this.src}.svg`).then((svg) => (this.svg = svg))
  },
}
</script>
