<template>
  <div>
    <div class="chart-container" :style="{ maxWidth: chartWidth }">
      <div class="chart-style pb-6 pl-4 pt-1">
        <div ref="huxChart" class="chart-section"></div>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3Select from "d3-selection"
import * as d3Axis from "d3-axis"
import * as d3Scale from "d3-scale"
import * as d3Array from "d3-array"

export default {
  name: "HorizontalBarChart",
  props: {
    value: {
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
      chartWidth: "",
      width: 350,
      height: 620,
      scoreTip: {
        score: 0,
        xPosition: 0,
        yPosition: 0,
      },
      margin: { top: 5, right: 50, bottom: 75, left: 180 },
    }
  },

  computed: {
    chartData() {
      return this.value
    },
  },

  watch: {
    chartDimensions: {
      handler() {
        d3Select.select(this.$refs.huxChart).selectAll("svg").remove()
        this.initiateHorizontalBarChart()
      },
      immediate: false,
      deep: true,
    },
  },

  mounted() {
    this.chartWidth = this.chartDimensions.width + "px"
  },
  methods: {
    async initiateHorizontalBarChart() {
      await this.chartDimensions
      let currentWidth = this.chartDimensions.width
      this.width = currentWidth

      this.width = this.width - this.margin.left - this.margin.right
      this.height = 515

      let svg = d3Select
        .select(this.$refs.huxChart)
        .append("svg")
        .attr("width", this.width + this.margin.left + this.margin.right)
        .attr("height", this.height + this.margin.top + this.margin.bottom)
        .append("g")
        .attr(
          "transform",
          "translate(" + this.margin.left + "," + this.margin.top + ")"
        )

      let xAxisDomain = d3Array.extent(this.chartData, (d) => d.score)

      let x = d3Scale
        .scaleLinear()
        .domain(xAxisDomain)
        .range([0, this.width])
        .nice(5)

      let y = d3Scale
        .scaleBand()
        .range([0, this.height])
        .domain(this.chartData.map((d) => d.name))
        .padding(0.1)

      let appendElipsis = (text) =>
        text && text.length > 20 ? text.slice(0, 20) + "..." : text

      svg
        .append("g")
        .attr("transform", "translate(0," + this.height + ")")
        .call(d3Axis.axisBottom(x).ticks(5).tickSize(0))
        .call((g) => g.selectAll(".path").attr("stroke", "#d0d0ce"))
        .attr("stroke-width", "0.2")
        .attr("stroke-opacity", "0.3")
        .selectAll("text")
        .attr("fill", "#4f4f4f")
        .style("font-size", "14px")

      svg
        .append("g")
        .call(d3Axis.axisLeft(y).tickSize(0).tickFormat(appendElipsis))
        .call((g) => {
          g.select("path").attr("opacity", 0.1).attr("stroke", "none")
          g.selectAll("text").attr("data", (d) => d)
        })
        .selectAll("text")
        .attr("fill", "#4f4f4f")
        .style("font-size", "14px")
        .style("text-anchor", "end")
        .on("mouseover", (d) =>
          applyHoverEffects(d.srcElement.getAttribute("data"))
        )
        .on("mouseout", () => removeHoverEffects())

      svg
        .append("g")
        .call(
          d3Axis
            .axisBottom(x)
            .tickSize(0)
            .tickFormat("")
            .ticks(5)
            .tickSizeInner(this.height)
        )
        .call((g) =>
          g
            .selectAll(".tick line")
            .attr("stroke", "#d0d0ce")
            .attr("stroke-opacity", "0.3")
        )
        .call((g) =>
          g
            .selectAll("path")
            .attr("stroke", "#d0d0ce")
            .attr("stroke-opacity", "0.3")
        )

      svg
        .append("line")
        .attr("class", "hover-line-y")
        .style("stroke", "#1E1E1E")
        .style("stroke-width", 1)
        .style("pointer-events", "none")

      svg
        .selectAll("myRect")
        .data(this.chartData)
        .enter()
        .append("rect")
        .attr("x", 0)
        .attr("rx", 2)
        .attr("ry", 2)
        .attr("data", (d) => d.name)
        .attr("y", (d) => y(d.name))
        .attr("width", (d) => x(d.score))
        .attr("height", 20)
        .attr("fill", "#00A3E0")
        .attr("class", "bar")
        .style("fill-opacity", "0.5")
        .on("mouseover", (d) =>
          applyHoverEffects(d.srcElement.getAttribute("data"))
        )
        .on("mouseout", () => removeHoverEffects())

      let applyHoverEffects = (data) => {
        d3Select.selectAll("rect").style("fill-opacity", "0.5")
        svg.select(`rect[data='${data}']`).style("fill-opacity", "1")
        d3Select
          .selectAll("text")
          .filter(function () {
            return d3Select.select(this).data() == data
          })
          .attr("fill", "#1E1E1E")
        let currentData = this.chartData.find((feature) => feature.name == data)
        changeHoverCirclePosition(currentData)
      }

      let removeHoverEffects = () => {
        d3Select.selectAll("rect").style("fill-opacity", "0.5")
        svg.selectAll(".hover-line-y").style("display", "none")
        svg.selectAll(".removeableCircleParent").style("display", "none")
        svg.selectAll(".removeableCircleChild").style("display", "none")
        this.showTip = false
        d3Select.select(this.$refs.huxChart).select("circle").remove()
        this.tooltipDisplay(false)
        d3Select.selectAll("text").attr("fill", "#4f4f4f")
      }

      let changeHoverCirclePosition = (data) => {
        let featureData = data
        featureData.xPosition = x(data.score)
        featureData.yPosition = y(data.name) + 10
        this.scoreTip.xPosition = x(data.score)
        this.scoreTip.yPosition = y(data.name) + 10
        this.scoreTip.score = data.score.toFixed(2)
        this.tooltipDisplay(true, featureData)
        svg
          .append("circle")
          .classed("removeableCircleParent", true)
          .attr("cx", this.scoreTip.xPosition)
          .attr("cy", this.scoreTip.yPosition)
          .attr("r", 7)
          .style("stroke", "white")
          .style("stroke-opacity", "1")
          .style("fill", "white")
          .style("pointer-events", "none")
        svg
          .append("circle")
          .classed("removeableCircleChild", true)
          .attr("cx", this.scoreTip.xPosition)
          .attr("cy", this.scoreTip.yPosition)
          .attr("r", 5)
          .style("stroke", "#00A3E0")
          .style("stroke-width", 2)
          .style("stroke-opacity", "1")
          .style("fill", "white")
          .style("pointer-events", "none")

        svg
          .selectAll(".hover-line-y")
          .attr("x1", this.scoreTip.xPosition)
          .attr("x2", this.scoreTip.xPosition)
          .attr("y1", 0)
          .attr("y2", this.height)
          .style("display", "block")
      }
    },

    tooltipDisplay(showTip, featureData) {
      this.$emit("tooltipDisplay", showTip, featureData)
    },
  },
}
</script>

<style lang="scss" scoped>
.chart-container {
  margin-bottom: 40px;
  min-height: 662px;
  .chart-style {
    position: relative;
    .chart-section {
      margin-bottom: -20px;
    }
  }
}
</style>
