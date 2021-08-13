<template>
  <div class="container">
    <div id="chart" @mousemove="getCordinates($event)"></div>
    <div ref="legend"></div>
    <doughnut-chart-tooltip
      :show-tooltip="showTooltip"
      :tooltip="tooltip"
      :source-input="sourceInput"
    />
  </div>
</template>

<script>
import DoughnutChartTooltip from "@/components/common/DoughnutChart/DoughnutChartTooltip"
import * as d3Select from "d3-selection"
import * as d3Scale from "d3-scale"
import * as d3Shape from "d3-shape"

export default {
  name: "DoughnutChart",
  components: { DoughnutChartTooltip },
  props: {
    data: {
      type: Array,
      required: true,
    },
    width: {
      type: Number,
      required: true,
    },
    height: {
      type: Number,
      required: true,
    },
    label: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      sourceInput: null,
      showTooltip: false,
      tooltip: {
        x: 0,
        y: 0,
      },
    }
  },
  mounted() {
    this.initiateChart()
  },
  methods: {
    async initiateChart() {
      let data = await this.data // TODO: Get this from API

      // Initialize width, height & color range
      let width = this.width,
        height = this.height,
        radius = Math.min(width, height) / 2
      let line = 0
      let col = 0
      let color = d3Scale
        .scaleOrdinal()
        .range(["#0C9DDB", "#005587", "#42EFFD"])

      // Define outer-radius & inner-radius of donut-chart
      let arc = d3Shape
        .arc()
        .outerRadius(radius - 10)
        .innerRadius(radius - 35)

      // Assign value to chart
      let pie = d3Shape
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
      let svg = d3Select
        .select("#mainPie")
        .append("svg")
        .attr("viewBox", `0 0 ${width} ${height}`) // for responsive
        .style("margin-left", "40px")
        .style("margin-right", "40px")
        .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")

      // create arc & append class attribute
      let g = svg
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
        .on("mouseover", (e, d) => showTooltip(e, d))
        .on("mouseout", (e, d) => hideTooltip(e, d))

      let showTooltip = (e, d) => {
        this.sourceInput = d.data
        this.showTooltip = true
      }
      let hideTooltip = (e, d) => {
        this.sourceInput = d.data
        this.showTooltip = false
      }

      // Creating legends svg element & apply style
      let legendSvg = d3Select
        .select(this.$refs.legend)
        .append("svg")
        .attr("viewBox", "0 0 200 25") // for responsive
        .attr("id", "mainSvg")
        .attr("class", "svgBox")
        .style("margin-left", "20px")
        .style("margin-right", "20px")

      // calculating distance b/n each legend
      let legend = legendSvg
        .selectAll(".legend")
        .data(data)
        .enter()
        .append("g")
        .attr("class", "legend")
        .attr("transform", function (d) {
          let y = line * 25
          let x = col
          col += d.label.length * 10 + 25
          return "translate(" + x + "," + y + ")"
        })

      // creating legend circle & fill color
      legend
        .append("circle")
        .attr("cx", 10)
        .attr("cy", 10)
        .attr("r", 6)
        .style("fill", function (d) {
          return color(d.population_percentage)
        })

      // creating legend text & apply css class
      legend
        .append("text")
        .attr("x", 18)
        .attr("y", 10)
        .attr("dy", ".35em")
        .attr("class", "neroBlack--text")
        .style("text-anchor", "start")
        .text(function (d) {
          return d.label
        })

      // Creating label svg element & apply style
      let label = d3Select
        .select("#label")
        .append("svg")
        .attr("width", 200)
        .attr("height", 20)
        .attr("id", "label")
        .style("margin-left", "5px")
        .style("margin-top", "20px")

      // Appending text to label & apply css class
      label
        .append("text")
        .attr("x", 18)
        .attr("y", 9)
        .attr("dy", ".35em")
        .attr("class", "neroBlack--text")
        .text(this.label)
    },
    getCordinates(event) {
      this.tooltip.x = event.offsetX + 60
      this.tooltip.y = event.offsetY - 200
    },
  },
}
</script>
<style lang="scss" scoped>
.container {
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
