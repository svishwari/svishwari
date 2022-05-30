<template>
  <div ref="trustIdComparisonChart" class="container-chart">
    <grouped-bar-chart
      v-model="chartSourceData"
      :chart-dimensions="chartDimensions"
      :empty-state="isEmptyState"
      @tooltipDisplay="toolTipDisplay"
    />
    <checkbox-chart-legends
      :legends-data="legendsData"
      class="ml-16 mt-7"
      @onCheckboxChange="filterSegmentData"
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
        <div class="text-body-2 black--text text--darken-4 caption">
          <div class="spend-count mb-1 text-h5">
            <span
              class="dots"
              :style="{ backgroundColor: currentData.color }"
            ></span>
            <span> {{ currentData.segmentName }}</span>
          </div>
          <div class="value-container">
            {{ currentData.attributeName }}
          </div>
          <div class="date-section">
            {{ currentData.score }}
          </div>
        </div>
      </template>
    </chart-tooltip>
  </div>
</template>

<script>
import GroupedBarChart from "@/components/common/Charts/GroupedBarChart/GroupedBarChart.vue"
import ChartTooltip from "@/components/common/Charts/Tooltip/ChartTooltip.vue"
import TooltipConfiguration from "@/components/common/Charts/Tooltip/tooltipStyleConfiguration.json"
import CheckboxChartLegends from "@/components/common/Charts/Legends/CheckBoxChartLegends.vue"

export default {
  name: "TrustComparisonChart",
  components: { GroupedBarChart, ChartTooltip, CheckboxChartLegends },
  props: {
    segmentScores: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      show: false,
      isEmptyState: false,
      colors: [
        "#0076A8",
        "#A0DCFF",
        "#00A3E0",
        "#E3E48D",
        "#007680",
        "#9DD4CF",
      ],
      attributes: [
        "trust_id",
        "humanity",
        "transparency",
        "capability",
        "reliability",
      ],
      currentData: {},
      chartSourceData: [],
      sourceData: [],
      legendsData: [],
      chartDimensions: {
        width: 0,
        height: 0,
      },
      toolTipStyle: TooltipConfiguration.trustIdComparisonChart,
    }
  },
  watch: {
    segmentScores: function () {
      this.initializeComparisonChart()
    },
  },
  mounted() {
    this.initializeComparisonChart()
  },

  methods: {
    initializeComparisonChart() {
      this.sizeHandler()
      this.initializeSegmentData()
      this.processData()
      this.setLegendsData()
      new ResizeObserver(this.sizeHandler).observe(
        this.$refs.trustIdComparisonChart
      )
    },
    toolTipDisplay(...arg) {
      this.show = arg[0]
      if (this.show) {
        this.currentData = arg[1]
        if (this.currentData.invertPosition) {
          this.toolTipStyle.left =
            this.currentData.color == "#0076A8"
              ? "-378px"
              : "-360px"
        } else this.toolTipStyle.left = "-228px"

        console.log(this.currentData)
      }
    },
    sizeHandler() {
      if (this.$refs.trustIdComparisonChart) {
        this.chartDimensions.width =
          this.$refs.trustIdComparisonChart.clientWidth
        this.chartDimensions.height = 350
      }
    },
    // Handles checkboxes event and reload chart accordingly
    filterSegmentData(itemsData) {
      this.initializeSegmentData()
      let uncheckedItems = itemsData.filter((data) => !data.checked)
      if (uncheckedItems) {
        for (let item of uncheckedItems) {
          this.sourceData = this.sourceData.filter(
            (data) => data.segment_name != item.text
          )
        }
      }
      this.processData()
    },
    // initialize source data to process for chart
    initializeSegmentData() {
      if (this.segmentScores) {
        this.sourceData = this.segmentScores.find(
          (data) => data.segment_type == "composite & factor scores"
        ).segments
        this.sourceData.forEach(
          (data, index) =>
            (data.color =
              this.colors[this.hasDefaultSegment() ? index : index + 1])
        )
      } else {
        this.isEmptyState = true
      }
    },
    // data manipulation and grouping for chart input
    processData() {
      this.chartSourceData = []
      if (this.segmentScores) {
        for (let attr of this.attributes) {
          let segmentAttrScore = []
          let currentAttribute = ""
          this.sourceData.forEach((data) => {
            let attr_data = data.attributes.find(
              (el) => el.attribute_type == attr
            )
            currentAttribute = attr_data.attribute_name
            segmentAttrScore.push({
              value: attr_data.attribute_score,
              color: data.color,
              segmentName: data.segment_name,
            })
          })
          this.chartSourceData.push({
            id: attr,
            label: currentAttribute,
            values: segmentAttrScore,
          })
        }
      }
    },
    // setting charts legends and checkbox data
    setLegendsData() {
      this.legendsData = []
      for (let [index, segment] of this.sourceData.entries()) {
        this.legendsData.push({
          color: this.colors[this.hasDefaultSegment() ? index : index + 1],
          checked: true,
          disabled: false,
          text: segment.segment_name,
        })
      }
    },

    hasDefaultSegment() {
      return this.sourceData.some((data) => data.default)
    },
  },
}
</script>

<style lang="scss" scoped>
.global-heading {
  font-style: normal;
  color: var(--v-black-base) !important;
  margin-bottom: 4px;
}
.container-chart {
  position: relative;
  height: 400px;
  padding: 0px !important;
  .value-container {
    margin-top: 2px;
    margin-bottom: 4px;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    font-weight: 700;
    @extend .global-heading;
    .text-label {
      margin-left: 4px !important;
    }
  }
  .value-section {
    @extend .global-heading;
    margin-left: 24px;
    margin-bottom: 10px;
  }
  .date-section {
    @extend .global-heading;
    color: var(--v-black-lighten4) !important;
  }
  .spend-count {
    .dots {
      margin-right: 4px;
      height: 10px;
      width: 10px;
      border-radius: 50%;
      display: inline-block;
    }
  }
}
</style>
