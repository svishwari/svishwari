<template>
  <div ref="customerEventChart" class="container-chart">
    <line-chart
      v-model="sourceData"
      :chart-dimensions="chartDimensions"
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
        <div class="neroBlack--text caption">
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
        </div>
      </template>
    </chart-tooltip>
  </div>
</template>

<script>
import LineChart from "@/components/common/Charts/LineChart/LineChart.vue"
import Icon from "@/components/common/Icon"
import ChartTooltip from "@/components/common/Charts/Tooltip/ChartTooltip.vue"
import TooltipConfiguration from "@/components/common/Charts/Tooltip/tooltipStyleConfiguration.json"
export default {
  name: "CustomerEventChart",
  components: { LineChart, Icon, ChartTooltip },
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
      colorCodes: ["columbiaBlue", "info", "pantoneBlue", "success"],
      sourceData: this.customersData,
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
