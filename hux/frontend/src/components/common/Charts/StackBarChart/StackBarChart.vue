<template>
  <div class="chart-container" :style="{ maxWidth: chartWidth }">
    <div ref="stackBarChart" class="chart-section"></div>
  </div>
</template>

<script>
import * as d3Axis from "d3-axis"
import * as d3Shape from "d3-shape"
import * as d3Scale from "d3-scale"
import * as d3Select from "d3-selection"
import * as d3Array from "d3-array"
import * as d3Regression from "d3-regression"
import * as d3Transition from "d3-transition"
import colors from "../../../../plugins/theme"

export default {
  name: "StackBarChart",
  props: {
    value: {
      type: Array,
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
      totalCustomerData: this.value,
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
        d3Select.select(this.$refs.stackBarChart).selectAll("svg").remove()
        clearInterval(this.lastBarAnimation)
        this.initiateStackBarChart()
      },
      immediate: false,
      deep: true,
    },
  },
  destroyed() {
    clearInterval(this.lastBarAnimation)
  },
  methods: {
    async initiateStackBarChart() {
      await this.value
      this.chartWidth = this.chartDimensions.width + "px"
      this.width = this.chartDimensions.width
      this.height = this.chartDimensions.height
      let margin = { top: 15, right: 45, bottom: 100, left: 68 }
      let w = this.chartDimensions.width - margin.left - margin.right
      let h = this.chartDimensions.height - margin.top - margin.bottom
      let barColorCodes = []
      let rx = 10
      let ry = 10

      let svg = d3Select
        .select(this.$refs.stackBarChart)
        .append("svg")
        .attr("width", this.width + margin.left + margin.right)
        .attr("height", this.height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`)

      this.colorCodes.forEach((color) => {
        if (color.variant == "darken2") {
          barColorCodes.push(colors.primary[color.variant])
        } else if (color.variant == "lighten9") {
          barColorCodes.push(colors.primary[color.variant])
        } else if (color.variant == "lighten5") {
          barColorCodes.push(colors.primary[color.variant])
        } else {
          barColorCodes.push(colors[color.base][color.variant])
        }
      })

      let stack = d3Shape
        .stack()
        .keys(["total_customers", "new_customers_added"])

      let stackedValues = stack(this.totalCustomerData)
      d3Transition.transition()

      stackedValues.forEach((layer) => {
        layer.forEach((d) => {
          d[1] = d[1] - d[0]
          d[0] = 0
        })
      })

      let xScale = d3Scale
        .scaleBand()
        .domain(d3Array.range(this.totalCustomerData.length))
        .range([0, w])
        .paddingInner(0.33)
        .paddingOuter(0.11)

      let yScale = d3Scale
        .scaleLinear()
        .domain([
          0,
          this.emptyState
            ? 100
            : d3Array.max(this.totalCustomerData, (d) => d.total_customers),
        ])
        .range([h, 0])
        .nice(4)

      let bars = svg.append("g").attr("class", "bars")

      let hideInitialTick =
        this.totalCustomerData.filter(
          (bar) => bar.index == 0 && bar.barIndex < 5
        ).length < 3

      let convertCalendarFormat = (value) => {
        let tickDate = this.barGroupChangeIndex.find(
          (bar) => bar.index == value
        )
        if (tickDate && tickDate.index == 0 && hideInitialTick) {
          return ""
        }
        return tickDate
          ? this.emptyState
            ? "date"
            : this.$options.filters.Date(tickDate.date, "MM[/01/]YY")
          : ""
      }

      let applyNumericFilter = (value) =>
        this.emptyState
          ? "-"
          : this.$options.filters.Numeric(value, true, false, true)

      svg
        .append("g")
        .classed("xAxis-alternate", true)
        .attr("transform", "translate(0," + 255 + ")")
        .call(d3Axis.axisBottom(xScale).tickSize(0).tickFormat(""))
        .style("stroke-width", 40)

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
        .style("font-size", "12px")

      svg
        .append("g")
        .classed("yAxis-main", true)
        .attr("transform", "translate(0, 0)")
        .call(d3Axis.axisLeft(yScale).ticks(4).tickFormat(applyNumericFilter))
        .attr("stroke-width", "1")
        .attr("stroke-opacity", "1")
        .style("font-size", "12px")

      let groups = bars
        .selectAll("g")
        .data(stackedValues)
        .enter()
        .append("g")
        .attr("class", (d, i) => (i == 0 ? "backGroundBars" : "foreGroundBars"))
        .style("fill-opacity", (d, i) => {
          if (i == 0) {
            return 0.5
          } else {
            return 1
          }
        })

      d3Select.selectAll(".domain").style("stroke", "rgba(208, 208, 206, 1)")
      d3Select.selectAll(".tick line").style("stroke", "rgba(208, 208, 206, 1)")
      d3Select
        .selectAll(".xAxis-main .tick text")
        .attr("x", 10)
        .style("color", "#4F4F4F")
      d3Select.selectAll(".yAxis-main .tick text").style("color", "#4F4F4F")
      d3Select.selectAll(".xAxis-alternate .domain").style("stroke", "white")
      d3Select.selectAll(".xAxis-main .tick text").attr("x", 14)

      let topRoundedRect = (x, y, width, height) => {
        height = height < 0 ? 0 : height
        return `M${x},${y + ry}
        a${rx},${ry} 0 0 1 ${rx},${-ry}
        h${width - 2 * rx}
        a${rx},${ry} 0 0 1 ${rx},${ry}
        v${height - ry}
        h${-width}Z`
      }

      groups
        .selectAll("bar")
        .data((d) => d)
        .enter()
        .append("path")
        .attr("class", (d, i) => {
          if (i == this.totalCustomerData.length - 1) {
            return "active-bar"
          }
        })
        .attr("height", 0)
        .attr("width", xScale.bandwidth() < 30 ? xScale.bandwidth() : 30)
        .attr("data", (d, i) => i)
        .style("fill", (d) =>
          this.emptyState ? "transparent" : barColorCodes[d.data.index]
        )
        .on("mouseover", (d) => applyHoverEffects(d, xScale.bandwidth()))
        .on("mouseout", () => removeHoverEffects())
        .transition()
        .duration(500)
        .delay((d, i) => i * 25)
        .attr("d", (d, i) =>
          topRoundedRect(
            xScale(i),
            yScale(d[1]),
            xScale.bandwidth() < 30 ? xScale.bandwidth() : 30,
            yScale(d[0]) - yScale(d[1])
          )
        )

      let linearRegression = d3Regression
        .regressionLinear()
        .x((d) => d.barIndex)
        .y((d) => d.total_customers)

      let regLine = linearRegression(
        this.totalCustomerData.filter((d) => d.total_customers != 0)
      )

      let max = d3Array.max(this.totalCustomerData, (d) => d.barIndex)
      svg
        .append("line")
        .attr("class", "regression")
        .style("stroke-dasharray", "6")
        .style("stroke", this.emptyState ? "transparent" : "#86BC25")
        .style("stroke-width", 1.5)
        .attr("x1", xScale(0) + 9)
        .attr("y1", yScale(regLine.a))
        .attr("x2", xScale(max) + 14)
        .attr("y2", yScale(regLine.b))

      let applyHoverEffects = (d, width) => {
        d3Select
          .select(d.srcElement)
          .attr("fill-opacity", (d) => barHoverIn(d.data, width))
      }

      let removeHoverEffects = () => {
        d3Select.selectAll(".foreGroundBars").style("fill-opacity", "1")
        d3Select
          .select(this.$refs.stackBarChart)
          .select(".removeableCircle")
          .remove()
        this.tooltipDisplay(false)
      }

      let barHoverIn = (data, width) => {
        svg
          .append("circle")
          .classed("removeableCircle", true)
          .attr("cx", xScale(data.barIndex) + width / 2)
          .attr("cy", yScale(data.total_customers))
          .attr("r", 4)
          .style("stroke", barColorCodes[data.index])
          .style("stroke-opacity", "2")
          .style("stroke-width", "2")
          .style("fill", "white")
          .style("pointer-events", "none")
        this.toolTip.xPosition = xScale(data.barIndex) + 40
        this.toolTip.yPosition = yScale(data.total_customers)
        this.toolTip.date = data.date
        this.toolTip.totalCustomers = data.total_customers
        this.toolTip.addedCustomers = data.new_customers_added
        this.toolTip.index = data.index
        this.toolTip.isEndingBar = data.isEndingBar
        this.tooltipDisplay(true, this.toolTip)
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
