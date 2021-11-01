<template>
  <div
    ref="chordChart"
    class="chart-section"
    @mouseover="getCordinates($event)"
  ></div>
</template>

<script>
import * as d3Chord from "d3-chord"
import * as d3Shape from "d3-shape"
import * as d3Scale from "d3-scale"
import * as d3Select from "d3-selection"
import * as d3Array from "d3-array"
export default {
  name: "ChordChart",
  props: {
    /**
     * Accepts an array of ranges in N*N matrix  format for creating chart arc & ribbon mapping
     * must be match with no. of color codes
     * eg: [1951, 0, 2060, 6171, 3622] for 5 color code ranges,
     */
    value: {
      type: Array,
      required: true,
    },
    /**
     * Accepts an Array of color codes for filling up chart arc.
     * eg: ["#43b02a", "#efa34c"],
     */
    colorCodes: {
      type: Array,
      required: true,
    },
    /**
     * Adjust chart height as per screen resolution.
     */
    chartDimensions: {
      type: Object,
      required: true,
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
      width: 190,
      height: 190,
      radius: 0,
      top: 50,
      left: 60,
      show: false,
      tooltip: {
        x: 0,
        y: 0,
      },
    }
  },
  watch: {
    chartDimensions: {
      handler() {
        d3Select.select(this.$refs.chordChart).selectAll("svg").remove()
        this.initiateChordChart()
      },
      immediate: false,
      deep: true,
    },
  },

  mounted() {
    this.initiateChordChart()
  },
  methods: {
    initiateChordChart() {
      this.radius = Math.min(this.width, this.height) / 2.1
      const padAngle = 0.03

      let svg = d3Select
        .select(this.$refs.chordChart)
        .append("svg")
        .attr("width", this.width)
        .attr("height", this.height)
        .attr("outerRadius", this.radius - 18)
        .attr("innerRadius", this.radius - 25)

      let chord = d3Chord
        .chord()
        .padAngle(padAngle)
        .sortSubgroups(d3Array.descending)

      let arc = d3Shape
        .arc()
        .innerRadius(this.radius - 25)
        .outerRadius(this.radius - 18)

      let transformedArc = d3Shape
        .arc()
        .innerRadius(this.radius - 12)
        .outerRadius(this.radius - 25)

      let ribbon = d3Chord
        .ribbon()
        .radius(this.radius - 25)
        .padAngle(padAngle)

      let color = d3Scale
        .scaleOrdinal()
        .domain(d3Array.range(this.colorCodes.length))
        .range(this.colorCodes)

      let g = svg
        .append("g")
        .attr(
          "transform",
          "translate(" + this.width / 2 + "," + this.height / 2 + ")"
        )
        .datum(chord(this.value))

      let group = g
        .append("g")
        .attr("class", "groups")
        .selectAll("g")
        .data((chords) => chords.groups)
        .enter()
        .append("g")

      group
        .append("path")
        .style("fill", (d) => color(d.index))
        .attr("d", arc)
        .on("mouseover", (g, i) => arcMouseOver(g, i))
        .on("mouseout", (g, i) => mouseOut(g, i))

      g.append("g")
        .attr("class", "ribbons")
        .selectAll("path")
        .data((chords) => chords)
        .enter()
        .append("path")
        .attr("d", ribbon)
        .attr("fill-opacity", "0.5")
        .style("fill", (d) => color(d.target.index))
        .on("mouseover", (e, d) => ribbonMouseOver(e, d))
        .on("mouseout", (g) => ribbonMouseOut(g))

      let arcMouseOver = (g, i) => {
        d3Select
          .select(g.srcElement)
          .attr("d", transformedArc)
          .style("filter", "drop-shadow(0px 3px 3px rgba(0, 0, 0, 0.4)")
        this.tooltipDisplay(true, true, [i.index])
        d3Select
          .selectAll("g.ribbons path")
          .filter(
            (d) => d.source.index !== i.index && d.target.index !== i.index
          )
          .attr("fill-opacity", "0.1")
          .style("fill", (d) => color(d.target.index))
      }

      let ribbonMouseOver = (e, d) => {
        d3Select
          .select(e.srcElement)
          .style("filter", "drop-shadow(0px 3px 3px rgba(0, 0, 0, 0.4)")
        this.tooltipDisplay(true, false, [d.source.index, d.target.index])
        d3Select
          .selectAll("g.ribbons path")
          .attr("fill-opacity", "0.1")
          .style("fill", (d) => color(d.target.index))

        d3Select
          .select(e.srcElement)
          .attr("fill-opacity", "1")
          .style("fill", (d) => color(d.target.index))
      }

      let mouseOut = (g) => {
        d3Select.select(g.srcElement).attr("d", arc).style("filter", "none")
        this.tooltipDisplay(false, false, [])
        d3Select
          .selectAll("g.ribbons path")
          .attr("fill-opacity", "0.5")
          .style("fill", (d) => color(d.target.index))
      }

      let ribbonMouseOut = (g) => {
        d3Select.select(g.srcElement).style("filter", "none")
        this.tooltipDisplay(false, false, [])
        d3Select
          .selectAll("g.ribbons path")
          .attr("fill-opacity", "0.5")
          .style("fill", (d) => color(d.target.index))
      }
    },

    getCordinates(event) {
      this.tooltip.x = event.offsetX
      this.tooltip.y = event.offsetY
      this.$emit("cordinates", this.tooltip)
    },

    tooltipDisplay(showTip, isArcHover, groupIndex) {
      this.$emit("tooltipDisplay", showTip, isArcHover, groupIndex)
    },
  },
}
</script>

<style lang="scss" scoped>
.chart-container {
  max-width: none;
  height: 247px;

  .legend-section {
    span {
      margin-left: 8px;
      font-size: 12px;
      line-height: 16px;
      color: var(--v-black-darken1) !important;
    }
  }

  .title-section {
    font-size: 15px;
    line-height: 20px;
    font-weight: 400;
  }

  .chart-section {
    margin-bottom: -20px;
  }
}
</style>
