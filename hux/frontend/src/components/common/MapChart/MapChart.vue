<template>
  <div ref="chartBox" class="container">
    <span v-if="mapChartData.length != 0">
    <geo-chart
      v-model="mapChartData"
      :chart-dimensions="chartDimensions"
      :configuration-data="configurationData"
      @cordinates="getCordinates"
      @tooltipDisplay="toolTipDisplay"
    />
    <map-chart-tooltip
      :configuration-data="configurationData"
      :position="{
        x: tooltip.x,
        y: tooltip.y,
      }"
      :show-tooltip="show"
      :source-input="currentData"
    >
    </map-chart-tooltip>
    </span>
    <span v-else>
        <img
        src="@/assets/images/USA.png"
        alt="Hux"
        width="548"
        height="290"
        class="d-flex ma-4"
      />
    </span>
  </div>
</template>

<script>
import MapChartTooltip from "@/components/common/MapChart/MapChartTooltip"
import GeoChart from "@/components/common/MapChart/GeoChart"

export default {
  name: "MapChart",
  components: { GeoChart, MapChartTooltip },
  props: {
    mapData: {
      type: Array,
      required: true,
    },
    configurationData: {
      type: Object,
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
      mapChartData: this.mapData,
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
