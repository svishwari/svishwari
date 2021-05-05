<template>
  <component :is="svg" :style="style" />
</template>

<script>
import EmptyLogo from "./EmptyLogo"
export default {
  name: "logo",

  components: {
    EmptyLogo,
  },

  data() {
    return {
      svg: EmptyLogo,
    }
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

  computed: {
    style() {
      return {
        width: `${this.size}px`,
        height: `${this.size}px`,
      }
    },
  },

  watch: {
    type: function (newValue) {
      import(`../../assets/logos/${newValue}.svg`).then((loadedSVG) => {
        this.svg = loadedSVG
      })
    },
  },

  mounted: function () {
    import(`../../assets/logos/${this.type}.svg`).then((loadedSVG) => {
      this.svg = loadedSVG
    })
  },
}
</script>
