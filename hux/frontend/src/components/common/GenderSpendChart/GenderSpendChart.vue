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
    <line-area-chart-tooltip
      :position="{
        x: tooltip.x,
        y: tooltip.y,
      }"
      :show-tooltip="show"
      :source-input="currentData"
    >
    </line-area-chart-tooltip>
  </div>
</template>

<script>
import LineAreaChartTooltip from "@/components/common/GenderSpendChart/LineAreaChartTooltip"
import LineAreaChart from "@/components/common/GenderSpendChart/LineAreaChart"
//TODO: API Integration
import data from "./genderSpendChart.json"

export default {
  name: "GenderSpendChart",
  components: { LineAreaChart, LineAreaChartTooltip },
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
