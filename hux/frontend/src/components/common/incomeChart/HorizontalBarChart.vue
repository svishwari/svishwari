<template>
  <div>
    <v-card
      class="rounded-lg card-style"
      maxWidth="300px"
      minHeight="150px"
      flat
    >
      <v-card-title class="d-flex justify-space-between pb-6 pl-6 pt-5">
        <div class="mt-2">
          <span class="d-flex align-center black--text text-decoration-none">
            Top locations &amp; spending
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
      width: 255,
      height: 237,
      show: false,
      tooltip: {
        x: 0,
        y: 0,
      },
      margin: { top: 20, right: 20, bottom: 20, left: 10 },
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

 var x = d3Scale.scaleLinear()
    .domain([0, 4000])
    .range([ 1, this.width]);


      let y = d3Scale
        .scaleBand()
        .range([0, this.height])
        .domain(this.chartData.map((d) => d.name))
        .padding(0.1)


   let appendCurrencySign = (text) =>
        "$" + text
        
      svg
        .append("g")
        .attr("transform", "translate(0," + this.height + ")")
        .call(d3Axis.axisBottom(x).ticks(3).tickSize(0).tickFormat(appendCurrencySign))
        .call((g) => g.selectAll(".path").attr("stroke", "none"))
        .attr("stroke-width", "0")
        .attr("stroke-opacity", "0.3")


      svg
        .append("g")
        // .call(d3Axis.axisLeft(y).tickSize(0).tickFormat(appendElipsis))
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

    //   svg
    //     .append("text")
    //     .attr("y", (d) => y(d.ltv))
    //     .attr('text-anchor', 'middle')
    //     .text((a) => `${d.name}%`)

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
        .on("mouseover", (d) => applyHoverEffects(d))
        .on("mouseout", () => removeHoverEffects())

         svg
        .selectAll("myRect")
        .data(this.chartData)
        .enter()
        .append("text")
        .attr("y", (d) => y(d.name))
        .attr('text-anchor', 'start')
         .attr(
          "transform",
          "translate(" +
            20 +
            " ," +
            22 +
            ")"
        )
        .style("fill","white")
        .text((d) => `${d.name}`)
        


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
        featureData.xPosition = x(data.ltv)
        featureData.yPosition = y(data.ltv) + 12
        this.tooltipDisplay(true, featureData)
        svg
          .append("circle")
          .classed("removeableCircle", false)
        //   .attr("cx", featureData.xPosition)
        //   .attr("cy", featureData.yPosition)
        //   .attr("r", 4)
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
  height: 325px;
  .chart-section {
    margin-bottom: -20px;
  }
}
</style>
