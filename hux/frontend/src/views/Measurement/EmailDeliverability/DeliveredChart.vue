<template>
  <v-card class="overview-card mt-6 pt-5 pb-6 pl-6 pr-6 box-shadow-5">
    <v-card-title class="d-flex justify-space-between pa-0 pr-2">
      <h3 class="text-h3 mb-2">Delivered count</h3>
      <h3 class="text-h3 mb-2">Open rate</h3>
    </v-card-title>
    <div ref="emailDeliverabilityChart" class="container-chart">
      <line-bar-chart
        v-model="chartSourceData"
        :bar-group-change-index="barGroupChangeIndex"
        :color-codes="colorCodes"
        :chart-dimensions="chartDimensions"
        :empty-state="isEmptyState"
        :months-duration="monthsDuration"
        @tooltipDisplay="toolTipDisplay"
      />
      <div class="value-container ma-8 mr-4">
        <span class="line mr-2"></span>
        <span class="text-label">Open rate</span>
      </div>
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
              <span
                class="dot"
                :style="{ background: getDynamicNotation(currentData.index) }"
              ></span>
              <span class="text-label">Delivered count</span>
            </div>
            <div class="value-section">
              {{ currentData.delivered_count | Numeric(true, false, false) }}
            </div>
            <div class="value-container">
              <span class="line"></span>
              <span class="text-label">Open rate</span>
            </div>
            <div class="value-section">
              {{ currentData.open_rate | Numeric(true, false, false, true) }}
            </div>
            <div class="date-section">
              {{ currentData.date | Date("MMM DD, YYYY") }}
            </div>
          </div>
        </template>
      </chart-tooltip>
    </div>
  </v-card>
</template>

<script>
import { timeFormat } from "d3-time-format"
import { nest } from "d3-collection"
import LineBarChart from "@/components/common/Charts/LineBarChart/LineBarChart.vue"
import ChartTooltip from "@/components/common/Charts/Tooltip/ChartTooltip.vue"
import TooltipConfiguration from "@/components/common/Charts/Tooltip/tooltipStyleConfiguration.json"
import emailData from "@/api/mock/fixtures/deliveredCountData.js"

export default {
  name: "DeliveredChart",
  components: { LineBarChart, ChartTooltip },
  props: {
    monthsDuration: {
      type: Number,
      required: false,
      default: 3,
    },
  },
  data() {
    return {
      show: false,
      isArcHover: false,
      isEmptyState: false,
      colorCodes: [
        { base: "primary", variant: "lighten4" },
        { base: "primary", variant: "lighten6" },
        { base: "primary", variant: "darken1" },
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
      toolTipStyle: TooltipConfiguration.emailDeliverabilityChart,
      emailData: emailData.delivered_open_rate_overivew,
    }
  },
  mounted() {
    this.sizeHandler()
    this.processSourceData()
    new ResizeObserver(this.sizeHandler).observe(
      this.$refs.emailDeliverabilityChart
    )
  },
  methods: {
    toolTipDisplay(...arg) {
      this.show = arg[0]
      if (this.show) {
        this.currentData = arg[1]
        if (this.monthsDuration != 6) {
          this.toolTipStyle.left = this.currentData.isEndingBar
            ? "-122px"
            : "28px"
        }
      }
    },
    sizeHandler() {
      if (this.$refs.emailDeliverabilityChart) {
        this.chartDimensions.width =
          this.$refs.emailDeliverabilityChart.clientWidth
        this.chartDimensions.height = 350
      }
    },
    dateFormatter(value) {
      return this.$options.filters.Date(value, "MM/DD/YYYY")
    },

    getDynamicNotation(index) {
      return `var(--v-${this.colorCodes[index].base}-${this.colorCodes[index].variant})`
    },

    processSourceData() {
      let initialIndex = 0
      let emailOverviewData = []
      let endingDate = new Date()
      let startingDate = new Date()

      // Getting date with 3 months date range
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
        emailOverviewData.push({
          date: date,
          open_rate: 0,
          delivered_count: 0,
        })
      })

      // Checking the empty state
      this.isEmptyState = this.emailData.length == 0

      // Mapping date collection with API response
      emailOverviewData.forEach((data) => {
        let dateMapper = this.emailData.find(
          (element) =>
            this.dateFormatter(element.date) == this.dateFormatter(data.date)
        )
        if (dateMapper) {
          data.open_rate = dateMapper.open_rate
          data.delivered_count = dateMapper.delivered_count
        }
      })

      // Creating a weekly based divider
      let week = timeFormat("%U")
      let weeklyAggData = nest()
        .key((d) => week(new Date(d.date)))
        .entries(emailOverviewData)

      let initialWeek = weeklyAggData[0].values
      let initialWeekEndingDate = initialWeek[initialWeek.length - 1].date
      this.barGroupChangeIndex.push({ index: 0, date: initialWeekEndingDate })
      let initialMonth = new Date(initialWeekEndingDate).getMonth()

      // Data aggregation on weekly basis
      weeklyAggData.forEach((element, index) => {
        let weekData = element.values
        let weekLastDate = weekData[weekData.length - 1].date
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

        this.sourceData.push({
          date: weekLastDate,
          delivered_count: weekData.reduce(
            (sum, d) => sum + d.delivered_count,
            0
          ),
          open_rate:
            (weekData.reduce((sum, d) => sum + d.open_rate, 0) * 1) / 7,
          index: index == weeklyAggData.length - 1 ? 3 : initialIndex,
          barIndex: index,
          isEndingBar: index > weeklyAggData.length - 3,
        })
      })

      this.chartSourceData = {
        sourceData: this.sourceData,
        monthsDuration: this.monthsDuration,
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.dot {
  height: 12px;
  width: 12px;
  background-color: var(--v-primary-darken2);
  border-radius: 50%;
  margin-right: 3px;
  display: inline-block;
}
.line {
  width: 15px;
  border-bottom: 3px solid var(--v-info-base) !important;
  display: inline-block;
  margin-right: 3px;
  pointer-events: none;
}
.global-heading {
  font-style: normal;
}
.container-chart {
  position: relative;
  height: 285px;
  padding: 0px !important;
  .value-container {
    margin-top: 2px;
    margin-bottom: 4px;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    @extend .global-heading;
  }
  .value-section {
    @extend .global-heading;
    margin-bottom: 10px;
  }
  .date-section {
    @extend .global-heading;
    color: var(--v-black-lighten4) !important;
  }
}
</style>
