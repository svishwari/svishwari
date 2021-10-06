<template>
  <div class="container">
    <span v-if="showChart">
      <div id="chart" ref="chart" @mousemove="getCordinates($event)"></div>
      <chart-legends :legends-data="legendsData" class="legend-style pl-5" />
      <chart-tooltip
        v-if="showTooltip"
        :position="{
          x: sourceInput.xPosition,
          y: sourceInput.yPosition,
        }"
        :tooltip-style="toolTipStyle"
      >
        <template #content>
          <div class="type mb-1">
            <span v-if="sourceInput.label == 'Men'" class="circle-men"></span>
            <span v-if="sourceInput.label == 'Women'" class="circle-women" />
            <span v-if="sourceInput.label == 'Other'" class="circle-other" />
            <span
              v-if="sourceInput.label == 'Men'"
              class="primary--text text--darken-1"
            >
              {{ sourceInput.label }}
            </span>
            <span v-if="sourceInput.label == 'Women'" class="primary--text">
              {{ sourceInput.label }}
            </span>
            <span
              v-if="sourceInput.label == 'Other'"
              class="primary--text text--lighten-7"
            >
              {{ sourceInput.label }}
            </span>
          </div>
          <div class="percentage black--text text--darken-4">
            {{ getPercentage(sourceInput.population_percentage) }}
          </div>
          <div class="value black--text text--darken-4">
            {{ sourceInput.size | Numeric }}
          </div>
        </template>
      </chart-tooltip>
    </span>
    <span v-else>
      <img
        src="@/assets/images/Chart_donut.png"
        alt="Hux"
        width="200"
        height="200"
        class="d-flex ml-10"
      />
      <div class="d-flex ml-6 global-text-line">
        <chart-legends :legends-data="legendsData" class="legend-style pl-5" />
      </div>
    </span>
  </div>
</template>

<script>
import ChartTooltip from "@/components/common/Charts/Tooltip/ChartTooltip.vue"
import ChartLegends from "@/components/common/Charts/Legends/ChartLegends.vue"
import TooltipConfiguration from "@/components/common/Charts/Tooltip/tooltipStyleConfiguration.json"
import * as d3Select from "d3-selection"
import * as d3Scale from "d3-scale"
import * as d3Shape from "d3-shape"

export default {
  name: "DoughnutChart",
  components: { ChartLegends, ChartTooltip },
  props: {
    data: {
      type: Array,
      required: true,
    },
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
    label: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      chartWidth: "",
      sourceInput: null,
      showTooltip: false,
      showChart: true,
      tooltip: {
        x: 0,
        y: 0,
      },
      toolTipStyle: TooltipConfiguration.genderChart,
      legendsData: [
        { color: "rgba(0, 85, 135, 1)", text: "Women" },
        { color: "rgba(12, 157, 219, 1)", text: "Men" },
        { color: "rgba(66, 239, 253, 1)", text: "Other" },
      ],
    }
  },
  watch: {
    chartDimensions: {
      handler() {
        d3Select.select(this.$refs.chart).selectAll("svg").remove()
        this.initiateChart()
      },
      immediate: false,
      deep: true,
    },
  },
  mounted() {
    this.initiateChart()
  },
  methods: {
    initiateChart() {
      let data = this.data
      this.showChart = false
      if (data.length != 0) {
        this.showChart = true
        // Initialize width, height & color range
        this.chartWidth = this.chartDimensions.width + "px"
        let width = this.chartDimensions.width - 50,
          height = this.chartDimensions.height - 10,
          radius = Math.min(width, height) / 1.8
        let color = d3Scale
          .scaleOrdinal()
          .range(["#0C9DDB", "#005587", "#42EFFD"])

        // Define outer-radius & inner-radius of donut-chart
        let arc = d3Shape
          .arc()
          .outerRadius(radius - 20)
          .innerRadius(radius - 30)

        let transformedArc = d3Shape
          .arc()
          .outerRadius(radius - 15)
          .innerRadius(radius - 35)

        // Assign value to chart
        let pie = d3Shape
          .pie()
          .sort(null)
          .value(function (d) {
            return parseInt((d.population_percentage * 100).toFixed(0))
          })

        // Append class & id
        d3Select
          .select("#chart")
          .append("div")
          .attr("id", "mainPie")
          .attr("class", "pieBox")

        // assign style attribute to chart div
        let svg = d3Select
          .select("#mainPie")
          .append("svg")
          .attr("width", width)
          .attr("height", height)
          .append("g")
          .attr(
            "transform",
            "translate(" + width / 2 + "," + (height - 2) / 2 + ")"
          )

        // create arc & append class attribute
        let g = svg
          .selectAll(".arc")
          .data(pie(data))
          .enter()
          .append("g")
          .attr("class", "arc")

        // fill the arc with colors
        g.append("path")
          .attr("d", arc)
          .style("fill", function (d) {
            return color(d.data.population_percentage)
          })
          .on("mouseover", (e, d) => applyArcHoverEvent(e, d))
          .on("mouseout", (e, d) => removeArcHoverEvent(e, d))

        let applyArcHoverEvent = (e, d) => {
          d3Select
            .select(e.srcElement)
            .attr("d", transformedArc)
            .style("filter", "drop-shadow(0px 3px 3px rgba(0, 0, 0, 0.4)")
          this.sourceInput = d.data
          this.showTooltip = true
          this.sourceInput.xPosition = this.tooltip.x - 20
          this.sourceInput.yPosition = this.tooltip.y
        }
        let removeArcHoverEvent = (e, d) => {
          d3Select.select(e.srcElement).attr("d", arc).style("filter", "none")
          this.sourceInput = d.data
          this.showTooltip = false
        }
      } else {
        this.legendsData = [
          { color: "rgba(208, 208, 206, 1)", text: "no data available" },
        ]
      }
    },
    getCordinates(evt) {
      this.tooltip.x = evt.offsetX + 60
      this.tooltip.y = evt.offsetY - 270
    },
    getPercentage(data) {
      return parseInt((data * 100).toFixed(0)) + "%"
    },
  },
}
</script>
<style lang="scss" scoped>
.container {
  padding: 0px !important;
  #chart {
    text-align: center;
  }
  .pieBox {
    display: inline-block;
  }
  .legend-style {
    margin-top: 8px;
  }
  .circle {
    height: 9px;
    border-radius: 9px;
    width: 9px;
    float: left;
    margin-top: 7px;
    margin-right: 3px;
  }
  .circle-men {
    @extend .circle;
    border: 2px solid var(--v-primary-darken1);
  }
  .circle-other {
    @extend .circle;
    border: 2px solid var(--v-primary-lighten7);
  }
  .circle-women {
    @extend .circle;
    border: 2px solid var(--v-primary-base);
  }
}
</style>
