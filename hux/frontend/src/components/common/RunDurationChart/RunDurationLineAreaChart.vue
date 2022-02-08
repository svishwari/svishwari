<template>
  <div class="chart-container" :style="{ maxWidth: chartWidth }">
    <div ref="lineAreaChart" class="chart-section"></div>
    <div></div>
  </div>
</template>

<script>
import * as d3Axis from "d3-axis"
import * as d3Shape from "d3-shape"
import * as d3Scale from "d3-scale"
import * as d3Select from "d3-selection"
import * as d3Array from "d3-array"
import * as d3Transition from "d3-transition"

export default {
  name: "RunDurationLineAreaChart",
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
    finalStatus: {
      type: String,
      required: false,
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
    initiatelineAreaChart() {
      this.chartWidth = this.chartDimensions.width + "px"
      this.width = this.chartDimensions.width
      this.height = this.chartDimensions.height
      let margin = { top: 15, right: 45, bottom: 100, left: 75 }
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

      let xScale = d3Scale.scaleLinear().rangeRound([0, w]).domain([1, 10])

      let yScale = d3Scale
        .scaleLinear()
        .rangeRound([h, 0])
        .domain([0, d3Array.max(this.data, (d) => d.duration)])
        .nice(3)

      let stackArea = d3Shape.stack().keys(["duration"])

      let areaData = []

      stackArea(this.data).forEach((layer) => {
        let currentStack = []
        layer.forEach((d) => {
          d[1] = d[1] - d[0]
          d[0] = 0
          currentStack.push({
            values: d,
            index: d.data.index,
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
            .ticks(10)
            .tickPadding(15)
            .tickFormat("")
        )
        .style("font-size", "14px")

      svg
        .append("g")
        .classed("yAlternateAxis", true)
        .attr("transform", "translate(0, 0)")
        .call(d3Axis.axisLeft(yScale).tickSize(6).ticks(3).tickFormat(""))
        .attr("stroke-width", "1")
        .attr("stroke-opacity", "1")
        .style("font-size", "12px")

      svg
        .append("g")
        .classed("xAxis", true)
        .attr("transform", `translate(0,${h})`)
        .call(d3Axis.axisBottom(xScale).tickSize(-h).ticks(10).tickPadding(15))
        .style("font-size", "14px")

      svg
        .append("g")
        .classed("yAxis", true)
        .attr("transform", "translate(0, 0)")
        .call(d3Axis.axisLeft(yScale).tickSize(-w).ticks(3).tickPadding(15))
        .attr("stroke-width", "1")
        .attr("stroke-opacity", "1")
        .style("font-size", "14px")

      svg
        .append("text")
        .classed("appendtext", true)
        .attr(
          "transform",
          "translate(-55," + this.height / 3 + ") rotate(-90 )"
        )
        .attr("fill", "#000000")
        .style("text-anchor", "middle")
        .style("color", "#000000")
        .style("font-size", "14px")
        .text("Time (minutes)")

      svg
        .append("text")
        .classed("appendtext", true)
        .attr(
          "transform",
          "translate(" +
            (this.width / 2 - 80) +
            "," +
            (this.height - 65) +
            ") rotate(-360)"
        )
        .attr("fill", "#000000")
        .style("text-anchor", "middle")
        .style("color", "#000000")
        .style("font-size", "14px")
        .text("Runs")

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
          .x(value ? 0 : (d) => xScale(d.index))
          .y(value ? h : (d) => yScale(d.duration))
      }

      let area = d3Shape
        .area()
        .x((dataPoint) => xScale(dataPoint.index))
        .y0((dataPoint) => yScale(dataPoint.values[0]))
        .y1((dataPoint) => yScale(dataPoint.values[1]))

      svg
        .selectAll(".area")
        .data(areaData)
        .enter()
        .append("path")
        .style("fill", "#9DD4CF")
        .attr("stroke-width", 2)
        .attr("fill-opacity", 0.2)
        .attr("d", (d) => area(d))

      svg
        .append("path")
        .datum(this.data)
        .attr("class", "line")
        .style("stroke", "#9DD4CF")
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
        .attr("cx", (d) => xScale(d.index))
        .attr("cy", (d) => yScale(d.duration))
        .style("fill", "transparent")
        .attr("stroke", "transparent")

      svg
        .append("line")
        .attr("class", "hover-line-y")
        .style("stroke", "#1E1E1E")
        .style("stroke-width", 1)

      svg
        .append("circle")
        .classed("final-circle", true)
        .attr("cx", xScale(this.data[this.data.length - 1].index))
        .attr("cy", yScale(this.data[this.data.length - 1].duration))
        .attr("r", 5)
        .style("fill", this.finalStatus === "Success" ? "#43B02A" : "#DA291C")
        .style("pointer-events", "none")
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

        let data = this.data.map((d) => d.index)
        let x0 = xScale.invert(d3Select.pointer(mouseEvent)[0])

        let i = bisectDate(data, x0, 1)
        let d0 = data[i - 1]
        let d1 = data[i] || {}
        let d = x0 - d0 > d1 - x0 ? d1 : d0
        let dateD = d
        let finalXCoordinate = xScale(dateD)
        let yData = {}
        let dataToolTip = this.data.find((element) => element.index == dateD)

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
              .style("stroke", "#9DD4CF")
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
