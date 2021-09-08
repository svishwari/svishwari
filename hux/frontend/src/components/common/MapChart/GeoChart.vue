<template>
  <div class="chart-container" :style="{ maxWidth: chartWidth }">
    <div ref="huxChart" @mouseover="getCordinates($event)"></div>
  </div>
</template>

<script>
import * as d3Select from "d3-selection"
import * as d3Scale from "d3-scale"
import * as d3Geo from "d3-geo"
import * as topojson from "topojson"
import * as topoData from "../../../../public/usaTopology.json"
import * as statesList from "../../../../public/usaStateList.json"

export default {
  name: "GeoChart",
  components: {},
  props: {
    value: {
      type: Array,
      required: true,
    },
    chartDimensions: {
      type: Object,
      required: false,
      default() {
        return {
          width: 0,
          height: 0,
        }
      },
    },
    configurationData: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      chartWidth: "",
      chartData: this.value,
      width: 700,
      height: 300,
      show: false,
      minValue: 0,
      maxValue: 0,
      tooltip: {
        x: 0,
        y: 0,
      },
    }
  },
  computed: {
    primaryMetric() {
      return this.configurationData.primary_metric.key
    },
    defaultMetric() {
      return this.configurationData.default_metric.key
    },
  },
  watch: {
    chartDimensions: {
      handler() {
        d3Select.select(this.$refs.huxChart).selectAll("svg").remove()
        this.initiateMapChart()
      },
      immediate: false,
      deep: true,
    },
  },
  methods: {
    async initiateMapChart() {
      await this.chartData

      this.chartWidth = this.chartDimensions.width + "px"
      let currentWidth = this.chartDimensions.width
      this.width = currentWidth == 0 ? 700 : currentWidth

      let svg = d3Select
        .select(this.$refs.huxChart)
        .append("svg")
        .attr("width", this.width)
        .attr("height", this.height)
        .attr("viewBox", `0 0 ${this.width} ${this.height}`)
        .attr("preserveAspectRatio", "xMidYMid")

      let us = topoData.default
      let usList = statesList.default

      let featureCollection = topojson.feature(
        us,
        us.objects.states,
        (a, b) => a !== b
      )

      featureCollection.features.forEach((state) => {
        let currentStateDetails = this.chartData.find(
          (data) =>
            data[this.defaultMetric] ==
            usList.find((us) => us.id == state.id)[this.defaultMetric]
        )
        state.properties = currentStateDetails
      })

      let total_range = featureCollection.features.map(
        (data) => data.properties ? data.properties[this.primaryMetric] : 0
      )

      this.maxValue = Math.max(...total_range)

      var projection = d3Geo.geoIdentity().fitExtent(
        [
          [20, 20],
          [this.width - 10, 350 - 50],
        ],
        featureCollection
      )

      let path = d3Geo.geoPath().projection(projection)

      let colorScale = d3Scale
        .scaleLinear()
        .domain([0, this.maxValue * 100])
        .range(["#ffffff", "#396286"])

      svg
        .selectAll("path")
        .data(featureCollection.features)
        .enter()
        .append("path")
        .attr("d", path)
        .style("stroke", "#1E1E1E")
        .style("stroke-width", "0.5")
        .style("fill", (d) =>
          colorScale(d.properties ?  d.properties[this.primaryMetric]* 100 : 0)
        )
        .attr("fill-opacity", "1")
        .on("mouseover", (d) => applyHoverChanges(d))
        .on("mouseout", () => removeHoverChanges())

      let applyHoverChanges = (d) => {
        svg
          .selectAll("path")
          .style("stroke", "#4F4F4F")
          .attr("fill-opacity", "0.4")
          .style("stroke-width", "0.2")
        d3Select
          .select(d.srcElement)
          .attr("fill-opacity", (d) => emitStateData(d))
          .style("stroke", "#1E1E1E")
          .style("stroke-width", "1")
      }

      let emitStateData = (d) => {
        if (d.properties) {
        this.tooltipDisplay(true, d.properties)
        }
        return "1"
      }

      let removeHoverChanges = () => {
        svg
          .selectAll("path")
          .style("stroke", "#1E1E1E")
          .style("stroke-width", "0.5")
          .style("fill", (d) =>
            colorScale(d.properties ? d.properties[this.primaryMetric] * 100 : 0)
          )
          .attr("fill-opacity", "1")
        this.tooltipDisplay(false)
      }
    },

    getCordinates(event) {
      this.tooltip.x = event.offsetX
      this.tooltip.y = event.offsetY
      this.$emit("cordinates", this.tooltip)
    },

    tooltipDisplay(showTip, currentStateData) {
      this.$emit("tooltipDisplay", showTip, currentStateData)
    },
  },
}
</script>

<style lang="scss" scoped>
.chart-container {
  margin-bottom: 40px;
  height: 125px;
  min-height: 100px;
  .map-slider {
    max-height: 30px;
  }
}
</style>
