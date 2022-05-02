<template>
  <div class="chart-container" :style="{ maxWidth: chartWidth }">
    <div ref="lineBarChart" class="chart-section"></div>
  </div>
</template>

<script>
import * as d3Axis from "d3-axis"
import * as d3Shape from "d3-shape"
import * as d3Scale from "d3-scale"
import * as d3Select from "d3-selection"
import * as d3Array from "d3-array"
import * as d3Transition from "d3-transition"
import colors from "../../../../plugins/theme"

export default {
  name: "LineBarChart",
  props: {
    value: {
      type: Object,
      required: true,
    },
    colorCodes: {
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
      lastBarAnimation: "",
      chartWidth: "",
      emailData: {},
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
        d3Select.select(this.$refs.lineBarChart).selectAll("svg").remove()
        clearInterval(this.lastBarAnimation)
        this.initiateLineBarChart()
      },
      immediate: false,
      deep: true,
    },
  },
  destroyed() {
    clearInterval(this.lastBarAnimation)
  },
  methods: {
    async initiateLineBarChart() {
      await this.value
      this.emailData = this.value.sourceData
      this.chartWidth = this.chartDimensions.width + "px"
      this.width = this.chartDimensions.width
      this.height = this.chartDimensions.height
      let margin = { top: 15, right: 60, bottom: 100, left: 40 }
      let w = this.chartDimensions.width - margin.left - margin.right
      let h = this.chartDimensions.height - margin.top - margin.bottom
      let barColorCodes = []

      let svg = d3Select
        .select(this.$refs.lineBarChart)
        .append("svg")
        .attr("width", this.width + margin.left + margin.right)
        .attr("height", this.height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`)

      this.colorCodes.forEach((color) => {
        if (color.variant == "lighten4") {
          barColorCodes.push(colors.primary[color.variant])
        } else if (color.variant == "lighten6") {
          barColorCodes.push(colors.primary[color.variant])
        } else if (color.variant == "darken1") {
          barColorCodes.push(colors.primary[color.variant])
        } else {
          barColorCodes.push(colors.success[color.variant])
        }
      })

      let stack = d3Shape.stack().keys(["delivered_count"])

      let stackedValues = stack(this.emailData)
      d3Transition.transition()

      stackedValues.forEach((layer) => {
        layer.forEach((d) => {
          d[1] = d[1] - d[0]
          d[0] = 0
        })
      })

      let xScale = d3Scale
        .scaleBand()
        .domain(d3Array.range(this.emailData.length))
        .range([0, w])
        .paddingInner(0.55)
        .paddingOuter(0.11)

      let yScale1 = d3Scale
        .scaleLinear()
        .domain([
          0,
          this.emptyState
            ? 100
            : d3Array.max(this.emailData, (d) => d.delivered_count),
        ])
        .range([h, 0])
        .nice(5)

      let yScale2 = d3Scale.scaleLinear().domain([0, 1.0]).range([h, 0]).nice(5)

      let hideInitialTick =
        this.emailData.filter((bar) => bar.index == 0 && bar.barIndex < 5)
          .length < 3

      let barWidth = xScale.bandwidth() < 40 ? xScale.bandwidth() : 40

      let convertCalendarFormat = (value) => {
        let tickDate = this.barGroupChangeIndex.find(
          (bar) => bar.index == value
        )
        if (tickDate && tickDate.index == 0 && hideInitialTick) {
          return ""
        }
        if (tickDate && tickDate.index == this.emailData.length - 1) {
          return ""
        }
        return tickDate
          ? this.emptyState
            ? "date"
            : this.$options.filters.Date(
                tickDate.date,
                this.value.monthsDuration == 6 ? "MM[/]YYYY" : "MM[/01/]YY"
              )
          : ""
      }

      let applyNumericFilter = (value) =>
        this.emptyState ? "-" : this.$options.filters.Numeric(value, true, true)

      let applyPercentageFilter = (value) =>
        this.emptyState
          ? "-"
          : this.$options.filters.Numeric(value, true, false, false, true)

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
        .call(d3Axis.axisLeft(yScale1).ticks(4).tickFormat(applyNumericFilter))
        .attr("stroke-width", "1")
        .attr("stroke-opacity", "1")
        .style("font-size", "14px")

      svg
        .append("g")
        .classed("yAxis-mirror", true)
        .attr("transform", `translate(${w}, 0)`)
        .call(
          d3Axis.axisRight(yScale2).ticks(4).tickFormat(applyPercentageFilter)
        )
        .attr("stroke-width", "1")
        .attr("stroke-opacity", "1")
        .style("font-size", "14px")

      svg
        .append("g")
        .classed("yAxis-alternate", true)
        .attr("transform", "translate(0, 0)")
        .call(d3Axis.axisLeft(yScale1).tickSize(-w).ticks(4).tickFormat(""))
        .attr("stroke-width", "0.5")
        .attr("stroke-opacity", "1")
        .style("font-size", "12px")

      d3Select
        .selectAll(".yAxis-alternate .tick line")
        .style("stroke", "#E2EAEC")

      let bars = svg.append("g").attr("class", "bars")
      let lineStock = d3Shape
        .line()
        .x((dataPoint) => xScale(dataPoint.data.barIndex))
        .y((dataPoint) => yScale2(dataPoint.data.open_rate))

      let groups = bars
        .selectAll("g")
        .data(stackedValues)
        .enter()
        .append("g")
        .attr("class", "backGroundBars")
        .style("fill-opacity", 0.8)

      d3Select.selectAll(".domain").style("stroke", "#E2EAEC")
      d3Select.selectAll(".tick line").style("stroke", "#E2EAEC")
      d3Select
        .selectAll(".xAxis-main .tick text")
        .attr("x", 10)
        .style("color", "#4F4F4F")
      d3Select.selectAll(".yAxis-main .tick text").style("color", "#4F4F4F")
      d3Select.selectAll(".yAxis-mirror .domain").style("stroke", "transparent")
      if (this.value.monthsDuration == 6) {
        d3Select.selectAll(".xAxis-main .tick text").attr("x", 18)
      } else {
        d3Select.selectAll(".xAxis-main .tick text").attr("x", 0)
      }

      svg
        .append("line")
        .attr("class", "hover-line-y")
        .style("stroke", "#1E1E1E")
        .style("stroke-width", 1)
        .style("pointer-events", "none")

      groups
        .selectAll("bar")
        .data((d) => d)
        .enter()
        .append("rect")
        .attr("class", (d, i) => {
          if (i == this.emailData.length - 1) {
            return "active-bar"
          }
        })
        .attr("data", (d, i) => i)
        .style("fill", (d) =>
          this.emptyState ? "transparent" : barColorCodes[d.data.index]
        )
        .on("mouseover", (d) => applyHoverEffects(d, barWidth))
        .on("mouseout", (d) => removeHoverEffects(d))
        .attr("height", (d) => yScale1(d[0]) - yScale1(d[1]))
        .attr("width", barWidth)
        .attr("x", (d, i) => xScale(i))
        .attr("y", (d) => yScale1(d[1]))
        .attr("rx", 2)
        .attr("ry", 2)
        .attr("d", (d) => d)

      groups
        .append("path")
        .attr("transform", "translate(20,0)")
        .attr("class", "line")
        .style("stroke", "#E3E48D")
        .attr("stroke-width", 3)
        .style("fill", "none")
        .attr("d", (d) => lineStock(d))

      let applyHoverEffects = (d, width) => {
        d3Select.select(d.srcElement).attr("fill-opacity", (d) => {
          barHoverIn(d.data, width)
          return 0.9
        })
      }

      let hoverCircles = [
        "foreGroundParentCircle",
        "foreGroundChildCircle",
        "backGroundParentCircle",
        "backGroundChildCircle",
      ]

      let removeHoverEffects = (d) => {
        d3Select.select(d.srcElement).attr("fill-opacity", 0.8)
        svg.selectAll(".hover-line-y").style("display", "none")
        d3Select.selectAll(".foreGroundBars").style("fill-opacity", "1")
        hoverCircles.forEach((circleName) => removeHoverCircle(circleName))
        this.tooltipDisplay(false)
      }

      let barHoverIn = (data, width) => {
        this.toolTip.xPosition = xScale(data.barIndex) + 40
        this.toolTip.yPosition = yScale1(data.delivered_count)
        this.toolTip.date = data.date
        this.toolTip.index = data.index
        this.toolTip.delivered_count = data.delivered_count
        this.toolTip.open_rate = data.open_rate
        this.toolTip.isEndingBar = data.isEndingBar
        this.tooltipDisplay(true, this.toolTip)

        svg
          .selectAll(".hover-line-y")
          .attr("x1", xScale(data.barIndex) + width / 2)
          .attr("x2", xScale(data.barIndex) + width / 2)
          .attr("y1", 0)
          .attr("y2", h)
          .style("display", "block")

        addHoverCircle(
          hoverCircles[0],
          9,
          data.barIndex,
          data.delivered_count,
          width,
          "white",
          2,
          1,
          true
        )
        addHoverCircle(
          hoverCircles[1],
          7,
          data.barIndex,
          data.delivered_count,
          width,
          barColorCodes[data.index],
          2,
          0.7,
          true
        )

        addHoverCircle(
          hoverCircles[2],
          9,
          data.barIndex,
          data.open_rate,
          width,
          "white",
          2,
          1,
          false
        )
        addHoverCircle(
          hoverCircles[3],
          7,
          data.barIndex,
          data.open_rate,
          width,
          "#E3E48D",
          2,
          0.7,
          false
        )
      }

      let blinkLastBar = () => {
        d3Select
          .select(".active-bar")
          .transition()
          .duration(500)
          .style("fill-opacity", "0.2")
          .transition()
          .duration(500)
          .style("fill-opacity", "0.5")
      }

      let addHoverCircle = (
        circleName,
        circleRadius,
        cX,
        cY,
        width,
        strokeColor,
        strokeWidth,
        strokeOpacity,
        isBarHover
      ) => {
        svg
          .append("circle")
          .classed(circleName, true)
          .attr("cx", xScale(cX) + width / 2)
          .attr("cy", isBarHover ? yScale1(cY) : yScale2(cY))
          .attr("r", circleRadius)
          .style("stroke", strokeColor)
          .style("stroke-opacity", strokeOpacity)
          .style("stroke-width", strokeWidth)
          .style("fill", "white")
          .style("pointer-events", "none")
      }

      let removeHoverCircle = (circleName) => {
        d3Select
          .select(this.$refs.lineBarChart)
          .select(`.${circleName}`)
          .remove()
      }

      this.lastBarAnimation = setInterval(blinkLastBar, 1000)
    },
    tooltipDisplay(showTip, customersData) {
      this.$emit("tooltipDisplay", showTip, customersData)
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
