<template>
  <div class="container">
    <chord-chart
      v-model="genderChartData"
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
import ChartTooltip from "@/components/common/DonutChart/ChartTooltip"
import ChordChart from "@/components/common/DonutChart/ChordChart"
import genderData from "@/components/common/DonutChart/genderData.json"
export default {
  name: "donut-chart",
  components: { ChordChart, ChartTooltip },
  data() {
    return {
      // TODO provide actual color code as per Icon colors
      colorCodes: ["#005587", "#42EFFD", "#0C9DDB"],
      // TODO Extracting it from the actual IDR data
      chartLegendsData: [
        { prop: "Men", icon: "name", color: "#005587" },
        { prop: "Women", icon: "address", color: "#42EFFD" },
        { prop: "Other", icon: "email", color: "#0C9DDB" },
      ],
      show: false,
      isArcHover: false,
      tooltip: {
        x: 0,
        y: 0,
      },
      chartData: genderData,
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
      genderChartData: genderData.gender,
      groupNames: [],
    }
  },
  methods: {
    generateChartGroups() {
      this.groupNames = Object.keys(this.genderChartData)
    },

    toolTipDisplay(...arg) {
      this.show = arg[0]
      // this.isArcHover = arg[1]
      // this.generateToolTipData(arg[2])
      this.currentData = arg[1]
    },

    getCordinates(args) {
      this.tooltip.x = args.x
      this.tooltip.y = args.y
    },

    // generateToolTipData(groupIndex) {
    //   if (groupIndex.length > 0) {
    //     let sourceData = this.genderData.identity_resolution
    //     let group1 = this.groupNames[groupIndex[0]]
    //     if (this.isArcHover) {
    //       this.arcData.name = this.$options.filters.TitleCase(group1)
    //       this.arcData.icon = group1
    //       this.arcData.assetsData = this.mapIdentitySources(
    //         sourceData[group1].data_sources
    //       )
    //     }
    //   }
    // },
    // mapIdentitySources(data_sources) {
    //   let assetsData = []
    //   for (let item of data_sources) {
    //     let tempSourceData = {}
    //     ;(tempSourceData.icon = item.name.toLowerCase()),
    //       (tempSourceData.description = item.name),
    //       (tempSourceData.value = this.$options.filters.percentageConvert(
    //         item.percentage,
    //         true,
    //         true
    //       ))
    //     assetsData.push(tempSourceData)
    //   }
    //   return assetsData
    // },

    transformData() {
      let sourceData = this.genderChartData
      for (let key of this.groupNames) {
        this.createGroupRelationMatrix(sourceData[key])
      }
    },

    createGroupRelationMatrix(element) {
      debugger
      let groupRelation = new Array(3).fill(0)
      // element.forEach((el) => {
      //   let extractedValues = this.extractCoOccurancesCount(el)
      //   groupRelation[extractedValues.index] = extractedValues.countValue
      // })
      this.genderChartData.push(groupRelation)
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

<style lang="scss" scoped>
.container {
  height: 280px;
  padding: 0px !important;
}
</style>
