<template>
  <v-card
    class="map-card-wrapper mt-3 rounded-lg card-shadow pa-5"
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
          data-e2e="map-chart"
        />
        <map-slider
          v-if="!loading"
          :map-data="data.geo"
          :configuration-data="configurationData"
        />
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
import Icon from "../../components/common/Icon.vue"
import MapChart from "../../components/common/MapChart/MapChart.vue"
import MapSlider from "../../components/common/MapChart/mapSlider.vue"
import configurationData from "@/components/common/MapChart/MapConfiguration.json"
export default {
  name: "Geography",
  components: { Icon, MapChart, MapSlider },
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
</style>
