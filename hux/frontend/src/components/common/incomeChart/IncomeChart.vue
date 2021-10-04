<template>
  <div ref="incomeChart" class="container">
    <span v-if="incomes.length != 0">
      <horizontal-bar-chart
        v-model="incomes"
        :chart-dimensions="chartDimensions"
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
          <div class="bar-hover">
            {{ currentData.ltv | Currency }}
          </div>
        </template>
      </chart-tooltip>
    </span>
    <span v-else>
      <img
        src="@/assets/images/Chart.png"
        alt="Hux"
        width="180"
        height="150"
        class="d-flex ma-6"
      />
      <div class="d-flex ml-6 mt-8 global-text-line">
        <chart-legends :legends-data="legendsData" />
      </div>
    </span>
  </div>
</template>

<script>
import HorizontalBarChart from "@/components/common/incomeChart/HorizontalBarChart"
import ChartLegends from "@/components/common/Charts/Legends/ChartLegends.vue"
import ChartTooltip from "@/components/common/Charts/Tooltip/ChartTooltip.vue"
import TooltipConfiguration from "@/components/common/Charts/Tooltip/tooltipStyleConfiguration.json"

export default {
  name: "IncomeChart",
  components: {
    HorizontalBarChart,
    ChartLegends,
    ChartTooltip,
  },
  props: {
    data: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      show: false,
      chartDimensions: {
        width: 0,
        height: 0,
      },
      toolTipStyle: TooltipConfiguration.incomeChart,
      incomes: this.data,
      currentData: {},
      legendsData: [
        { color: "rgba(208, 208, 206, 1)", text: "no data available" },
      ],
    }
  },
  created() {
    window.addEventListener("resize", this.sizeHandler)
  },
  destroyed() {
    window.removeEventListener("resize", this.sizeHandler)
  },
  mounted() {
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
      if (this.$refs.incomeChart) {
        this.chartDimensions.width = this.$refs.incomeChart.clientWidth
        this.chartDimensions.height = 220
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.container {
  height: 350px;
  padding: 0px !important;
  position: relative;
  .global-text-line {
    display: inline-block;
    font-weight: normal;
    font-style: normal;
    font-size: 12px;
    line-height: 16px;
    color: var(--v-black-darken2) !important;
  }
  .bar-hover {
    padding: 5px 10px 5px 10px;
    color: var(--v-primary-darken1) !important;
  }
}
</style>
