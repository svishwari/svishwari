<template>
  <v-alert
    :type="type"
    text
    dismissible
    :outlined="outlined"
    :height="size == 'large' ? 72 : 40"
    :width="size == 'large' ? 1216 : 710"
    :class="size == 'large' ? 'pt-6' : 'pb-10'"
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
}
</script>

<style lang="scss" scoped>
.alert-label {
  color: black;
  font-weight: bold;
}
</style>
