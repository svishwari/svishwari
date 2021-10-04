<template>
  <div ref="chartBox" class="container">
    <horizontal-bar-chart
      v-model="features"
      :chart-dimensions="chartDimensions"
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
      <div class="bar-hover black--text text--darken-4">
        <span class="feature-name">
          {{ currentData.name }}
        </span>
        <span class="feature-description">
          {{ currentData.description }}
        </span>
      </div>
      </template>
    </chart-tooltip>
  </div>
</template>

<script>
import HorizontalBarChart from "@/components/common/featureChart/HorizontalBarChart"
import ChartTooltip from "@/components/common/Charts/Tooltip/ChartTooltip.vue"
import TooltipConfiguration from "@/components/common/Charts/Tooltip/tooltipStyleConfiguration.json"
export default {
  name: "FeatureChart",
  components: { HorizontalBarChart, ChartTooltip },
  props: {
    featureData: {
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
      currentData: {},
      toolTipStyle: TooltipConfiguration.featureChart,
      chartDimensions: {
        width: 0,
        height: 0,
      },
    }
  },
  computed: {
    features() {
      return this.featureData
    },
  },
  mounted() {
    this.chartDimensions.width = this.$refs.chartBox.clientWidth
    this.chartDimensions.height = this.$refs.chartBox.clientHeight
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
.global-text-format {
  display: inline-block;
  font-weight: normal;
  font-style: normal;
  font-size: 12px;
  line-height: 16px;
  color: var(--v-black-darken2) !important;
}
.container {
  height: 650px;
  padding: 0px !important;
  position: relative;
    .bar-hover {
    padding: 7px 20px 20px 20px;
    .feature-name {
      @extend .global-text-format;
    }
    .feature-description {
      @extend .global-text-format;
      margin-top: 8px;
    }
  }
}
</style>
