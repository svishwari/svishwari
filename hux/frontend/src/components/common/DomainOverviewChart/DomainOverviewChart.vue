<template>
  <div ref="domainChart" class="container-chart">
    <domain-chart
      v-model="sourceData"
      :chart-dimensions="chartDimensions"
      :domain-type="sourceType"
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
            <span class="dots"></span>
            <span>{{ domain_name }}</span>
          </div>
          <div v-if="sourceType == 'sent'" class="value-container">
            {{ currentData[domain_name] }}
          </div>
          <div v-else class="value-container">
            {{ currentData[domain_name] | Percentage }}
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
import DomainChart from "@/components/common/Charts/DomainChart/DomainChart.vue"
import ChartTooltip from "@/components/common/Charts/Tooltip/ChartTooltip.vue"
import TooltipConfiguration from "@/components/common/Charts/Tooltip/tooltipStyleConfiguration.json"

export default {
  name: "DomainOverviewChart",
  components: { DomainChart, ChartTooltip },
  props: {
    chartData: {
      type: Array,
      required: true,
    },
    chartType: {
      type: String,
      required: false,
    },
  },
  data() {
    return {
      show: false,
      currentData: {},
      sourceData: this.chartData,
      sourceType: this.chartType,
      domain_name: null,
      chartDimensions: {
        width: 0,
        height: 0,
      },
      toolTipStyle: TooltipConfiguration.domainChart,
    }
  },
  mounted() {
    new ResizeObserver(this.sizeHandler).observe(this.$refs.domainChart)
    this.sizeHandler()
  },
  methods: {
    toolTipDisplay(...arg) {
      this.show = arg[0]
      if (this.show) {
        this.currentData = arg[1]
        this.domain_name = arg[1].domain_name
        this.toolTipStyle.left = this.currentData.invertPosition
            ? "-85px"
            : "85px"
      }
    },
    sizeHandler() {
      if (this.$refs.domainChart) {
        this.chartDimensions.width = this.$refs.domainChart.clientWidth
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
      background-color: var(--v-primary-darken1) !important;
      display: inline-block;
    }
  }
}
</style>
