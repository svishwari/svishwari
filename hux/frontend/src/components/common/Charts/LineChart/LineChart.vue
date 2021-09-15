<template>
  <div class="chart-container" :style="{ maxWidth: chartWidth }">
    <div ref="lineChart" class="chart-section"></div>
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
  name: "LineChart",
  props: {
    value: {
      type: Array,
      required: true,
    },
    colorCodes: {
      type: Array,
      required: false,
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
      data: this.value,
      chartWidth: "",
      toolTip: {
        xPosition: 0,
        yPosition: 0,
        index: 0,
        date: "",
        totalCustomers: 0,
        addedCustomers: 0,
      },
    }
  },

  watch: {
    chartDimensions: {
      handler() {
        d3Select.select(this.$refs.lineChart).selectAll("svg").remove()
        this.initiateLineChart()
      },
      immediate: false,
      deep: true,
    },
  },
  methods: {
    async initiateLineChart() {
      await this.value
      this.chartWidth = this.chartDimensions.width + "px"
      this.width = this.chartDimensions.width
      this.height = this.chartDimensions.height
      let margin = { top: 15, right: 45, bottom: 100, left: 48 }
      let w = this.chartDimensions.width - margin.left - margin.right
      let h = this.chartDimensions.height - margin.top - margin.bottom

       d3Select.select(this.$refs.lineChart).selectAll("svg").remove()

      let svg = d3Select
        .select(this.$refs.lineChart)
        .append("svg")
        .attr("width", this.width + margin.left + margin.right)
        .attr("height", this.height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`)

      let dateFormatter = (value) =>
        this.$options.filters.Date(value, "MM/DD/YYYY")

      let xScale = d3Scale
        .scaleTime()
        .rangeRound([0, w])
        .domain(
          d3Array.extent(this.data, (d) => new Date(dateFormatter(d.date)))
        )
        .nice(8)

      let yScale = d3Scale
        .scaleLinear()
        .rangeRound([h, 0])
        .domain([0, d3Array.max(this.data, (d) => d.total_event_count)])
        .nice(2)

      svg
        .append("g")
        .classed("xAlternateAxis", true)
        .attr("transform", `translate(0,${h})`)
        .call(
          d3Axis
            .axisBottom(xScale)
            .tickSize(10)
            .ticks(8)
            .tickPadding(15)
            .tickFormat("")
        )
        .style("font-size", "14px")

      svg
        .append("g")
        .classed("yAlternateAxis", true)
        .attr("transform", "translate(0, 0)")
        .call(d3Axis.axisLeft(yScale).tickSize(10).ticks(4).tickFormat(""))
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
            .ticks(8)
            .tickPadding(15)
            .tickFormat(d3TimeFormat.timeFormat("%m/%d/%y"))
        )
        .style("font-size", "12px")

      svg
        .append("g")
        .classed("yAxis", true)
        .attr("transform", "translate(0, 0)")
        .call(d3Axis.axisLeft(yScale).tickSize(-w).ticks(4).tickPadding(15))
        .attr("stroke-width", "1")
        .attr("stroke-opacity", "1")
        .style("font-size", "12px")

      d3Select.selectAll(".domain").style("stroke", "#E2EAEC")
      d3Select.selectAll(".tick line").style("stroke", "#E2EAEC")
      d3Select
        .selectAll(".xAxis .tick text")
        .attr("x", 10)
        .style("color", "#4F4F4F")
      d3Select.selectAll(".yAxis .tick text").style("color", "#4F4F4F")
      d3Select.selectAll(".yAlternateAxis .tick line").style("stroke", "black")
      d3Select.selectAll(".xAlternateAxis .tick line").style("stroke", "black")

      d3Transition.transition()

      let lineTrace = (value) => {
        return d3Shape
          .line()
          .x(value ? 0 : (d) => xScale(new Date(dateFormatter(d.date))))
          .y(value ? h : (d) => yScale(d.total_event_count))
      }

      svg
        .append("path")
        .datum(this.data)
        .attr("class", "line")
        .style("stroke", "#9DD4CF")
        .style("stroke-width", 2)
        .style("fill", "transparent")
        .attr("d", lineTrace(0))
        .transition()
        .duration(1000)
        .delay((d, i) => i * 15)
        .attr("d", lineTrace())

      svg
        .selectAll("bar")
        .data(this.data)
        .enter()
        .append("circle")
        .attr("class", "dot")
        .attr("r", 4)
        .attr("cx", (d) => xScale(new Date(dateFormatter(d.date))))
        .attr("cy", (d) => yScale(d.total_event_count))
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

      let bisectDate = d3Array.bisector((d) => d).left

      let mouseout = () => {
        svg.selectAll(".hover-line-y").style("display", "none")
        svg.selectAll(".hover-circle").remove()
        this.tooltipDisplay(false)
      }

      let mousemove = (mouseEvent) => {
        svg.selectAll(".hover-circle").remove()
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
              .classed("hover-circle", true)
              .attr("cx", finalXCoordinate)
              .attr("cy", yPosition)
              .attr("r", 5.5)
              .style("stroke", "#9DD4CF")
              .style("stroke-opacity", "1")
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
