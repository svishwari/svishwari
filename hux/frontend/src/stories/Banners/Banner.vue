<template>
  <v-alert
    :type="type"
    text
    dismissible
    :outlined="outlined"
    :height="getHeight"
    :width="getWidth"
    class="pl-8 pr-8 banner-padding"
  >
    <template #prepend>
      <icon :type="getIcon" :size="24" :color="type" class="mr-2" />
    </template>
    <template #close="{ toggle }">
      <icon type="cross" :size="8" color="black" class="mr-2" @click="toggle" />
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
    getIcon() {
      let iconToRet = ""
      switch (this.type) {
        case "warning":
          iconToRet = "exclamation_outline"
          break
        case "success":
          iconToRet = "success"
          break
        case "error":
          iconToRet = "sad-face"
          break
        default:
          iconToRet = "success"
          break
      }
      return iconToRet
    },
  },
}
</script>

<style lang="scss" scoped>
.banner-padding {
  display: flex;
  align-items: center;
}
.banner-label {
  color: var(--v-black-base);
  font-weight: bold;
}
</style>
