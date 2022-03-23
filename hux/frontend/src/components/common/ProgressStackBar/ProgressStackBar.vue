<template>
  <div class="chart-container">
    <div ref="progressStackBarChart" :class="dynamicChartID"></div>
  </div>
</template>

<script>
import groupData from "./groupData"
import sampleData from "./sampleData"
import * as d3Format from "d3-format"
import * as d3Scale from "d3-scale"
import * as d3Select from "d3-selection"

export default {
  name: "ProgressStackBar",
  props: {
    width: {
      type: [Number, String],
      required: true,
    },
    height: {
      type: [Number, String],
      required: true,
    },
    showPercentage: {
      type: Boolean,
      default: false,
      required: false,
    },
    value: {
      type: Array,
      default: sampleData,
      required: false,
    },
    barId: {
      type: Number,
      default: 1,
      required: false,
    },
  },
  data() {
    return {
      dynamicChartID: `bar-${this.barId}`,
    }
  },
  watch: {
    chartDimensions: {
      handler() {
        d3Select
          .select(this.$refs.progressStackBarChart)
          .selectAll("svg")
          .remove()
        this.stackedBar(`.${this.dynamicChartId}`, this.value)
      },
      immediate: false,
      deep: true,
    },
  },
  mounted() {
    this.dynamicChartId = `bar-${this.barId}`
    this.stackedBar(`.${this.dynamicChartId}`, this.value)
  },
  methods: {
    rounded_rect(x, y, w, h, r, tl, tr, bl, br) {
      var retval
      retval = "M" + (x + r) + "," + y
      retval += "h" + (w - 2 * r)
      if (tr) {
        retval += "a" + r + "," + r + " 0 0 1 " + r + "," + r
      } else {
        retval += "h" + r
        retval += "v" + r
      }
      retval += "v" + (h - 2 * r)
      if (br) {
        retval += "a" + r + "," + r + " 0 0 1 " + -r + "," + r
      } else {
        retval += "v" + r
        retval += "h" + -r
      }
      retval += "h" + (2 * r - w)
      if (bl) {
        retval += "a" + r + "," + r + " 0 0 1 " + -r + "," + -r
      } else {
        retval += "h" + -r
        retval += "v" + -r
      }
      retval += "v" + (2 * r - h)
      if (tl) {
        retval += "a" + r + "," + r + " 0 0 1 " + r + "," + -r
      } else {
        retval += "v" + -r
        retval += "h" + r
      }
      retval += "z"
      return retval
    },
    async stackedBar(bind, data, config) {
      config = {
        f: d3Format.format(".1f"),
        margin: { top: 20, right: 10, bottom: 20, left: 10 },
        width: this.width,
        height: this.showPercentage ? 200 : this.height,
        barHeight: this.height,
        colors: ["#DA291C", "#FFCD00", "#86BC25"],
        ...config,
      }
      const { margin, width, height, barHeight, colors } = config
      const w = width - margin.left - margin.right
      const h = height - margin.top - margin.bottom
      const halfBarHeight = barHeight / 2

      const total = data.reduce((accum, item) => accum + item.value, 0)
      const _data = groupData(data, total)
      // set up scales for horizontal placement
      const xScale = d3Scale.scaleLinear().domain([0, total]).range([0, w])

      // create svg in passed in div
      const selection = d3Select
        .select(bind)
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")

      // stack rect for each data value
      selection
        .selectAll("rect")
        .data(_data)
        .enter()
        .append("path")
        .attr("class", "rect-stacked")
        .attr("x", (d) => xScale(d.cumulative))
        .attr("y", h / 2 - halfBarHeight)
        .attr("height", barHeight)
        .attr("width", (d) => xScale(d.value))
        .attr("d", (d, i) =>
          i == 0
            ? this.rounded_rect(
                xScale(d.cumulative),
                h / 2 - halfBarHeight,
                xScale(d.value),
                barHeight,
                3,
                true,
                false,
                true,
                false
              )
            : i == 2
            ? this.rounded_rect(
                xScale(d.cumulative),
                h / 2 - halfBarHeight,
                xScale(d.value),
                barHeight,
                3,
                false,
                true,
                false,
                true
              )
            : this.rounded_rect(
                xScale(d.cumulative),
                h / 2 - halfBarHeight,
                xScale(d.value),
                barHeight,
                3,
                false,
                false,
                false,
                false
              )
        )
        .style("fill", (d, i) => colors[i])

      // add the labels
      if (this.showPercentage) {
        selection
          .selectAll(".text-label")
          .data(_data)
          .enter()
          .append("text")
          .attr("class", "text-label")
          .attr("text-anchor", "middle")
          .attr("x", (d) => xScale(d.cumulative) + xScale(d.value) / 2)
          .attr("y", h / 2 + halfBarHeight * 1.1 + 20)
          .text((d) => d.value + "%")
          .style("font-size", "12px")
          .style("font-weight", "600")
          .style("line-height", "16.34px")
      }
    },
  },
}
</script>
<style lang="scss" scoped></style>
