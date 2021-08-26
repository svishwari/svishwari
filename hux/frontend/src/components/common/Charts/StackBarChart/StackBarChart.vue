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
import * as d3TimeFormat from "d3-time-format"
import * as d3Collection from "d3-collection"
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
      totalCustomerData: this.value,
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
        d3Select.select(this.$refs.stackBarChart).selectAll("svg").remove()
        this.initiateStackBarChart()
      },
      immediate: false,
      deep: true,
    },
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
      let formattedData = []
      let initialIndex = 0
      let barColorCodes = []
      let monthChangeIndexs = []
      let rx = 15
      let ry = 15

      let svg = d3Select
        .select(this.$refs.stackBarChart)
        .append("svg")
        .attr("width", this.width + margin.left + margin.right)
        .attr("height", this.height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`)

      this.colorCodes.forEach((color) => barColorCodes.push(colors[color]))

      let week = d3TimeFormat.timeFormat("%U")
      let weeklyAggData = d3Collection
        .nest()
        .key((d) => week(new Date(d.date)))
        .entries(this.totalCustomerData)

      let initialWeek = weeklyAggData[0].values
      let initialWeekEndingDate = initialWeek[initialWeek.length - 1].date

      monthChangeIndexs.push({ index: 0, date: initialWeekEndingDate })

      let initialMonth = new Date(initialWeekEndingDate).getMonth()

      weeklyAggData.forEach((element, index) => {
        let weekData = element.values
        let weekLastDate = weekData[weekData.length - 1].date
        if (new Date(weekLastDate).getMonth() != initialMonth) {
          initialMonth = new Date(weekLastDate).getMonth()
          if (initialIndex == 2) {
            initialIndex = 0
          } else initialIndex++

          monthChangeIndexs.push({
            index: index,
            date: weekLastDate,
          })
        }

        formattedData.push({
          date: weekLastDate,
          total_customers: weekData.reduce(
            (sum, d) => sum + d.total_customers,
            0
          ),
          new_customers_added: weekData.reduce(
            (sum, d) => sum + d.new_customers_added,
            0
          ),
          index: index == weeklyAggData.length - 1 ? 3 : initialIndex,
          barIndex: index,
          isEndingBar: index > weeklyAggData.length - 3
        })
      })

      let stack = d3Shape
        .stack()
        .keys(["total_customers", "new_customers_added"])
      let stackedValues = stack(formattedData)

      stackedValues.forEach((layer) => {
        layer.forEach((d) => {
          d[1] = d[1] - d[0]
          d[0] = 0
        })
      })

      let xScale = d3Scale
        .scaleBand()
        .domain(d3Array.range(formattedData.length))
        .range([0, w])
        .paddingInner(0.33)
        .paddingOuter(0.11)

      let yScale = d3Scale
        .scaleLinear()
        .domain([0, d3Array.max(formattedData, (d) => d.total_customers)])
        .range([h, 0])
        .nice(4)

      let bars = svg.append("g").attr("class", "bars")

      let convertCalendarFormat = (value) => {
        let tickDate = monthChangeIndexs.find((bar) => bar.index == value)
        if (tickDate) {
          return this.$options.filters.Date(tickDate.date, "MMM [']YY")
        } else return ""
      }

      let applyNumericFilter = (value) =>
        this.$options.filters.Numeric(value, true, false, true)

      svg
        .append("g")
        .classed("xAxis-alternate", true)
        .attr("transform", "translate(0," + 243 + ")")
        .call(d3Axis.axisBottom(xScale).tickSize(0).tickFormat(""))
        .style("stroke-width", 16)

      svg
        .append("g")
        .classed("xAxis", true)
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
        .classed("yAxis", true)
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
      d3Select.selectAll(".xAxis .tick text").attr("x", 10).style("color", "#4F4F4F")
      d3Select.selectAll(".yAxis .tick text").style("color", "#4F4F4F")
      d3Select.selectAll(".xAxis-alternate .domain").style("stroke", "white")

      let topRoundedRect = (x, y, width, height) =>
        `M${x},${y + ry}
        a${rx},${ry} 0 0 1 ${rx},${-ry}
        h${width - 2 * rx}
        a${rx},${ry} 0 0 1 ${rx},${ry}
        v${height - ry}
        h${-width}Z`

      groups
        .selectAll("bar")
        .data((d) => d)
        .enter()
        .append("path")
        .attr("d", (d, i) =>
          topRoundedRect(
            xScale(i),
            yScale(d[1]),
            xScale.bandwidth() < 30 ? xScale.bandwidth() : 30,
            yScale(d[0]) - yScale(d[1])
          )
        )
        .style("fill", (d) => barColorCodes[d.data.index])
        .on("mouseover", (d) => applyHoverEffects(d, xScale.bandwidth()))
        .on("mouseout", () => removeHoverEffects())

      let getLinearRegression = (data, x, y, minX, minY) => {
        let n = data.length
        let pts = []
        data.forEach((d) => {
          let obj = {}
          obj.x = d[x]
          obj.y = d[y]
          obj.mult = obj.x * obj.y
          pts.push(obj)
        })
        let sum = 0
        let xSum = 0
        let ySum = 0
        let sumSq = 0
        pts.forEach((pt) => {
          sum = sum + pt.mult
          xSum = xSum + pt.x
          ySum = ySum + pt.y
          sumSq = sumSq + pt.x * pt.x
        })
        let a = sum * n
        let b = xSum * ySum
        let c = sumSq * n
        let d = xSum * xSum
        let m = (a - b) / (c - d)
        let e = ySum
        let f = m * xSum
        b = (e - f) / n
        return {
          ptA: {
            x: minX,
            y: m * minX + b,
          },
          ptB: {
            y: minY,
            x: (minY - b) / m,
          },
        }
      }

      let lg = getLinearRegression(
        formattedData,
        "barIndex",
        "total_customers",
        d3Array.min(formattedData, (d) => d.barIndex),
        d3Array.min(formattedData, (d) => d.total_customers)
      )

      let max = d3Array.max(formattedData, (d) => d.barIndex)
      svg
        .append("line")
        .attr("class", "regression")
        .style("stroke-dasharray", "6")
        .style("stroke", "#86BC25")
        .style("stroke-width", 1.5)
        .attr("x1", xScale(0) + 9)
        .attr("y1", yScale(lg.ptB.y))
        .attr("x2", xScale(max) + 14)
        .attr("y2", yScale(lg.ptA.y))

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
