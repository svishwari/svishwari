<template>
  <div ref="chartBox" class="container">
    <span v-if="mapChartData.length != 0">
      <geo-chart
        v-model="mapChartData"
        :chart-dimensions="chartDimensions"
        :configuration-data="configurationData"
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
              class="sub-props pt-4"
            >
              <span
                v-if="metric.is_Combined_Metric"
                class="subprop-name mr-2"
                >{{ metric.label }}</span
              >
              <span
                v-if="!metric.is_Combined_Metric"
                class="subprop-name mr-2"
                >{{ metric.label }}</span
              >
              <span v-if="metric.is_Combined_Metric" class="value ml-1">
                <span v-for="(value, index) in metric.key" :key="value">
                  {{ applyFilter(currentData[value], metric.format) }}
                  <span v-if="index !== metric.key.length - 1">|</span>
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
        width="548"
        height="290"
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
  },
  data() {
    return {
      show: false,
      tooltip: {
        x: 0,
        y: 0,
      },
      chartDimensions: {
        width: 0,
        height: 0,
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
  created() {
    window.addEventListener("resize", this.sizeHandler)
  },
  destroyed() {
    window.removeEventListener("resize", this.sizeHandler)
  },
  mounted() {
    this.chartDimensions.width = this.$refs.chartBox.clientWidth
    this.chartDimensions.height = this.$refs.chartBox.clientHeight
  },
  methods: {
    toolTipDisplay(...arg) {
      this.show = arg[0]
      if (this.show) {
        this.generateToolTipData(arg[1])
      }
    },
    sizeHandler() {
      this.chartDimensions.width = this.$refs.chartBox.clientWidth
      this.chartDimensions.height = this.$refs.chartBox.clientHeight
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
  @extend .font-weight-semi-bold;
  font-style: normal;
  font-size: $font-size-root;
  line-height: 19px;
  padding-left: 2px;
}

.global-text-line {
  display: inline-block;
  font-weight: normal;
  font-style: normal;
  font-size: 12px;
  line-height: 16px;
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
      height: 30px;
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
