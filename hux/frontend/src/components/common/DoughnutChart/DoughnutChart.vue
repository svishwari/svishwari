<template>
  <div class="container" :style="{ maxWidth: chartWidth }">
    <div id="chart" ref="chart" @mousemove="getCordinates($event)"></div>
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
    chartDimensions: {
      type: Object,
      required: true,
      default() {
        return {
          width: 0,
          height: 0,
        }
      },
    },
    label: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      chartWidth: "",
      sourceInput: null,
      showTooltip: false,
      tooltip: {
        x: 0,
        y: 0,
      },
    }
  },
  watch: {
    chartDimensions: {
      handler() {
        d3Select.select(this.$refs.chart).selectAll("svg").remove()
        this.initiateChart()
      },
      immediate: false,
      deep: true,
    },
  },
  mounted() {
    this.initiateChart()
  },
  methods: {
    initiateChart() {
      let data = this.data // TODO: Get this from API
      // Initialize width, height & color range
      this.chartWidth = this.chartDimensions.width + "px"
      let width = this.chartDimensions.width - 50,
        height = this.chartDimensions.height - 25,
        radius = Math.min(width, height) / 1.8
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
        .attr("width", width)
        .attr("height", height)
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
      d3Select.select(this.$refs.legend).selectAll("svg").remove()

      let legendSvg = d3Select
        .select("#mainPie")
        .append("svg")
        .attr("viewBox", "0 0 200 60") // for responsive
        .attr("width", width - 50)
        .attr("height", 54)
        .attr("id", "mainSvg")
        .attr("class", "svgBox")
        .style("margin-left", "-10px")
        .style("text-align", "left")
        .style("margin-top", "15px")

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
        .attr("class", "black--text text--darken-4")
        .style("text-anchor", "start")
        .text(function (d) {
          return d.label
        })
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
  padding: 0px !important;
  #chart {
    text-align: center;
  }
  .pieBox {
    display: inline-block;
  }
}
</style>
