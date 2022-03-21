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
import * as d3Transition from "d3-transition"
import { formatText } from "@/utils"
import { dynamicIcons } from "@/components/common/Charts/GroupedBarChart/dynamicIcon.js"

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
      itemWidth: 120,
      xMargin: 60,
    }
  },
  mounted() {
    // single handler for multiple props watch
    this.$watch(
      (prop) => [prop.chartDimensions, prop.value],
      () => {
        d3Select.select(this.$refs.groupedBarChart).selectAll("svg").remove()
        this.initiateGroupedBarChart()
      },
      {
        immediate: true,
        deep: true,
      }
    )
  },
  methods: {
    async initiateGroupedBarChart() {
      await this.value
      this.segmentScores = this.value
      this.chartWidth = this.chartDimensions.width + "px"
      this.width = this.chartDimensions.width
      this.height = this.chartDimensions.height
      let margin = { top: 15, right: 30, bottom: 130, left: 68 }
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

      // Adding dynamic domain values
      let getdomainValues = () => {
        if (this.emptyState) {
          return [0, 100]
        } else {
          return [
            d3Array.min(this.segmentScores, (d) =>
              Math.min(...d.values.map((em) => em.value))
            ),
            d3Array.max(this.segmentScores, (d) =>
              Math.max(...d.values.map((em) => em.value))
            ),
          ]
        }
      }

      let yScale = d3Scale
        .scaleLinear()
        .domain(getdomainValues())
        .range([h, 0])
        .nice(5)

      // Formatting X-Axis ticks
      let formatAxisLabel = (text) => {
        return text == "trust_id" ? "HX TrustID" : formatText(text)
      }

      // Custom Icon positioning fix
      let tickIconPosition = (text) => {
        if (text == "transparency") {
          return -60
        } else if (text == "trust_id") {
          return -55
        } else {
          return -50
        }
      }

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
        .call(d3Axis.axisLeft(yScale).ticks(5))
        .attr("stroke-width", "1")
        .attr("stroke-opacity", "1")
        .style("font-size", "14px")

      // adding grid lines to Y-Axis
      svg
        .append("g")
        .classed("yAxis-alternate", true)
        .attr("transform", "translate(0, 0)")
        .call(d3Axis.axisLeft(yScale).tickSize(-w).ticks(5).tickFormat(""))
        .attr("stroke-width", "0.5")
        .attr("stroke-opacity", "1")
        .style("font-size", "12px")

      // setting grid lines stroke color
      d3Select
        .selectAll(".yAxis-alternate .tick line")
        .style("stroke", "#E2EAEC")

      d3Select.selectAll(".domain").style("stroke", "#E2EAEC")
      d3Select.selectAll(".tick line").style("stroke", "#E2EAEC")
      d3Select
        .selectAll(".xAxis-main .tick text")
        .style("color", "#4F4F4F")
        .style("font-family", "Open Sans")

      // Adding dynamic icon to xis ticks
      d3Select
        .selectAll(".xAxis-main .tick")
        .each(function (d) {
          d3Select
            .select(this)
            .append("svg")
            .attr("x", () => tickIconPosition(d))
            .attr("class", "image-icon")
            .attr("y", "14")
            .attr("height", "14")
            .attr("width", "14")
            .attr("viewBox", "0 0 14 14")
            .html(dynamicIcons[d.toLowerCase()])
        })
        .attr(
          "transform",
          (d) => `translate(${this.xMargin + xScale(d) + this.itemWidth / 2},0)`
        )

      // Adding vertical Label
      svg
        .append("text")
        .classed("appendtext", true)
        .attr(
          "transform",
          "translate(-40," + this.height / 3 + ") rotate(-90 )"
        )
        .attr("fill", "#1E1E1E")
        .style("text-anchor", "middle")
        .style("font-size", "16px")
        .text("Score")

      d3Select.selectAll(".yAxis-main .tick text").style("color", "#4F4F4F")

      // Setting bar width as per their number
      let barSize = (totalAttributes) => {
        let barWidth = 0
        switch (totalAttributes) {
          case 1:
            barWidth = 56
            break
          case 2:
            barWidth = 46
            break
          case 3:
            barWidth = 40
            break
          case 4:
            barWidth = 32
            break
          case 5:
            barWidth = 24
            break
        }
        return xScale.bandwidth() < barWidth ? xScale.bandwidth() : barWidth
      }
      d3Transition.transition()

      // Adding bar group domain
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
          // Adding bars to the specific attribute group
          const barDomain = d3Select.select(this)
          let barProp = d.values
          for (let i = 0; i < barProp.length; i++) {
            const currentBar = d.values[i]
            const y = yScale(currentBar.value)
            const height = currentBar.value < 0 ? y - yScale(0) : yScale(0) - y
            const barWidth = barSize(barProp.length)
            const x = (i - barProp.length / 2) * (barWidth + 2)

            let currentData = {
              segmentName: currentBar.segmentName,
              attributeName: d.label,
              score: currentBar.value,
              xPosition: x + barWidth / 2,
              yPosition: y,
              width: barWidth,
              color: currentBar.color,
            }

            barDomain
              .append("rect")
              .attr("x", x)
              .attr("y", currentBar.value > 0 ? y : yScale(0))
              .attr("rx", 2)
              .attr("ry", 2)
              .on("mouseover", () => applyHoverEffects(currentData, barDomain))
              .on("mouseout", () => removeHoverEffects())
              .attr("width", barWidth)
              .attr("height", 0)
              .transition()
              .duration(1000)
              .attr("height", height)
              .style("fill", currentBar.color)
              .style("fill-opacity", 1)
          }
        })

      let hoverCircles = ["foreGroundParentCircle", "foreGroundChildCircle"]

      let addHoverCircle = (
        element,
        circleName,
        circleRadius,
        cX,
        cY,
        strokeColor,
        strokeWidth,
        strokeOpacity
      ) => {
        element
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

      let applyHoverEffects = (data, element) => {
        // Adding hover vertical line to targetted bar
        element
          .append("line")
          .attr("class", "hover-line-y")
          .style("stroke", "#1E1E1E")
          .style("stroke-width", 1)
          .style("pointer-events", "none")
          .attr("x1", data.xPosition)
          .attr("x2", data.xPosition)
          .attr("y1", yScale(0))
          .attr("y2", data.score > 0 ? 0 : h) // It will be 0 to max for positive bar and 0 to min for negative bar

        // Adding hover circle to target grouping element (Bar)
        addHoverCircle(
          element,
          hoverCircles[0],
          9,
          data.xPosition,
          data.yPosition,
          "white",
          2,
          1
        )
        addHoverCircle(
          element,
          hoverCircles[1],
          7,
          data.xPosition,
          data.yPosition,
          data.color,
          2,
          1
        )

        // Setting tooltip data
        let tooltipData = JSON.parse(JSON.stringify(data))

        // Setting dynamic positioning for external tooltips
        tooltipData.xPosition =
          window.scrollX +
          document
            .querySelector(".foreGroundParentCircle")
            .getBoundingClientRect().left
        this.tooltipDisplay(true, tooltipData)
      }

      // Eliminating hover effects
      let removeHoverEffects = () => {
        svg.selectAll(".hover-line-y").style("display", "none")
        hoverCircles.forEach((circleName) => removeHoverCircle(circleName))
        this.tooltipDisplay(false)
      }
    },
    // Emitting tooltip data
    tooltipDisplay(showTip, segmentData) {
      this.$emit("tooltipDisplay", showTip, segmentData)
    },
  },
}
</script>

<style lang="scss" scoped>
.chart-container {
  height: 220px;
  position: relative;
  .chart-section {
    margin-bottom: -20px;
  }
}
</style>
