<template>
  <div class="chart-container" :style="{ maxWidth: chartWidth }">
    <div ref="lineAreaChart" class="chart-section"></div>
  </div>
</template>

<script>
import * as d3Axis from "d3-axis"
import * as d3Shape from "d3-shape"
import * as d3Scale from "d3-scale"
import * as d3Select from "d3-selection"
import * as d3Array from "d3-array"
import * as d3TimeFormat from "d3-time-format"
import * as d3Transition from "d3-transition"

export default {
  name: "LineAreaChart",
  props: {
    value: {
      type: Array,
      required: true,
    },
    chartDimensions: {
      type: Object,
      required: false,
      default() {
        return {
          width: 600,
          height: 350,
        }
      },
    },
  },
  data() {
    return {
      data: this.value,
      chartWidth: "",
      toolTip: {
        xPosition: 0,
        yPosition: 0,
        date: "",
        spend: 0,
      },
    }
  },

  watch: {
    chartDimensions: {
      handler() {
        d3Select.select(this.$refs.lineAreaChart).selectAll("svg").remove()
        this.initiatelineAreaChart()
      },
      immediate: false,
      deep: true,
    },
  },
  methods: {
    async initiatelineAreaChart() {
      await this.value
      this.chartWidth = this.chartDimensions.width + "px"
      this.width = this.chartDimensions.width
      this.height = this.chartDimensions.height
      let margin = { top: 15, right: 45, bottom: 100, left: 60 }
      let w = this.chartDimensions.width - margin.left - margin.right
      let h = this.chartDimensions.height - margin.top - margin.bottom

      d3Select.select(this.$refs.lineAreaChart).selectAll("svg").remove()

      let svg = d3Select
        .select(this.$refs.lineAreaChart)
        .append("svg")
        .classed("main-svg", true)
        .attr("width", this.width + margin.left + margin.right)
        .attr("height", this.height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`)

      let dateFormatter = (value) =>
        this.$options.filters.Date(value, "MM/DD/YYYY")

      let appendyAxisFormat = (text) =>
        `$${this.$options.filters.Numeric(text, false, true, false)}`

      let xScale = d3Scale
        .scaleTime()
        .rangeRound([0, w])
        .domain(
          d3Array.extent(this.data, (d) => new Date(dateFormatter(d.date)))
        )

      let yScale = d3Scale
        .scaleLinear()
        .rangeRound([h, 0])
        .domain([0, d3Array.max(this.data, (d) => d.spend)])
        .nice(5)

      let stackArea = d3Shape.stack().keys(["spend"])

      let areaData = []

      stackArea(this.data).forEach((layer) => {
        let currentStack = []
        layer.forEach((d) => {
          d[1] = d[1] - d[0]
          d[0] = 0
          currentStack.push({
            values: d,
            date: new Date(dateFormatter(d.data.date)),
          })
        })
        areaData.push(currentStack)
      })

      svg
        .append("g")
        .classed("xAlternateAxis", true)
        .attr("transform", `translate(0,${h})`)
        .call(
          d3Axis
            .axisBottom(xScale)
            .tickSize(10)
            .ticks(6)
            .tickPadding(15)
            .tickFormat("")
        )
        .style("font-size", "14px")

      svg
        .append("g")
        .classed("yAlternateAxis", true)
        .attr("transform", "translate(0, 0)")
        .call(d3Axis.axisLeft(yScale).tickSize(6).ticks(5).tickFormat(""))
        .attr("stroke-width", "1")
        .attr("stroke-opacity", "1")
        .style("font-size", "12px")

      svg
        .append("g")
        .classed("xAxis", true)
        .attr("transform", `translate(0,${h})`)
        .call(
          d3Axis
            .axisBottom(xScale)
            .tickSize(-h)
            .ticks(6)
            .tickPadding(15)
            .tickFormat(d3TimeFormat.timeFormat("%m/%Y"))
        )
        .style("font-size", "14px")

      svg
        .append("g")
        .classed("yAxis", true)
        .attr("transform", "translate(0, 0)")
        .call(
          d3Axis
            .axisLeft(yScale)
            .tickSize(-w)
            .ticks(5)
            .tickPadding(15)
            .tickFormat(appendyAxisFormat)
        )
        .attr("stroke-width", "1")
        .attr("stroke-opacity", "1")
        .style("font-size", "14px")

      d3Select.selectAll(".domain").style("stroke", "#E2EAEC")
      d3Select.selectAll(".tick line").style("stroke", "#E2EAEC")
      d3Select
        .selectAll(".xAxis .tick text")
        .attr("x", 10)
        .style("color", "#4F4F4F")
      d3Select.selectAll(".yAxis .tick text").style("color", "#4F4F4F")
      d3Select
        .selectAll(".yAlternateAxis .tick line")
        .style("stroke", "#E2EAEC")
      d3Select
        .selectAll(".xAlternateAxis .tick line")
        .style("stroke", "#E2EAEC")

      d3Transition.transition()

      let lineTrace = (value) => {
        return d3Shape
          .line()
          .x(value ? 0 : (d) => xScale(new Date(dateFormatter(d.date))))
          .y(value ? h : (d) => yScale(d.spend))
      }

      let area = d3Shape
        .area()
        .x((dataPoint) => xScale(new Date(dateFormatter(dataPoint.date))))
        .y0((dataPoint) => yScale(dataPoint.values[0]))
        .y1((dataPoint) => yScale(dataPoint.values[1]))

      svg
        .selectAll(".area")
        .data(areaData)
        .enter()
        .append("path")
        .style("fill", "#0C9DDB")
        .attr("stroke-width", 2)
        .attr("fill-opacity", 0.2)
        .attr("d", (d) => area(d))

      svg
        .append("path")
        .datum(this.data)
        .attr("class", "line")
        .style("stroke", "#0C9DDB")
        .style("stroke-width", 3)
        .style("fill", "transparent")
        .attr("d", lineTrace())

      svg
        .selectAll("area")
        .data(this.data)
        .enter()
        .append("circle")
        .attr("class", "dot")
        .attr("r", 4)
        .attr("cx", (d) => xScale(new Date(dateFormatter(d.date))))
        .attr("cy", (d) => yScale(d.spend))
        .style("fill", "transparent")
        .attr("stroke", "transparent")

      svg
        .append("line")
        .attr("class", "hover-line-y")
        .style("stroke", "#1E1E1E")
        .style("stroke-width", 1)

      svg
        .append("rect")
        .attr("width", w)
        .attr("height", h)
        .style("stroke", "transparent")
        .style("fill", "transparent")
        .on("mousemove", (mouseEvent) => mousemove(mouseEvent))
        .on("mouseout", () => mouseout())

      let bisectDate = d3Array.bisector((d) => d).right

      let mouseout = () => {
        svg.selectAll(".hover-line-y").style("display", "none")
        svg.selectAll(".parent-hover-circle").remove()
        svg.selectAll(".child-hover-circle").remove()
        this.tooltipDisplay(false)
      }

      let mousemove = (mouseEvent) => {
        svg.selectAll(".parent-hover-circle").remove()
        svg.selectAll(".child-hover-circle").remove()
        this.tooltipDisplay(false)

        let data = this.data.map((d) => dateFormatter(d.date))
        let x0 = dateFormatter(xScale.invert(d3Select.pointer(mouseEvent)[0]))

        let i = bisectDate(data, x0, 1)
        let d0 = data[i - 1]
        let d1 = data[i] || {}
        let d = x0 - d0 > d1 - x0 ? d1 : d0
        let dateD = dateFormatter(d)
        let finalXCoordinate = xScale(new Date(dateD))
        let yData = {}
        let dataToolTip = this.data.find(
          (element) => dateFormatter(element.date) == dateD
        )

        svg
          .selectAll(".hover-line-y")
          .attr("x1", finalXCoordinate)
          .attr("x2", finalXCoordinate)
          .attr("y1", 0)
          .attr("y2", h)
          .style("display", "block")

        svg.selectAll(".dot").each(function () {
          if (this.getAttribute("cx") == finalXCoordinate) {
            let yPosition = this.getAttribute("cy")
            yData = yPosition
            svg
              .append("circle")
              .classed("parent-hover-circle", true)
              .attr("cx", finalXCoordinate)
              .attr("cy", yPosition)
              .attr("r", 9)
              .style("stroke", "white")
              .style("stroke-opacity", "1")
              .style("stroke-width", 1)
              .style("fill", "white")
              .style("pointer-events", "none")

            svg
              .append("circle")
              .classed("child-hover-circle", true)
              .attr("cx", finalXCoordinate)
              .attr("cy", yPosition)
              .attr("r", 7)
              .style("stroke", "#0C9DDB")
              .style("stroke-opacity", "1")
              .style("stroke-width", 2)
              .style("fill", "white")
              .style("pointer-events", "none")
          }
        })
        dataToolTip.xPosition = finalXCoordinate
        dataToolTip.yPosition = yData
        this.tooltipDisplay(true, dataToolTip)
      }
    },
    tooltipDisplay(showTip, eventsData) {
      this.$emit("tooltipDisplay", showTip, eventsData)
    },
  },
}
</script>

<style lang="scss" scoped>
.chart-container {
  height: 252px;
  position: relative;

  .chart-section {
    margin-bottom: -20px;
  }
}
</style>
