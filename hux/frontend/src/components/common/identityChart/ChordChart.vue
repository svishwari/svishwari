<template>
  <v-card tile class="chart-container rounded-lg box-shadow-5">
    <v-list-item three-line>
      <v-list-item-content>
        <div class="title-section">
          <tooltip position-top>
            <template #label-content>
              Individual Identity
              <icon type="info" :size="12" />
            </template>
            <template #hover-content>
              {{ tooltipText }}
            </template>
          </tooltip>
        </div>
        <v-list-item-subtitle
          v-for="item in legendsData"
          :key="item.id"
          class="legend-section"
        >
          <icon :type="item.icon" :size="12" color="primary" />
          <span>{{ item.prop }}</span>
        </v-list-item-subtitle>
      </v-list-item-content>
      <div
        ref="huxChart"
        class="chart-section"
        @mouseover="getCordinates($event)"
      ></div>
    </v-list-item>
  </v-card>
</template>

<script>
import * as d3Chord from "d3-chord"
import * as d3Shape from "d3-shape"
import * as d3Scale from "d3-scale"
import * as d3Select from "d3-selection"
import * as d3Array from "d3-array"
import Tooltip from "@/components/common/Tooltip"
import Icon from "@/components/common/Icon"
export default {
  name: "ChordChart",
  components: { Icon, Tooltip },
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
     * Accepts an Array of Objects needs to map with legends.
     * eg: {prop: '', icon: ''}
     */
    chartLegendsData: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      width: 220,
      height: 250,
      outerRadius: 0,
      innerRadius: 0,
      tooltipText: "Most recent co-occurence between identifiers",
      legendsData: this.chartLegendsData,
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
    value: function () {
      d3Select.select(this.$refs.huxChart).select("svg").remove()
      this.calculateChartValues()
    },
  },

  mounted() {
    this.initializeValues()
    this.calculateChartValues()
  },
  methods: {
    initializeValues() {
      this.outerRadius = Math.min(this.width, this.height) * 0.5 - 10
      this.innerRadius = this.outerRadius - 7
    },

    calculateChartValues() {
      const padAngle = 0.03

      let svg = d3Select
        .select(this.$refs.huxChart)
        .append("svg")
        .attr("width", this.width)
        .attr("height", this.height)
        .attr("outerRadius", this.outerRadius)
        .attr("innerRadius", this.innerRadius)

      let chord = d3Chord
        .chord()
        .padAngle(padAngle)
        .sortSubgroups(d3Array.descending)

      let arc = d3Shape
        .arc()
        .innerRadius(this.innerRadius)
        .outerRadius(this.outerRadius)

      let ribbon = d3Chord.ribbon().radius(this.innerRadius).padAngle(padAngle)

      let color = d3Scale
        .scaleOrdinal()
        .domain(d3Array.range(this.colorCodes.length))
        .range(this.colorCodes)

      let g = svg
        .append("g")
        .attr(
          "transform",
          "translate(" + this.width * 0.5 + "," + this.height * 0.5 + ")"
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
        .on("mouseout", () => mouseOut())

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
        .on("mouseout", () => mouseOut())

      let arcMouseOver = (g, i) => {
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

      let mouseOut = () => {
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
  height: 252px;

  .legend-section {
    span {
      margin-left: 8px;
      font-size: 12px;
      line-height: 16px;
      color: var(--v-gray-base) !important;
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
