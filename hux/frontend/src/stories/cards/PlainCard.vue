<template>
  <v-card class="pa-6 pt-5" :width="getWidth">
    <div class="mb-4 card-header">
      <h4>{{ title }}</h4>
      <slot name="call-to-action"></slot>
    </div>
    <slot name="body"></slot>
  </v-card>
</template>

<script>
export default {
  name: "PlainCard",
  props: {
    title: {
      type: String,
      required: true,
    },
    size: {
      type: String,
      required: false,
      default: "small",
    },
  },

  computed: {
    getWidth() {
      return this.size == "small" ? 368 : this.size == "medium" ? 564 : 1152
    },
  },
}
</script>

<style lang="scss" scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  height: 24px;
}
</style>
