<template>
  <div ref="chartBox" class="container">
    <span v-if="mapChartData.length != 0">
      <geo-chart
        v-model="mapChartData"
        :chart-dimensions="chartDimensions"
        :configuration-data="configurationData"
        :disable-hover-effects="disableHoverEffects"
        @cordinates="getCordinates"
        @tooltipDisplay="toolTipDisplay"
      />
      <chart-tooltip
        v-if="show"
        :position="{
          x: tooltip.x,
          y: tooltip.y,
        }"
        :tooltip-style="toolTipStyle"
      >
        <template #content>
          <div class="map-hover">
            <span class="prop-name font-weight-semi-bold">
              {{ currentData[defaultMetric] }}
            </span>
            <div
              v-for="metric in configurationData.tooltip_metrics"
              :key="metric.label"
              class="sub-props mt-2 body-2"
            >
              <span v-if="metric.is_Combined_Metric" class="subprop-name mr-2"
                >{{ metric.label }}
              </span>
              <span v-if="!metric.is_Combined_Metric" class="subprop-name mr-2"
                >{{ metric.label }}
              </span>
              <span v-if="metric.is_Combined_Metric" class="value ml-1">
                <span v-for="(value, index) in metric.key" :key="value">
                  {{ applyFilter(currentData[value], metric.format) }}
                  <span v-if="index !== metric.key.length - 1">-</span>
                </span>
              </span>
              <span v-if="!metric.is_Combined_Metric" class="value ml-1">
                {{ applyFilter(currentData[metric.key], metric.format) }}
              </span>
            </div>
          </div>
        </template>
      </chart-tooltip>
    </span>
    <span v-else>
      <img
        src="@/assets/images/USA.png"
        alt="Hux"
        :width="chartDimensions.width"
        :height="chartDimensions.height"
        class="d-flex ma-4"
      />
    </span>
  </div>
</template>

<script>
import GeoChart from "@/components/common/MapChart/GeoChart"
import ChartTooltip from "@/components/common/Charts/Tooltip/ChartTooltip.vue"
import TooltipConfiguration from "@/components/common/Charts/Tooltip/tooltipStyleConfiguration.json"

export default {
  name: "MapChart",
  components: { GeoChart, ChartTooltip },
  props: {
    mapData: {
      type: Array,
      required: true,
    },
    configurationData: {
      type: Object,
      required: true,
    },
    disableHoverEffects: {
      type: Boolean,
      required: false,
      default: false,
    },
    dimension: {
      type: Object,
      required: false,
      default: () => {},
    },
  },
  data() {
    return {
      show: false,
      tooltip: {
        x: 0,
        y: 0,
      },
      chartDimensions: {
        width: (this.dimension && this.dimension.width) || 0,
        height: (this.dimension && this.dimension.height) || 0,
      },
      mapChartData: this.mapData,
      currentData: {},
      toolTipStyle: TooltipConfiguration.mapChart,
    }
  },
  computed: {
    defaultMetric() {
      return this.configurationData.default_metric.key
    },
  },
  mounted() {
    this.sizeHandler()
    new ResizeObserver(this.sizeHandler).observe(this.$refs.chartBox)
  },
  methods: {
    toolTipDisplay(...arg) {
      this.show = arg[0]
      if (this.show) {
        this.generateToolTipData(arg[1])
      }
    },
    sizeHandler() {
      if (this.$refs.chartBox) {
        this.chartDimensions.width = this.$refs.chartBox.clientWidth
        this.chartDimensions.height = this.$refs.chartBox.clientHeight
      }
    },
    getCordinates(args) {
      this.tooltip.x = args.x
      this.tooltip.y = args.y
    },
    generateToolTipData(currentStateinfo) {
      this.currentData = currentStateinfo
    },
    applyFilter(value, filter) {
      switch (filter) {
        case "numeric":
          return this.$options.filters.Numeric(value, true, false, false)
        case "percentage":
          return this.$options.filters.Numeric(value, true, false, false, true)
        case "currency":
          return this.$options.filters.Currency(value)
        default:
          return this.$options.filters.Empty
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.global-heading {
  padding-left: 2px;
}
.global-text-line {
  display: inline-block;
}
.container {
  position: relative;
  padding: 0px !important;
  .map-hover {
    .prop-name {
      @extend .global-heading;
    }
    .sub-props {
      display: flex;
      justify-content: flex-end;
      align-items: center;
      height: 15px;
      .subprop-name {
        @extend .global-text-line;
        flex: 0 0 40%;
        padding-left: 5px;
      }
      .value {
        @extend .global-text-line;
        flex: 1;
        text-align: left;
      }
    }
  }
}
</style>
