<template>
    <div
      class="chart-container"
    >
      <!-- <v-card-title class="d-flex justify-space-between pb-6 pl-6 pt-5"> -->
        <!-- <div class="mt-2">
          <a
            href="#"
            class="d-flex align-center black--text text-decoration-none"
          >
            Demographic overview
          </a>
        </div> -->
        <div
          ref="huxChart"
          class="chart-section"
          @mouseover="getCordinates($event)"
        ></div>
        <div class="map-slider">
          <map-slider
            v-if="minValue && maxValue"
            :min="minValue"
            :max="maxValue"
          ></map-slider>
        </div>
      <!-- </v-card-title> -->
      <!-- <v-card-text class="pl-6 pr-6 pb-6"> </v-card-text> -->
    </div>
</template>

<script>
import * as d3Select from "d3-selection"
import * as d3Scale from "d3-scale"
import * as d3Geo from "d3-geo"
import * as topojson from "topojson"
import * as topoData from "../../../../public/usaTopology.json"
import * as statesList from "../../../../public/usaStateList.json"
import mapSlider from "@/components/common/MapChart/mapSlider"

export default {
  name: "GeoChart",
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

  watch: {
    value: function () {
      d3Select.select(this.$refs.huxChart).select("svg").remove()
      this.initiateMapChart()
    },
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

      let total_range = featureCollection.features.map(
        (data) => data.properties.population_percentage
      )

      this.minValue = Math.min(...total_range)
      this.maxValue = Math.max(...total_range)

      // let projection = d3Geo
      //   .geoIdentity()
      //   .fitSize([500, 300], featureCollection)


          var projection = d3Geo.geoIdentity()
  .fitExtent([[20,20],[700-10,350-50]], featureCollection)

      let path = d3Geo.geoPath().projection(projection)

      let colorScale = d3Scale
        .scaleLinear()
        .domain([this.minValue * 100, this.maxValue * 100])
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
}
</script>

<style lang="scss" scoped>
.chart-container {
  margin-bottom: 40px;
  height: 550px;
  max-width: 798px;
  min-height: 100px;
  .chart-section {
   // margin-bottom: -20px;
  }
  .map-slider {
    max-height: 30px;
  }
}
</style>
