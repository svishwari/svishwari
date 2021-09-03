<template>
  <div ref="customerEventChart" class="container-chart">
    <line-chart
      v-model="sourceData"
      :chart-dimensions="chartDimensions"
      @tooltipDisplay="toolTipDisplay"
    />
    <line-chart-tooltip
      :show-tool-tip="show"
      :color-codes="colorCodes"
      :source-input="currentData"
    />
  </div>
</template>

<script>
import LineChartTooltip from "@/components/common/CustomerEventChart/LineChartTooltip"
import LineChart from "@/components/common/Charts/LineChart/LineChart.vue"
export default {
  name: "CustomerEventChart",
  components: { LineChart, LineChartTooltip },
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
      if (this.$refs.customerEventChart) {
        this.chartDimensions.width = this.$refs.customerEventChart.clientWidth
        this.chartDimensions.height = 350
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
