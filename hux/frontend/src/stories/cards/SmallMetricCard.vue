<template>
  <v-card class="pa-4 card-style" width="192">
    <div class="mb-2 card-header">
      <icon v-if="icon" :type="icon" size="14" class="ma-1" />
      <h4>{{ title }}</h4>
      <icon type="info" size="14" class="ml-3 mt-1" color="primary" />
      <slot name="call-to-action"></slot>
    </div>
    <slot name="body"><div>-</div></slot>
  </v-card>
</template>

<script>
import icon from "../icons/Icon2.vue"

export default {
  name: "SmallMetricCard",
  components: { icon },
  props: {
    icon: {
      type: String,
      required: false,
    },
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
}
</script>

<style lang="scss" scoped>
.card-style {
  border-radius: 12px;
}
.card-header {
  display: flex;
  height: 24px;
}
</style>
