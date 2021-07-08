<template>
  <div>
    <div class="container d-flex justify-space-around">
      <geo-chart
        v-model="chartMatrix"
        :colorCodes="colorCodes"
        :chartLegendsData="chartLegendsData"
        v-on:cordinates="getCordinates"
        v-on:tooltipDisplay="toolTipDisplay"
      />
      <v-card class="rounded-lg card-style" minHeight="20px">
        <v-card-title class="d-flex justify-space-between pb-2 pl-6 pt-5">
          <div class="mt-2">
            <a
              href="#"
              class="d-flex align-center primary--text text-decoration-none"
            >
              United States
            </a>
          </div>
        </v-card-title>
        <v-divider class="ml-6 mr-6 mt-1 mb-2" />
        <v-card-text minHeight="100px" class="content-style pl-6 pr-6 pb-6">
          <div
            class="sub-props pt-4"
            v-for="item in mapChartData"
            :key="item.name"
          >
            <span class="subprop-name">{{ item.name }}</span>
            <span class="value ml-2">{{
              item.population_percentage | percentageConvert(true, true)
            }}</span>
          </div>
        </v-card-text>
      </v-card>
    </div>
    <map-chart-tooltip
      :position="{
        x: tooltip.x,
        y: tooltip.y,
      }"
      :showTooltip="show"
      :sourceInput="currentData"
    >
    </map-chart-tooltip>
  </div>
</template>

<script>
import MapChartTooltip from "@/components/common/MapChart/MapChartTooltip"
import GeoChart from "@/components/common/MapChart/GeoChart"
import demographic_overview from "./mapData.json"
export default {
  name: "map-chart",
  components: { GeoChart, MapChartTooltip },
  data() {
    return {
      show: false,
      isArcHover: false,
      tooltip: {
        x: 0,
        y: 0,
      },
      mapChartData: demographic_overview.demographic_overview,
      currentData: {},
    }
  },
  methods: {
    toolTipDisplay(...arg) {
      this.show = arg[0]
      if (this.show) {
        this.generateToolTipData(arg[1])
      }
    },

    getCordinates(args) {
      this.tooltip.x = args.x
      this.tooltip.y = args.y
    },

    generateToolTipData(currentStateinfo) {
      this.currentData = currentStateinfo
    },
  },
  mounted() {
    this.generateChartGroups()
    this.transformData()
  },
}
</script>

<style lang="scss" scoped>
.global-text-line {
  display: inline-block;
  font-weight: normal;
  font-style: normal;
  font-size: 12px;
  line-height: 16px;
}
.container {
  height: 550px;
  padding: 0px !important;
  .card-style {
    .content-style {
      max-height: 450px;
      overflow-y: scroll;
      .sub-props {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        .subprop-name {
          @extend .global-text-line;
          flex: 1 0 50%;
          padding-left: 5px;
        }
        .value {
          @extend .global-text-line;
          font-weight: bold;
        }
      }
    }

    ::-webkit-scrollbar {
      width: 5px;
    }

    /* Track */
    ::-webkit-scrollbar-track {
      box-shadow: inset 0 0 5px white;
      border-radius: 10px;
    }

    /* Handle */
    ::-webkit-scrollbar-thumb {
      background: #d0d0ce;
      border-radius: 5px;
    }

    /* Handle on hover */
    ::-webkit-scrollbar-thumb:hover {
      background: #d0d0ce;
    }
  }
}
</style>
