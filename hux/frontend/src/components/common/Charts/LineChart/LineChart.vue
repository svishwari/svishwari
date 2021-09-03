<template>
  <div class="chart-container" :style="{ maxWidth: chartWidth }">
    <div ref="stackBarChart" class="chart-section"></div>
  </div>
</template>

<script>
import * as d3Axis from "d3-axis"
import * as d3Shape from "d3-shape"
import * as d3Scale from "d3-scale"
import * as d3Select from "d3-selection"
import * as d3Array from "d3-array"
import * as d3TimeFormat from "d3-time-format"
import * as d3Collection from "d3-collection"
import * as d3Regression from "d3-regression"
import colors from "../../../../plugins/theme"

export default {
  name: "LineChart",
  props: {
    value: {
      type: Array,
      required: true,
    },
    colorCodes: {
      type: Array,
      required: false,
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
      data: this.value,
      chartWidth: "",
      toolTip: {
        xPosition: 0,
        yPosition: 0,
        index: 0,
        date: "",
        totalCustomers: 0,
        addedCustomers: 0,
      },
    }
  },

  watch: {
    chartDimensions: {
      handler() {
        d3Select.select(this.$refs.stackBarChart).selectAll("svg").remove()
        this.initiateStackBarChart()
      },
      immediate: false,
      deep: true,
    },
  },
  methods: {
    async initiateStackBarChart() {
      await this.value

    //  console.log(this.totalCustomerData)
      this.chartWidth = this.chartDimensions.width + "px"
      this.width = this.chartDimensions.width
      this.height = this.chartDimensions.height
      let margin = { top: 15, right: 45, bottom: 100, left: 68 }
      let w = this.chartDimensions.width - margin.left - margin.right
      let h = this.chartDimensions.height - margin.top - margin.bottom
      let formattedData = []
      let initialIndex = 0
      let barColorCodes = []
      let monthChangeIndexs = []


      let svg = d3Select
        .select(this.$refs.stackBarChart)
        .append("svg")
        .attr("width", this.width + margin.left + margin.right)
        .attr("height", this.height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`)

     // this.colorCodes.forEach((color) => barColorCodes.push(colors[color]))

      // let week = d3TimeFormat.timeFormat("%U")
      // let weeklyAggData = d3Collection
      //   .nest()
      //   .key((d) => week(new Date(d.date)))
      //   .entries(this.totalCustomerData)

      // let initialWeek = weeklyAggData[0].values
      // let initialWeekEndingDate = initialWeek[initialWeek.length - 1].date

      // monthChangeIndexs.push({ index: 0, date: initialWeekEndingDate })

      // let initialMonth = new Date(initialWeekEndingDate).getMonth()
      // let lastWeekEndingData = 0

      // weeklyAggData.forEach((element, index) => {
      //   let weekData = element.values
      //   let weekLastDate = weekData[weekData.length - 1].date
      //   let currentWeekEndingData =
      //     weekData[weekData.length - 1].total_customers
      //   if (new Date(weekLastDate).getMonth() != initialMonth) {
      //     initialMonth = new Date(weekLastDate).getMonth()
      //     if (initialIndex == 2) {
      //       initialIndex = 0
      //     } else initialIndex++

      //     monthChangeIndexs.push({
      //       index: index,
      //       date: weekLastDate,
      //     })
      //   }
      //   formattedData.push({
      //     date: weekLastDate,
      //     total_customers: currentWeekEndingData,
      //     new_customers_added:
      //       lastWeekEndingData == 0
      //         ? weekData.reduce((sum, d) => sum + d.new_customers_added, 0)
      //         : currentWeekEndingData - lastWeekEndingData,
      //     index: index == weeklyAggData.length - 1 ? 3 : initialIndex,
      //     barIndex: index,
      //     isEndingBar: index > weeklyAggData.length - 3,
      //   })
      //   lastWeekEndingData = currentWeekEndingData
      // })

      let stack = d3Shape
        .stack()
        .keys(["total_customers", "new_customers_added"])
      let stackedValues = stack(formattedData)

      stackedValues.forEach((layer) => {
        layer.forEach((d) => {
          d[1] = d[1] - d[0]
          d[0] = 0
        })
      })

      let dateArr = this.data.map(d => d.date)

   //   console.log(dateArr)

      let xScale = d3Scale
        .scaleTime()
        .domain(
          d3Array.extent(dateArr, function (d) {
            return new Date(d)
          })
        )
        .range([0, w])
        .nice(8)

      // let xScale = d3Scale
      //   .scaleBand()
      //   .domain([0, 100])
      //   .range([0, w])
      //   .nice(8)
        // .paddingInner(0.33)
        // .paddingOuter(0.11)

      let yScale = d3Scale
        .scaleLinear()
        .domain([0, d3Array.max(this.data, (d) => d.total_event_count)])
        .range([h, 0])
        .nice(4)

      // let chart = svg.append("g").attr(
      //     "transform",
      //     `translate(-${margin.left - strokeWidth},-${margin.top})`
      //   )

            let chart = svg
        .append("g")
        .attr("transform", `translate(${margin.left},0)`)

let strokeWidth = 1.5
      let grp = chart
        .append("g")
        .attr(
          "transform",
          `translate(-${margin.left - strokeWidth},-${margin.top})`
        )
      // let convertCalendarFormat = (value) => {
      //   let tickDate = monthChangeIndexs.find((bar) => bar.index == value)
      //   if (tickDate) {
      //     return this.$options.filters.Date(tickDate.date, "MMM [']YY")
      //   } else return ""
      // }

      // let applyNumericFilter = (value) =>
      //   this.$options.filters.Numeric(value, true, false, true)

      // svg
      //   .append("g")
      //   .classed("xAxis-alternate", true)
      //   .attr("transform", "translate(0," + 243 + ")")
      //   .call(d3Axis.axisBottom(xScale).tickSize(0).tickFormat(""))
      //   .style("stroke-width", 16)

      svg
        .append("g")
        .classed("xAlternateAxis", true)
        .attr("transform", `translate(0,${h})`)
        .call(
          d3Axis
            .axisBottom(xScale)
            .tickSize(10)
            .ticks(6)
            .tickPadding(15)
            .tickFormat("")
        )
        .style("font-size", "14px")

        svg
        .append("g")
        .classed("yAlternateAxis", true)
        .attr("transform", "translate(0, 0)")
        .call(d3Axis.axisLeft(yScale).tickSize(10).ticks(4).tickFormat(""))
        .attr("stroke-width", "1")
        .attr("stroke-opacity", "1")
        .style("font-size", "12px")

      svg
        .append("g")
        .classed("xAxis", true)
        .attr("transform", `translate(0,${h})`)
        .call(
          d3Axis
            .axisBottom(xScale)
            .tickSize(-h)
            .ticks(6)
            .tickPadding(15)
            .tickFormat(d3TimeFormat.timeFormat("%-m/%-d/%Y"))
        )
        .style("font-size", "14px")

      svg
        .append("g")
        .classed("yAxis", true)
        .attr("transform", "translate(0, 0)")
        .call(d3Axis.axisLeft(yScale).tickSize(-w).ticks(4).tickPadding(15))
        .attr("stroke-width", "1")
        .attr("stroke-opacity", "1")
        .style("font-size", "12px")

      //  let linePath = chart
      //   .selectAll("g")
      //   .attr("class", "linePath")
      //   .data(this.data)
      //   .enter()
      //   .append("g")

      d3Select.selectAll(".domain").style("stroke", "#E2EAEC")
      d3Select.selectAll(".tick line").style("stroke", "#E2EAEC")
      d3Select
        .selectAll(".xAxis .tick text")
        .attr("x", 10)
        .style("color", "#4F4F4F")
      d3Select.selectAll(".yAxis .tick text").style("color", "#4F4F4F")
       d3Select.selectAll(".yAlternateAxis .tick line").style("stroke", "black")
        d3Select.selectAll(".xAlternateAxis .tick line").style("stroke", "black")

      // let series = grp
      //   .selectAll(".series")
      //   .data(this.data)
      //   .enter()
      //   .append("g")
      //   .attr("class", "series")



      let line = d3Shape
        .line()
        .x((dataPoint) => { console.log(dataPoint)
        return xScale(dataPoint.date)})
        .y((dataPoint) => yScale(dataPoint.total_event_count))


        var lines = svg.selectAll("path.line")
        .data(this.data)
        .enter()
        .append("path")
            .attr("d", d =>  {
             // console.log(d)
              return line(d)
            })
            .attr("class", "line")
            .attr("fill", "none")
            .attr("stroke", "red");

      // series.selectAll(".series")
      //   .append("path")
      //   .attr("transform", `translate(${margin.left},0)`)
      //   .attr("class", "line")
      //   .style("stroke", "red")
      //   .attr("stroke-width", 2)
      //   .style("fill", "none")
      //   .attr("d", (d) => {
      //     console.log(d)
      //     return lineTrace(d)
      //   } )


//               svg.selectAll("myRect")
//         .data(this.data)
//         .enter()
//         .append("path")
//         .attr("transform", `translate(${margin.left},0)`)
//         .attr("class", "line")
//         .style("stroke", "black")
//         .attr("stroke-width", 2)
//         .style("fill", "none")
// .attr("d", lineTrace)


//               svg
//         .selectAll("myLine")
//         .data(this.data)
//         .enter()
//         .append("path")
//         .attr("d", (d) => lineTrace(d))
//         // .attr("x", d => xScale(new Date(d.date)))
//         // .attr("y", (d) => yScale(d.total_event_count))
// .attr("stroke", "red")
      // let topRoundedRect = (x, y, width, height) => {
      //   if (height < 0) {
      //     height = 0
      //   }
      //   return `M${x},${y + ry}
      //   a${rx},${ry} 0 0 1 ${rx},${-ry}
      //   h${width - 2 * rx}
      //   a${rx},${ry} 0 0 1 ${rx},${ry}
      //   v${height - ry}
      //   h${-width}Z`
      // }

      // groups
      //   .selectAll("bar")
      //   .data((d) => d)
      //   .enter()
      //   .append("path")
      //   .attr("d", (d, i) =>
      //     topRoundedRect(
      //       xScale(i),
      //       yScale(d[1]),
      //       xScale.bandwidth() < 30 ? xScale.bandwidth() : 30,
      //       yScale(d[0]) - yScale(d[1])
      //     )
      //   )
      //   .style("fill", (d) => barColorCodes[d.data.index])
      //   .on("mouseover", (d) => applyHoverEffects(d, xScale.bandwidth()))
      //   .on("mouseout", () => removeHoverEffects())

      let linearRegression = d3Regression
        .regressionLinear()
        .x((d) => d.barIndex)
        .y((d) => d.total_customers)

      let regLine = linearRegression(formattedData)

      let max = d3Array.max(formattedData, (d) => d.barIndex)
      // svg
      //   .append("line")
      //   .attr("class", "regression")
      //   .style("stroke-dasharray", "6")
      //   .style("stroke", "#86BC25")
      //   .style("stroke-width", 1.5)
      //   .attr("x1", xScale(0) + 9)
      //   .attr("y1", yScale(regLine.a))
      //   .attr("x2", xScale(max) + 14)
      //   .attr("y2", yScale(regLine.b))

      let applyHoverEffects = (d, width) => {
        d3Select
          .select(d.srcElement)
          .attr("fill-opacity", (d) => barHoverIn(d.data, width))
      }

      let removeHoverEffects = () => {
        d3Select.selectAll(".foreGroundBars").style("fill-opacity", "1")
        d3Select
          .select(this.$refs.stackBarChart)
          .select(".removeableCircle")
          .remove()
        this.tooltipDisplay(false)
      }

      let barHoverIn = (data, width) => {
        svg
          .append("circle")
          .classed("removeableCircle", true)
          .attr("cx", xScale(data.barIndex) + width / 2)
          .attr("cy", yScale(data.total_customers))
          .attr("r", 4)
          .style("stroke", barColorCodes[data.index])
          .style("stroke-opacity", "2")
          .style("stroke-width", "2")
          .style("fill", "white")
          .style("pointer-events", "none")
        this.toolTip.xPosition = xScale(data.barIndex) + 40
        this.toolTip.yPosition = yScale(data.total_customers)
        this.toolTip.date = data.date
        this.toolTip.totalCustomers = data.total_customers
        this.toolTip.addedCustomers = data.new_customers_added
        this.toolTip.index = data.index
        this.toolTip.isEndingBar = data.isEndingBar
        this.tooltipDisplay(true, this.toolTip)
      }
    },
    tooltipDisplay(showTip, customersData) {
      this.$emit("tooltipDisplay", showTip, customersData)
    },
  },
}
</script>

<style lang="scss" scoped>
.chart-container {
  height: 252px;
  position: relative;

  .chart-section {
    margin-bottom: -20px;
  }
}
</style>
