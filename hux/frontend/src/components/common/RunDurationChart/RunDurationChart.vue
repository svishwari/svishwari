<template>
  <div ref="runDurationChart" class="container-chart">
    <div v-if="sourceData">
      <!-- <div class="outer-text">
        Time Minutes
      </div> -->
      <RunDurationLineAreaChart
        v-model="sourceData"
        :chart-dimensions="chartDimensions"
        :finalStatus="finalStatus"
        @tooltipDisplay="toolTipDisplay"
      />
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
        <div class="text-body-2 black--text text--base caption ma-2">
          <div class="spend-count mb-2 text-h5">
            <span
              >{{ currentData.index }} run of last {{ sourceData.length }}</span
            >
          </div>
          <div class="value-container mb-2">
            <span
              v-if="currentData.status === 'Success'"
              class="greenDot"
            ></span>
            <span v-else class="redDot mr-2"></span>
            {{ currentData.status }}
          </div>
          <div class="mb-2"  v-if="currentData.status === 'Success'">
            {{ currentData.showDuration }}
          </div>
          <div class="date-section black--text text--darken-4">
            {{ currentData.timestamp | Date("MMM DD, YYYY") }}
          </div>
        </div>
      </template>
    </chart-tooltip>
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
      dateData: [],
      durationData: [],
      chartDimensions: {
        width: 0,
        height: 0,
      },
      toolTipStyle: TooltipConfiguration.runDurationChart,
      count: 1,
      durationArray: [],
      finalStatus: "Success",
    }
  },
  mounted() {
    new ResizeObserver(this.sizeHandler).observe(this.$refs.runDurationChart)
    this.formattedData()
    this.sizeHandler()
  },
  computed: {},
  methods: {
    formattedData() {
      this.sourceData.map((element) => {
        element.showDuration = element.duration
        this.durationData = element.duration.split("m")
        element.duration = parseInt(this.durationData[0])
        element.index = this.count++
      })
      this.finalStatus = this.sourceData[this.sourceData.length - 1].status
    },
    toolTipDisplay(...arg) {
      this.show = arg[0]
      if (this.show) {
        this.currentData = arg[1]
      }
    },
    sizeHandler() {
      if (this.$refs.runDurationChart) {
        this.chartDimensions.width = this.$refs.runDurationChart.clientWidth
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
  height: 300px;
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
  .dots {
    margin-right: 4px;
    height: 13px;
    width: 13px;
    border-radius: 50%;
    display: inline-block;
  }
  .greenDot {
    @extend .dots;
    background-color: var(--v-success-base) !important;
  }
  .redDot {
    @extend .dots;
    background-color: var(--v-error-base) !important;
  }
  // .outer-text {
  //   transform: rotate(-90) !important;
  // }
}
</style>
