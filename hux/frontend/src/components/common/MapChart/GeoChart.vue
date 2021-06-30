<template>
  <v-card tile class="chart-container rounded-lg box-shadow-5">
    <v-list-item three-line>
      <div
        class="chart-section"
        ref="huxChart"
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
import * as d3Geo from "d3-geo"

export default {
  name: "geo-chart",
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
      width: 900,
      height: 900,
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

      let chord = d3Chord
        .chord()
        .padAngle(padAngle)
        .sortSubgroups(d3Array.descending)

    
    let projection = d3Geo.albersUsa().translate([this.width/2, this.height/2]).scale([1000]);  

    let path = d3Geo.path().projection(projection); 

    let color = d3Scale.linear().range(["rgb(213,222,217)","rgb(69,173,168)","rgb(84,36,55)","rgb(217,91,67)"]);

    let legendText = ["Cities Lived", "States Lived", "States Visited", "Nada"];

    
     
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
}
</script>

<style lang="scss" scoped>
.chart-container {
  max-width: 100%;
  height: 500px;

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
