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
      <template #right> <tips-menu /></template>
    </page-header>
    <div>
      <v-row>
        <v-col class="col-8 attribute-div"></v-col>
        <v-col class="col-4 overview-div pr-6">
          <v-card
            class="map-card-wrapper mt-3 rounded-lg card-shadow"
            height="311"
          >
          </v-card>
          <v-card
            class="map-card-wrapper mt-3 rounded-lg card-shadow"
            height="311"
          >
            <div class="d-flex justify-space-between">
              <h5 class="text-h3 mt-2">USA</h5>
              <div>
                <v-btn text small min-width="30" @click="showMapView = true">
                  <icon type="world" color="primary" :size="32" class="mr-1" />
                </v-btn>
                <v-btn text small min-width="30" @click="showMapView = false">
                  <icon type="list" color="primary" :size="32" class="mr-1" />
                </v-btn>
              </div>
            </div>

            <v-progress-linear
              v-if="loadingOverview"
              :active="loadingOverview"
              :indeterminate="loadingOverview"
            />
            <map-chart
              v-if="!loadingOverview"
              :map-data="overview.geo"
              :configuration-data="configurationData"
              :disable-hover-effects="true"
              data-e2e="map-chart"
            />
            <map-slider
              v-if="!loadingOverview"
              :map-data="overview.geo"
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
import TipsMenu from "./TipsMenu"
import MapChart from "@/components/common/MapChart/MapChart"
import mapSlider from "@/components/common/MapChart/mapSlider"
import Icon from "@/components/common/Icon"
import configurationData from "@/components/common/MapChart/MapConfiguration.json"

export default {
  name: "SegmentPlayground",
  components: {
    PageHeader,
    Breadcrumb,
    TipsMenu,
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
      loadingOverview: false,
      showMapView: true,
      configurationData: configurationData,
    }
  },
  computed: {
    ...mapGetters({
      overview: "customers/overview",
    }),
  },

  async mounted() {
    this.loadingOverview = true
    await this.getOverview()
    this.loadingOverview = false
  },

  methods: {
    ...mapActions({
      getOverview: "customers/getOverview",
    }),
  },
}
</script>
<style lang="scss" scoped>
.playground-wrap {
  background: var(--v-white-base) !important;
  .attribute-div {
    border-right: 1px solid var(--v-black-lighten3);
    height: 100vh;
  }
  .overview-div {
    .map-card-wrapper {
      border: 1px solid var(--v-black-lighten2);
      padding: 20px 15px;
      ::v-deep .map-chart {
        svg {
          height: 230px;
        }
      }
      ::v-deep .hux-map-slider {
        margin-top: -30px;
      }
    }
  }
}
</style>
