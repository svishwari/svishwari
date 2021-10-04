<template>
  <div>
    <v-card
      class="mx-auto chart-tooltip"
      tile
      :max-width="tooltipStyle.maxWidth"
      :min-width="tooltipStyle.minWidth"
      :style="{
        transform: `translate(${position.x}px, ${position.y}px)`,
        top: tooltipStyle.top,
        left: tooltipStyle.left,
        padding: tooltipStyle.padding,
      }"
    >
      <slot name="content" />
    </v-card>
  </div>
</template>

<script>
export default {
  name: "ChartTooltip",
  props: {
    // for Co-ordinates positioning
    position: {
      type: Object,
      required: false,
      default() {
        return {
          x: 0,
          y: 0,
        }
      },
    },
    // for Dynamic styling properties
    tooltipStyle: {
      type: Object,
      required: false,
      default() {
        return {
          padding: 0,
          top: 0,
          left: 0,
          minWidth: "auto",
          maxWidth: "auto",
        }
      },
    },
  },
}
</script>

<style lang="scss" scoped>
::v-deep .v-card {
  border-radius: 0px !important;
}

.chart-tooltip {
  @extend .box-shadow-3;
  pointer-events: none;
  position: absolute;
  height: auto;
  z-index: 999999;
}
</style>
