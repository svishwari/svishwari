<template>
  <div class="chart-container" :style="{ maxWidth: chartWidth }">
    <div ref="groupedBarChart" class="chart-section"></div>
  </div>
</template>

<script>
import * as d3Axis from "d3-axis"
import * as d3Scale from "d3-scale"
import * as d3Select from "d3-selection"
import * as d3Array from "d3-array"
import { formatText } from "@/utils"
import { addIcon } from "@/components/common/Charts/GroupedBarChart/dynamicIcon.js"

export default {
  name: "GroupedBarChart",
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
  },
  data() {
    return {
      chartWidth: "",
      segmentScores: [],
      colors: ["brown", "red", "orange", "green", "blue"],
      toolTip: {
        xPosition: 0,
        yPosition: 0,
        segmentName: "",
        attributeName: "",
        color: "",
        score: 0,
      },
      chartData: [
        {
          id: "trust_id",
          label: "HX TrustID",
          values: [
            { value: 50 },
            { value: 40 },
            { value: 30 },
            { value: 40 },
            { value: 30 },
          ],
        },
        {
          id: "humanity",
          label: "Humanity",
          values: [
            { value: 20 },
            { value: 30 },
            { value: 45 },
            { value: 30 },
            { value: 45 },
          ],
        },
        {
          id: "transperancy",
          label: "Transperancy",
          values: [
            { value: 20 },
            { value: 30 },
            { value: 45 },
            { value: 30 },
            { value: 45 },
          ],
        },
        {
          id: "capability",
          label: "Capability",
          values: [
            { value: 47 },
            { value: 29 },
            { value: 38 },
            { value: 29 },
            { value: 38 },
          ],
        },
        {
          id: "reliability",
          label: "Reliability",
          values: [
            { value: 29 },
            { value: 35 },
            { value: 45 },
            { value: 29 },
            { value: 38 },
          ],
        },
      ],
      chartHeight: 150,
      itemWidth: 100,
      barWidth: 20,
      barMargin: 2,
      xMargin: 50,
      yMargin: 20,
    }
  },
  watch: {
    chartDimensions: {
      handler() {
        d3Select.select(this.$refs.groupedBarChart).selectAll("svg").remove()
        this.initiateGroupedBarChart()
      },
      immediate: false,
      deep: true,
    },
  },
  methods: {
    async initiateGroupedBarChart() {
      await this.value
      this.segmentScores = this.value
      this.chartWidth = this.chartDimensions.width + "px"
      this.width = this.chartDimensions.width
      this.height = this.chartDimensions.height
      let margin = { top: 15, right: 30, bottom: 100, left: 68 }
      let w = this.chartDimensions.width - margin.left - margin.right
      let h = this.chartDimensions.height - margin.top - margin.bottom
      //   let barColorCodes = []

      let svg = d3Select
        .select(this.$refs.groupedBarChart)
        .append("svg")
        .attr("width", this.width + margin.left + margin.right)
        .attr("height", this.height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`)

      let maxScoreValue = (paramObj) => {
        return Object.keys(paramObj).reduce((a, b) =>
          paramObj[a] > paramObj[b] ? paramObj[a] : paramObj[b]
        )
      }

      let xScale = d3Scale
        .scaleBand()
        .domain(this.chartData.map((d) => d.id))
        .range([0, w])
        .paddingInner(0.22)
        .paddingOuter(0.11)

      let yScale = d3Scale
        .scaleLinear()
        .domain([
          0,
          this.emptyState
            ? 100
            : d3Array.max(this.segmentScores, (d) =>
                maxScoreValue(d.scores_overview)
              ),
        ])
        .range([h, 0])
        .nice(4)

      let applyNumericFilter = (value) =>
        this.emptyState ? "-" : this.$options.filters.Numeric(value, true, true)

      let formatAxisLabel = (text) => formatText(text)

      svg
        .append("g")
        .classed("xAxis-main", true)
        .attr("transform", `translate(0,${h})`)
        .call(
          d3Axis
            .axisBottom(xScale)
            .tickSize(0)
            .tickFormat(formatAxisLabel)
            .tickPadding(15)
        )
        .style("font-size", "14px")

      svg
        .append("g")
        .classed("yAxis-main", true)
        .attr("transform", "translate(0, 0)")
        .call(d3Axis.axisLeft(yScale).ticks(4).tickFormat(applyNumericFilter))
        .attr("stroke-width", "1")
        .attr("stroke-opacity", "1")
        .style("font-size", "14px")

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

      d3Select.selectAll(".domain").style("stroke", "#E2EAEC")
      d3Select.selectAll(".tick line").style("stroke", "#E2EAEC")
      d3Select.selectAll(".xAxis-main .tick text").style("color", "#4F4F4F")

      d3Select.selectAll(".xAxis-main .tick").each(function () {
        d3Select
          .select(this)
          .append("svg")
          .attr("x", "-50")
          .attr("class", "image-icon")
          .attr("y", "10")
          .attr("height", "20")
          .attr("width", "20")
          .attr("viewBox", "0 0 40 40")
          .html(addIcon)
      })

      d3Select.selectAll(".yAxis-main .tick text").style("color", "#4F4F4F")

      let colors = ["#0076A8", "#A0DCFF", "#00A3E0", "#E3E48D", "#007680"]

      svg
        .selectAll("myRect")
        .data(this.chartData, (d) => d.id)
        .enter()
        .append("g")
        .classed("attributes", true)
        .attr(
          "transform",
          (d) =>
            `translate(${this.xMargin + xScale(d.id) + this.itemWidth / 2},0)`
        )
        .each(function (d) {
          const city = d3Select.select(this)
          for (let i = 0; i < d.values.length; i++) {
            const y = yScale(d.values[i].value)
            const height = yScale(0) - y
            const x = (i - d.values.length / 2) * 42

            let label = d

            let xPosition = xScale(label.id) + x + 120

            let shareData = {}
            shareData.name = "Segment 1"
            shareData.attributeName = label.label
            shareData.score = 78
            shareData.xPosition = xPosition
            shareData.cx = x
            shareData.cy = y
            shareData.yPosition = height
            shareData.width = 40
            shareData.color = colors[i]

            city
              .append("rect")
              .classed("foreGroundBars", true)
              .attr("data", label)
              .attr("x", x)
              .attr("y", y)
              .attr("rx", 2)
              .attr("ry", 2)
              .attr("width", 40)
              .attr("height", height)
              .style("fill", colors[i])
              .style("fill-opacity", 1)
              .on("mouseover", (d) => applyHoverEffects(d, shareData))
              .on("mouseout", () => removeHoverEffects())
          }
        })

      svg
        .append("line")
        .attr("class", "hover-line-y")
        .style("stroke", "#1E1E1E")
        .style("stroke-width", 1)
        .style("pointer-events", "none")

      let hoverCircles = ["foreGroundParentCircle", "foreGroundChildCircle"]

      let addHoverCircle = (
        circleName,
        circleRadius,
        cX,
        cY,
        strokeColor,
        strokeWidth,
        strokeOpacity
      ) => {
        svg
          .append("circle")
          .classed(circleName, true)
          .attr("cx", cX)
          .attr("cy", cY)
          .attr("r", circleRadius)
          .style("stroke", strokeColor)
          .style("stroke-opacity", strokeOpacity)
          .style("stroke-width", strokeWidth)
          .style("fill", "white")
          .style("pointer-events", "none")
      }

      let removeHoverCircle = (circleName) => {
        d3Select
          .select(this.$refs.groupedBarChart)
          .select(`.${circleName}`)
          .remove()
      }

      let applyHoverEffects = (d, data) => {
        d3Select.select(d.srcElement).attr("fill-opacity", 1)
        barHoverIn(data)
      }

      let removeHoverEffects = () => {
        svg.selectAll(".hover-line-y").style("display", "none")
        hoverCircles.forEach((circleName) => removeHoverCircle(circleName))
        this.tooltipDisplay(false)
      }

      let barHoverIn = (data) => {
        this.toolTip.xPosition = data.xPosition + 40
        this.toolTip.yPosition = data.cy
        this.toolTip.segmentName = data.name
        this.toolTip.attributeName = data.attributeName
        this.toolTip.score = data.score
        this.toolTip.color = data.color
        this.tooltipDisplay(true, this.toolTip)

        svg
          .selectAll(".hover-line-y")
          .attr("x1", data.xPosition)
          .attr("x2", data.xPosition)
          .attr("y1", 0)
          .attr("y2", h)
          .style("display", "block")

        addHoverCircle(
          hoverCircles[0],
          9,
          data.xPosition,
          data.cy,
          "white",
          2,
          1
        )
        addHoverCircle(
          hoverCircles[1],
          7,
          data.xPosition,
          data.cy,
          data.color,
          2,
          1
        )
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
