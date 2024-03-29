<template>
  <div ref="chartBox" class="container">
    <horizontal-bar-chart
      v-model="features"
      :chart-dimensions="chartDimensions"
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
        <div class="bar-hover">
          <div class="text-body-2 black--text text--base mb-1">Feature</div>
          <div class="text-body-2 black--text text--base mb-1">
            <span class="dot"></span> {{ currentData.name }}
          </div>
          <div class="text-body-2 black--text text--base mb-1">
            {{ currentData.score }}
          </div>
          <div class="text-body-2 black--text text--lighten-4 mb-1">
            {{ currentData.description }}
          </div>
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
    this.sizeHandler()
    new ResizeObserver(this.sizeHandler).observe(this.$refs.chartBox)
  },
  methods: {
    toolTipDisplay(...arg) {
      this.show = arg[0]
      if (this.show) {
        this.currentData = arg[1]
        this.tooltip.x = arg[1].xPosition
        this.tooltip.y = arg[1].yPosition
      }
    },

    sizeHandler() {
      if (this.$refs.chartBox) {
        this.chartDimensions.width = this.$refs.chartBox.clientWidth
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
.container {
  height: 548px;
  padding: 0px !important;
  position: relative;
  .bar-hover {
    padding: 8px !important;
  }
}
.dot {
  height: 12px;
  width: 12px;
  background-color: var(--v-primary-darken2);
  border-radius: 50%;
  display: inline-block;
}
</style>
