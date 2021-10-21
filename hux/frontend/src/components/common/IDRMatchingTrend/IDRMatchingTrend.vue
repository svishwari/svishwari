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
            <div class="date-font">
              {{ currentData.date | Date("MMM DD[,] YYYY") }}
            </div>
            <div>
              <span class="append-circle color-known-ids" />
              <span class="font-size-tooltip">
                {{
                  currentData.known_ids | Numeric(false, false, true) | Empty
                }}
              </span>
            </div>
            <div>
              <span class="append-circle color-unique-hux-ids" />
              <span class="font-size-tooltip">
                {{
                  currentData.unique_hux_ids
                    | Numeric(false, false, true)
                    | Empty
                }}
              </span>
            </div>
            <div>
              <span class="append-circle color-anonymous-ids" />
              <span class="font-size-tooltip">
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
      colorCodes: ["#42EFFD", "#347DAC", "#75787B"],
      toolTipStyle: TooltipConfiguration.idrMatchingTrendChart,
      currentData: {},
      chartDimensions: {
        width: 0,
        height: 0,
      },
    }
  },
  mounted() {
    this.sizeHandler()
    new ResizeObserver(this.sizeHandler).observe(this.$refs.trendsChart)
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
    sizeHandler() {
      if (this.$refs.trendsChart) {
        this.chartDimensions.width = this.$refs.trendsChart.clientWidth
        this.chartDimensions.height = 300
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
    background-color: var(--v-white-base);
    border-radius: 50%;
    display: inline-block;
    margin-top: 6px;
    margin-right: 8px;
  }
  .color-known-ids {
    border: 2px solid #42effd;
  }
  .color-anonymous-ids {
    border: 2px solid #75787b;
  }
  .color-unique-hux-ids {
    border: 2px solid #347dac;
  }
}
</style>
