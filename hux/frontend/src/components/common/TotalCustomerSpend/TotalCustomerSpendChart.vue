<template>
  <div ref="totalCustomerSpendChart" class="container-chart">
    <line-area-chart
      v-model="spendData"
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
        <!-- <div class="text-body-2 black--text text--darken-4 caption">
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
        </div> -->
      </template>
    </chart-tooltip>
  </div>
</template>

<script>
import LineAreaChart from "@/components/common/Charts/LineAreaChart/LineAreaChart.vue"
import ChartTooltip from "@/components/common/Charts/Tooltip/ChartTooltip.vue"
import TooltipConfiguration from "@/components/common/Charts/Tooltip/tooltipStyleConfiguration.json"
import Icon from "@/components/common/Icon"

export default {
  name: "TotalCustomerSpendChart",
  components: { LineAreaChart, ChartTooltip, Icon },
  props: {
    customersData: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      show: false,
      currentData: {},
      chartSourceData: {},
      sourceData: [],
      chartDimensions: {
        width: 0,
        height: 0,
      },
      toolTipStyle: TooltipConfiguration.totalCustomerChart,
      spendData: [
        {
          date: "2021-05-08T09:04:38.371Z",
          spend: 35000,
        },
        {
          date: "2021-06-08T09:04:38.371Z",
          spend: 70000,
        },
        {
          date: "2021-07-08T09:04:38.371Z",
          spend: 50000,
        },
        {
          date: "2021-08-08T09:04:38.371Z",
          spend: 80000,
        },
        {
          date: "2021-09-08T09:04:38.371Z",
          spend: 60000,
        },
        {
          date: "2021-10-08T09:04:38.371Z",
          spend: 95000,
        },
      ],
    }
  },
  mounted() {
    this.sizeHandler()
    new ResizeObserver(this.sizeHandler).observe(this.$refs.totalCustomerSpendChart)
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
        this.chartDimensions.width = this.$refs.totalCustomerSpendChart.clientWidth
        this.chartDimensions.height = 350
      }
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
