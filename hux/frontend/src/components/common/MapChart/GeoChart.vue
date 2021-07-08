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
            class="d-flex align-center primary--text text-decoration-none"
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
import demographic_overview from "./mapData.json"

export default {
  name: "geo-chart",
  components: {
    mapSlider,
  },
  data() {
    return {
      chartData: demographic_overview.demographic_overview,
      width: 950,
      height: 700,
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
    initializeValues() {},

    async calculateChartValues() {
      await this.chartData
      var width = 700
      var height = 500

      let svg = d3
        .select(this.$refs.huxChart)
        .append("svg")
        .attr("width", width)
        .attr("height", height)
      let us = data.default
      var list = us.objects.states.geometries
      var usList = states.default

      for (let i = 0; i < list.length; i++) {
        usList.forEach((data) => {
          if (list[i].id === data.id) {
            list[i].name = data.name
          }
        })
      }

      var featureCollection = topojson.feature(
        us,
        us.objects.states,
        (a, b) => a !== b
      )

      var projection = d3.geoIdentity().fitSize([600, 500], featureCollection)
      var path = d3.geoPath().projection(projection)

      let colorScale = d3
        .scaleLinear()
        .domain([0, 100])
        .range(["#ffffff", "#396286"])

      svg
        .selectAll("path")
        .data(topojson.feature(us, us.objects.states).features)
        .enter()
        .append("path")
        .attr("d", path)
        .style("stroke", "white")
        .style("stroke-width", "0.5")
        .style("fill", (d) => colorScale(70))
        .on("mouseover", (d) => {
          d3Select
            .select(d.srcElement)
            .attr("fill-opacity", "1")
            .style("fill", (d) => getCurrentStateData(d.id))
        })
        .on("mouseout", () => this.tooltipDisplay(false))

      let getCurrentStateData = (id) => {
        let currentStateDetails = this.chartData.find(
          (data) => data.name == usList.find((data) => data.id == id).name
        )
        this.tooltipDisplay(true, currentStateDetails)
        return colorScale(20)
      }

      function loadStateColors(id) {
        const name = usList.find((data) => data.id == id).name
        let currentStateDetails = this.chartData.find(
          (data) => data.name == name
        )
        return currentStateDetails
          ? colorScale(
              this.$options.filters
                .percentageConvert(
                  currentStateDetails.population_percentage,
                  true,
                  true
                )
                .slice(0, -1)
            )
          : colorScale(50)
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
      this.calculateChartValues()
    },
  },

  mounted() {
    this.initializeValues()
    this.calculateChartValues()
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
