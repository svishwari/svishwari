<template>
  <div class="chart-container">
    <div class="chart-section" ref="huxChart"></div>
    <v-card
      v-if="showToolTip"
      tile
      :style="{
        transform: `translate(${toolTip.xPosition}px, ${toolTip.yPosition}px)`,
      }"
      class="mx-auto tooltip-style"
    >
      <div class="neroBlack--text caption">
        <div>
          <span>Date</span>
      <icon
        type="name"
        :size="12"
        color="persianGreen"
      />
      <span class="prop-name">Total customers</span>
      <span>1223</span>
      <icon
        type="name"
        :size="12"
        color="persianGreen"
      />
      <span class="prop-name">New customer added</span>
      <span>12</span>
        </div>
      </div>
    </v-card>
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
import Tooltip from "@/components/common/Tooltip"
import Icon from "@/components/common/Icon"
import customerData from "@/components/common/TotalCustomerChart/TotalCustomerData.json"
export default {
  name: "stack-bar-chart",
  components: { Icon, Tooltip },
  props: {
    value: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      totalCustomerData: customerData.customersData,
      width: 1400,
      height: 500,
      outerRadius: 0,
      innerRadius: 0,
      tooltipText: "Most recent co-occurence between identifiers",
      legendsData: this.chartLegendsData,
      top: 50,
      left: 60,
      show: false,
      showToolTip: false,
      toolTip: {
        xPosition: 0,
        yPosition: 0,
      },
    }
  },
  methods: {
    initializeValues() {
      this.outerRadius = Math.min(this.width, this.height) * 0.5 - 10
      this.innerRadius = this.outerRadius - 7
    },

    calculateChartValues() {
      var margin = { top: 20, right: 50, bottom: 50, left: 40 },
        w = 1000 - margin.left - margin.right,
        h = 500 - margin.top - margin.bottom

      let colorCodes = [
        "rgba(160, 220, 255, 1)",
        "rgba(0, 163, 224, 1)",
        "rgba(0, 118, 168, 1)",
        "#43B02A",
      ]

      let svg = d3Select
        .select(this.$refs.huxChart)
        .append("svg")
        .attr("width", this.width)
        .attr("height", this.height)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")

      var week = d3TimeFormat.timeFormat("%U")
      var nest = d3Collection
        .nest()
        .key((d) => week(new Date(d.date)))
        .entries(this.totalCustomerData)

      let initialMonth = new Date(nest[0].values[1].date).getMonth()

      let formattedData = []
      let initialIndex = 0

      nest.forEach((val, index) => {
        if (
          new Date(val.values[val.values.length - 1].date).getMonth() !=
          initialMonth
        ) {
          initialMonth = new Date(
            val.values[val.values.length - 1].date
          ).getMonth()
          if (initialIndex == 2) {
            initialIndex = 0
          } else initialIndex++
        }

        formattedData.push({
          date: val.values[val.values.length - 1].date,
          total_customers: val.values.reduce(
            (sum, d) => sum + d.total_customers,
            0
          ),
          new_customers_added: val.values.reduce(
            (sum, d) => sum + d.new_customers_added,
            0
          ),
          index: index == nest.length - 1 ? 3 : initialIndex,
          barIndex: index,
        })
      })

      //// Globals ////
      var margin = { top: 50, right: 150, bottom: 50, left: 110 },
        w = 1400 - margin.left - margin.right,
        h = 500 - margin.top - margin.bottom

      let stack = d3Shape
        .stack()
        .keys(["total_customers", "new_customers_added"])
      let stackedValues = stack(formattedData)
      let stackedData = []

      stackedValues.forEach((layer) => {
        let currentStack = []
        layer.forEach((d, i) => {
          d[1] = d[1] - d[0]
          d[0] = 0
          currentStack.push({
            values: d,
            date: new Date(formattedData[i].date),
          })
        })
        stackedData.push(currentStack)
      })

      let xAxisDomain = d3Array.extent(formattedData, (d) => d.date)
      var xScale = d3Scale
        .scaleBand()
        .domain(d3Array.range(formattedData.length))
        .range([0, w])
        .paddingInner(0.33)
        .paddingOuter(0.11)

      let yAxisDomain = d3Array.extent(formattedData, (d) => d.total_customers)

      let yScale = d3Scale
        .scaleLinear()
        .domain([0, d3Array.max(formattedData, (d) => d.total_customers)])
        .range([h, 0])
        .nice(4)

      var axis = svg.append("g").attr("class", "axis")

      var bars = svg.append("g").attr("class", "bars")

      svg
        .append("g")
        .attr("transform", "translate(0," + h + ")")
        .call(
          d3Axis.axisBottom(xScale).tickValues([0, 4, 8, 12, 16]).tickSize(0)
          // .tickPadding(12)
          // .tickSizeInner(0)
          // .tickSizeOuter(0)
        )

      let applyNumericFilter = (value) =>
        this.$options.filters.Numeric(value, true, false, true)

      svg
        .append("g")
        .classed("yAxis", true)
        .attr("transform", "translate(0, 0)")
        .call(
          d3Axis.axisLeft(yScale).ticks(4).tickFormat(applyNumericFilter)
          //  .tickPadding(12)
          //  .tickSizeInner(10)
          //  .tickSizeOuter(10)
        )
        // .call((g) => g.selectAll(".path").attr("stroke", "red"))
        .attr("stroke-width", "1")
        .attr("stroke-opacity", "1")

      var groups = bars
        .selectAll("g")
        .data(stackedValues)
        .enter()
        .append("g")
        .attr("class", (d, i) => (i == 0 ? "backGroundBars" : "foreGroundBars"))
        .style("fill-opacity", (d, i) => {
          if (i == 0) {
            return 0.4
          } else {
            return 1
          }
        })

      d3Select.selectAll(".domain").style("stroke", "rgba(208, 208, 206, 1)")
      d3Select.selectAll(".tick line").style("stroke", "rgba(208, 208, 206, 1)")

      const rx = 15
      const ry = 12

      var rects = groups
        .selectAll("bar")
        .data((d) => d)
        .enter()
        .append("path")
        .attr("d", (d, i) =>
          rightRoundedRect(
            xScale(i),
            yScale(d[1]),
            xScale.bandwidth(),
            yScale(d[0]) - yScale(d[1]),
            15
          )
        )
        .style("margin-right", "10px")
        .style("fill", (d) => colorCodes[d.data.index])
        .on("mouseover", (d) => applyHoverEffects(d))
        .on("mouseout", () => removeHoverEffects())

      let applyHoverEffects = (d) => {
        d3Select
          .select(d.srcElement)
          .attr("fill-opacity", (d) => barHoverIn(d))
      }

      let removeHoverEffects = (d, i) => {
        d3Select.selectAll(".foreGroundBars").style("fill-opacity", "1")
        d3Select
          .select(this.$refs.huxChart)
          .select(".removeableCircle")
          .remove()
        this.showToolTip = false
      }

      let barHoverIn = (data) => {
        svg
          .append("circle")
          .classed("removeableCircle", true)
          .attr("cx", xScale(data.data.barIndex) + 14)
          .attr("cy", yScale(data.data.total_customers))
          .attr("r", 4)
          .style("stroke", colorCodes[data.data.index])
          .style("stroke-opacity", "2")
          .style("stroke-width", "2")
          .style("fill", "white")
          .style("pointer-events", "none")
          this.toolTip.xPosition = xScale(data.data.barIndex) + 14
          this.toolTip.yPosition = yScale(data.data.total_customers)
          this.showToolTip = true
      }

      function calcLinear(data, x, y, minX, minY) {
        var n = data.length
        var pts = []
        data.forEach(function (d, i) {
          var obj = {}
          obj.x = d[x]
          obj.y = d[y]
          obj.mult = obj.x * obj.y
          pts.push(obj)
        })
        var sum = 0
        var xSum = 0
        var ySum = 0
        var sumSq = 0
        pts.forEach(function (pt) {
          sum = sum + pt.mult
          xSum = xSum + pt.x
          ySum = ySum + pt.y
          sumSq = sumSq + pt.x * pt.x
        })
        var a = sum * n
        var b = xSum * ySum
        var c = sumSq * n
        var d = xSum * xSum

        var m = (a - b) / (c - d)

        var e = ySum

        var f = m * xSum

        var b = (e - f) / n
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

      var lg = calcLinear(
        formattedData,
        "barIndex",
        "total_customers",
        d3Array.min(formattedData, function (d) {
          return d.barIndex
        }),
        d3Array.min(formattedData, function (d) {
          return d.total_customers
        })
      )
      var max = d3Array.max(formattedData, function (d) {
        return d.barIndex
      })
      svg
        .append("line")
        .attr("class", "regression")
        .style("stroke-dasharray", "3, 3")
        .style("stroke", "#86BC25")
        .style("stroke-width", 2)
        .attr("x1", xScale(0) + 9)
        .attr("y1", yScale(lg.ptB.y))
        .attr("x2", xScale(max) + 14)
        .attr("y2", yScale(lg.ptA.y))

      function rightRoundedRect(x, y, width, height) {
        return `M${x},${y + ry}
        a${rx},${ry} 0 0 1 ${rx},${-ry}
        h${width - 2 * rx}
        a${rx},${ry} 0 0 1 ${rx},${ry}
        v${height - ry}
        h${-width}Z`
      }
    },
  },

  watch: {
    value: function () {
      d3Select.select(this.$refs.huxChart).select("svg").remove()
      this.calculateChartValues()
    },
  },

  mounted() {
    this.initializeValues()
    this.calculateChartValues()
  },
}
</script>

<style lang="scss" scoped>
.global-heading {
  @extend .font-weight-semi-bold;
  font-style: normal;
  font-size: $font-size-root;
  line-height: 19px;
  padding-left: 10px;
}
.chart-container {
  max-width: 424px;
  height: 252px;
  position: relative;

  .chart-section {
    margin-bottom: -20px;
  }
  .tooltip-style {
      @extend .box-shadow-3;
      border-radius: 0px;
      padding: 7px 14px 12px 14px;
      max-width: 172px;
      height: 112px;
      z-index: 1;
      border-radius: 0px !important;
      position: absolute;
      left: 47px;
      top: -38px;
      .prop-name {
      @extend .global-heading;
    }
    }
}
</style>
