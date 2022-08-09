<template>
  <v-menu
    :top="positionTop"
    offset-y
    open-on-hover
    :content-class="`tooltipContentClass ${contentClass}`"
    :max-width="maxWidth"
    :min-width="minWidth"
    :nudge-right="nudgeRight"
    :nudge-top="nudgeTop"
    :z-index="zIndex"
  >
    <template #activator="{ on }">
      <span class="new-b3" v-on="on">
        <slot name="label-content"></slot>
        <slot name="default"></slot>
      </span>
    </template>
    <div class="px-4 py-2 tooltip-hover new-b3" :style="style">
      <slot name="hover-content"></slot>
      <slot name="tooltip"></slot>
    </div>
  </v-menu>
</template>

<script>
export default {
  name: "Tooltip",
  props: {
    positionTop: {
      type: Boolean,
      required: false,
      default: false,
    },
    contentClass: {
      type: String,
      required: false,
      default: "",
    },
    maxWidth: {
      type: [String, Number],
      required: false,
      default: "auto",
    },
    minWidth: {
      type: [String, Number],
      required: false,
      default: "auto",
    },
    nudgeRight: {
      type: [String, Number],
      required: false,
      default: 0,
    },
    nudgeTop: {
      type: [String, Number],
      required: false,
      default: 0,
    },
    zIndex: {
      type: [String, Number],
      required: false,
      default: undefined,
    },
    color: {
      type: String,
      required: false,
      default: "white-base",
    },
    backgroundColor: {
      type: String,
      required: false,
      default: "primary-base",
    },
  },
  computed: {
    style() {
      let style = {}
      if (this.color) style.color = `var(--v-${this.color})`
      if (this.backgroundColor)
        style.background = `var(--v-${this.backgroundColor})`
      return style
    },
  },
}
</script>
<style lang="scss" scoped>
.tooltip-hover {
  border-radius: 8px !important;
}
.tooltipContentClass {
  @extend .box-shadow-15-8;
  border-radius: 8px;
}
</style>
