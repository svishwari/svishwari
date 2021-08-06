<template>
  <div>
    <v-card
      class="rounded-lg card-style"
      max-width="450px"
      min-height="150px"
      flat
    >
      <v-card-title class="d-flex justify-space-between pb-6 pl-6 pt-5">
        <div class="mt-1 ml-2 mb-2">
          <span
            class="
              d-flex
              align-center
              area-card-title
              black--text
              text-decoration-none
            "
          >
            Area Chart
          </span>
        </div>
        <div ref="huxChart" class="chart-section"></div>
      </v-card-title>
      <v-card-text class="pl-6 pr-6 pb-6">
        <div id="legend"></div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import * as d3Shape from "d3-shape"
import * as d3Scale from "d3-scale"
import * as d3Select from "d3-selection"
import * as d3Array from "d3-array"
import * as d3Axis from "d3-axis"
import * as d3TimeFormat from "d3-time-format"

export default {
  name: "LineAreaChart",
  props: {
    value: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      width: 355,
      height: 250,
      gender_men: [],
      gender_other: [],
      gender_women: [],
      yValueData: [],
      areaChart: [],
      areaChartData: [],
      genders: ["Women", "Men", "Other"],
      chartData: this.value,
    }
  },

  //adds dots where original data would go but without error

  watch: {
    value: function () {
      d3Select.select(this.$refs.huxChart).select("svg").remove()
      this.initiateAreaChart()
    },
  },

  mounted() {
    this.initiateAreaChart()
  },
  methods: {
    async initiateAreaChart() {
      this.gender_men.push(...this.chartData.gender_men)
      this.gender_women.push(...this.chartData.gender_women)
      this.gender_other.push(...this.chartData.gender_other)
      this.gender_men.forEach((element) => {
        this.gender_women.forEach((value) => {
          if (element.date === value.date) {
            this.areaChart.push({
              date: element.date,
              men_spend: element.ltv,
              women_spend: value.ltv,
            })
          }
        })
      })

      this.areaChart.forEach((element) => {
        this.gender_other.forEach((value) => {
          if (element.date === value.date) {
            this.yValueData.push(
              element.men_spend,
              element.women_spend,
              value.ltv
            )
            this.areaChartData.push({
              date: element.date,
              men_spend: element.men_spend,
              women_spend: element.women_spend,
              others_spend: value.ltv,
            })
          }
        })
      })

      let colorCodes = [
        "rgba(0, 85, 135, 1)",
        "rgba(12, 157, 219, 1)",
        "rgba(66, 239, 253, 1)",
      ]

      let svg = d3Select
        .select(this.$refs.huxChart)
        .append("svg")
        .attr("width", this.width)
        .attr("height", this.height)

      let strokeWidth = 1.5
      let margin = { top: 0, bottom: 20, left: 40, right: 20 }
      let chart = svg
        .append("g")
        .attr("transform", `translate(${margin.left},0)`)

      let width =
        +svg.attr("width") - margin.left - margin.right - strokeWidth * 2
      let height = +svg.attr("height") - margin.top - margin.bottom

      let grp = chart
        .append("g")
        .attr(
          "transform",
          `translate(-${margin.left - strokeWidth},-${margin.top})`
        )

      let stack = d3Shape
        .stack()
        .keys(["women_spend", "men_spend", "others_spend"])
      let stackedValues = stack(this.areaChartData)
      let stackedData = []

      stackedValues.forEach((layer) => {
        let currentStack = []
        layer.forEach((d, i) => {
          d[1] = d[1] - d[0]
          d[0] = 0
          currentStack.push({
            values: d,
            date: new Date(this.areaChartData[i].date),
          })
        })

        stackedData.push(currentStack)
      })

      let appendyAxisFormate = (text) => `$ ${parseInt(text / 1000) + "k"}`

      let yScale = d3Scale
        .scaleLinear()
        .range([height, 0])
        .domain([0, Math.max(...this.yValueData) + 500])

      let xScale = d3Scale
        .scaleLinear()
        .range([0, width])
        .domain(
          d3Array.extent(
            this.areaChartData,
            (dataPoint) => new Date(dataPoint.date)
          )
        )

      let area = d3Shape
        .area()
        .x((dataPoint) => xScale(dataPoint.date))
        .y0((dataPoint) => yScale(dataPoint.values[0]))
        .y1((dataPoint) => yScale(dataPoint.values[1]))

      let series = grp
        .selectAll(".series")
        .data(stackedData)
        .enter()
        .append("g")
        .attr("class", "series")

      series
        .append("path")
        .attr("transform", `translate(${margin.left},0)`)
        .style("fill", (d, i) => colorCodes[i])
        .attr("stroke", (d, i) => colorCodes[i])
        .attr("stroke-linejoin", "round")
        .attr("stroke-linecap", "round")
        .attr("stroke-width", 2)
        .attr("stroke-width", 2)
        .attr("fill-opacity", 0.5)
        .attr("d", (d) => area(d))

      chart
        .append("g")
        .attr("transform", `translate(0,${height})`)
        .call(
          d3Axis
            .axisBottom(xScale)
            .ticks(this.areaChartData.length)
            .tickFormat(d3TimeFormat.timeFormat("%b %Y"))
        )

      chart
        .append("g")
        .attr("transform", "translate(0, 0)")
        .call(d3Axis.axisLeft(yScale).ticks(6).tickFormat(appendyAxisFormate))

      stackedValues.forEach(function (layer, index) {
        layer.forEach((points) => {
          svg
            .append("circle")
            .attr("class", "dot")
            .attr("r", 3)
            .attr("cx", () => xScale(new Date(points.data.date)) + 40)
            .attr("cy", () => yScale(points[1]))
            .style("fill", colorCodes[index])
            .attr("stroke", colorCodes[index])
        })
      })
    },
  },
}
</script>

<style lang="scss" scoped>
.card-style {
  margin-bottom: 40px;
  height: 325px;
  .chart-section {
    margin-bottom: -20px;
  }
  .area-card-title {
    font-family: Open Sans;
    font-style: normal;
    font-weight: normal;
    font-size: 15px;
    line-height: 20px;
  }
}
</style>
