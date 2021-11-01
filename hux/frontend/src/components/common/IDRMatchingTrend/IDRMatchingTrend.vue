<template>
  <div ref="trendsChart" class="container-chart">
    <multi-line-chart
      v-model="mapData"
      :chart-dimensions="chartDimensions"
      :color-codes="colorCodes"
      @cordinates="getCordinates"
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
            <div>
              <span class="append-circle color-primary-base" />
              <span class="font-size-tooltip">
                Unique Hux IDs
                <br />
                {{
                  currentData.unique_hux_ids
                    | Numeric(false, false, true)
                    | Empty
                }}
              </span>
            </div>
            <div>
              <span class="append-circle color-primary-lighten9" />
              <span class="font-size-tooltip">
                Known IDs
                <br />
                {{
                  currentData.known_ids | Numeric(false, false, true) | Empty
                }}
              </span>
            </div>
            <div>
              <span class="append-circle color-primary-darken2" />
              <span class="font-size-tooltip">
                Anonymous IDs
                <br />
                {{
                  currentData.anonymous_ids
                    | Numeric(false, false, true)
                    | Empty
                }}
              </span>
            </div>
          </div>
        </div>
      </template>
    </chart-tooltip>
  </div>
</template>

<script>
import MultiLineChart from "@/components/common/IDRMatchingTrend/MultiLineChart.vue"
import ChartTooltip from "@/components/common/Charts/Tooltip/ChartTooltip.vue"
import TooltipConfiguration from "@/components/common/Charts/Tooltip/tooltipStyleConfiguration.json"
import colors from "@/plugins/colors.js"

export default {
  name: "IDRMatchingTrend",
  components: { MultiLineChart, ChartTooltip },
  props: {
    mapData: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      show: false,
      isArcHover: false,
      tooltip: {
        x: 0,
        y: 0,
      },
      colorCodes: [colors.darkBlue, colors.chart3, colors.chart2],
      toolTipStyle: TooltipConfiguration.idrMatchingTrendChart,
      currentData: {},
      chartDimensions: {
        width: 0,
        height: 0,
      },
    }
  },
  mounted() {
    new ResizeObserver(() => {
      if (this.$refs.trendsChart) {
        this.chartDimensions.width = this.$refs.trendsChart.clientWidth
        this.chartDimensions.height = 300
      }
    }).observe(this.$refs.trendsChart)
  },
  methods: {
    toolTipDisplay(...arg) {
      this.show = arg[0]
      if (this.show) {
        this.currentData = arg[1]
      }
    },
    getCordinates(args) {
      this.tooltip.x = args.x
      this.tooltip.y = args.y
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
  padding: 0px !important;
  .value-container {
    margin-top: 2px;
    @extend .global-heading;
    .text-label {
      margin-left: 8px !important;
    }
  }
  .value-section {
    @extend .global-heading;
  }
  .item_count {
    font-weight: bold;
  }
  .append-circle {
    height: 12px;
    width: 12px;
    border-radius: 50%;
    display: inline-block;
    margin-top: 6px;
  }
  .color-primary-lighten9 {
    background-color: var(--v-primary-lighten9);
  }
  .color-primary-darken2 {
    background-color: var(--v-primary-darken2);
  }
  .color-primary-base {
    background-color: var(--v-primary-base);
  }
}
</style>
