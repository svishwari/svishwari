<template>
  <div
    class="chart-tooltip"
    :style="{ top: coordinates[0], left: coordinates[1] }"
  >
    <slot name="default" />
  </div>
</template>

<script>
export default {
  name: "ChartTooltip",
  props: {
    coordinates: {
      type: Array,
      required: false,
      default: () => {
        return ["0px", "0px"]
      },
    },
  },
}
</script>
<style lang="scss" scoped>
.chart-tooltip {
  padding: 6px 16px;
  position: fixed;
  background: var(--v-white-base);
  @extend .box-shadow-25;
}
</style>
