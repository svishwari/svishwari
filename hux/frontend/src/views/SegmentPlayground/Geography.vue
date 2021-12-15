<template>
  <v-card
    class="map-card-wrapper mt-3 rounded-lg card-shadow pa-6"
    height="400"
  >
    <v-card-title class="d-flex justify-space-between pa-0">
      <h5 class="text-h3">USA</h5>
      <v-btn-toggle v-model="toggle_view" tile class="toggle-options">
        <v-btn text min-width="36" small @click="showMapView = true">
          <icon type="world" color="black" :size="36" class="mr-1" />
        </v-btn>
        <v-btn text min-width="36" small @click="showMapView = false">
          <icon type="list" color="black" :size="36" />
        </v-btn>
      </v-btn-toggle>
    </v-card-title>
    <v-card-text class="pa-0">
      <v-progress-linear
        v-if="loading"
        :active="loading"
        :indeterminate="loading"
      />
      <div v-if="showMapView && data.geo">
        <map-chart
          v-if="!loading"
          :map-data="data.geo"
          :configuration-data="configurationData"
          :disable-hover-effects="true"
          data-e2e="map-chart"
        />
        <map-slider
          v-if="!loading"
          :map-data="data.geo"
          :configuration-data="configurationData"
        />
      </div>
      <div v-if="!showMapView && data.geo" class="pt-2">
        <map-state-list
          v-if="!loadingGeoOverview"
          :map-data="data.geo"
          :configuration-data="configurationData"
          :header-config="headerConfig"
          :sort-metric="sortMetric"
          :height="330"
        />
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
import Icon from "../../components/common/Icon.vue"
import MapChart from "../../components/common/MapChart/MapChart.vue"
import MapSlider from "../../components/common/MapChart/mapSlider.vue"
import MapStateList from "@/components/common/MapChart/MapStateList"
import configurationData from "@/components/common/MapChart/MapConfiguration.json"
export default {
  name: "Geography",
  components: { Icon, MapChart, MapSlider, MapStateList },
  props: {
    data: {
      type: Object,
      required: false,
      default: () => {},
    },
    loading: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    return {
      toggle_view: 0,
      showMapView: true,
      configurationData: configurationData,
      headerConfig: ["name", "population_percentage"],
      sortMetric: "population_percentage",
    }
  },
}
</script>

<style lang="scss" scoped>
.toggle-options {
  .v-btn {
    background: none;
    border: none;
    border-width: inherit !important;
    &::before {
      opacity: 0;
    }
    &.v-item--active {
      svg {
        fill: var(--v-primary-lighten6) !important;
      }
    }
  }
}

.map-card-wrapper {
  ::-webkit-scrollbar {
    width: 5px;
  }
  ::-webkit-scrollbar-track {
    box-shadow: inset 0 0 5px var(--v-white-base);
    border-radius: 10px;
  }
  ::-webkit-scrollbar-thumb {
    background: var(--v-black-lighten3);
    border-radius: 5px;
  }
  ::-webkit-scrollbar-thumb:hover {
    background: var(--v-black-lighten3);
  }

  ::v-deep .hux-data-table {
    table {
      tbody {
        tr {
          display: table;
          width: 100%;
          td {
            &:first-child {
              color: var(--v-black-lighten4);
            }
            &:last-child {
              color: var(--v-black-base);
            }
          }
        }
      }
    }
    .v-data-table {
      .v-data-table-header {
        tr {
          height: 40px !important;
        }
        th {
          background: var(--v-primary-lighten2);
          &:first-child {
            border-top-left-radius: 12px;
          }
          &:last-child {
            border-top-right-radius: 12px;
          }
        }
      }
    }
  }
  ::v-deep .v-input__prepend-outer {
    margin-right: 4px;
    .slider-value-display {
      width: 37px !important;
    }
  }
}
</style>
