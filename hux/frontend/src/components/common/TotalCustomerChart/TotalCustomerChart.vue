<template>
  <div ref="totalCustomerChart" class="container-chart">
    <stack-bar-chart
      v-model="chartSourceData"
      :bar-group-change-index="barGroupChangeIndex"
      :color-codes="colorCodes"
      :chart-dimensions="chartDimensions"
      :empty-state="isEmptyState"
      :months-duration="monthsDuration"
      @tooltipDisplay="toolTipDisplay"
    />
    <chart-tooltip
      v-if="show"
      :position="{
        x: currentData.xPosition,
        y: currentData.yPosition,
      }"
      :tooltip-style="toolTipStyle"
    >
      <template #content>
        <div class="text-body-2 black--text text--darken-4 caption">
          <div class="value-container">
            <icon
              type="customer"
              :size="20"
              :stroke-opacity="0.5"
              :stroke="colorCodes[currentData.index].base"
              :variant="colorCodes[currentData.index].variant"
            />
            <span class="text-label">Total customers</span>
          </div>
          <div class="value-section">
            {{ currentData.totalCustomers | Numeric(true, false, false) }}
          </div>
          <div class="value-container">
            <icon
              type="new-customer"
              :size="20"
              :stroke="colorCodes[currentData.index].base"
              :variant="colorCodes[currentData.index].variant"
            />
            <span class="text-label">New customers added</span>
          </div>
          <div class="value-section">
            {{ currentData.addedCustomers | Numeric(true, false, false) }}
          </div>
          <div class="value-container">
            <icon
              type="left-customer"
              :size="20"
              :stroke-opacity="0.5"
              stroke="black"
              variant="lighten4"
            />
            <span class="text-label">Customers left</span>
          </div>
          <div class="value-section">
            <span v-if="currentData.leftCustomers > 0">-</span>
            {{ currentData.leftCustomers | Numeric(true, false, false) }}
          </div>
          <div class="date-section">
            {{ currentData.date | Date("MMM DD, YYYY") }}
          </div>
        </div>
      </template>
    </chart-tooltip>
  </div>
</template>

<script>
import { timeFormat } from "d3-time-format"
import { nest } from "d3-collection"
import StackBarChart from "@/components/common/Charts/StackBarChart/StackBarChart.vue"
import ChartTooltip from "@/components/common/Charts/Tooltip/ChartTooltip.vue"
import Icon from "@/components/common/Icon"
import TooltipConfiguration from "@/components/common/Charts/Tooltip/tooltipStyleConfiguration.json"

export default {
  name: "TotalCustomerChart",
  components: { StackBarChart, ChartTooltip, Icon },
  props: {
    customersData: {
      type: Array,
      required: true,
    },
    monthsDuration: {
      type: Number,
      required: false,
      default: 6,
    },
  },
  data() {
    return {
      show: false,
      isArcHover: false,
      isEmptyState: false,
      colorCodes: [
        { base: "primary", variant: "lighten6" },
        { base: "primary", variant: "darken1" },
        { base: "primary", variant: "darken3" },
        { base: "success", variant: "base" },
      ],
      currentData: {},
      chartSourceData: {},
      sourceData: [],
      barGroupChangeIndex: [],
      chartDimensions: {
        width: 0,
        height: 0,
      },
      toolTipStyle: TooltipConfiguration.totalCustomerChart,
    }
  },
  mounted() {
    this.sizeHandler()
    this.processSourceData()
    new ResizeObserver(this.sizeHandler).observe(this.$refs.totalCustomerChart)
  },
  methods: {
    toolTipDisplay(...arg) {
      this.show = arg[0]
      if (this.show) {
        this.currentData = arg[1]
        if (this.monthsDuration != 6) {
          this.toolTipStyle.left = this.currentData.isEndingBar
            ? "-150px"
            : "45px"
        }
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
      startingDate.setMonth(startingDate.getMonth() - this.monthsDuration)

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

      // Checking the empty state
      this.isEmptyState = this.customersData.length == 0

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
          customers_left:
            currentWeekEndingData < lastWeekEndingData
              ? lastWeekEndingData - currentWeekEndingData
              : 0,
          index: index == weeklyAggData.length - 1 ? 3 : initialIndex,
          barIndex: index,
          isEndingBar: index > weeklyAggData.length - 5,
        })

        lastWeekEndingData = currentWeekEndingData
      })

      this.chartSourceData = {
        sourceData: this.sourceData,
        monthsDuration: this.monthsDuration,
      }
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
.global-heading {
  font-style: normal;
}
.container-chart {
  position: relative;
  height: 650px;
  padding: 0px !important;
  .value-container {
    margin-top: 2px;
    margin-bottom: 4px;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    @extend .global-heading;
    .text-label {
      margin-left: 4px !important;
    }
  }
  .value-section {
    @extend .global-heading;
    margin-left: 24px;
    margin-bottom: 10px;
  }
  .date-section {
    @extend .global-heading;
    color: var(--v-black-lighten4) !important;
  }
}
</style>
