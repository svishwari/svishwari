<template>
  <div>
    <v-card
      tile
      class="mx-auto chart-tooltip"
      :style="{
        transform: `translate(${position.x}px, ${position.y}px)`,
        padding: tooltipStyle.padding,
        top: tooltipStyle.top,
        left: tooltipStyle.left,
        minWidth: tooltipStyle.minWidth,
        maxWidth: tooltipStyle.maxWidth,
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
          minWidth: '100px',
          maxWidth: '200px',
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

.global-font-style {
  font-style: normal;
  font-size: 12px;
  line-height: 19px;
}

.chart-tooltip {
  @extend .global-font-style;
  @extend .box-shadow-3;
  background: var(--v-white-base);
  pointer-events: none;
  position: fixed;
  height: auto;
}
</style>
