<template>
  <div ref="genderSpendChart" class="container">
    <line-area-chart
      v-model="modificationData"
      :chart-dimensions="chartDimensions"
      :y-value-data="yAxisData"
      :date-data="dateData"
      @cordinates="getCordinates"
      @tooltipDisplay="toolTipDisplay"
    />

    <line-area-chart-tooltip
      :position="{
        x: tooltip.x,
        y: tooltip.y,
      }"
      :show-tooltip="show"
      :source-input="currentData"
    >
    </line-area-chart-tooltip>
  </div>
</template>

<script>
import LineAreaChartTooltip from "@/components/common/GenderSpendChart/LineAreaChartTooltip"
import LineAreaChart from "@/components/common/GenderSpendChart/LineAreaChart"

export default {
  name: "GenderSpendChart",
  components: { LineAreaChart, LineAreaChartTooltip },
  props: {
    data: {
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
      spendData: [],
      yAxisData: [],
      currentData: {},
      dateData: [],
    }
  },
  computed: {
    modificationData() {
      let dataValue = this.data
      let areaChart = []
      let areaChartData = []

      dataValue.gender_men.forEach((element) => {
        dataValue.gender_women.forEach((value) => {
          if (element.date === value.date) {
            areaChart.push({
              date: element.date,
              men_spend: element.ltv,
              women_spend: value.ltv,
            })
          }
        })
      })

      areaChart.forEach((element) => {
        dataValue.gender_other.forEach((value) => {
          if (element.date === value.date) {
            this.yAxisData.push(
              element.men_spend,
              element.women_spend,
              value.ltv
            )
            areaChartData.push({
              date: element.date,
              men_spend: element.men_spend,
              women_spend: element.women_spend,
              others_spend: value.ltv,
            })
          }
        })
      })

      areaChartData.forEach((element) => {
        this.dateData.push(new Date(element.date))
      })

      return areaChartData
    },
  },

  created() {
    this.modificationData
    window.addEventListener("resize", this.sizeHandler)
  },
  destroyed() {
    window.removeEventListener("resize", this.sizeHandler)
  },
  mounted() {
    this.sizeHandler()
    this.modificationData
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
      if (this.$refs.genderSpendChart) {
        this.chartDimensions.width = this.$refs.genderSpendChart.clientWidth
        this.chartDimensions.height = 180
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
  height: 500px;
  padding: 0px !important;
}
</style>
