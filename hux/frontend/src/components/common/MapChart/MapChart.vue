<template>
  <div ref="chartBox" class="container">
    <geo-chart
      v-model="mapChartData"
      :chart-dimensions="chartDimensions"
      @cordinates="getCordinates"
      @tooltipDisplay="toolTipDisplay"
    />
    <map-chart-tooltip
      :position="{
        x: tooltip.x,
        y: tooltip.y,
      }"
      :show-tooltip="show"
      :source-input="currentData"
    >
    </map-chart-tooltip>
  </div>
</template>

<script>
import MapChartTooltip from "@/components/common/MapChart/MapChartTooltip"
import GeoChart from "@/components/common/MapChart/GeoChart"

export default {
  name: "MapChart",
  components: { GeoChart, MapChartTooltip },
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
      mapChartData: this.mapData,
      currentData: {},
    }
  },
  props: {
    mapData: {
      type: Array,
      required: true,
    },
  },
  created() {
    window.addEventListener("resize", this.sizeHandler)
  },
  destroyed() {
    window.removeEventListener("resize", this.sizeHandler)
  },
  mounted() {
    this.chartDimensions.width = this.$refs.chartBox.clientWidth
    this.chartDimensions.height = this.$refs.chartBox.clientHeight
  },
  methods: {
    toolTipDisplay(...arg) {
      this.show = arg[0]
      if (this.show) {
        this.generateToolTipData(arg[1])
      }
    },
    sizeHandler() {
      this.chartDimensions.width = this.$refs.chartBox.clientWidth
      this.chartDimensions.height = this.$refs.chartBox.clientHeight
    },
    getCordinates(args) {
      this.tooltip.x = args.x
      this.tooltip.y = args.y
    },
    generateToolTipData(currentStateinfo) {
      this.currentData = currentStateinfo
    },
  },
}
</script>

<style lang="scss" scoped>
.container {
  position: relative;
  padding: 0px !important;
}
</style>
