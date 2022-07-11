<template>
  <v-alert
    :color="'var(--v-' + iconColor + ')'"
    text
    dismissible
    :outlined="outlined"
    :height="getHeight"
    :width="getWidth"
    class="banner-container px-8"
    :class="size == 'small' ? 'py-2' : 'py-6'"
  >
    <template #prepend>
      <icon
        :type="type"
        :size="24"
        :color="
          type == 'Checkmark' || type == 'Error'
            ? 'white-base'
            : 'black-lighten6'
        "
        :bg-color="iconColor"
        :border-color="iconColor"
        outline
        class="mr-2"
      />
    </template>
    <template #close>
      <icon type="Close & Remove" :size="16" color="black" @click="toggle" />
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
      default: "Guide",
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

    iconColor() {
      switch (this.type) {
        case "Checkmark":
          return "success-darken1"

        case "Error":
          return "error-lighten1"

        case "Error & Warning":
          return "warning-lighten1"

        case "Guide":
          return "yellow-lighten3"

        default:
          // informative
          return "yellow-lighten3"
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
  line-height: 20px;
}
</style>
