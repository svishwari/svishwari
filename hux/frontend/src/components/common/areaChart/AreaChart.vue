<template>
  <div class="container">
    <div class="d-flex justify-content-start">
      <line-area-chart
      />
    </div>
    <!-- <bar-chart-tooltip
      :position="{
        x: tooltip.x,
        y: tooltip.y,
      }"
      :showTooltip="show"
      :sourceInput="currentData"
    >
    </bar-chart-tooltip> -->
  </div>
</template>

<script>
// import BarChartTooltip from "@/components/common/incomeChart/BarChartTooltip"
import LineAreaChart from "@/components/common/areaChart/LineAreaChart"
//TODO: API Integration
// import data from "./incomeData.json"

export default {
  name: "area-chart",
  components: { LineAreaChart },
  data() {
    return {
      show: false,
      tooltip: {
        x: 0,
        y: 0,
      },
    //   incomes: data.income,
      currentData: {},
    }
  },
  methods: {
    // toolTipDisplay(...arg) {
    //   this.show = arg[0]
    //   if (this.show) {
    //     this.currentData = arg[1]
    //   }
    // },

    // getCordinates(args) {
    //   this.tooltip.x = args.x
    //   this.tooltip.y = args.y
    // },
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
  height: 350px;
  padding: 0px !important;
}
</style>
