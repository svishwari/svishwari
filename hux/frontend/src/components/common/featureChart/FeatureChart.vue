<template>
  <div class="container">
    <div class="d-flex justify-content-start">
      <horizontal-bar-chart
        v-model="features"
        @cordinates="getCordinates"
        @tooltipDisplay="toolTipDisplay"
      />
    </div>
    <bar-chart-tooltip
      :position="{
        x: tooltip.x,
        y: tooltip.y,
      }"
      :showTooltip="show"
      :sourceInput="currentData"
    >
    </bar-chart-tooltip>
  </div>
</template>

<script>
import BarChartTooltip from "@/components/common/featureChart/BarChartTooltip"
import HorizontalBarChart from "@/components/common/featureChart/HorizontalBarChart"
import data from "./featureData.json"
export default {
  name: "feature-chart",
  components: { HorizontalBarChart, BarChartTooltip },
  data() {
    return {
      show: false,
      isArcHover: false,
      tooltip: {
        x: 0,
        y: 0,
      },
      features: data.featureList,
      currentData: {},
    }
  },
  methods: {
    toolTipDisplay(...arg) {
      this.show = arg[0]
      if (this.show) {
        this.currentData = arg[1]
      }
    },

    getCordinates(args) {
      this.tooltip.x = args.x
      this.tooltip.y = args.y
    },
  },
}
</script>

<style lang="scss" scoped>
.global-text-line {
  display: inline-block;
  font-style: normal;
  font-size: $font-size-root;
  line-height: 19px;
}
.container {
  height: 650px;
  padding: 0px !important;
}
</style>
