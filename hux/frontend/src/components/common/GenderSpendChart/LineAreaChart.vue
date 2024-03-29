<template>
  <div class="main-container">
    <div
      ref="huxChart"
      class="chart-section"
      @mouseover="getCordinates($event)"
    ></div>
    <chart-legends :legends-data="legendsData" class="legend-style pl-7" />
  </div>
</template>

<script>
import * as d3Shape from "d3-shape"
import * as d3Scale from "d3-scale"
import * as d3Select from "d3-selection"
import * as d3Array from "d3-array"
import * as d3Axis from "d3-axis"
import * as d3TimeFormat from "d3-time-format"
import ChartLegends from "@/components/common/Charts/Legends/ChartLegends.vue"

export default {
  name: "LineAreaChart",
  components: { ChartLegends },
  props: {
    value: {
      type: Array,
      required: false,
    },
    yValueData: {
      type: Array,
      required: false,
    },
    dateData: {
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
      chartWidth: "",
      width: 355,
      height: 180,
      show: false,
      tooltip: {
        x: 0,
        y: 0,
      },
      areaChartData: this.value,
      legendsData: [
        { color: "rgba(0, 85, 135, 1)", text: "Women" },
        { color: "rgba(12, 157, 219, 1)", text: "Men" },
        { color: "rgba(66, 239, 253, 1)", text: "Other" },
      ],
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
      await this.areaChartData
      this.chartWidth = this.chartDimensions.width + "px"
      this.width = this.chartDimensions.width
      this.height = this.chartDimensions.height
      let margin = {}
      margin = { top: 10, bottom: 20, left: 60, right: 40 }
      let colorCodes = [
        "rgba(0, 85, 135, 1)",
        "rgba(12, 157, 219, 1)",
        "rgba(66, 239, 253, 1)",
      ]
      if (this.areaChartData.length === 0) {
        this.legendsData = [
          { color: "rgba(208, 208, 206, 1)", text: "no data available" },
        ]
        margin = { top: 10, bottom: 20, left: 40, right: 40 }
        colorCodes = ["rgba(208, 208, 206, 1)"]
      }

      let svg = d3Select
        .select(this.$refs.huxChart)
        .append("svg")
        .attr("width", this.width)
        .attr("height", this.height)

      let strokeWidth = 1.5

      let chart = svg
        .append("g")
        .attr("transform", `translate(${margin.left},10)`)

      let width =
        +svg.attr("width") - margin.left - margin.right - strokeWidth * 2
      let height = +svg.attr("height") - margin.top - margin.bottom

      let grp = chart
        .append("g")
        .attr("transform", `translate(-${margin.left - strokeWidth},0)`)

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
        .domain([0, d3Array.max(this.yValueData, (d) => d)])
        .nice(4)

      let xScale = d3Scale
        .scaleTime()
        .domain(
          d3Array.extent(this.dateData, function (d) {
            return d
          })
        )
        .range([0, width])

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
        .attr("fill-opacity", 0.2)
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
        .classed("xAxis", true)
        .call(
          d3Axis
            .axisBottom(xScale)
            .ticks(this.areaChartData.length)
            .tickFormat(d3TimeFormat.timeFormat("%m/%d/%y"))
            .tickValues(
              this.dateData.map(function (d) {
                return d
              })
            )
        )
        .call((g) => g.selectAll(".tick line").attr("stroke", "#ECECEC"))
        .call((g) => g.selectAll("path").attr("stroke", "#ECECEC"))
        .style("font-size", 12)

      chart
        .append("g")
        .attr("transform", "translate(0, 0)")
        .attr("fill", "#4f4f4f")
        .classed("yAxis", true)
        .call(d3Axis.axisLeft(yScale).ticks(4).tickFormat(appendyAxisFormat))
        .call((g) => g.selectAll(".tick line").attr("stroke", "#ECECEC"))
        .call((g) => g.selectAll("path").attr("stroke", "#ECECEC"))
        .style("font-size", 12)

      d3Select
        .selectAll(".xAxis .tick text")
        .attr("x", 0)
        .attr("y", 11)
        .style("color", "#4F4F4F")

      d3Select.selectAll(".yAxis .tick text").style("color", "#4F4F4F")
      svg
        .append("rect")
        .attr("width", width)
        .attr("transform", `translate(${margin.left},${margin.top})`)
        .attr("height", height)
        .style("stroke", "transparent")
        .style("fill", "transparent")
        .on("mousemove", (mouseEvent) => mousemove(mouseEvent))
        .on("mouseout", () => mouseout())

      let bisectDate = d3Array.bisector((d) => d).left

      svg
        .append("line")
        .attr("class", "hover-line-y")
        .style("stroke", "#1E1E1E")
        .style("stroke-width", 1)

      let mouseout = () => {
        svg.selectAll(".hover-line-y").style("display", "none")
        svg.selectAll(".hover-circle").remove()
        this.tooltipDisplay(false)
      }

      let mousemove = (mouseEvent) => {
        svg.selectAll(".hover-circle").remove()
        this.tooltipDisplay(false)
        if (this.areaChartData.length !== 0) {
          let data = this.dateData
          let x0 = xScale.invert(d3Select.pointer(mouseEvent)[0])

          let i = bisectDate(data, x0, 1)
          let d0 = data[i - 1]
          let d1 = data[i] || {}
          let d = x0 - d0 > d1 - x0 ? d1 : d0
          let finalXCoordinate = xScale(d) + margin.left
          let dateD = this.$options.filters.Date(d, "DD/MM/YY")
          let yData
          let dataToolTip = this.areaChartData.find(
            (element) =>
              this.$options.filters.Date(new Date(element.date), "DD/MM/YY") ==
              dateD
          )

          svg
            .selectAll(".hover-line-y")
            .attr("x1", finalXCoordinate)
            .attr("x2", finalXCoordinate)
            .attr("y1", margin.top)
            .attr("y2", height + margin.top)
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
                .style("stroke", this.getAttribute("addData"))
                .style("stroke-opacity", "1")
                .style("fill", "white")
                .style("pointer-events", "none")
            }
          })
          dataToolTip.xPosition = finalXCoordinate + 8
          dataToolTip.yPosition = yData
          this.tooltipDisplay(true, dataToolTip)
        }
      }

      stackedValues.forEach(function (layer, index) {
        layer.forEach((points) => {
          svg
            .append("circle")
            .attr("class", "dot")
            .attr("r", 2.5)
            .attr("cx", () => xScale(new Date(points.data.date)) + margin.left)
            .attr("cy", () => yScale(points[1]) + margin.top)
            .attr("data", () => points.data)
            .attr("addData", colorCodes[index])
            .style("fill", "transparent")
            .attr("stroke", "transparent")
        })
      })
    },
    getCordinates(event) {
      this.tooltip.x = event.offsetX
      this.tooltip.y = event.offsetY - 150
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
  .legend-style {
    margin-top: 35px;
  }
}
</style>
