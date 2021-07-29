<template>
  <div class="container">
    <v-card tile class="chart-container rounded-lg box-shadow-5">
      <div id="label"></div>
      <div id="chart"></div>
      <div id="legend"></div>
    </v-card>
  </div>
</template>

<script>
import data from "@/components/common/GenderChart/data.json"
import * as d3Select from "d3-selection"
import * as d3Scale from "d3-scale"
import * as d3Shape from "d3-shape"
import "d3-transition"

export default {
  name: "GenderChart",
  components: {},
  props: {
    value: {
      type: Array,
      required: false, // TODO: Integration & change to true while accepting the data
    },
  },
  data() {
    return {
      chartData: data,
      width: 700,
      height: 500,
    }
  },
  methods: {
    async initiateGenderChart() {
      await this.chartData

      var data = [
        {
          label: "Men",
          population_percentage:
            this.chartData.gender.gender_men.population_percentage,
          size: this.chartData.gender.gender_men.size,
        },
        {
          label: "Women",
          population_percentage:
            this.chartData.gender.gender_women.population_percentage,
          size: this.chartData.gender.gender_women.size,
        },
        {
          label: "Other",
          population_percentage:
            this.chartData.gender.gender_other.population_percentage,
          size: this.chartData.gender.gender_other.size,
        },
      ]

      // Initialize width, height & color range
      var width = 250,
        height = 273,
        radius = Math.min(width, height) / 2
      var line = 0
      var col = 0
      var color = d3Scale
        .scaleOrdinal()
        .range(["#0C9DDB", "#005587", "#42EFFD"])

      // Define outer-radius & inner-radius of donut-chart
      var arc = d3Shape
        .arc()
        .outerRadius(radius - 10)
        .innerRadius(radius - 30)

      // Assign value to chart
      var pie = d3Shape
        .pie()
        .sort(null)
        .value(function (d) {
          return parseInt((d.population_percentage * 100).toFixed(0))
        })

      // Append class & id
      d3Select
        .select("#chart")
        .append("div")
        .attr("id", "mainPie")
        .attr("class", "pieBox")

      // assign style attribute to chart div
      var svg = d3Select
        .select("#mainPie")
        .append("svg")
        .attr("viewBox", `0 0 ${width} ${height}`) // for responsive
        .style("margin-left", "40px")
        .style("margin-right", "40px")
        .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")

      // create arc & append class attribute
      var g = svg
        .selectAll(".arc")
        .data(pie(data))
        .enter()
        .append("g")
        .attr("class", "arc")

      // fill the arc with colors
      g.append("path")
        .attr("d", arc)
        .style("fill", function (d) {
          return color(d.data.population_percentage)
        })

      // Creating legends svg element
      var legendSvg = d3Select
        .select("#legend")
        .append("svg")
        .attr("viewBox", `0 0 200 25`) // for responsive
        .attr("id", "mainSvg")
        .attr("class", "svgBox")
        .style("margin-left", "20px")
        .style("margin-right", "20px")

      // calculating legend distance
      var legend = legendSvg
        .selectAll(".legend")
        .data(data)
        .enter()
        .append("g")
        .attr("class", "legend")
        .attr("transform", function (d) {
          var y = line * 25
          var x = col
          col += d.label.length * 10 + 25
          return "translate(" + x + "," + y + ")"
        })

      // creating legend circle
      legend
        .append("circle")
        .attr("cx", 10)
        .attr("cy", 10)
        .attr("r", 6)
        .style("fill", function (d) {
          return color(d.population_percentage)
        })

      // creating legend text
      legend
        .append("text")
        .attr("x", 18)
        .attr("y", 9)
        .attr("dy", ".35em")
        .attr("class", "neroBlack--text")
        .style("text-anchor", "start")
        .text(function (d) {
          return d.label
        })

      // Creating label svg element
      var label = d3Select
        .select("#label")
        .append("svg")
        .attr("width", 200)
        .attr("height", 20)
        .attr("id", "label")
        .style("margin-left", "24px")
        .style("margin-top", "20px")

      // Appending text to label
      label
        .append("text")
        .attr("x", 18)
        .attr("y", 9)
        .attr("dy", ".35em")
        .attr("class", "neroBlack--text")
        .text(function () {
          return "Gender"
        })
    },
  },
  mounted() {
    this.initiateGenderChart()
  },
}
</script>
<style lang="scss" scoped>
.chart-container {
  max-width: 100%;
  #chart {
    text-align: center;
  }
  .pieBox {
    display: inline-block;
    height: auto;
  }
}
</style>
