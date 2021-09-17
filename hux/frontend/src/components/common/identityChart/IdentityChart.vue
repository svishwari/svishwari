<template>
  <div class="container">
    <chord-chart
      v-model="chartMatrix"
      :color-codes="colorCodes"
      :chart-legends-data="chartLegendsData"
      @cordinates="getCordinates"
      @tooltipDisplay="toolTipDisplay"
    />
    <chart-tooltip
      :position="{
        x: tooltip.x,
        y: tooltip.y,
      }"
      :show-tooltip="show"
      :is-arc-hover="isArcHover"
      :source-input="currentData"
    >
    </chart-tooltip>
  </div>
</template>

<script>
import ChartTooltip from "@/components/common/identityChart/ChartTooltip"
import ChordChart from "@/components/common/identityChart/ChordChart"
export default {
  name: "IdentityChart",

  components: { ChordChart, ChartTooltip },

  props: {
    chartData: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      // TODO provide actual color code as per Icon colors
      colorCodes: ["#005587", "#da291c", "#00a3e0", "#43b02a", "#efa34c"],
      // TODO Extracting it from the actual IDR data
      chartLegendsData: [
        { prop: "Name", icon: "name", color: "#005587" },
        { prop: "Address", icon: "address", color: "#da291c" },
        { prop: "Email", icon: "email", color: "#00a3e0" },
        { prop: "Phone", icon: "phone", color: "#43b02a" },
        { prop: "Cookie", icon: "cookie", color: "#efa34c" },
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
    }
  },
  mounted() {
    this.generateChartGroups()
    this.transformData()
  },
  methods: {
    generateChartGroups() {
      this.groupNames = Object.keys(this.chartData)
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
.container {
  height: 280px;
  padding: 0px !important;
}
</style>
