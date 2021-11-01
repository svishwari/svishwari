<template>
  <div ref="identityChart" class="container">
    <div class="legend-chart-divider">
      <div class="chart-legends pl-4">
        <div
          v-for="item in chartLegendsData"
          :key="item.id"
          class="legend-section mb-2"
        >
          <icon
            :type="item.icon"
            :size="13"
            :color="item.color"
            :variant="item.variant"
          />
          <span class="text--body-2 ml-1 black--text text--lighten-4">{{
            item.prop
          }}</span>
        </div>
      </div>
      <div ref="chordsChart" class="chart-svg">
        <chord-chart
          v-model="chartMatrix"
          :color-codes="colorCodes"
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
            <div v-if="isArcHover" class="arc-hover">
              <icon
                v-if="currentData.icon"
                :type="currentData.icon"
                :size="13"
                :color="getIconInfo(currentData.icon)['color']"
                :variant="getIconInfo(currentData.icon)['variant']"
              />
              <span class="prop-name">{{ currentData.name }}</span>
              <div
                v-for="item in currentData.assetsData"
                :key="item.name"
                class="sub-props pt-4"
              >
                <logo v-if="item.icon" :type="item.icon" :size="14" />
                <span class="subprop-name">{{ item.description }}</span>
                <span class="value ml-1">{{ item.value }}</span>
              </div>
            </div>
            <div v-if="!isArcHover" class="ribbon-hover">
              <icon
                v-if="currentData.sourceIcon"
                :type="currentData.sourceIcon"
                :color="getIconInfo(currentData.sourceIcon)['color']"
                :variant="getIconInfo(currentData.sourceIcon)['variant']"
                :size="13"
              />
              <span class="prop-name">{{ currentData.sourceName }}</span>
              <span class="pipe"></span>
              <icon
                v-if="currentData.targetIcon"
                :type="currentData.targetIcon"
                :size="13"
                :color="getIconInfo(currentData.targetIcon)['color']"
                :variant="getIconInfo(currentData.targetIcon)['variant']"
              />
              <span class="prop-name">{{ currentData.targetName }}</span>
              <span class="text-line">
                {{ currentData.currentOccurence }} Co-occurrences
              </span>
              <span class="text-line-italic">
                out of {{ currentData.totalOccurence }} total co-occurrences
              </span>
            </div>
          </template>
        </chart-tooltip>
      </div>
    </div>
  </div>
</template>

<script>
import ChordChart from "@/components/common/identityChart/ChordChart"
import ChartTooltip from "@/components/common/Charts/Tooltip/ChartTooltip.vue"
import TooltipConfiguration from "@/components/common/Charts/Tooltip/tooltipStyleConfiguration.json"
import Icon from "@/components/common/Icon"
import Logo from "@/components/common/Logo"
export default {
  name: "IdentityChart",
  components: { ChordChart, ChartTooltip, Icon, Logo },
  props: {
    chartData: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      // TODO provide actual color code as per Icon colors
      colorCodes: ["#0076A8", "#42EFFD", "#00A3E0", "#43B02A", "#E3E48D"],
      // TODO Extracting it from the actual IDR data
      chartLegendsData: [
        { prop: "Name", icon: "name", color: "primary", variant: "darken1" },
        {
          prop: "Address",
          icon: "address",
          color: "primary",
          variant: "darken4",
        },
        { prop: "Email", icon: "email", color: "primary", variant: "base" },
        { prop: "Phone", icon: "phone", color: "success", variant: "base" },
        { prop: "Cookie", icon: "cookie", color: "info", variant: "base" },
      ],
      show: false,
      isArcHover: false,
      tooltip: {
        x: 0,
        y: 0,
      },
      currentData: {},
      arcData: {
        icon: null,
        name: null,
        assetsData: [
          {
            icon: null,
            description: null,
            value: null,
          },
          {
            icon: null,
            description: null,
            value: null,
          },
        ],
      },
      ribbonData: {
        sourceIcon: null,
        sourceName: null,
        targetIcon: null,
        targetName: null,
        currentOccurence: 0,
        totalOccurence: 0,
      },
      chartMatrix: [],
      groupNames: [],
      chartDimensions: {
        width: 0,
        height: 0,
      },
      toolTipStyle: TooltipConfiguration.identityChart,
    }
  },
  mounted() {
    this.generateChartGroups()
    this.transformData()
    this.sizeHandler()
    new ResizeObserver(this.sizeHandler).observe(this.$refs.chordsChart)
  },
  methods: {
    generateChartGroups() {
      this.groupNames = Object.keys(this.chartData)
    },

    getIconInfo(iconType) {
      return this.chartLegendsData.filter((leg) => leg.icon === iconType)[0]
    },

    toolTipDisplay(...arg) {
      this.show = arg[0]
      this.isArcHover = arg[1]
      this.generateToolTipData(arg[2])
      this.currentData = this.isArcHover ? this.arcData : this.ribbonData
    },

    getCordinates(args) {
      this.tooltip.x = args.x
      this.tooltip.y = args.y
    },

    sizeHandler() {
      if (this.$refs.chordsChart) {
        this.chartDimensions.width = this.$refs.chordsChart.clientWidth
        this.chartDimensions.height = 190
      }
    },

    generateToolTipData(groupIndex) {
      if (groupIndex.length > 0) {
        let sourceData = this.chartData
        let group1 = this.groupNames[groupIndex[0]]
        if (this.isArcHover) {
          this.arcData.name = this.$options.filters.TitleCase(group1)
          this.arcData.icon = group1
          this.arcData.assetsData = this.mapIdentitySources(
            sourceData[group1].data_sources
          )
        } else {
          let group2 = this.groupNames[groupIndex[1]]
          this.ribbonData.sourceName = this.$options.filters.TitleCase(group1)
          this.ribbonData.sourceIcon = group1
          this.ribbonData.targetName = this.$options.filters.TitleCase(group2)
          this.ribbonData.targetIcon = group2
          this.mapCoOccurences(sourceData[group1].cooccurrences, group2)
        }
      }
    },
    mapIdentitySources(data_sources) {
      let assetsData = []
      for (let item of data_sources) {
        let tempSourceData = {}
        ;(tempSourceData.icon = item.name.toLowerCase()),
          (tempSourceData.description = item.name),
          (tempSourceData.value = this.$options.filters.Percentage(
            item.percentage
          ))
        assetsData.push(tempSourceData)
      }
      return assetsData
    },
    mapCoOccurences(cooccurences, identifier) {
      this.ribbonData.totalOccurence = cooccurences.reduce((a, b) => ({
        count: a.count + b.count,
      })).count
      this.ribbonData.currentOccurence = cooccurences.find(
        (data) => data.identifier === identifier
      ).count
    },

    transformData() {
      let sourceData = this.chartData
      for (let key of this.groupNames) {
        this.createGroupRelationMatrix(sourceData[key].cooccurrences)
      }
    },

    createGroupRelationMatrix(element) {
      let groupRelation = new Array(5).fill(0)
      element.forEach((el) => {
        let extractedValues = this.extractCoOccurencesCount(el)
        groupRelation[extractedValues.index] = extractedValues.countValue
      })
      this.chartMatrix.push(groupRelation)
    },

    extractCoOccurencesCount(value) {
      let extractedValues = {
        index: 0,
        countValue: 0,
      }

      for (let i = 0; i < this.groupNames.length; i++) {
        if (this.groupNames[i] == value.identifier) {
          extractedValues.index = i
          extractedValues.countValue = value.count
          break
        }
      }
      return extractedValues
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
  padding-left: 10px;
}

.global-text-line {
  display: inline-block;
  font-weight: normal;
  font-style: normal;
  font-size: 12px;
  line-height: 16px;
}

.card-padding {
  padding: 10px 20px 20px 20px;
}
.container {
  height: 280px;

  .legend-chart-divider {
    margin-top: 57px;

    display: flex;
    justify-content: flex-start;
    align-items: center;
    height: 30px;
    .chart-legends {
      flex: 1 0 32%;
      padding-left: 5px;
      .legend-section {
      }
    }
    .chart-svg {
      min-width: 200px;
      max-width: 240px;
      position: relative;
      .ribbon-hover {
        @extend .card-padding;
        .pipe {
          border-left: 1px solid var(--v-black-lighten3) !important;
          height: 500px;
          transform: rotate(90deg);
          margin-left: 10px;
          margin-right: 10px;
        }
        .prop-name {
          @extend .global-heading;
        }
        .text-line {
          @extend .global-text-line;
          margin-top: 10px;
        }
        .text-line-italic {
          @extend .global-text-line;
          font-style: italic;
        }
      }

      .arc-hover {
        @extend .card-padding;
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
            flex: 1 0 50%;
            padding-left: 5px;
          }
          .value {
            @extend .global-text-line;
          }
        }
      }
    }
  }
}
</style>
