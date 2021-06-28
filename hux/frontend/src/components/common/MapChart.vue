<template>
  <div>
    <chord-chart
      v-model="chartMatrix"
      :colorCodes="colorCodes"
      :chartLegendsData="chartLegendsData"
      v-on:cordinates="getCordinates"
      v-on:tooltipDisplay="toolTipDisplay"
    />
    <ChartTooltip
      :position="{
        x: tooltip.x,
        y: tooltip.y,
      }"
      :showTooltip="show"
      :isArcHover="isArcHover"
      :sourceInput="currentData"
    >
    </ChartTooltip>
  </div>
</template>

<script>
import ChartTooltip from "@/components/common/ChartTooltip"
import ChordChart from "@/components/common/ChordChart"
import identity_resolution from "@/components/common/chartData.json"
export default {
  name: "map-chart",
  components: { ChordChart, ChartTooltip },
  data() {
    return {
      colorCodes: ["#005587", "#da291c", "#00a3e0", "#43b02a", "#efa34c"],
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
      chartData: identity_resolution,
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
        icon1: null,
        name1: null,
        icon2: null,
        name2: null,
        currentOccurance: 0,
        totalOccurance: 0,
      },

      chartData: identity_resolution,
      chartMatrix: [],
      groupNames: [],
    }
  },
  methods: {
    generateChartGroups() {
      this.groupNames = Object.keys(this.chartData.identity_resolution)
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
        let sourceData = this.chartData.identity_resolution
        let group1 = this.groupNames[groupIndex[0]]
        if (this.isArcHover) {
          this.arcData.name = this.$options.filters.TitleCase(group1)
          this.arcData.icon = group1
          this.arcData.assetsData = this.mapIdentitySources(
            sourceData[group1].data_sources
          )
        } else {
          let group2 = this.groupNames[groupIndex[1]]
          this.ribbonData.name1 = this.$options.filters.TitleCase(group1)
          this.ribbonData.icon1 = group1
          this.ribbonData.name2 = this.$options.filters.TitleCase(group2)
          this.ribbonData.icon2 = group2
          this.mapCoOccurances(sourceData[group1].cooccurrences, group2)
        }
      }
    },

    mapIdentitySources(data_sources) {
      let assetsData = []
      for (let item of data_sources) {
        let tempSourceData = {}
        tempSourceData.icon = "cookie"
        ;(tempSourceData.description = item.name),
          (tempSourceData.value = this.$options.filters.percentageConvert(
            item.percentage,
            true,
            true
          ))
        assetsData.push(tempSourceData)
      }
      return assetsData
    },
    mapCoOccurances(cooccurances, identifier) {
      this.ribbonData.totalOccurance = cooccurances.reduce((a, b) => ({
        count: a.count + b.count,
      })).count
      this.ribbonData.currentOccurance = cooccurances.find(
        (data) => data.identifier === identifier
      ).count
    },

    transformData() {
      let sourceData = this.chartData.identity_resolution
      for (let key of this.groupNames) {
        this.createGroupRelationMatrix(sourceData[key].cooccurrences)
      }
    },

    createGroupRelationMatrix(element) {
      let groupRelation = new Array(5).fill(0)
      element.forEach((el) => {
        let extractedValues = this.extractCoOccurancesCount(el)
        groupRelation[extractedValues.index] = extractedValues.countValue
      })
      this.chartMatrix.push(groupRelation)
    },

    extractCoOccurancesCount(value) {
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
  mounted() {
    this.generateChartGroups()
    this.transformData()
  },
}
</script>
