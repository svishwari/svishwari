<template>
  <div class="container">
    <span v-if="showChart">
      <div id="chart" ref="chart" @mousemove="getCordinates($event)"></div>
    <div class="pt-2 pl-4">
      <div id="chartLegend"></div>
    </div>
      <doughnut-chart-tooltip
        :show-tooltip="showTooltip"
        :tooltip="tooltip"
        :source-input="sourceInput"
      />
    </span>
    <span v-else>
      <img
        src="@/assets/images/Chart_donut.png"
        alt="Hux"
        width="200"
        height="200"
        class="d-flex ml-10"
      />
      <div class="d-flex ml-6 global-text-line">
        <span class="append-circle"></span> no data available
      </div>
    </span>
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
      showChart: true,
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
      let data = this.data

      let legendsData = [
          { label: "Women", position: 10 },
          { label: "Men", position: 47 },
          { label: "Other", position: 78 },
        ]

        let colorCodes = [ "#005587","#0C9DDB", "#42EFFD"]

      this.showChart = false
      if (data.length != 0) {
        this.showChart = true
        // Initialize width, height & color range
        this.chartWidth = this.chartDimensions.width + "px"
        let width = this.chartDimensions.width - 50,
          height = this.chartDimensions.height - 25,
          radius = Math.min(width, height) / 1.8
        let color = d3Scale
          .scaleOrdinal()
          .range(["#0C9DDB", "#005587", "#42EFFD"])

        // Define outer-radius & inner-radius of donut-chart
        let arc = d3Shape
          .arc()
          .outerRadius(radius - 10)
          .innerRadius(radius - 25)

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
      d3Select.select("#chartLegend").selectAll("svg").remove()
      let legendSvg = d3Select
        .select("#chartLegend")
        .append("svg")
        .attr("viewBox", "8 0 130 42")
        .attr("id", "mainSvg")
        .attr("class", "svgBox")
        .style("margin-right", "20px")
        .style("margin-left", "-10px")
        .style("text-align", "left")

      let legend = legendSvg
        .selectAll(".legend")
        .data(legendsData)
        .enter()
        .append("g")
        .attr("class", "legend")
        .attr("transform", function (d) {
          return `translate(${d.position}, 0)`
        })

      legend
        .append("circle")
        .attr("cx", 10)
        .attr("cy", 10)
        .attr("r", 3)
        .style("fill", function (d, i) {
          return colorCodes[i]
        })

      legend
        .append("text")
        .attr("x", 16)
        .attr("y", 9)
        .attr("dy", ".55em")
        .attr("class", "neroBlack--text")
        .style("font-size", "6px")
        .style("text-anchor", "start")
        .text(function (d) {
          return d.label
        })
      }
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
  #chartLegend {
    max-width: 400px;
    min-width: 150px;
  }
  .pieBox {
    display: inline-block;
  }
  .append-circle {
    height: 12px;
    width: 12px;
    background-color: rgba(208, 208, 206, 1);
    border-radius: 50%;
    display: inline-block;
    margin-top: 6px;
    margin-right: 8px;
  }
}
</style>
