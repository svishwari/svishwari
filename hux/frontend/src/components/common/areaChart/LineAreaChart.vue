<template>
  <div>
    <v-card
      class="rounded-lg card-style"
      maxWidth="450px"
      minHeight="150px"
      flat
    >
      <v-card-title class="d-flex justify-space-between pb-6 pl-6 pt-5">
        <div class="mt-2 ml-2">
          <span
            class="
              d-flex
              align-center
              income-card-title
              black--text
              text-decoration-none
            "
          >
            Area Chart
          </span>
        </div>
        <div
          class="chart-section"
          ref="huxChart"
        ></div>
      </v-card-title>
      <v-card-text class="pl-6 pr-6 pb-6"> 
           <div id="legend"></div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import * as d3Shape from "d3-shape"
import * as d3Scale from "d3-scale"
import * as d3Select from "d3-selection"
import * as d3Array from "d3-array"
import * as d3Axis from "d3-axis"
import * as d3TimeFormat from "d3-time-format"

export default {
  name: "line-area-chart",
  props: {
    value: {
      type: Array,
      required: true,
    },

  },
  data() {
    return {
      width: 355,
      height: 237,
      chartData: this.value,
    }
  },
  methods: {
    async initiateAreaChart() {
      let areaChartData = [
        {
          year: "2020-11-30T00:00:00.000Z",
          aData: 2144,
          bData: 3199,
          cData: 3088,
        },
        {
          year: "2020-12-30T00:00:00.000Z",
          aData: 3144,
          bData: 4265,
           cData: 3842,
        },
        {
          year: "2021-01-30T00:00:00.000Z",
          aData: 3211,
          bData: 4986,
           cData: 3999,
        },
        {
          year: "2021-02-28T00:00:00.000Z",
          aData: 3211,
          bData: 4986,
           cData: 3999,
        },
        {
           year: "2021-03-30T00:00:00.000Z",
          aData: 4866,
          bData: 6109,
           cData: 6109,
        },
      ]

      let colorCodes = ["rgba(0, 85, 135, 1)", "rgba(12, 157, 219, 1)","rgba(66, 239, 253, 1)"]

      let svg = d3Select
        .select(this.$refs.huxChart)
        .append("svg")
        .attr("width", this.width)
        .attr("height", this.height)

 

      let strokeWidth = 1.5
      let margin = { top: 0, bottom: 20, left: 40, right: 20 }
      let chart = svg
        .append("g")
        .attr("transform", `translate(${margin.left},0)`)

 

      let width =
        +svg.attr("width") - margin.left - margin.right - strokeWidth * 2
      let height = +svg.attr("height") - margin.top - margin.bottom

 

      let grp = chart
        .append("g")
        .attr(
          "transform",
          `translate(-${margin.left - strokeWidth},-${margin.top})`
        )

 

      let stack = d3Shape.stack().keys(["aData", "bData", "cData"])
      let stackedValues = stack(areaChartData)
      let stackedData = []

 

      stackedValues.forEach((layer, index) => {
        let currentStack = []
        layer.forEach((d, i) => {
         d[1] = d[1]-d[0]
         d[0] = 0
          currentStack.push({
            values: d,
            year: new Date(areaChartData[i].year),
          })
        })
       
        stackedData.push(currentStack)
       
      })
      //  console.log("stackedData",stackedData)

 

      let yScale = d3Scale
        .scaleLinear()
        .range([height, 0])
        .domain([
          0,
          d3Array.max(stackedValues[stackedValues.length - 1], (dp) => dp[1]),
        ])

      let xScale = d3Scale
        .scaleLinear()
        .range([0, width])
        .domain(d3Array.extent(areaChartData, (dataPoint) => new Date(dataPoint.year)))

      let area = d3Shape
        .area()
        .x((dataPoint) => xScale(dataPoint.year))
        .y0((dataPoint) => yScale(dataPoint.values[0]))
        .y1((dataPoint) => yScale(dataPoint.values[1]))


      let series = grp
        .selectAll(".series")
        .data(stackedData)
        .enter()
        .append("g")
        .attr("class", "series")
        
       series
        .append("path")
        .attr("transform", `translate(${margin.left},0)`)
        .style("fill", (d, i) => colorCodes[i])
        .attr("stroke", (d, i) => colorCodes[i])
        .attr("stroke-linejoin", "round")
        .attr("stroke-linecap", "round")
        .attr("stroke-width", 2)
        .attr("stroke-width", 2)
        .attr("fill-opacity", 0.5)
        .attr("d", (d) => area(d))
        .on("mouseover", (d) => appendLine(d))
        // .on("mouseout", () => removeHover())


let appendLine = (d) => {
  console.log("d",d.srcElement)
     d3Select
          .select(d.srcElement)
          .attr("fill-opacity", (d) => appendData(d))
          .style("fill-opacity", "1")
    // svg.selectAll(".dot")
    // .attr("r", 5)
    // .style("fill", "white")

       svg
          .append("circle")
          .classed("removeableCircle", true)
          .attr("cx", 30)
          .attr("cy", 40)
          .attr("r", 5)
          .style("stroke", "red")
          .style("stroke-opacity", "1")
          .style("fill", "white")
          .style("pointer-events", "none")
    
  //        stackedValues.forEach(function(layer, index) {
  //     console.log("layer", layer.index)
  // layer.forEach(points => {
  // svg
  //  .append("circle")
  //  .attr("class", "dot")
  //  .attr("r", 10)
  //  .attr("cx",  (d) => xScale(new Date(points.data.year)) + 40)
  //  .attr("cy", (d) => yScale(points[1]))
  // .style("fill","red")
  //       .attr("stroke", "red")
  // });
  
    //   svg
    //     .append("g")
    //     .call(
    //       d3Axis
    //         .axisBottom(xScale)
    //         .tickSize(0)
    //         .tickFormat("")
    //         .ticks(5)
    //         .tickSizeInner(this.height)
    //     )
    //     .call((g) =>
    //       g
    //         .selectAll(".tick line")
    //         .attr("stroke", "#d0d0ce")
    //         .attr("stroke-opacity", "0.3")
    //     )
    //     .call((g) =>
    //       g
    //         .selectAll("path")
    //         .attr("stroke", "none")
    //         .attr("stroke-opacity", "0.3")
    //     )


     
}

 let appendData = (data) => {

 }
// let removeHover = () => {
//   d3Select.select(this.$refs.huxChart).select(".tick line").remove()
// }
      chart
        .append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3Axis.axisBottom(xScale).ticks(areaChartData.length).tickFormat(d3TimeFormat.timeFormat("%b %Y")))

 

      chart
        .append("g")
        .attr("transform", `translate(0, 0)`)
        .call(d3Axis.axisLeft(yScale))

stackedValues.forEach(function(layer, index) {
  layer.forEach(points => {
  svg
   .append("circle")
   .attr("class", "dot")
   .attr("r", 3)
   .attr("cx",  (d) => xScale(new Date(points.data.year)) + 40)
   .attr("cy", (d) => yScale(points[1]))
  .style("fill", colorCodes[index])
        .attr("stroke", colorCodes[index])
  });

//    var legendSvg = d3Select
//         .select("#legend")
//         .append("svg")
//         .attr("viewBox", "0 0 200 25") // for responsive
//         .attr("id", "mainSvg")
//         .attr("class", "svgBox")
//         .style("margin-left", "20px")
//         .style("margin-right", "20px")

//           // calculating distance b/n each legend
//       var legend = legendSvg
//         .selectAll(".legend")
//         .data(data)
//         .enter()
//         .append("g")
//         .attr("class", "legend")
//         .attr("transform", function (d) {
//           var y = line * 25
//           var x = col
//           col += d.label.length * 10 + 25
//           return "translate(" + x + "," + y + ")"
//         })

//          // creating legend circle & fill color
//       legend
//         .append("circle")
//         .attr("cx", 10)
//         .attr("cy", 10)
//         .attr("r", 6)
//         .style("fill", function (d) {
//           return color(d.population_percentage)
//         })

})



    },
  },

 //adds dots where original data would go but without error



  watch: {
    value: function () {
      d3Select.select(this.$refs.huxChart).select("svg").remove()
      this.initiateAreaChart()
    },
  },

 

  mounted() {
    this.initiateAreaChart()
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