<template>
  <div>
    <v-card
      class="rounded-lg card-style"
      maxWidth="798px"
      minHeight="100px"
      flat
    >
      <v-card-title class="d-flex justify-space-between pb-6 pl-6 pt-5">
        <div class="mt-2">
          <a
            href="#"
            class="d-flex align-center black--text text-decoration-none"
          >
            Demographic overview
          </a>
        </div>
        <div
          class="chart-section"
          ref="huxChart"
          @mouseover="getCordinates($event)"
        ></div>
        <div class="map-slider">
          <map-slider
            v-if="total_range.length > 0"
            :range="total_range"
          ></map-slider>
        </div>
      </v-card-title>
      <v-card-text class="pl-6 pr-6 pb-6"> </v-card-text>
    </v-card>
  </div>
</template>

<script>
import * as d3Select from "d3-selection"
import * as d3Scale from "d3-scale"
import * as d3Geo from "d3-geo"
import * as topojson from "topojson"
import * as topoData from "@/components/common/MapChart/MapSource/usaTopology.json"
import * as statesList from "@/components/common/MapChart/MapSource/usaStateList.json"
import mapSlider from "@/components/common/MapChart/mapSlider"

export default {
  name: "geo-chart",
  components: {
    mapSlider,
  },
  props: {
    value: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      chartData: this.value,
      width: 700,
      height: 500,
      top: 50,
      left: 60,
      show: false,
      total_range: [],
      tooltip: {
        x: 0,
        y: 0,
      },
    }
  },
  methods: {
    async initiateMapChart() {
      await this.chartData

      let svg = d3Select
        .select(this.$refs.huxChart)
        .append("svg")
        .attr("width", this.width)
        .attr("height", this.height)

      let us = topoData.default
      let usList = statesList.default

      let featureCollection = topojson.feature(
        us,
        us.objects.states,
        (a, b) => a !== b
      )

      featureCollection.features.forEach((state) => {
        let currentStateDetails = this.chartData.find(
          (data) => data.name == usList.find((us) => us.id == state.id).name
        )
        state.properties = currentStateDetails
      })

      this.total_range = featureCollection.features.map(
        (data) => data.properties.population_percentage
      )

      let projection = d3Geo
        .geoIdentity()
        .fitSize([600, 500], featureCollection)
      let path = d3Geo.geoPath().projection(projection)

      let colorScale = d3Scale
        .scaleLinear()
        .domain([0, 100])
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
          colorScale(d.properties.population_percentage * 100)
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
        this.tooltipDisplay(true, d.properties)
        return "1"
      }

      let removeHoverChanges = () => {
        svg
          .selectAll("path")
          .style("stroke", "#1E1E1E")
          .style("stroke-width", "0.5")
          .style("fill", (d) =>
            colorScale(d.properties.population_percentage * 100)
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

  watch: {
    value: function () {
      d3Select.select(this.$refs.huxChart).select("svg").remove()
      this.initiateMapChart()
    },
  },

  mounted() {
    this.initiateMapChart()
  },
}
</script>

<style lang="scss" scoped>
.card-style {
  margin-bottom: 40px;
  height: 550px;
  .chart-section {
    margin-bottom: -20px;
  }
  .map-slider {
    max-height: 30px;
  }
}
</style>
