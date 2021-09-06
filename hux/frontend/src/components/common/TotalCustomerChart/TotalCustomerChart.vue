<template>
  <div ref="totalCustomerChart" class="container-chart">
    <stack-bar-chart
      v-model="sourceData"
      :bar-group-change-index="barGroupChangeIndex"
      :color-codes="colorCodes"
      :chart-dimensions="chartDimensions"
      @tooltipDisplay="toolTipDisplay"
    />
    <stack-bar-chart-tooltip
      :show-tool-tip="show"
      :color-codes="tooltipColorCodes"
      :source-input="currentData"
    />
  </div>
</template>

<script>
import { timeFormat } from "d3-time-format"
import { nest } from "d3-collection"
import StackBarChartTooltip from "@/components/common/TotalCustomerChart/StackBarChartTooltip"
import StackBarChart from "@/components/common/Charts/StackBarChart/StackBarChart.vue"
export default {
  name: "TotalCustomerChart",
  components: { StackBarChart, StackBarChartTooltip },
  props: {
    customersData: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      show: false,
      isArcHover: false,
      colorCodes: ["lighten5", "lighten8", "darken3", "success"],
      tooltipColorCodes: [
        "var(--v-primary-lighten5)",
        "var(--v-primary-lighten8)",
        "var(--v-primary-darken3)",
        "var(--v-success-base)",
      ],
      sourceData: this.customersData,
      currentData: {},
      sourceData: [],
      barGroupChangeIndex: [],
      chartDimensions: {
        width: 0,
        height: 0,
      },
    }
  },
  mounted() {
    this.sizeHandler()
    this.processSourceData()
  },
  created() {
    window.addEventListener("resize", this.sizeHandler)
  },
  destroyed() {
    window.removeEventListener("resize", this.sizeHandler)
  },
  methods: {
    toolTipDisplay(...arg) {
      this.show = arg[0]
      if (this.show) {
        this.currentData = arg[1]
      }
    },
    sizeHandler() {
      if (this.$refs.totalCustomerChart) {
        this.chartDimensions.width = this.$refs.totalCustomerChart.clientWidth
        this.chartDimensions.height = 350
      }
    },
    dateFormatter(value) {
      return this.$options.filters.Date(value, "MM/DD/YYYY")
    },
    processSourceData() {
      let initialIndex = 0
      let totalCustomerData = []
      let endingDate = new Date()
      let startingDate = new Date()

      // Getting date with 9 months date range
      startingDate.setMonth(startingDate.getMonth() - 9)

      // Creating a date collection between current and starting date
      let dateCollection = []
      let start = new Date(this.dateFormatter(startingDate))
      let end = new Date(this.dateFormatter(endingDate))
      let newend = end.setDate(end.getDate())
      end = new Date(newend)
      while (start < end) {
        dateCollection.push(this.dateFormatter(start))
        let newDate = start.setDate(start.getDate() + 1)
        start = new Date(newDate)
      }

      // Initializing date collection with 0 records
      dateCollection.forEach((date) => {
        totalCustomerData.push({
          date: date,
          total_customers: 0,
          new_customers_added: 0,
        })
      })

      // Mapping date collection with API response
      totalCustomerData.forEach((data) => {
        let dateMapper = this.customersData.find(
          (element) =>
            this.dateFormatter(element.date) == this.dateFormatter(data.date)
        )
        if (dateMapper) {
          data.total_customers = dateMapper.total_customers
          data.new_customers_added = dateMapper.new_customers_added
        }
      })

      // Creating a weekly based divider
      let week = timeFormat("%U")
      let weeklyAggData = nest()
        .key((d) => week(new Date(d.date)))
        .entries(totalCustomerData)

      let initialWeek = weeklyAggData[0].values
      let initialWeekEndingDate = initialWeek[initialWeek.length - 1].date

      this.barGroupChangeIndex.push({ index: 0, date: initialWeekEndingDate })

      let initialMonth = new Date(initialWeekEndingDate).getMonth()
      let lastWeekEndingData = 0

      // Data aggregation on weekly basis
      weeklyAggData.forEach((element, index) => {
        let weekData = element.values
        let weekLastDate = weekData[weekData.length - 1].date
        let currentWeekEndingData =
          weekData[weekData.length - 1].total_customers
        if (new Date(weekLastDate).getMonth() != initialMonth) {
          initialMonth = new Date(weekLastDate).getMonth()
          if (initialIndex == 2) {
            initialIndex = 0
          } else initialIndex++

          this.barGroupChangeIndex.push({
            index: index,
            date: weekLastDate,
          })
        }

        currentWeekEndingData = this.getCurrentWeekValue(
          currentWeekEndingData,
          weekData,
          lastWeekEndingData
        )

        this.sourceData.push({
          date: weekLastDate,
          total_customers: currentWeekEndingData,
          new_customers_added:
            lastWeekEndingData == 0
              ? weekData.reduce((sum, d) => sum + d.new_customers_added, 0)
              : currentWeekEndingData - lastWeekEndingData,
          index: index == weeklyAggData.length - 1 ? 3 : initialIndex,
          barIndex: index,
          isEndingBar: index > weeklyAggData.length - 5,
        })

        lastWeekEndingData = currentWeekEndingData
      })
    },

    // Setting week's last day count in case of no records
    getCurrentWeekValue(currentValue, currentWeek, lastWeekEndingData) {
      if (currentValue == 0) {
        let noZeroCustomerCount = currentWeek.some(
          (data) => data.total_customers !== 0
        )
        if (noZeroCustomerCount) {
          let lastIndex = currentWeek
            .map((weekData) => weekData.total_customers !== 0)
            .lastIndexOf(true)
          return currentWeek[lastIndex].total_customers
        } else {
          return lastWeekEndingData
        }
      } else return currentValue
    },
  },
}
</script>

<style lang="scss" scoped>
.global-text-line {
  display: inline-block;
  font-style: normal;
  font-size: $font-size-root;
  line-height: 19px;
}
.container-chart {
  position: relative;
  height: 650px;
  padding: 0px !important;
}
</style>
