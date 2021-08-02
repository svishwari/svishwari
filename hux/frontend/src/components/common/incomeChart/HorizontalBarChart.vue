<template>
  <div>
    <v-card
      class="rounded-lg card-style"
      maxWidth="300px"
      minHeight="150px"
      flat
    >
      <v-card-title class="d-flex justify-space-between pb-6 pl-6 pt-5">
        <div class="mt-2 ml-2">
          <span
            class="
              d-flex
              align-center
              income-card-title
              black--text
              text-decoration-none
            "
          >
            Area Chart
          </span>
        </div>
        <div
          class="chart-section"
          ref="huxChart"
        ></div>
      </v-card-title>
      <v-card-text class="pl-6 pr-6 pb-6"> </v-card-text>
    </v-card>
  </div>
</template>

<script>
import * as d3Shape from "d3-shape"
import * as d3Scale from "d3-scale"
import * as d3Select from "d3-selection"
import * as d3Array from "d3-array"
import * as d3Axis from "d3-axis"

export default {
  name: "horizontal-bar-chart",
  props: {
    value: {
      type: Array,
      required: true,
    },

  },
  data() {
    return {
      width: 255,
      height: 237,
      chartData: this.value,
    }
  },
  methods: {
    async initiateAreaChart() {
      let areaChartData = [
        {
          year: 2000,
          aData: 2144,
          bData: 3199,
          cData: 3088,
        },
        {
          year: 2001,
          aData: 3144,
          bData: 4265,
           cData: 3842,
        },
        {
          year: 2002,
          aData: 3211,
          bData: 4986,
           cData: 3999,
        },
        {
          year: 2003,
          aData: 3211,
          bData: 4986,
           cData: 3999,
        },
        {
          year: 2004,
          aData: 4866,
          bData: 6109,
           cData: 6109,
        },
      ]



      let colorCodes = ["lightgreen", "lightblue", "yellow"]

      let svg = d3Select
        .select(this.$refs.huxChart)
        .append("svg")
        .attr("width", this.width)
        .attr("height", this.height)

 

      let strokeWidth = 1.5
      let margin = { top: 0, bottom: 20, left: 30, right: 20 }
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

 

      let stack = d3Shape.stack().keys(["aData", "bData", "cData"])
      let stackedValues = stack(areaChartData)
      let stackedData = []

 

      stackedValues.forEach((layer, index) => {
        let currentStack = []
        layer.forEach((d, i) => {
         d[1] = d[1]-d[0]
         d[0] = 0
          currentStack.push({
            values: d,
            year: new Date(areaChartData[i].year),
          })
        })
        // console.log("currentStack",currentStack);
        stackedData.push(currentStack)
        console.log("stackedData",stackedData)
      })

 

      let yScale = d3Scale
        .scaleLinear()
        .range([height, 0])
        .domain([
          0,
          d3Array.max(stackedValues[stackedValues.length - 1], (dp) => dp[1]),
        ])

      let xScale = d3Scale
        .scaleLinear()
        .range([0, width])
        .domain(d3Array.extent(areaChartData, (dataPoint) => dataPoint.year))

//  let xScale = d3Scale
//         .scaleLinear()
//         .range([0, width])
//         .domain(d3Array.min(areaChartData, (dataPoint) => dataPoint.year),d3Array.max(areaChartData, (dataPoint) => dataPoint.year))


      let area = d3Shape
        .area()
        .x((dataPoint) => xScale(dataPoint.year))
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
        .attr("stroke", "steelblue")
        .attr("stroke-linejoin", "round")
        .attr("stroke-linecap", "round")
        .attr("stroke-width", strokeWidth)
        .attr("d", (d) => area(d))

 

      chart
        .append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3Axis.axisBottom(xScale).ticks(areaChartData.length))

 

      chart
        .append("g")
        .attr("transform", `translate(0, 0)`)
        .call(d3Axis.axisLeft(yScale))
    },
  },

 

  watch: {
    value: function () {
      d3Select.select(this.$refs.huxChart).select("svg").remove()
      this.initiateAreaChart()
    },
  },

 

  mounted() {
    this.initiateAreaChart()
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
}
</style>