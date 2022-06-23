<template>
  <v-alert
    :color="bgColor"
    text
    dismissible
    :outlined="outlined"
    :height="getHeight"
    :width="getWidth"
    class="banner-container px-8"
    :class="size == 'small' ? 'py-2' : 'py-6'"
  >
    <template #prepend>
      <icon :type="type" :size="24" class="mr-2" />
    </template>
    <template #close>
      <icon
        type="cross"
        :size="10"
        color="black"
        class="mr-2"
        @click="toggle"
      />
    </template>
    <div class="banner-label" :style="cssVars">{{ label }}</div>
  </v-alert>
</template>

<script>
import Icon from "../icons/Icon2.vue"
export default {
  name: "Banner",
  components: { Icon },
  props: {
    label: {
      type: String,
      required: true,
    },
    type: {
      type: String,
      required: false,
      default: "warning",
    },
    size: {
      type: String,
      required: false,
      default: "small",
    },
    height: {
      type: Number,
      required: false,
    },
    width: {
      type: Number,
      required: false,
    },
    outlined: {
      type: Boolean,
      required: false,
      default: false,
    },
  },

  computed: {
    getHeight() {
      return this.height ? this.height : this.size == "large" ? 72 : 40
    },
    getWidth() {
      return this.width ? this.width : this.size == "large" ? 1216 : 710
    },
    cssVars() {
      return { width: this.getWidth - 104 + "px" }
    },
    bgColor() {
      switch (this.type) {
        case "positive":
          return "var(--v-success-darken1)"

        case "negative":
          return "var(--v-error-lighten1)"

        case "warning":
          return "var(--v-warning-lighten1)"

        case "guiding":
          return "var(--v-yellow-lighten3)"

        default:
          // informative
          return "var(--v-yellow-lighten3)"
      }
    },
  },

  methods: {
    closeAlert() {},
  },
}
</script>

<style lang="scss" scoped>
.banner-container {
  display: flex;
  justify-content: center;
}
.banner-label {
  color: var(--v-black-base);
  font-weight: bold;
}
</style>
