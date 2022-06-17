<template>
  <v-card class="pa-6" :width="getWidth">
    <div class="mb-4">
      <div class="card-header" :class="$slots.filters ? 'mb-2' : ''">
        <h4>{{ title }}</h4>
        <slot name="call-to-action"></slot>
      </div>
      <slot name="filters" class="filters-bar"></slot>
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
.filters-bar {
  padding-left: -24px;
  padding-right: -24px;
}
</style>
