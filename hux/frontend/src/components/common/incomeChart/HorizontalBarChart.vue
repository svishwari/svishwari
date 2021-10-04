<template>
  <div class="chart-container" :style="{ maxWidth: chartWidth }">
    <div ref="huxChart" class="chart-section"></div>
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
      width: 255,
      height: 200,
      show: false,
      chartWidth: "",
      tooltip: {
        x: 0,
        y: 0,
      },
      margin: { top: 5, right: 40, bottom: 20, left: 22 },
      chartData: this.value,
    }
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
    this.initiateHorizontalBarChart()
  },
  methods: {
    async initiateHorizontalBarChart() {
      await this.chartData
      this.width = this.chartDimensions.width
      this.height = this.chartDimensions.height
      this.chartWidth = this.chartDimensions.width + "px"

      this.width = this.width - this.margin.left - this.margin.right
      this.height = this.height - this.margin.top - this.margin.bottom
      d3Select.select(this.$refs.huxChart).selectAll("svg").remove()
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

      let xAxisDomain = d3Array.extent(this.chartData, (d) => d.ltv)

      let x = d3Scale
        .scaleLinear()
        .domain([0, xAxisDomain[1]])
        .range([1, this.width])

      let y = d3Scale
        .scaleBand()
        .range([0, this.height])
        .domain(this.chartData.map((d) => d.name))
        .padding(0.1)
      let appendCurrencySign = (text) => "$" + text.toLocaleString()
      svg
        .append("g")
        .classed("xAxis", true)
        .attr("transform", "translate(0," + this.height + ")")
        .call(
          d3Axis
            .axisBottom(x)
            .ticks(3)
            .tickSize(4)
            .tickFormat(appendCurrencySign)
        )
        .call((g) => g.selectAll(".path").attr("stroke", "none"))
        .attr("stroke-width", "0")
        .attr("stroke-opacity", "0.3")
        .style("font-size", 12)
      svg
        .append("g")
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
            .ticks(3)
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
            .attr("stroke", "none")
            .attr("stroke-opacity", "0.3")
        )

      svg
        .selectAll("myRect")
        .data(this.chartData)
        .enter()
        .append("rect")
        .attr("x", x(0))
        .attr("y", (d) => y(d.name))
        .attr("width", (d) => x(d.ltv))
        .attr("height", y.bandwidth())
        .attr("fill", "#40BAE8")
        .attr("class", "bar")
        .attr("rx", 2)
        .on("mouseover", (d) => applyHoverEffects(d))
        .on("mouseout", () => removeHoverEffects())
      svg
        .selectAll("myRect")
        .data(this.chartData)
        .enter()
        .append("text")
        .attr("y", (d) => y(d.name))
        .attr("text-anchor", "start")
        .attr("transform", "translate(" + 10 + " ," + 22 + ")")
        .style("fill", "white")
        .style("font-size", 12)
        .text((d) => `${d.name}`)
        .style("pointer-events", "none")
      let applyHoverEffects = (d) => {
        d3Select.selectAll("rect").style("fill-opacity", "0.5")
        d3Select
          .select(d.srcElement)
          .attr("fill-opacity", (d) => changeHoverPosition(d))
          .style("fill-opacity", "1")
      }
      let removeHoverEffects = () => {
        d3Select.selectAll("rect").style("fill-opacity", "1")
        this.tooltipDisplay(false)
      }
      let changeHoverPosition = (data) => {
        let incomeData = data
        incomeData.xPosition = x(data.ltv)
        incomeData.yPosition = y(data.name) - 380
        this.tooltipDisplay(true, incomeData)
      }
    },
    tooltipDisplay(showTip, incomeData) {
      this.$emit("tooltipDisplay", showTip, incomeData)
    },
  },
}
</script>

<style lang="scss" scoped>
.chart-container {
  margin-bottom: 40px;
  height: 325px;
  min-height: 150px;
  .chart-section {
    margin-bottom: -20px;
  }
  .income-card-title {
    font-family: Open Sans;
    font-style: normal;
    font-weight: normal;
    font-size: 15px;
    line-height: 20px;
  }
}
</style>
