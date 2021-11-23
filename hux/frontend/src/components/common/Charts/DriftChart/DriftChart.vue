<template>
  <div ref="hux-drift-chart-container">
    <div ref="hux-drift-chart"></div>
    <chart-tooltip
      v-if="showTooltip"
      :position="{
        x: finalXCoordinate,
        y: finalYCoordinate,
      }"
      :tooltip-style="toolTipStyle"
    >
      <template #content>
        <div class="body-2 mb-1 margin-sides-dec">
          <span class="dot mr-1"></span>{{ title }}
        </div>
        <div class="body-2 my-1 margin-sides-dec">{{ tooltipValue }}</div>
        <div class="body-2 mt-1 margin-sides-dec" style="color: #4f4f4f">
          {{ tooltipValueDate | Date("MMM DD, YYYY") | Empty }}
        </div>
      </template>
    </chart-tooltip>
  </div>
</template>

<script>
import * as d3Select from "d3-selection"
import * as d3Scale from "d3-scale"
import * as d3Axis from "d3-axis"
import * as d3Shape from "d3-shape"
import * as d3Array from "d3-array"
import * as d3TimeFormat from "d3-time-format"
import * as d3Time from "d3-time"
import ChartTooltip from "@/components/common/Charts/Tooltip/ChartTooltip.vue"
import TooltipConfiguration from "@/components/common/Charts/Tooltip/tooltipStyleConfiguration.json"

export default {
  name: "DriftChart",

  components: {
    ChartTooltip,
  },

  props: {
    value: {
      type: Array,
      required: true,
    },
    tickPadding: {
      type: Number,
      required: false,
      default: 10,
    },
    xAxisMaxTicks: {
      type: Number,
      required: false,
      default: 5,
    },
    yAxisMaxTicks: {
      type: Number,
      required: false,
      default: 5,
    },
    xAxisFormat: {
      type: String,
      required: false,
      default: "%Y",
    },
    yAxisFormatingFunc: {
      type: Function,
      required: false,
      default: (x) => {
        return x
      },
    },
    enableGrid: {
      type: Array,
      required: false,
      default: () => {
        return [false, false]
      },
    },
    axisTextColor: {
      type: String,
      required: false,
      default: "#4F4F4F",
    },
    lineColor: {
      type: String,
      required: false,
      default: "#00a3e0",
    },
    tickColor: {
      type: String,
      required: false,
      default: "rgba(208, 208, 206, 0.3)",
    },
    enableAxisLines: {
      type: Boolean,
      required: false,
      default: false,
    },
    margin: {
      type: Object,
      required: false,
      default: () => {
        return { top: 20, right: 30, bottom: 30, left: 40 }
      },
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
    title: {
      type: String,
      required: false,
      default: "Drift AUC",
    },
  },

  data() {
    return {
      tooltipValue: null,
      tooltipValueDate: null,
      showTooltip: false,
      toolTipStyle: TooltipConfiguration.driftChart,
      finalXCoordinate: "",
      finalYCoordinate: "",
    }
  },

  watch: {
    chartDimensions: {
      handler() {
        d3Select.select(this.$refs["hux-drift-chart"]).selectAll("svg").remove()
        this.generateChart()
      },
      immediate: false,
      deep: true,
    },
  },

  mounted() {
    this.generateChart()
  },

  methods: {
    async generateChart() {
      let width = this.chartDimensions.width
      let height = this.chartDimensions.height

      let xAxisMinMaxValue = d3Array.extent(this.value, (d) => d.xAxisValue)
      let yAxisMinMaxValue = d3Array.extent(this.value, (d) => d.yAxisValue)

      // generates an svg and appends to the dom
      let svg = d3Select
        .select(this.$refs["hux-drift-chart"])
        .append("svg")
        .attr("width", width)
        .attr("height", height)

      // function to generate coordinates for x-axis
      let xCoordinateFunction = d3Scale
        .scaleTime()
        .domain(xAxisMinMaxValue)
        .range([this.margin.left, width - this.margin.right])
        .nice(this.xAxisMaxTicks)

      // function to generate coordinates for y-axis
      let yCoordinateFunction = d3Scale
        .scaleLinear()
        .domain(yAxisMinMaxValue)
        .range([height - this.margin.bottom, this.margin.top])
        .nice(this.yAxisMaxTicks)

      // function to map coordinates to line
      let line = d3Shape
        .line()
        .x((d) => xCoordinateFunction(d.xAxisValue))
        .y((d) => yCoordinateFunction(d.yAxisValue))

      // function to map coordinates to line area
      var area = d3Shape
        .area()
        .x((d) => xCoordinateFunction(d.xAxisValue))
        .y0(height - this.margin.bottom)
        .y1((d) => yCoordinateFunction(d.yAxisValue))

      // generates x-axis
      let xAxis = null

      const days =
        1 + d3Time.timeDay.count(xAxisMinMaxValue[0], xAxisMinMaxValue[1])
      if (days <= 7) {
        xAxis = svg
          .append("g")
          .attr("transform", `translate(0,${height - this.margin.bottom})`)
          .classed("xAxis", true)
          .style("font-size", 14)
          .call(
            d3Axis
              .axisBottom(xCoordinateFunction)
              .tickSize(this.enableGrid[0] ? -height : 0)
              .ticks(d3Time.timeDay)
              .tickPadding(this.tickPadding)
              .tickFormat(d3TimeFormat.timeFormat(this.xAxisFormat))
          )
      } else if (days <= 100) {
        xAxis = svg
          .append("g")
          .attr("transform", `translate(0,${height - this.margin.bottom})`)
          .classed("xAxis", true)
          .style("font-size", 14)
          .call(
            d3Axis
              .axisBottom(xCoordinateFunction)
              .tickSize(this.enableGrid[0] ? -height : 0)
              .ticks(d3Time.timeWeek)
              .tickPadding(this.tickPadding)
              .tickFormat(d3TimeFormat.timeFormat(this.xAxisFormat))
          )
      } else {
        xAxis = svg
          .append("g")
          .attr("transform", `translate(0,${height - this.margin.bottom})`)
          .classed("xAxis", true)
          .style("font-size", 14)
          .call(
            d3Axis
              .axisBottom(xCoordinateFunction)
              .tickSize(this.enableGrid[0] ? -height : 0)
              .ticks(d3Time.timeMonth)
              .tickPadding(this.tickPadding)
              .tickFormat(d3TimeFormat.timeFormat(this.xAxisFormat))
          )
      }

      // generates y-axis
      let yAxis = svg
        .append("g")
        .attr("transform", `translate(${this.margin.left},0)`)
        .style("font-size", 14)
        .call(
          d3Axis
            .axisLeft(yCoordinateFunction)
            .ticks(this.yAxisMaxTicks)
            .tickSize(this.enableGrid[1] ? -width : 0)
            .tickPadding(this.tickPadding)
            .tickFormat((d) => this.yAxisFormatingFunc(d))
        )

      if (this.enableGrid[0]) {
        xAxis
          .selectAll("line")
          .attr("y2", this.margin.top + this.margin.bottom - height)
      }
      if (this.enableGrid[1]) {
        yAxis
          .selectAll("line")
          .attr("x2", width - this.margin.right - this.margin.left)
      }

      // generates line
      svg
        .append("path")
        .datum(this.value)
        .attr("fill", "none")
        .attr("stroke", this.lineColor)
        .attr("stroke-width", 2)
        .attr("stroke-linejoin", "round")
        .attr("stroke-linecap", "round")
        .attr("d", line)

      // fill area under line
      svg
        .append("path")
        .datum(this.value)
        .attr("d", area)
        .style("opacity", 0.15)
        .style("fill", this.lineColor)

      // enables x-axis and y-axis lines
      if (!this.enableAxisLines) {
        svg.selectAll(".domain").call((g) => g.remove())
      }

      // Changes the color of the tick lines
      svg.selectAll("line").attr("stroke", this.tickColor)
      svg.selectAll("text").attr("fill", this.axisTextColor)

      // Changes the color of the axis lines
      svg.selectAll(".domain").attr("fill", this.tickColor)

      svg.select(".xAxis").selectAll("line").style("stroke", "transparent")

      let bisectDate = d3Array.bisector(function (d) {
        return d.xAxisValue
      }).left

      svg
        .append("line")
        .attr("class", "hover-line-x")
        .style("stroke", "#1E1E1E")

      svg
        .append("line")
        .attr("class", "hover-line-y")
        .style("stroke", "#1E1E1E")

      // Shows tooltip
      let tooltip = svg.append("g").style("display", "none")

      tooltip
        .append("circle")
        .attr("r", 5)
        .style("stroke", this.lineColor)
        .style("fill", "white")
        .style("stroke-width", "1")

      svg
        .append("rect")
        .attr(
          "width",
          width - this.margin.right > 0
            ? width - this.margin.right - this.margin.left
            : 0
        )
        .attr("transform", `translate(${this.margin.left},${this.margin.top})`)
        .attr(
          "height",
          height - this.margin.bottom > 0
            ? height - this.margin.bottom - this.margin.top
            : 0
        )
        .style("stroke", "transparent")
        .style("fill", "transparent")
        .on("mouseover", () => {
          this.showTooltip = false
          this.tooltipValue = null
          this.tooltipValueDate = null
          tooltip.style("display", null)
          svg.selectAll(".hover-line-x").style("display", null)
          svg.selectAll(".hover-line-y").style("display", null)
        })
        .on("mouseout", () => {
          this.showTooltip = false
          this.tooltipValue = null
          this.tooltipValueDate = null
          tooltip.style("display", "none")
          svg.selectAll(".hover-line-x").style("display", "none")
          svg.selectAll(".hover-line-y").style("display", "none")
        })
        .on("mousemove", (mouseEvent) => mousemove(mouseEvent, this.value))

      let mousemove = (mouseEvent, data) => {
        let x0 = xCoordinateFunction.invert(d3Select.pointer(mouseEvent)[0])
        let i = bisectDate(data, x0, 1)
        let d0 = data[i - 1]
        let d1 = data[i] || {}
        let d = x0 - d0.xAxisValue > d1.xAxisValue - x0 ? d1 : d0

        this.finalXCoordinate = xCoordinateFunction(d.xAxisValue)
        this.finalYCoordinate = yCoordinateFunction(d.yAxisValue)

        svg
          .selectAll(".hover-line-x")
          .attr("x1", this.margin.left)
          .attr("x2", width - this.margin.right)
          .attr("y1", this.finalYCoordinate)
          .attr("y2", this.finalYCoordinate)

        svg
          .selectAll(".hover-line-y")
          .attr("x1", this.finalXCoordinate)
          .attr("x2", this.finalXCoordinate)
          .attr("y1", this.margin.top)
          .attr("y2", height - this.margin.bottom)

        tooltip.attr(
          "transform",
          `translate(${this.finalXCoordinate},${this.finalYCoordinate})`
        )

        this.showTooltip = true
        this.tooltipValue = d.yAxisValue
        this.tooltipValueDate = d.xAxisValue
      }
    },
  },
}
</script>
<style lang="scss" scoped>
.dot {
  height: 12px;
  width: 12px;
  background-color: var(--v-primary-darken2);
  border-radius: 50%;
  display: inline-block;
}
.margin-sides-dec {
  margin-left: -5px;
  margin-right: -5px;
}
</style>
