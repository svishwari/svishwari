<template>
  <div class="main-container" :style="{ maxWidth: chartWidth }">
    <div class="">
      <div
        ref="huxChart"
        class="chart-section"
        @mouseover="getCordinates($event)"
      ></div>
    </div>
    <div class="pt-2">
      <div id="legend"></div>
    </div>
  </div>
</template>

<script>
import * as d3Shape from "d3-shape"
import * as d3Scale from "d3-scale"
import * as d3Select from "d3-selection"
import * as d3Array from "d3-array"
import * as d3Axis from "d3-axis"
import * as d3TimeFormat from "d3-time-format"

export default {
  name: "LineAreaChart",
  props: {
    value: {
      type: Object,
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
      chartWidth: "",
      width: 355,
      height: 180,
      show: false,
      tooltip: {
        x: 0,
        y: 0,
      },
      gender_men: [],
      gender_other: [],
      gender_women: [],
      yValueData: [],
      areaChart: [],
      areaChartData: [],
      chartData: this.value,
    }
  },
  watch: {
    chartDimensions: {
      handler() {
        d3Select.select(this.$refs.huxChart).selectAll("svg").remove()
        this.initiateAreaChart()
      },
      immediate: false,
      deep: true,
    },
  },
  methods: {
    async initiateAreaChart() {
      await this.chartData
      this.chartWidth = this.chartDimensions.width + "px"
      this.width = this.chartDimensions.width
      let line = 0
      let col = 0
      let genders = [{ label: "Women" }, { label: "Men" }, { label: "Other" }]
      this.gender_men.push(...this.chartData.gender_men)
      this.gender_women.push(...this.chartData.gender_women)
      this.gender_other.push(...this.chartData.gender_other)
      this.gender_men.forEach((element) => {
        this.gender_women.forEach((value) => {
          if (element.date === value.date) {
            this.areaChart.push({
              date: element.date,
              men_spend: element.ltv,
              women_spend: value.ltv,
            })
          }
        })
      })

      this.areaChart.forEach((element) => {
        this.gender_other.forEach((value) => {
          if (element.date === value.date) {
            this.yValueData.push(
              element.men_spend,
              element.women_spend,
              value.ltv
            )
            this.areaChartData.push({
              date: element.date,
              men_spend: element.men_spend,
              women_spend: element.women_spend,
              others_spend: value.ltv,
            })
          }
        })
      })

      let colorCodes = [
        "rgba(0, 85, 135, 1)",
        "rgba(12, 157, 219, 1)",
        "rgba(66, 239, 253, 1)",
      ]

      let color = d3Scale
        .scaleOrdinal()
        .range([
          "rgba(0, 85, 135, 1)",
          "rgba(12, 157, 219, 1)",
          "rgba(66, 239, 253, 1)",
        ])

      let svg = d3Select
        .select(this.$refs.huxChart)
        .append("svg")
        .attr("width", this.width)
        .attr("height", this.height)

      let strokeWidth = 1.5
      let margin = { top: 0, bottom: 20, left: 40, right: 20 }
      let chart = svg
        .append("g")
        .attr("transform", `translate(${margin.left},0)`)

      let width =
        +svg.attr("width") - margin.left - margin.right - strokeWidth * 2
      let height = +svg.attr("height") - margin.top - margin.bottom

      let grp = chart
        .append("g")
        .attr(
          "transform",
          `translate(-${margin.left - strokeWidth},-${margin.top})`
        )

      let stack = d3Shape
        .stack()
        .keys(["women_spend", "men_spend", "others_spend"])
      let stackedValues = stack(this.areaChartData)
      let stackedData = []

      stackedValues.forEach((layer) => {
        let currentStack = []
        layer.forEach((d, i) => {
          d[1] = d[1] - d[0]
          d[0] = 0
          currentStack.push({
            values: d,
            date: new Date(this.areaChartData[i].date),
          })
        })

        stackedData.push(currentStack)
      })

      let appendyAxisFormat = (text) =>
        `$${this.$options.filters.Numeric(text, false, true, false)}`

      let yScale = d3Scale
        .scaleLinear()
        .range([height, 0])
        .domain([0, Math.max(...this.yValueData) + 500])

      let xScale = d3Scale
        .scaleLinear()
        .range([0, width])
        .domain(
          d3Array.extent(
            this.areaChartData,
            (dataPoint) => new Date(dataPoint.date)
          )
        )

      let area = d3Shape
        .area()
        .x((dataPoint) => xScale(dataPoint.date))
        .y0((dataPoint) => yScale(dataPoint.values[0]))
        .y1((dataPoint) => yScale(dataPoint.values[1]))

      let series = grp
        .selectAll(".series")
        .data(stackedData)
        .enter()
        .append("g")
        .attr("class", "series")

      series
        .append("path")
        .attr("transform", `translate(${margin.left},0)`)
        .style("fill", (d, i) => colorCodes[i])
        .attr("stroke-width", 2)
        .attr("fill-opacity", 0.5)
        .attr("d", (d) => area(d))

      let lineStock = d3Shape
        .line()
        .x((dataPoint) => xScale(dataPoint.date))
        .y((dataPoint) => yScale(dataPoint.values[1]))

      series
        .append("path")
        .attr("transform", `translate(${margin.left},0)`)
        .attr("class", "line")
        .style("stroke", (d, i) => colorCodes[i])
        .attr("stroke-width", 2)
        .style("fill", "none")
        .attr("d", (d) => lineStock(d))

      chart
        .append("g")
        .attr("transform", `translate(0,${height})`)
        .attr("fill", "#4f4f4f")
        .call(
          d3Axis
            .axisBottom(xScale)
            .ticks(this.areaChartData.length)
            .tickFormat(d3TimeFormat.timeFormat("%b %Y"))
        )
        .call((g) => g.selectAll(".tick line").attr("stroke", "#ECECEC"))
        .call((g) => g.selectAll("path").attr("stroke", "#ECECEC"))
        .style("font-size", 12)

      chart
        .append("g")
        .attr("transform", "translate(0, 0)")
        .attr("fill", "#4f4f4f")
        .call(d3Axis.axisLeft(yScale).ticks(6).tickFormat(appendyAxisFormat))
        .call((g) => g.selectAll(".tick line").attr("stroke", "#ECECEC"))
        .call((g) => g.selectAll("path").attr("stroke", "#ECECEC"))
        .style("font-size", 12)

      stackedValues.forEach(function (layer, index) {
        layer.forEach((points) => {
          svg
            .append("circle")
            .attr("class", "dot")
            .attr("r", 3.5)
            .attr("cx", () => xScale(new Date(points.data.date)) + 40)
            .attr("cy", () => yScale(points[1]))
            .attr("data", () => points.data)
            .style("fill", colorCodes[index])
            .attr("stroke", colorCodes[index])
            .on("mouseover", (d) => dotHoverIn(d, points.data))
            .on("mouseout", (d) => dotHoverOut(d))
        })
      })

      let dotHoverIn = (d, value) => {
        let areaData = value
        let xPosition = d.srcElement.getAttribute("cx")
        svg
          .append("line")
          .attr("class", "hover-line")
          .style("stroke", "black")
          .attr("x1", xPosition)
          .attr("y1", 0)
          .attr("x2", xPosition)
          .attr("y2", height)

        svg.selectAll(".dot").each(function () {
          if (this.getAttribute("cx") == xPosition) {
            svg
              .append("circle")
              .classed("hover-circle", true)
              .attr("cx", xPosition)
              .attr("cy", this.getAttribute("cy"))
              .attr("r", 6)
              .style("stroke", this.getAttribute("stroke"))
              .style("stroke-opacity", "1")
              .style("fill", "white")
              .style("pointer-events", "none")
          }
        })
        this.tooltipDisplay(true, areaData)
      }

      let dotHoverOut = () => {
        d3Select.selectAll(".hover-line").remove()
        d3Select.selectAll(".hover-circle").remove()
        this.tooltipDisplay(false)
      }

      d3Select.select("#legend").selectAll("svg").remove()

      let legendSvg = d3Select
        .select("#legend")
        .append("svg")
        .attr("viewBox", "0 0 200 25")
        .attr("id", "mainSvg")
        .attr("class", "svgBox")
        .style("margin-left", "20px")
        .style("margin-right", "20px")

      let legend = legendSvg
        .selectAll(".legend")
        .data(genders)
        .enter()
        .append("g")
        .attr("class", "legend")
        .attr("transform", function () {
          let y = line * 25
          let x = col
          col += 35
          return "translate(" + x + "," + y + ")"
        })

      legend
        .append("circle")
        .attr("cx", 10)
        .attr("cy", 10)
        .attr("r", 2.5)
        .style("fill", function (d) {
          return color(d.label)
        })

      legend
        .append("text")
        .attr("x", 16)
        .attr("y", 9)
        .attr("dy", ".55em")
        .attr("class", "neroBlack--text")
        .style("font-size", 5)
        .style("text-anchor", "start")
        .text(function (d) {
          return d.label
        })
    },
    getCordinates(event) {
      this.tooltip.x = event.offsetX
      this.tooltip.y = event.offsetY
      this.$emit("cordinates", this.tooltip)
    },
    tooltipDisplay(showTip, spendData) {
      this.$emit("tooltipDisplay", showTip, spendData)
    },
  },
}
</script>

<style lang="scss" scoped>
.main-container {
  margin-bottom: 40px;
  max-width: 450px;
  min-height: 120px;
  height: 325px;
  .chart-section {
    margin-bottom: -20px;
  }
  .area-card-title {
    font-family: Open Sans;
    font-style: normal;
    font-weight: normal;
    font-size: 15px;
    line-height: 20px;
  }
}
</style>
