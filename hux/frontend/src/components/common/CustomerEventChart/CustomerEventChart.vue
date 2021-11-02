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
        <!-- <div class="neroBlack--text caption">
          <div class="value-section">
            <div>{{ currentData.day }}</div>
            <div>
              {{ currentData.month }} {{ currentData.date | Date("DD, YYYY") }}
            </div>
          </div>
          <div class="item_count">
            {{ currentData.total_event_count }}
            <span v-if="currentData.total_event_count > 1">Events</span>
            <span v-else>Event</span>
          </div>
          <div
            v-for="event in eventsLabels"
            :key="event.event_name"
            class="value-container"
          >
            <div
              v-if="currentData.eventsCollection.includes(event.event_name)"
              class="event-list"
            >
              <icon :type="event.event_name" :size="16" />
              <span class="text-label">{{ event.label_name }}</span>
            </div>
          </div>
        </div> -->
      </template>
    </chart-tooltip>
  </div>
</template>

<script>
import BarChart from "@/components/common/Charts/BarChart/BarChart.vue"
import Icon from "@/components/common/Icon"
import ChartTooltip from "@/components/common/Charts/Tooltip/ChartTooltip.vue"
import TooltipConfiguration from "@/components/common/Charts/Tooltip/tooltipStyleConfiguration.json"
import { timeFormat } from "d3-time-format"
import { nest } from "d3-collection"

export default {
  name: "CustomerEventChart",
  components: { BarChart, Icon, ChartTooltip },
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
      colorCodes: ["columbiaBlue", "info", "pantoneBlue", "success"],
      sourceData: [],
      barGroupChangeIndex: [],
      currentData: {},
      chartDimensions: {
        width: 0,
        height: 0,
      },
      toolTipStyle: TooltipConfiguration.customerEventChart,
      eventsLabels: [
        {
          label_name: "Abandoned cart",
          event_name: "abandoned_cart",
        },
        {
          label_name: "Customer login",
          event_name: "customer_login",
        },
        {
          label_name: "Trait computed",
          event_name: "trait_computed",
        },
        {
          label_name: "Viewed cart",
          event_name: "viewed_cart",
        },
        {
          label_name: "Viewed checkout",
          event_name: "viewed_checkout",
        },
        {
          label_name: "Viewed sale item",
          event_name: "viewed_sale_item",
        },
        {
          label_name: "Item purchased",
          event_name: "item_purchased",
        },
      ],
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
        let eventsOnly = []
        Object.entries(arg[1].event_type_counts)
          .filter(([k, v]) => (v > 0 ? k : ""))
          .forEach((data) => eventsOnly.push(data[0]))
        this.currentData = arg[1]
        let date = new Date(this.currentData.date)
        this.currentData.day = date.toLocaleString("en-us", { weekday: "long" })
        this.currentData.month = date.toLocaleString("default", {
          month: "long",
        })
        this.currentData.eventsCollection = eventsOnly
      }
    },
    sizeHandler() {
      if (this.$refs.customerEventChart) {
        this.chartDimensions.width = this.$refs.customerEventChart.clientWidth
        this.chartDimensions.height = 350
      }
    },
    dateFormatter(value) {
      return this.$options.filters.Date(value, "MM/DD/YYYY")
    },
    processSourceData() {
      let initialIndex = 0
      let customerEventData = []
      let endingDate = new Date()
      let startingDate = new Date()

      // Getting date with 6 months date range
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
        customerEventData.push({
          date: date,
          total_event_count: 0,
          event_type_counts: {}
        })
      })

      debugger

      // Checking the empty state
      this.isEmptyState = this.customersData.length == 0

      // Mapping date collection with API response
      customerEventData.forEach((data) => {
        let dateMapper = this.customersData.find(
          (element) =>
            this.dateFormatter(element.date) == this.dateFormatter(data.date)
        )
        if (dateMapper) {
          data.total_event_count = dateMapper.total_event_count,
          data.event_type_counts = dateMapper.event_type_counts
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
          total_event_count: weekData.reduce((sum, d) => sum + d.total_event_count, 0),
          // new_customers_added:
          //   lastWeekEndingData == 0
          //     ? weekData.reduce((sum, d) => sum + d.new_customers_added, 0)
          //     : currentWeekEndingData - lastWeekEndingData,
          // customers_left:
          //   currentWeekEndingData < lastWeekEndingData
          //     ? lastWeekEndingData - currentWeekEndingData
          //     : 0,
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
.global-heading {
  font-style: normal;
  font-size: 12px;
  line-height: 19px;
}
.container-chart {
  position: relative;
  height: 650px;
  padding: 0px !important;

  .value-container {
    margin-top: 2px;
    @extend .global-heading;
    .event-list {
      display: flex;
      justify-content: flex-start;
      align-items: center;
      margin-bottom: 8px !important;
      .text-label {
        margin-left: 7px !important;
        flex: 1 0 50%;
      }
    }
  }
  .value-section {
    @extend .global-heading;
  }
  .item_count {
    margin-top: 5px;
    margin-bottom: 5px;
    font-weight: bold;
  }
}
</style>
