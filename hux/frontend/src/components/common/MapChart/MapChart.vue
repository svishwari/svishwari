<template>
  <div class="container">
    <div class="d-flex justify-space-around">
      <geo-chart
        v-model="mapChartData"
        @cordinates="getCordinates"
        @tooltipDisplay="toolTipDisplay"
      />
      <v-card class="rounded-lg card-style" min-height="20px">
        <v-card-title class="d-flex justify-space-between pb-2 pl-6 pt-5">
          <div class="mt-2">
            <span class="d-flex align-center black--text text-decoration-none">
              United States
            </span>
          </div>
        </v-card-title>
        <v-divider class="ml-6 mr-8 mt-0 mb-2" />
        <v-card-text min-height="100px" class="content-style pl-6 pr-4 pb-4">
          <div
            v-for="item in mapChartData"
            :key="item.name"
            class="sub-props pt-4"
          >
            <span class="subprop-name">{{ item.name }}</span>
            <span class="value ml-2 font-weight-semi-bold">
              {{ item.population_percentage | Percentage }}
            </span>
          </div>
        </v-card-text>
      </v-card>
    </div>
    <map-chart-tooltip
      :position="{
        x: tooltip.x,
        y: tooltip.y,
      }"
      :show-tooltip="show"
      :source-input="currentData"
    >
    </map-chart-tooltip>
  </div>
</template>

<script>
import MapChartTooltip from "@/components/common/MapChart/MapChartTooltip"
import GeoChart from "@/components/common/MapChart/GeoChart"
// TODO: this should be come up from props while doing API Integration
import mapData from "./mapData.json"
export default {
  name: "MapChart",
  components: { GeoChart, MapChartTooltip },
  data() {
    return {
      show: false,
      tooltip: {
        x: 0,
        y: 0,
      },
      mapChartData: mapData.demographic_overview,
      currentData: {},
    }
  },
  mounted() {
    this.sortStateData()
  },
  methods: {
    sortStateData() {
      if (this.mapChartData) {
        this.mapChartData.sort(
          (a, b) => b.population_percentage - a.population_percentage
        )
      }
    },
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
  height: 550px;
  padding: 0px !important;
  .card-style {
    max-height: 550px;
    .content-style {
      padding-top: 0px !important;
      max-height: 450px;
      overflow-y: scroll;
      .sub-props {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        .subprop-name {
          @extend .global-text-line;
          flex: 1 0 40%;
          text-align: right;
          margin-right: 30px;
        }
        .value {
          @extend .global-text-line;
          color: var(--v-neroBlack-base);
          flex: 1;
          text-align: left;
        }
      }
    }
    ::-webkit-scrollbar {
      width: 5px;
    }
    ::-webkit-scrollbar-track {
      box-shadow: inset 0 0 5px var(--v-white-base);
      border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb {
      background: var(--v-lightGrey-base);
      border-radius: 5px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: var(--v-lightGrey-base);
    }
  }
}
</style>
