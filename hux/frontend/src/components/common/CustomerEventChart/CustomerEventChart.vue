<template>
  <div ref="customerEventChart" class="container-chart">
    <bar-chart
      v-model="sourceData"
      :bar-group-change-index="barGroupChangeIndex"
      :chart-dimensions="chartDimensions"
      :empty-state="isEmptyState"
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
          <div class="item_count text-h5">
            <span class="dots"></span>
            {{ currentData.total_event_count }}
            <span v-if="currentData.total_event_count > 1">Events</span>
            <span v-else>Event</span>
          </div>
          <div
            v-for="event in currentData.eventsCollection"
            :key="event"
            class="value-container"
          >
            <div class="event-list">
              <span class="text-label"
                >{{ formatText(event) }} ({{ eventCount(event) }})</span
              >
            </div>
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
import { formatText } from "@/utils"
import BarChart from "@/components/common/Charts/BarChart/BarChart.vue"
import ChartTooltip from "@/components/common/Charts/Tooltip/ChartTooltip.vue"
import TooltipConfiguration from "@/components/common/Charts/Tooltip/tooltipStyleConfiguration.json"
import { timeFormat } from "d3-time-format"
import { nest } from "d3-collection"

export default {
  name: "CustomerEventChart",
  components: { BarChart, ChartTooltip },
  props: {
    customersData: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      show: false,
      isEmptyState: false,
      sourceData: [],
      barGroupChangeIndex: [],
      eventsData: [],
      currentData: {},
      chartDimensions: {
        width: 0,
        height: 0,
      },
      toolTipStyle: TooltipConfiguration.customerEventChart,
    }
  },
  mounted() {
    this.sizeHandler()
    this.processSourceData()
    new ResizeObserver(this.sizeHandler).observe(this.$refs.customerEventChart)
  },
  methods: {
    toolTipDisplay(...arg) {
      this.show = arg[0]
      if (this.show) {
        this.toolTipStyle.left = this.currentData.isEndingBar
          ? "-160px"
          : "56px"
        this.eventsData = []
        Object.entries(arg[1].event_type_counts)
          .filter(([k, v]) => (v > 0 ? k : ""))
          .forEach((data) => this.eventsData.push(data))
        this.currentData = arg[1]
        this.currentData.eventsCollection = this.eventsData.map(
          (data) => data[0]
        )
      }
    },
    sizeHandler() {
      if (this.$refs.customerEventChart) {
        this.chartDimensions.width = this.$refs.customerEventChart.clientWidth
        this.chartDimensions.height = 320
      }
    },
    eventCount(eventName) {
      let eventCounts = this.eventsData.filter(
        (data) => data[0] === eventName
      )[0]
      return eventCounts[1]
    },
    dateFormatter(value) {
      return this.$options.filters.Date(value, "MM/DD/YYYY")
    },
    processSourceData() {
      let initialIndex = 0
      let customerEventData = []

      // Creating a date collection between current and starting date
      let dateCollection = []
      let start = new Date(this.dateFormatter(this.customersData[0].date))
      let end = new Date(
        this.dateFormatter(
          this.customersData[this.customersData.length - 1].date
        )
      )
      let newend = end.setDate(end.getDate())
      end = new Date(newend)
      while (start < end) {
        dateCollection.push(this.dateFormatter(start))
        let newDate = start.setDate(start.getDate() + 1)
        start = new Date(newDate)
      }

      // Initializing date collection with 0 records
      dateCollection.forEach((date) => {
        customerEventData.push({
          date: date,
          total_event_count: 0,
          event_type_counts: {},
        })
      })

      // Checking the empty state
      this.isEmptyState = this.customersData.length == 0

      // Mapping date collection with API response
      customerEventData.forEach((data) => {
        let dateMapper = this.customersData.find(
          (element) =>
            this.dateFormatter(element.date) == this.dateFormatter(data.date)
        )
        if (dateMapper) {
          ;(data.total_event_count = dateMapper.total_event_count),
            (data.event_type_counts = dateMapper.event_type_counts)
        }
      })

      // Creating a weekly based divider
      let week = timeFormat("%U")
      let weeklyAggData = nest()
        .key((d) => week(new Date(d.date)))
        .entries(customerEventData)

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
          weekData[weekData.length - 1].total_event_count
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
          total_event_count: weekData.reduce(
            (sum, d) => sum + d.total_event_count,
            0
          ),
          event_type_counts: this.getEventsAggregation(weekData),
          index: index == weeklyAggData.length - 1 ? 3 : initialIndex,
          barIndex: index,
          isEndingBar: index > weeklyAggData.length - 4,
        })

        lastWeekEndingData = currentWeekEndingData
      })
    },

    getEventsAggregation(currentWeek) {
      let allCurrentWeekEvents = currentWeek
        .filter((data) => data.total_event_count !== 0)
        .map((data) => data.event_type_counts)
      return allCurrentWeekEvents.length > 0
        ? this.getEventSumbyKey(allCurrentWeekEvents)
        : {}
    },

    getEventSumbyKey([...events]) {
      return events.reduce((event1, event2) => {
        for (let key in event2) {
          if (key in event2) event1[key] = (event1[key] || 0) + event2[key]
        }
        return event1
      }, {})
    },

    // Setting week's last day count in case of no records
    getCurrentWeekValue(currentValue, currentWeek, lastWeekEndingData) {
      if (currentValue == 0) {
        let noZeroCustomerCount = currentWeek.some(
          (data) => data.total_event_count !== 0
        )
        if (noZeroCustomerCount) {
          let lastIndex = currentWeek
            .map((weekData) => weekData.total_event_count !== 0)
            .lastIndexOf(true)
          return currentWeek[lastIndex].total_event_count
        } else {
          return lastWeekEndingData
        }
      } else return currentValue
    },
    formatText: formatText,
  },
}
</script>

<style lang="scss" scoped>
.global-heading {
  font-style: normal;
  color: var(--v-black-base) !important;
}
.container-chart {
  position: relative;
  padding: 0px !important;

  .value-container {
    margin-top: 2px;
    margin-bottom: 10px;
    @extend .global-heading;
    .event-list {
      display: flex;
      justify-content: flex-start;
      align-items: center;
      margin-bottom: 6px !important;
      .text-label {
        margin-left: 3px !important;
        flex: 1 0 50%;
      }
    }
  }
  .value-section {
    @extend .global-heading;
  }
  .date-section {
    @extend .global-heading;
    color: var(--v-black-lighten4) !important;
  }
  .item_count {
    margin-top: 5px;
    margin-bottom: 8px;
    .dots {
      margin-left: 4px;
      margin-right: -1px;
      height: 10px;
      width: 10px;
      border-radius: 50%;
      background-color: var(--v-secondary-lighten1) !important;
      display: inline-block;
    }
  }
}
</style>
