<template>
  <div ref="incomeChart" class="container">
    <span v-if="incomes.length != 0">
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
    </span>
    <span v-else>
      <img
        src="@/assets/images/Chart.png"
        alt="Hux"
        width="180"
        height="150"
        class="d-flex ma-6"
      />
      <div class="d-flex ma-6 global-text-line">
        <span class="append-circle"></span> no data available
      </div>
    </span>
  </div>
</template>

<script>
import BarChartTooltip from "@/components/common/incomeChart/BarChartTooltip"
import HorizontalBarChart from "@/components/common/incomeChart/HorizontalBarChart"

export default {
  name: "IncomeChart",
  components: { HorizontalBarChart, BarChartTooltip },
  props: {
    data: {
      type: Array,
      required: true,
    },
  },
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
      incomes: this.data,
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
  height: 350px;
  padding: 0px !important;
}
.append-circle {
  height: 12px;
  width: 12px;
  background-color: rgba(208, 208, 206, 1);
  border-radius: 50%;
  display: inline-block;
  margin-top: 4px;
  margin-right: 8px;
}
</style>
