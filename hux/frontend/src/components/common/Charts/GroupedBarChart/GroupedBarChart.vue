<template>
  <div class="chart-container" :style="{ maxWidth: chartWidth }">
    <div ref="groupedBarChart" class="chart-section"></div>
    <chart-legends v-if="showLegends" :legends-data="legendsData" class="legend-style pl-7" />
  </div>
</template>

<script>
import * as d3Axis from "d3-axis"
import * as d3Scale from "d3-scale"
import * as d3Select from "d3-selection"
import { formatText } from "@/utils"
import { dynamicIcons } from "@/components/common/Charts/GroupedBarChart/dynamicIcon.js"
import ChartLegends from "@/components/common/Charts/Legends/ChartLegends.vue"

export default {
  name: "GroupedBarChart",
  components: { ChartLegends },
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
      itemWidth: 100,
      xMargin: 50,
      legendsData: [
        { color: "rgba(0, 85, 135, 1)", text: "Segment 1" },
        { color: "rgba(12, 157, 219, 1)", text: "Segment 2" },
        { color: "rgba(66, 239, 253, 1)", text: "Segment 3" },
      ],
      showLegends: false,
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

      let svg = d3Select
        .select(this.$refs.groupedBarChart)
        .append("svg")
        .attr("width", this.width + margin.left + margin.right)
        .attr("height", this.height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`)

      let xScale = d3Scale
        .scaleBand()
        .domain(this.segmentScores.map((d) => d.id))
        .range([0, w])
        .paddingInner(0.22)
        .paddingOuter(0.11)

      let yScale = d3Scale
        .scaleLinear()
        .domain([
          0,100
        ])
        .range([h, 0])
        .nice(4)

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
        .call(d3Axis.axisLeft(yScale).ticks(4))
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

      d3Select.selectAll(".xAxis-main .tick").each(function (d) {
        d3Select
          .select(this)
          .append("svg")
          .attr("x", "-50")
          .attr("class", "image-icon")
          .attr("y", "14")
          .attr("height", "14")
          .attr("width", "14")
          .attr("viewBox", "0 0 14 14")
          .html(dynamicIcons[d.toLowerCase()])
      })

      svg
        .append("text")
        .classed("appendtext", true)
        .attr(
          "transform",
          "translate(-40," + this.height / 3 + ") rotate(-90 )"
        )
        .attr("fill", "#000000")
        .style("text-anchor", "middle")
        .style("color", "#000000")
        .style("font-size", "14px")
        .text("Score")

      d3Select.selectAll(".yAxis-main .tick text").style("color", "#4F4F4F")

      let barSize = (totalAttributes) => {
        let barWidth = 0
        switch (totalAttributes) {
          case 1:
            barWidth =  56
            break
          case 2:
            barWidth =  46
            break
          case 3:
            barWidth =  40
            break
          case 4:
            barWidth =  32
            break
          case 5:
            barWidth =  24
            break
        }
        return xScale.bandwidth() < barWidth ? xScale.bandwidth() : barWidth
      }

      svg
        .selectAll("myRect")
        .data(this.segmentScores, (d) => d.id)
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
            let y = yScale(d.values[i].value)
            let height = yScale(0) - y

            let barWidth = barSize(d.values.length)

            const x = (i - d.values.length / 2) * (barWidth + 2)

            let label = d

            let xPosition = xScale(label.id) + x + (d.values.length*barWidth)

            let shareData = {}
            shareData.name = "Segment 1"
            shareData.attributeName = label.label
            shareData.score = 78
            shareData.xPosition = xPosition
            shareData.cx = x
            shareData.cy = y
            shareData.yPosition = height
            shareData.width = barWidth
            shareData.color = d.values[i].color

            city
              .append("rect")
              .classed("foreGroundBars", true)
              .attr("data", label)
              .attr("x", x)
              .attr("y", y)
              .attr("rx", 2)
              .attr("ry", 2)
              .attr("width", barWidth)
              .attr("height", height)
              .style("fill", d.values[i].color)
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
