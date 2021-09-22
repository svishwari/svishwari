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
      <div class="d-flex ml-6 mt-8 global-text-line">
        <chart-legends :legends-data="legendsData" />
      </div>
    </span>
  </div>
</template>

<script>
import BarChartTooltip from "@/components/common/incomeChart/BarChartTooltip"
import HorizontalBarChart from "@/components/common/incomeChart/HorizontalBarChart"
import ChartLegends from "@/components/common/Charts/Legends/ChartLegends.vue"

export default {
  name: "IncomeChart",
  components: { HorizontalBarChart, BarChartTooltip, ChartLegends },
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
      legendsData: [
        { color: "rgba(208, 208, 206, 1)", text: "no data available" },
      ],
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
</style>
