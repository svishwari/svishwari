<template>
  <div class="playground-wrap">
    <page-header :header-height-changes="'py-3'" :header-height="110">
      <template slot="left">
        <div class="mt-n3">
          <breadcrumb :items="breadcrumbItems" />
        </div>
        <div class="text-subtitle-1 font-weight-regular mt-1">
          Get immediate insights by segmenting your customer list based on
          attributes that you want to explore.
        </div>
      </template>
      <template #right> </template>
    </page-header>
    <div>
      <v-row>
        <v-col class="col-8 attribute-div"></v-col>
        <v-col class="col-4 overview-div">
          <v-card class="mt-3 rounded-lg box-shadow-5" height="386"> </v-card>
          <v-card class="mt-3 rounded-lg box-shadow-5" height="386">
            <div class="d-flex justify-space-between pb-2 pl-5 pt-5">
            <h5 class="text-h3 mb-1">USA</h5>
            <div>
            <v-btn
              text
              small
              @click="showMapView()"
            >
              <icon
                type="world"
                color="primary"
                :size="32"
                class="mr-1"
              />
            </v-btn>
              <v-btn
              text
              small
              @click="showListView()"
            >
              <icon
                type="list"
                color="primary"
                :size="32"
                class="mr-1"
              />
            </v-btn>
            </div>
          </div>
            
            <v-progress-linear
              v-if="loadingGeoOverview"
              :active="loadingGeoOverview"
              :indeterminate="loadingGeoOverview"
            />
            <map-chart
              v-if="!loadingGeoOverview"
              :map-data="customersGeoOverview"
              :configuration-data="configurationData"
              :disable-hover-effects="true"
              data-e2e="map-chart"
            />
            <map-slider
              v-if="!loadingGeoOverview"
              :map-data="customersGeoOverview"
              :configuration-data="configurationData"
            />
          </v-card>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import MapChart from "@/components/common/MapChart/MapChart"
import mapSlider from "@/components/common/MapChart/mapSlider"
import Icon from "@/components/common/Icon"
import configurationData from "@/components/common/MapChart/MapConfiguration.json"

export default {
  name: "SegmentPlayground",
  components: {
    PageHeader,
    Breadcrumb,
    MapChart,
    mapSlider,
    Icon,
  },
  data() {
    return {
      breadcrumbItems: [
        {
          text: "Segment Playground",
          disabled: true,
          icon: "playground",
        },
      ],
      loadingGeoOverview: false,
      configurationData: configurationData,
    }
  },
  computed: {
    ...mapGetters({
      customersGeoOverview: "customers/geoOverview",
    }),

    showMapView() {
      
    }
  },

  mounted() {
    this.fetchGeoOverview()
  },
  methods: {
    ...mapActions({
      getGeoOverview: "customers/getGeoOverview",
    }),

    async fetchGeoOverview() {
      this.loadingGeoOverview = true
      await this.getGeoOverview()
      this.loadingGeoOverview = false
    },

    showMapView() {
    },

    showListView() {
    }
  },
}
</script>
<style lang="scss" scoped>
.playground-wrap {
  background: white;
  .attribute-div {
    border-right: 1px solid var(--v-black-lighten3);
    height: 100vh;
  }
}
</style>
