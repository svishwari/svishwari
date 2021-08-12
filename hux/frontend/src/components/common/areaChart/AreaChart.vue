<template>
  <div ref="chartBox" class="container">
    <div class="d-flex justify-content-start">
      <line-area-chart
        v-model="spendData"
        :chart-dimensions="chartDimensions"
        @cordinates="getCordinates"
        @tooltipDisplay="toolTipDisplay"
      />
    </div>
    <area-chart-tooltip
      :position="{
        x: tooltip.x,
        y: tooltip.y,
      }"
      :show-tooltip="show"
      :source-input="currentData"
    >
    </area-chart-tooltip>
  </div>
</template>

<script>
import AreaChartTooltip from "@/components/common/AreaChart/AreaChartTooltip"
import LineAreaChart from "@/components/common/AreaChart/LineAreaChart"
//TODO: API Integration
import data from "./areaChart.json"

export default {
  name: "AreaChart",
  components: { LineAreaChart, AreaChartTooltip },
  data() {
    return {
      show: false,
      tooltip: {
        x: 0,
        y: 0,
      },
      chartDimensions: {
        width: 0,
        height: 0,
      },
      spendData: data.spend,
      currentData: {},
    }
  },
  mounted() {
    this.chartDimensions.width = this.$refs.chartBox.clientWidth
    this.chartDimensions.height = this.$refs.chartBox.clientHeight
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
  height: 350px;
  padding: 0px !important;
}
</style>
