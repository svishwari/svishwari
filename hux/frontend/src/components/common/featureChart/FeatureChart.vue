<template>
  <div ref="chartBox" class="container">
    <horizontal-bar-chart
      v-model="features"
      @cordinates="getCordinates"
      @tooltipDisplay="toolTipDisplay"
      :chartDimensions="chartDimensions"
    />
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
export default {
  name: "feature-chart",
  components: { HorizontalBarChart, BarChartTooltip },
  props: {
    featureData: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      show: false,
      isArcHover: false,
      tooltip: {
        x: 0,
        y: 0,
      },
      features: this.featureData,
      currentData: {},
      chartDimensions: {
        width: 0,
        height: 0,
      },
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
  mounted() {
    this.chartDimensions.width = this.$refs.chartBox.clientWidth
    this.chartDimensions.height = this.$refs.chartBox
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
