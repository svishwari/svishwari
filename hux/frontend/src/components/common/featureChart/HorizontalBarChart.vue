<template>
  <div>
    <v-card
      class="rounded-lg card-style box-shadow-5"
      maxWidth="608px"
      minHeight="662px"
      flat
    >
      <v-card-title class="d-flex justify-space-between pb-6 pl-6 pt-5">
        <div class="mt-2">
          <span class="d-flex align-center black--text text-decoration-none">
            Top 20 feature importance
          </span>
        </div>
        <div
          class="chart-section"
          ref="huxChart"
          @mouseover="getCordinates($event)"
        ></div>
      </v-card-title>
      <v-card-text class="pl-6 pr-6 pb-6"> </v-card-text>
    </v-card>
  </div>
</template>

<script>
import * as d3Select from "d3-selection"
import * as d3Axis from "d3-axis"
import * as d3Scale from "d3-scale"

export default {
  name: "horizontal-bar-chart",
  props: {
    value: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      width: 560,
      height: 620,
      show: false,
      tooltip: {
        x: 0,
        y: 0,
      },
      margin: { top: 20, right: 10, bottom: 70, left: 110 },
      chartData: this.value,
    }
  },
  methods: {
    initiateHorizontalBarChart() {
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

      let x = d3Scale.scaleLinear().domain([0, 3]).range([0, this.width])

      let appendElipsis = (text) =>
        text && text.length > 20 ? text.slice(0, 19) + "..." : text

      let y = d3Scale
        .scaleBand()
        .range([0, this.height])
        .domain(this.chartData.map((d) => d.name))
        .padding(0.1)

      svg
        .append("g")
        .attr("transform", "translate(0," + this.height + ")")
        .call(d3Axis.axisBottom(x).ticks(5).tickSize(0))
        .call((g) => g.selectAll(".path").attr("stroke", "#d0d0ce"))
        .attr("stroke-width", "0.2")
        .attr("stroke-opacity", "0.3")

      svg
        .append("g")
        .call(d3Axis.axisLeft(y).tickSize(0).tickFormat(appendElipsis))
        .call((g) => {
          g.select("path").attr("opacity", 0.1).attr("stroke", "none")
        })
        .selectAll("text")
        .style("text-anchor", "end")

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
            (this.height + this.margin.top + 20) +
            ")"
        )
        .style("text-anchor", "middle")
        .text("Score")

      svg
        .selectAll("myRect")
        .data(this.chartData)
        .enter()
        .append("rect")
        .attr("x", x(0))
        .attr("y", (d) => y(d.name))
        .attr("width", (d) => x(d.score))
        .attr("height", y.bandwidth())
        .attr("fill", "#93d8f2")
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
        d3Select.select(this.$refs.huxChart).select("circle").remove()
        this.tooltipDisplay(false)
      }

      let changeHoverCirclePosition = (data) => {
        let featureData = data
        featureData.xPosition = x(data.score)
        featureData.yPosition = y(data.name) + 12
        this.tooltipDisplay(true, featureData)
        svg
          .append("circle")
          .classed("removeableCircle", true)
          .attr("cx", featureData.xPosition)
          .attr("cy", featureData.yPosition)
          .attr("r", 4)
          .style("stroke", "#00A3E0")
          .style("stroke-opacity", "1")
          .style("fill", "white")
          .style("pointer-events", "none")
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

  watch: {
    value: function () {
      d3Select.select(this.$refs.huxChart).select("svg").remove()
      this.initiateHorizontalBarChart()
    },
  },

  mounted() {
    this.initiateHorizontalBarChart()
  },
}
</script>

<style lang="scss" scoped>
.card-style {
  margin-bottom: 40px;
  height: 550px;
  .chart-section {
    margin-bottom: -20px;
  }
}
</style>
