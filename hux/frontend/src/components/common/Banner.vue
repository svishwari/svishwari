<template>
  <v-alert
    :type="type"
    text
    dismissible
    :outlined="outlined"
    :height="Height"
    :width="Width"
    :class="classValue"
    class="pl-8 pr-8"
  >
    <span class="alert-label">{{ label }}</span>
  </v-alert>
</template>

<script>
export default {
  name: "Banner",
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
    outlined: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  computed: {
    Height() {
      return this.size == "large" ? 72 : 40
    },
    Width() {
      return this.size == "large" ? 1216 : 710
    },
    classValue() {
      return this.size == "large" ? "pt-6" : "pb-10"
    },
  },
}
</script>

<style lang="scss" scoped>
.alert-label {
  color: var(--v-black-base);
  font-weight: bold;
}
</style>
