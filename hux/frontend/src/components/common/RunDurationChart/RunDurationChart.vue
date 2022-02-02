<template>
  <div ref="runDurationChart" class="container-chart">
    <!-- <line-area-chart
      v-model="sourceData"
      :chart-dimensions="chartDimensions"
      @tooltipDisplay="toolTipDisplay"
    /> -->

    <!-- {{runDurationData.training.run_duration}} -->
    <RunDurationLineAreaChart v-model="runDurationData" />
    <!-- <chart-tooltip
      v-if="show"
      :position="{
        x: currentData.xPosition,
        y: currentData.yPosition,
      }"
      :tooltip-style="toolTipStyle"
    >
      <template #content>
        <div class="text-body-2 black--text text--darken-4 caption">
          <div class="spend-count mb-1 text-h5">
            <span class="dots"></span>
            <span>Total customer spend</span>
          </div>
          <div class="value-container">
            ${{ currentData.spend | Numeric(true, false, false) }}
          </div>
          <div class="date-section">
            {{ currentData.date | Date("MMM DD, YYYY") }}
          </div>
        </div>
      </template>
    </chart-tooltip> -->
  </div>
</template>

<script>
import RunDurationLineAreaChart from "./RunDurationLineAreaChart.vue"
import ChartTooltip from "@/components/common/Charts/Tooltip/ChartTooltip.vue"
import TooltipConfiguration from "@/components/common/Charts/Tooltip/tooltipStyleConfiguration.json"

export default {
  name: "RunDurationChart",
  components: { RunDurationLineAreaChart, ChartTooltip },
  props: {
    runDurationData: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      show: false,
      currentData: {},
      sourceData: this.runDurationData,
      chartDimensions: {
        width: 0,
        height: 0,
      },
      toolTipStyle: TooltipConfiguration.runDurationChart,
    }
  },
  mounted() {
    new ResizeObserver(this.sizeHandler).observe(
      this.$refs.runDurationChart
    )
    this.sizeHandler()
  },
  methods: {
    toolTipDisplay(...arg) {
      this.show = arg[0]
      if (this.show) {
        this.currentData = arg[1]
      }
    },
    sizeHandler() {
      if (this.$refs.runDurationChart) {
        this.chartDimensions.width =
          this.$refs.runDurationChart.clientWidth
        this.chartDimensions.height = 350
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.global-heading {
  font-style: normal;
  color: var(--v-black-base) !important;
  margin-bottom: 4px;
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
  .spend-count {
    .dots {
      margin-right: 4px;
      height: 10px;
      width: 10px;
      border-radius: 50%;
      background-color: var(--v-primary-darken2) !important;
      display: inline-block;
    }
  }
}
</style>
