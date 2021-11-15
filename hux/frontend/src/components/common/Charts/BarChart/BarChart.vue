<template>
  <div class="chart-container" :style="{ maxWidth: chartWidth }">
    <div ref="barChart" class="chart-section"></div>
  </div>
</template>

<script>
import * as d3Axis from "d3-axis"
import * as d3Shape from "d3-shape"
import * as d3Scale from "d3-scale"
import * as d3Select from "d3-selection"
import * as d3Array from "d3-array"

export default {
  name: "BarChart",
  props: {
    value: {
      type: Array,
      required: true,
    },
    emptyState: {
      type: Boolean,
      default: false,
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
    barGroupChangeIndex: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      chartWidth: "",
      customerEventData: this.value,
      toolTip: {
        xPosition: 0,
        yPosition: 0,
        index: 0,
        date: "",
        total_event_count: 0,
        event_type_counts: {},
      },
    }
  },
  watch: {
    chartDimensions: {
      handler() {
        d3Select.select(this.$refs.barChart).selectAll("svg").remove()
        this.initiateBarChart()
      },
      immediate: false,
      deep: true,
    },
  },

  methods: {
    async initiateBarChart() {
      await this.value
      this.chartWidth = this.chartDimensions.width + "px"
      this.width = this.chartDimensions.width
      this.height = this.chartDimensions.height
      let margin = { top: 15, right: 30, bottom: 100, left: 68 }
      let w = this.chartDimensions.width - margin.left - margin.right
      let h = this.chartDimensions.height - margin.top - margin.bottom
      let chartHeight = this.height - 35

      let svg = d3Select
        .select(this.$refs.barChart)
        .append("svg")
        .attr("width", this.width + margin.left + margin.right)
        .attr("height", chartHeight)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`)

      let stack = d3Shape.stack().keys(["total_event_count"])

      let stackedValues = stack(this.customerEventData)

      stackedValues.forEach((layer) => {
        layer.forEach((d) => {
          d[1] = d[1] - d[0]
          d[0] = 0
        })
      })

      let xScale = d3Scale
        .scaleBand()
        .domain(d3Array.range(this.customerEventData.length))
        .range([0, w])
        .paddingInner(0.22)
        .paddingOuter(0.11)

      let yScale = d3Scale
        .scaleLinear()
        .domain([
          0,
          this.emptyState
            ? 100
            : d3Array.max(this.customerEventData, (d) => d.total_event_count),
        ])
        .range([h, 0])
        .nice(5)

      let hideInitialTick =
        this.customerEventData.filter(
          (bar) => bar.index == 0 && bar.barIndex < 5
        ).length < 3

      let convertCalendarFormat = (value) => {
        let tickDate = this.barGroupChangeIndex.find(
          (bar) => bar.index == value
        )
        if (tickDate && tickDate.index == 0 && hideInitialTick) {
          return ""
        }
        if (tickDate && tickDate.index == this.customerEventData.length - 1) {
          return ""
        }
        return tickDate
          ? this.emptyState
            ? "date"
            : this.$options.filters.Date(tickDate.date, "MM[/01/]YY")
          : ""
      }

      let applyNumericFilter = (value) =>
        this.emptyState ? "-" : this.$options.filters.Numeric(value, true, true)

      svg
        .append("g")
        .classed("xAxis-main", true)
        .attr("transform", `translate(0,${h})`)
        .call(
          d3Axis
            .axisBottom(xScale)
            .tickSize(0)
            .tickFormat(convertCalendarFormat)
            .tickPadding(15)
        )
        .style("font-size", "14px")

      svg
        .append("g")
        .classed("yAxis-main", true)
        .attr("transform", "translate(0, 0)")
        .call(d3Axis.axisLeft(yScale).ticks(5).tickFormat(applyNumericFilter))
        .attr("stroke-width", "1")
        .attr("stroke-opacity", "1")
        .style("font-size", "14px")

      svg
        .append("g")
        .classed("yAxis-alternate", true)
        .attr("transform", "translate(0, 0)")
        .call(d3Axis.axisLeft(yScale).tickSize(-w).ticks(5).tickFormat(""))
        .attr("stroke-width", "0.5")
        .attr("stroke-opacity", "1")
        .style("font-size", "12px")

      d3Select
        .selectAll(".yAxis-alternate .tick line")
        .style("stroke", "#E2EAEC")

      let bars = svg.append("g").attr("class", "bars")

      let groups = bars
        .selectAll("g")
        .data(stackedValues)
        .enter()
        .append("g")
        .style("fill-opacity", (d, i) => {
          if (i == 0) {
            return 0.5
          } else {
            return 1
          }
        })

      d3Select.selectAll(".domain").style("stroke", "transparent")
      d3Select.selectAll(".tick line").style("stroke", "#E2EAEC")
      d3Select
        .selectAll(".xAxis-main .tick text")
        .attr("x", 10)
        .style("color", "#4F4F4F")
      d3Select.selectAll(".yAxis-main .tick text").style("color", "#4F4F4F")
      d3Select.selectAll(".xAxis-main .tick text").attr("x", 16)

      svg
        .append("line")
        .attr("class", "hover-line-y")
        .style("stroke", "#1E1E1E")
        .style("stroke-width", 1)
        .style("pointer-events", "none")

      let barWidth = xScale.bandwidth() < 30 ? xScale.bandwidth() : 30

      groups
        .selectAll("bar")
        .data((d) => d)
        .enter()
        .append("rect")
        .attr("data", (d, i) => i)
        .style("fill", this.emptyState ? "transparent" : "#9DD4CF")
        .on("mouseover", (d) => applyHoverEffects(d))
        .on("mouseout", (d) => removeHoverEffects(d))
        .attr("height", (d) => yScale(d[0]) - yScale(d[1]))
        .attr("width", barWidth)
        .attr("x", (d, i) => xScale(i))
        .attr("y", (d) => yScale(d[1]))
        .attr("rx", 2)
        .attr("ry", 2)
        .attr("d", (d) => d)

      let applyHoverEffects = (d) => {
        d3Select.select(d.srcElement).attr("fill-opacity", (d) => {
          barHoverIn(d.data)
          return 1
        })
      }

      let hoverCircles = ["foreGroundParentCircle", "foreGroundChildCircle"]

      let removeHoverEffects = (d) => {
        d3Select.select(d.srcElement).attr("fill-opacity", 0.5)
        svg.selectAll(".hover-line-y").style("display", "none")
        hoverCircles.forEach((circleName) => removeHoverCircle(circleName))
        this.tooltipDisplay(false)
      }

      let barHoverIn = (data) => {
        this.toolTip.xPosition = xScale(data.barIndex) + 40
        this.toolTip.yPosition = yScale(data.total_event_count)
        this.toolTip.date = data.date
        this.toolTip.total_event_count = data.total_event_count
        this.toolTip.event_type_counts = data.event_type_counts
        this.toolTip.index = data.index
        this.toolTip.isEndingBar = data.isEndingBar
        this.tooltipDisplay(true, this.toolTip)

        svg
          .selectAll(".hover-line-y")
          .attr("x1", xScale(data.barIndex) + barWidth / 2)
          .attr("x2", xScale(data.barIndex) + barWidth / 2)
          .attr("y1", 0)
          .attr("y2", h)
          .style("display", "block")

        addHoverCircle(
          hoverCircles[0],
          5,
          data.barIndex,
          data.total_event_count,
          "white"
        )
        addHoverCircle(
          hoverCircles[1],
          4,
          data.barIndex,
          data.total_event_count,
          "#9DD4CF"
        )
      }

      let addHoverCircle = (circleName, circleRadius, cX, cY, strokeColor) => {
        svg
          .append("circle")
          .classed(circleName, true)
          .attr("cx", xScale(cX) + barWidth / 2)
          .attr("cy", yScale(cY))
          .attr("r", circleRadius)
          .style("stroke", strokeColor)
          .style("stroke-opacity", 1)
          .style("stroke-width", 2)
          .style("fill", "white")
          .style("pointer-events", "none")
      }

      let removeHoverCircle = (circleName) => {
        d3Select.select(this.$refs.barChart).select(`.${circleName}`).remove()
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
