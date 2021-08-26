<template>
  <div ref="incomeChart" class="container">
    <horizontal-bar-chart
      v-model="incomes"
      :chart-dimensions="chartDimensions"
      @cordinates="getCordinates"
      @tooltipDisplay="toolTipDisplay"
    />
    <bar-chart-tooltip
      :position="{
        x: tooltip.x,
        y: tooltip.y,
      }"
      :show-tooltip="show"
      :source-input="currentData"
    >
    </bar-chart-tooltip>
  </div>
</template>

<script>
import BarChartTooltip from "@/components/common/incomeChart/BarChartTooltip"
import HorizontalBarChart from "@/components/common/incomeChart/HorizontalBarChart"
//TODO: API Integration
import data from "./incomeData.json"

export default {
  name: "IncomeChart",
  components: { HorizontalBarChart, BarChartTooltip },
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
      incomes: data.income,
      currentData: {},
    }
  },
  created() {
    window.addEventListener("resize", this.sizeHandler)
  },
  destroyed() {
    window.removeEventListener("resize", this.sizeHandler)
  },
  mounted() {
    this.sizeHandler()
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
    sizeHandler() {
      if (this.$refs.incomeChart) {
        this.chartDimensions.width = this.$refs.incomeChart.clientWidth
        this.chartDimensions.height = 220
      }
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
  height: 450px;
  padding: 0px !important;
}
</style>
