<template>
  <div ref="trustIdComparisonChart" class="container-chart">
    <grouped-bar-chart
      v-model="segmentScores"
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
          <div class="spend-count mb-1 text-h5">
            <span
              class="dots"
              :style="{ backgroundColor: currentData.color }"
            ></span>
            <span> {{ currentData.segmentName }}</span>
          </div>
          <div class="value-container">
            {{ currentData.attributeName }}
          </div>
          <div class="date-section">
            {{ currentData.score }}
          </div>
        </div>
      </template>
    </chart-tooltip>
  </div>
</template>

<script>
import GroupedBarChart from "@/components/common/Charts/GroupedBarChart/GroupedBarChart.vue"
import ChartTooltip from "@/components/common/Charts/Tooltip/ChartTooltip.vue"
import TooltipConfiguration from "@/components/common/Charts/Tooltip/tooltipStyleConfiguration.json"

export default {
  name: "TrustComparisonChart",
  components: { GroupedBarChart, ChartTooltip },
  props: {
    segmentScores: {
      type: Array,
      required: true,
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
      toolTipStyle: TooltipConfiguration.trustIdComparisonChart,
    }
  },
  mounted() {
    this.sizeHandler()
    new ResizeObserver(this.sizeHandler).observe(
      this.$refs.trustIdComparisonChart
    )
  },
  methods: {
    toolTipDisplay(...arg) {
      this.show = arg[0]
      if (this.show) {
        this.currentData = arg[1]
      }
    },
    sizeHandler() {
      if (this.$refs.trustIdComparisonChart) {
        this.chartDimensions.width =
          this.$refs.trustIdComparisonChart.clientWidth
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
    font-weight: 700;
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
      display: inline-block;
    }
  }
}
</style>
