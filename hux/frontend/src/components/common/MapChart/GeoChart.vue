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
      </v-card-title>
      <v-card-text class="pl-6 pr-6 pb-6">
        <div class="map-slider"><map-slider :value="0.45"></map-slider></div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import * as d3Select from "d3-selection"
import * as d3 from "d3"
import * as topojson from "topojson"
import mapSlider from "@/components/common/MapChart/mapSlider"
import * as data from "./usStates.json"
import * as states from "./usdetails.json"

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
      tooltip: {
        x: 0,
        y: 0,
      },
    }
  },
  methods: {
    calculateValues() {
    //  setTimeout(() => {

  //    console.log(Math.min(null, state_population_percentage))
  //    console.log(Math.max(state_population_percentage))
  //    }, 1000);

    },

    async initiateMapChart() {
      await this.chartData

      let svg = d3
        .select(this.$refs.huxChart)
        .append("svg")
        .attr("width", this.width)
        .attr("height", this.height)


      let us = data.default
      let usList = states.default



      var featureCollection = topojson.feature(
        us,
        us.objects.states,
        (a, b) => a !== b
      )

      featureCollection.features.forEach(state => {
        let currentStateDetails = this.chartData.find(
        (data) => data.name == usList.find((us) => us.id == state.id).name
        )
        state.properties = currentStateDetails
      })
      
      let state_population = featureCollection.features.map(data => data.properties.population_percentage)

      var projection = d3.geoIdentity().fitSize([600, 500], featureCollection)
      var path = d3.geoPath().projection(projection)

      let colorScale = d3
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
        .style("fill", (d) => colorScale(d.properties.population_percentage * 100))
        .attr("fill-opacity", "1")
        .on("mouseover", (d) => applyHoverChanges(d))
        .on("mouseout", (d) => removeHoverChanges(d))

      let applyHoverChanges = (d) => {
          svg.selectAll("path")
          .style("stroke", "#4F4F4F")
          .attr("fill-opacity", "0.5")
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

      let removeHoverChanges = (d) => {
          svg.selectAll("path")
          .style("stroke", "#1E1E1E")
          .style("stroke-width", "0.5")
          .style("fill", (d) => colorScale(d.properties.population_percentage * 100))
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
    this.calculateValues()
    this.initiateMapChart()
  },
}
</script>

<style lang="scss" scoped>
.card-style {
  margin-bottom: 40px;
  height: 550px;
}
.chart-container {
  max-width: 70%;
  height: 500px;

  .legend-section {
    span {
      margin-left: 8px;
      font-size: 12px;
      line-height: 16px;
      color: var(--v-gray-base) !important;
    }
  }

  .title-section {
    font-size: 15px;
    line-height: 20px;
    font-weight: 400;
  }

  .chart-section {
    margin-bottom: -20px;
  }
}
.chart-container2 {
  max-width: 50%;
  height: 500px;

  .legend-section {
    span {
      margin-left: 8px;
      font-size: 12px;
      line-height: 16px;
      color: var(--v-gray-base) !important;
    }
  }
}

.map-slider {
  max-height: 30px;
}

.total {
  display: flex;
  flex-wrap: wrap;
}
</style>
