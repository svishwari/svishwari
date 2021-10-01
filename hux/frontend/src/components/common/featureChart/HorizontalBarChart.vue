<template>
  <div>
    <div class="chart-container" :style="{ maxWidth: chartWidth }">
      <div class="chart-style pb-6 pl-4 pt-1">
        <div
          ref="huxChart"
          class="chart-section"
          @mouseover="getCordinates($event)"
        ></div>
        <v-card
          v-if="showScoreTip"
          tile
          :style="{
            transform: `translate(${scoreTip.xPosition}px, ${scoreTip.yPosition}px)`,
          }"
          class="mx-auto score-tooltip-style"
        >
          <div class="black--text text--darken-4 caption">
            {{ scoreTip.score }}
          </div>
        </v-card>
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
      show: false,
      showScoreTip: false,
      scoreTip: {
        score: 0,
        xPosition: 0,
        yPosition: 0,
      },
      tooltip: {
        x: 0,
        y: 0,
      },
      margin: { top: 5, right: 50, bottom: 75, left: 150 },
    }
  },

  computed: {
    chartData() {
      return this.value
    },
  },

  watch: {
    value: function () {
      d3Select.select(this.$refs.huxChart).select("svg").remove()
      this.initiateHorizontalBarChart()
    },
    chartDimensions: function () {
      this.chartWidth = this.chartDimensions.width + "px"
      this.width =
        this.chartDimensions.width == 0 ? 560 : this.chartDimensions.width
    },
  },

  mounted() {
    this.chartWidth = this.chartDimensions.width + "px"
    this.initiateHorizontalBarChart()
  },
  methods: {
    async initiateHorizontalBarChart() {
      await this.chartDimensions
      let currentWidth = this.chartDimensions.width
      this.width = currentWidth == 0 ? 560 : currentWidth

      this.width = this.width - this.margin.left - this.margin.right
      this.height = this.height - this.margin.top - this.margin.bottom

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

      let featureLabelHover = (srcData) => {
        let currentFeature = this.chartData.find(
          (data) => data.name == srcData.getAttribute("data")
        )
        this.tooltipDisplay(true, currentFeature)
      }

      svg
        .append("g")
        .attr("transform", "translate(0," + this.height + ")")
        .call(d3Axis.axisBottom(x).ticks(5).tickSize(0))
        .call((g) => g.selectAll(".path").attr("stroke", "#d0d0ce"))
        .attr("stroke-width", "0.2")
        .attr("stroke-opacity", "0.3")
        .selectAll("text")
        .attr("fill", "#4f4f4f")
        .style("font-size", "12px")

      svg
        .append("g")
        .call(d3Axis.axisLeft(y).tickSize(0).tickFormat(appendElipsis))
        .call((g) => {
          g.select("path").attr("opacity", 0.1).attr("stroke", "none")
          g.selectAll("text").attr("data", (d) => d)
        })
        .selectAll("text")
        .attr("fill", "#4f4f4f")
        .style("font-size", "12px")
        .style("text-anchor", "end")
        .on("mouseover", (d) => featureLabelHover(d.srcElement))
        .on("mouseout", () => this.tooltipDisplay(false))

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
        .append("text")
        .attr(
          "transform",
          "translate(" +
            this.width / 2 +
            " ," +
            (this.height + this.margin.top + 30) +
            ")"
        )
        .style("text-anchor", "middle")
        .attr("fill", "#4f4f4f")
        .text("Score")

      svg
        .selectAll("myRect")
        .data(this.chartData)
        .enter()
        .append("rect")
        .attr("x", 0)
        .attr("y", (d) => y(d.name))
        .attr("width", (d) => x(d.score))
        .attr("height", y.bandwidth())
        .attr("fill", "#93d8f2")
        .attr("class", "bar")
        .on("mouseover", (d) => applyHoverEffects(d))
        .on("mouseout", () => removeHoverEffects())

      let applyHoverEffects = (d) => {
        d3Select.selectAll("rect").style("fill-opacity", "0.5")
        d3Select
          .select(d.srcElement)
          .attr("fill-opacity", (d) => changeHoverCirclePosition(d))
          .style("fill-opacity", "1")
      }

      let removeHoverEffects = () => {
        d3Select.selectAll("rect").style("fill-opacity", "1")
        this.showTip = false
        d3Select.select(this.$refs.huxChart).select("circle").remove()
        this.showScoreTip = false
        this.tooltipDisplay(false)
      }

      let changeHoverCirclePosition = (data) => {
        let featureData = data
        this.scoreTip.xPosition = x(data.score)
        this.scoreTip.yPosition = y(data.name) + 12
        this.scoreTip.score = data.score.toFixed(2)
        this.tooltipDisplay(true, featureData)
        svg
          .append("circle")
          .classed("removeableCircle", true)
          .attr("cx", this.scoreTip.xPosition)
          .attr("cy", this.scoreTip.yPosition)
          .attr("r", 4)
          .style("stroke", "#00A3E0")
          .style("stroke-opacity", "1")
          .style("fill", "white")
          .style("pointer-events", "none")
        this.showScoreTip = true
      }
    },

    getCordinates(event) {
      this.tooltip.x = event.offsetX
      this.tooltip.y = event.offsetY
      this.$emit("cordinates", this.tooltip)
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
    .score-tooltip-style {
      @extend .box-shadow-3;
      border-radius: 0px;
      padding: 7px 14px 12px 14px;
      max-width: 70px;
      height: 30px;
      z-index: 1;
      border-radius: 0px !important;
      position: absolute;
      left: 171px;
      top: -6px;
    }
  }
}
</style>
