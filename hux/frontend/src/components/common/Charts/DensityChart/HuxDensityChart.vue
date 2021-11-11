<template>
  <div ref="hux-density-chart" />
</template>

<script>
import * as d3Shape from "d3-shape"
import * as d3Array from "d3-array"
import * as d3Scale from "d3-scale"
import * as d3Select from "d3-selection"

export default {
  name: "HuxDensityChart",

  props: {
    data: {
      type: Array,
      required: true,
    },
    range: {
      type: Array,
      required: true,
    },
    min: {
      type: [Number, String],
      required: true,
    },
    max: {
      type: [Number, String],
      required: true,
    },
    step: {
      type: [Number, String],
      required: false,
      default: 1,
    },
    id: {
      type: String,
      required: true,
    },
    chartDimensions: {
      type: Object,
      required: false,
      default() {
        return {
          width: 0,
          height: 0,
        }
      },
    },
  },

  data() {
    return {
      localData: [],
    }
  },

  watch: {
    chartDimensions: {
      handler() {
        d3Select
          .select(this.$refs["hux-density-chart"])
          .selectAll("svg")
          .remove()
        this.generateChart()
      },
      immediate: false,
      deep: true,
    },
    range: {
      handler() {
        d3Select
          .select(this.$refs["hux-density-chart"])
          .selectAll("svg")
          .remove()
        this.generateChart()
      },
      immediate: true,
    },
  },

  mounted() {
    this.generateChart()
  },

  methods: {
    async generateChart() {
      let width = this.chartDimensions.width
      let height = this.chartDimensions.height

      this.localData.push([this.min, 0])
      this.localData.push(...this.data)
      this.localData.push([this.max, 0])

      // generates an svg and appends to the dom
      let svg = d3Select
        .select(this.$refs["hux-density-chart"])
        .append("svg")
        .attr("width", "100%")
        .attr("height", height)

      let yAxisMinMaxValue = d3Array.extent(this.localData, (d) => d[1])

      // function to generate coordinates for x-axis
      let xCoordinateFunction = d3Scale
        .scaleLinear()
        .domain([this.min, this.max])
        .range([0, width])

      // function to generate coordinates for y-axis
      let yCoordinateFunction = d3Scale
        .scaleLinear()
        .domain(yAxisMinMaxValue)
        .range([height, 0])

      let linearGradient = svg
        .append("defs")
        .append("linearGradient")
        .attr("id", `hux-density-chart-${this.id}`)

      linearGradient
        .append("stop")
        .attr("offset", Number((this.range[0] / this.max).toFixed(2)))
        .style("stop-color", "#E6F4F3")
        .style("stop-opacity", "1.0")

      linearGradient
        .append("stop")
        .attr("offset", Number((this.range[0] / this.max).toFixed(2)))
        .style("stop-color", "#9DD4CF")
        .style("stop-opacity", "1.0")

      linearGradient
        .append("stop")
        .attr("offset", Number((this.range[1] / this.max).toFixed(2)))
        .style("stop-color", "#9DD4CF")
        .style("stop-opacity", "1.0")

      linearGradient
        .append("stop")
        .attr("offset", Number((this.range[1] / this.max).toFixed(2)))
        .style("stop-color", "#E6F4F3")
        .style("stop-opacity", "1.0")

      // Add the area
      svg
        .append("path")
        .datum(this.localData)
        .attr("fill", `url(#hux-density-chart-${this.id})`)
        .attr(
          "d",
          d3Shape
            .area()
            .x(function (d) {
              return xCoordinateFunction(d[0])
            })
            .y0(yCoordinateFunction(0))
            .y1(function (d) {
              return yCoordinateFunction(d[1])
            })
        )
    },
  },
}
</script>
