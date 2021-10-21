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

      let svg = d3Select
        .select(this.$refs.stackBarChart)
        .append("svg")
        .attr("width", this.width + margin.left + margin.right)
        .attr("height", this.height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`)

      this.colorCodes.forEach((color) => {
        if (color.variant == "lighten6") {
          barColorCodes.push(colors.primary[color.variant])
        } else if (color.variant == "darken1") {
          barColorCodes.push(colors.primary[color.variant])
        } else if (color.variant == "darken3") {
          barColorCodes.push(colors.primary[color.variant])
        } else {
          barColorCodes.push(colors.success[color.variant])
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
        .paddingInner(0.22)
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
        .style("font-size", "12px")

      svg
        .append("g")
        .classed("yAxis-main", true)
        .attr("transform", "translate(0, 0)")
        .call(d3Axis.axisLeft(yScale).ticks(4).tickFormat(applyNumericFilter))
        .attr("stroke-width", "1")
        .attr("stroke-opacity", "1")
        .style("font-size", "12px")

      svg
        .append("g")
        .classed("yAxis-alternate", true)
        .attr("transform", "translate(0, 0)")
        .call(d3Axis.axisLeft(yScale).tickSize(-w).ticks(4).tickFormat(""))
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
        .attr("class", (d, i) => (i == 0 ? "backGroundBars" : "foreGroundBars"))
        .style("fill-opacity", (d, i) => {
          if (i == 0) {
            return 0.5
          } else {
            return 1
          }
        })

      d3Select.selectAll(".domain").style("stroke", "#E2EAEC")
      d3Select.selectAll(".tick line").style("stroke", "#E2EAEC")
      d3Select
        .selectAll(".xAxis-main .tick text")
        .attr("x", 10)
        .style("color", "#4F4F4F")
      d3Select.selectAll(".yAxis-main .tick text").style("color", "#4F4F4F")
      d3Select.selectAll(".xAxis-main .tick text").attr("x", 14)

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
          if (i == this.totalCustomerData.length - 1) {
            return "active-bar"
          }
        })
        .attr("data", (d, i) => i)
        .style("fill", (d) =>
          this.emptyState ? "transparent" : barColorCodes[d.data.index]
        )
        .on("mouseover", (d) => applyHoverEffects(d, xScale.bandwidth()))
        .on("mouseout", (d) => removeHoverEffects(d))
        .attr("height", (d) => yScale(d[0]) - yScale(d[1]))
        .attr("width", xScale.bandwidth() < 30 ? xScale.bandwidth() : 30)
        .attr("x", (d, i) => xScale(i))
        .attr("y", (d) => yScale(d[1]))
        .attr("rx", 4)
        .attr("ry", 4)
        .attr("d", (d) => d)

      let applyHoverEffects = (d, width) => {
        d3Select.select(d.srcElement).attr("fill-opacity", (d) => {
          barHoverIn(d.data, width)
          return 0.7
        })
      }

      let hoverCircles = [
        "foreGroundParentCircle",
        "foreGroundChildCircle",
        "backGroundParentCircle",
        "backGroundChildCircle",
      ]

      let removeHoverEffects = (d) => {
        d3Select.select(d.srcElement).attr("fill-opacity", 0.5)
        svg.selectAll(".hover-line-y").style("display", "none")
        d3Select.selectAll(".foreGroundBars").style("fill-opacity", "1")
        hoverCircles.forEach((circleName) => removeHoverCircle(circleName))
        this.tooltipDisplay(false)
      }

      let barHoverIn = (data, width) => {
        this.toolTip.xPosition = xScale(data.barIndex) + 40
        this.toolTip.yPosition = yScale(data.total_customers)
        this.toolTip.date = data.date
        this.toolTip.totalCustomers = data.total_customers
        this.toolTip.addedCustomers = data.new_customers_added
        this.toolTip.leftCustomers = data.customers_left
        this.toolTip.index = data.index
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
          5,
          data.barIndex,
          data.total_customers,
          width,
          "white",
          2,
          1
        )
        addHoverCircle(
          hoverCircles[1],
          4,
          data.barIndex,
          data.total_customers,
          width,
          barColorCodes[data.index],
          2,
          0.7
        )
        addHoverCircle(
          hoverCircles[2],
          5,
          data.barIndex,
          data.new_customers_added,
          width,
          "white",
          2,
          1
        )
        addHoverCircle(
          hoverCircles[3],
          4,
          data.barIndex,
          data.new_customers_added,
          width,
          barColorCodes[data.index],
          2,
          1
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
        strokeOpacity
      ) => {
        svg
          .append("circle")
          .classed(circleName, true)
          .attr("cx", xScale(cX) + width / 2)
          .attr("cy", yScale(cY))
          .attr("r", circleRadius)
          .style("stroke", strokeColor)
          .style("stroke-opacity", strokeOpacity)
          .style("stroke-width", strokeWidth)
          .style("fill", "white")
          .style("pointer-events", "none")
      }

      let removeHoverCircle = (circleName) => {
        d3Select
          .select(this.$refs.stackBarChart)
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
