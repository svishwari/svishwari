<template>
  <div ref="customerEventChart" class="container-chart">
    <multi-line-chart
      v-model="sourceData"
      :chart-dimensions="chartDimensions"
      :data-keys="modificationData"
      :color-codes="colorCodes"
      @cordinates="getCordinates"
      @tooltipDisplay="toolTipDisplay"
    />
    <i-d-r-matching-trend-tool-tip
      :position="{
        x: tooltip.x,
        y: tooltip.y,
      }"
      :show-tool-tip="show"
      :source-input="currentData"
    />
  </div>
</template>

<script>
import IDRMatchingTrendToolTip from "@/components/common/IDRMatchingTrend/IDRMatchingTrendToolTip"
import MultiLineChart from "@/components/common/IDRMatchingTrend/MultiLineChart.vue"
//TODO
import data from "./IDRMatchingTrendData.json"

export default {
  name: "IDRMatchingTrend",
  components: { MultiLineChart, IDRMatchingTrendToolTip },
  props: {
    mapData: {
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
      colorCodes: ["#42EFFD", "#347DAC", "#75787B"],
      sourceData: data,
      currentData: {},
      chartDimensions: {
        width: 0,
        height: 0,
      },
    }
  },

  computed: {
    modificationData() {
      return Object.keys(this.sourceData[0])
    },
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
    getCordinates(args) {
      this.tooltip.x = args.x
      this.tooltip.y = args.y
    },
    sizeHandler() {
      if (this.$refs.customerEventChart) {
        this.chartDimensions.width = 1200
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
