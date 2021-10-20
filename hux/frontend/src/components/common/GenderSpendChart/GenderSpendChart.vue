<template>
  <div ref="genderSpendChart" class="container">
    <line-area-chart
      v-model="modificationData"
      :chart-dimensions="chartDimensions"
      :y-value-data="yAxisData"
      :date-data="dateData"
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
          <div class="date-font text-body-2">
            {{ currentData.date | date("MMM DD[,] YYYY") }}
          </div>
          <div>
            <span class="append-circle color-women"></span>
            <span class="font-size-tooltip text-body-2">
              {{ currentData.women_spend | currency }}
            </span>
          </div>
          <div>
            <span class="append-circle color-men"></span>
            <span class="font-size-tooltip text-body-2">
              {{ currentData.men_spend | currency }}
            </span>
          </div>
          <div>
            <span class="append-circle color-other"></span>
            <span class="font-size-tooltip">
              {{ currentData.others_spend | currency }}
            </span>
          </div>
        </div>
      </template>
    </chart-tooltip>
  </div>
</template>

<script>
import LineAreaChart from "@/components/common/GenderSpendChart/LineAreaChart"
import ChartTooltip from "@/components/common/Charts/Tooltip/ChartTooltip.vue"
import TooltipConfiguration from "@/components/common/Charts/Tooltip/tooltipStyleConfiguration.json"

export default {
  name: "GenderSpendChart",
  components: { LineAreaChart, ChartTooltip },
  props: {
    data: {
      type: Object,
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
      spendData: [],
      yAxisData: [],
      currentData: {},
      dateData: [],
      toolTipStyle: TooltipConfiguration.genderSpendChart,
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
.container {
  height: 500px;
  padding: 0px !important;
  position: relative;

  .append-circle {
    height: 12px;
    width: 12px;
    background-color: var(--v-white-base);
    border-radius: 50%;
    display: inline-block;
    margin-top: 6px;
    margin-right: 8px;
  }
  .color-women {
    border: 1px solid rgba(0, 85, 135, 1);
  }
  .color-men {
    border: 1px solid var(--v-primary-darken1);
  }
  .color-other {
    border: 1px solid var(--v-primary-lighten7);
  }
  .hover-font {
    font-family: Open Sans;
    font-style: normal;
    font-weight: normal;
    font-size: 12px;
    line-height: 16px;
  }
  .font-size-tooltip {
    @extend .hover-font;
    color: var(--v-black-darken1);
    position: absolute;
    margin-top: 5px;
  }
  .date-font {
    @extend .hover-font;
    color: var(--v-naroBlack-base);
  }
}
</style>
