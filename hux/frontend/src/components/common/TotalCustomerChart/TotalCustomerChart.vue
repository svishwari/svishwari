<template>
  <div ref="totalCustomerChart" class="container-chart">
    <stack-bar-chart
      v-model="sourceData"
      :color-codes="colorCodes"
      :chart-dimensions="chartDimensions"
      @tooltipDisplay="toolTipDisplay"
    />
    <stack-bar-chart-tooltip
      :show-tool-tip="show"
      :color-codes="colorCodes"
      :source-input="currentData"
    />
  </div>
</template>

<script>
import StackBarChartTooltip from "@/components/common/TotalCustomerChart/StackBarChartTooltip"
import StackBarChart from "@/components/common/Charts/StackBarChart/StackBarChart.vue"
export default {
  name: "TotalCustomerChart",
  components: { StackBarChart, StackBarChartTooltip },
  props: {
    customersData: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      show: false,
      isArcHover: false,
      colorCodes: ["columbiaBlue", "info", "pantoneBlue", "success"],
      sourceData: this.customersData,
      currentData: {},
      chartDimensions: {
        width: 0,
        height: 0,
      },
    }
  },
  mounted() {
    this.sizeHandler()
  },
  created() {
    window.addEventListener("resize", this.sizeHandler)
  },
  destroyed() {
    window.removeEventListener("resize", this.sizeHandler)
  },
  methods: {
    toolTipDisplay(...arg) {
      this.show = arg[0]
      if (this.show) {
        this.currentData = arg[1]
      }
    },
    sizeHandler() {
      if (this.$refs.totalCustomerChart) {
        this.chartDimensions.width = this.$refs.totalCustomerChart.clientWidth
        this.chartDimensions.height = 500
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
.container-chart {
  position: relative;
  height: 650px;
  padding: 0px !important;
}
</style>
