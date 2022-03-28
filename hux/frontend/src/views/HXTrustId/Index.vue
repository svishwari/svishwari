<template>
  <page max-width="100%" class="hx-trust-id-wrapper">
    <template #header>
      <page-header
        class="page-header py-5"
        header-min-height="110"
        header-max-height="120"
      >
        <template #left>
          <div>
            <breadcrumb
              :items="[
                {
                  text: 'HX TrustID',
                  disabled: true,
                  href: '/hx-trustid',
                  icon: 'hx-trustid-colored',
                  iconSize: 36,
                  iconColor: 'black',
                  iconColorVariant: 'base',
                },
              ]"
            />
          </div>
          <div class="text-subtitle-1 font-weight-regular pt-0 pl-0">
            Measure the signals of trust, predict how trust sentiment will
            impact customer &nbsp; employee behaviors, and identify actions to
            (re)build trust.
          </div>
        </template>
      </page-header>
      <v-progress-linear :active="loading" :indeterminate="loading" />
    </template>
    <template>
      <div class="d-flex">
        <div
          class="flex-grow-1 flex-shrink-1 overflow-auto mw-100 content-section"
        >
          <overview v-if="!loading" :data="overviewData" />
          <v-tabs v-model="tabOption" class="mt-8">
            <v-tabs-slider color="primary" class="tab-slider"></v-tabs-slider>
            <div class="d-flex">
              <v-tab
                key="comparison"
                class="pa-2 mr-3 text-h3"
                color
                data-e2e="comparison-tab"
              >
                Comparison
              </v-tab>
              <v-tab key="attributes" class="text-h3" data-e2e="attributes-tab">
                Attributes
              </v-tab>
            </div>
          </v-tabs>
          <v-tabs-items v-model="tabOption" class="mt-2 tabs-item">
            <v-tab-item key="comparison" class="tab-item">
              <v-row>
                <v-col md="12">
                  <v-card
                    class="mt-3 rounded-lg box-shadow-5 tab-card-1"
                    height="365"
                  >
                    <v-progress-linear
                      v-if="segmentComparisonLoading"
                      :active="segmentComparisonLoading"
                      :indeterminate="segmentComparisonLoading"
                    />
                    <v-card-title class="pb-2 pl-6 pt-5">
                      <span class="d-flex">
                        <h3 class="text-h3">
                          HX TrustID scores across segments
                        </h3>
                      </span>
                    </v-card-title>
                    <trust-comparison-chart
                      v-if="!segmentComparisonLoading"
                      :segment-scores="segmentScores"
                      data-e2e="trust-comparison-chart"
                    />
                  </v-card>
                </v-col>
              </v-row>
            </v-tab-item>
            <v-tab-item key="attributes" class="tab-item">
              <trust-id-attributes :data="attributeData"> </trust-id-attributes>
            </v-tab-item>
          </v-tabs-items>
        </div>
        <div class="ml-auto segment-drawer">
          <add-segment-drawer
            ref="filters"
            v-model="isFilterToggled"
            view-height="calc(100vh - 180px)"
            :segment-data="addSegmentData"
            :segment-length="segmentLength"
            @onSectionAction="addSegment"
          />
        </div>
      </div>
      <link-dropdown
        :data-list="getSegment"
        :width="245"
        @onselect="getSelectedData"
      ></link-dropdown>
      <div>
        <v-list class="add-segment no-data-width" :height="22">
          <v-list-item @click="filterToggle()">
            <hux-icon
              type="plus"
              :size="16"
              color="primary"
              class="mr-4 ml-2"
            />
            <v-btn
              text
              min-width="7rem"
              height="2rem"
              class="primary--text text-body-1"
            >
              New segment to compare
            </v-btn>
          </v-list-item>
        </v-list>
      </div>
    </template>
  </page>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import Overview from "./Overview.vue"
import Breadcrumb from "@/components/common/Breadcrumb.vue"
import LinkDropdown from "@/components/common/LinkDropdown.vue"
import Page from "@/components/Page.vue"
import PageHeader from "@/components/PageHeader.vue"
import TrustComparisonChart from "@/components/common/TrustIDComparisonChart/TrustComparisonChart"
import TrustIdAttributes from "./AttributeTable.vue"
import HuxIcon from "@/components/common/Icon.vue"
import AddSegmentDrawer from "@/views/HXTrustId/Drawers/AddSegmentDrawer.vue"
import addSegmentData from "@/api/mock/fixtures/addSegmentData.js"
import segmentScores from "@/api/mock/fixtures/segmentComparisonScores.js"
import overviewData from "@/api/mock/fixtures/trustIdOverview.js"

export default {
  name: "HXTrustID",
  components: {
    Overview,
    Breadcrumb,
    LinkDropdown,
    Page,
    PageHeader,
    TrustComparisonChart,
    TrustIdAttributes,
    HuxIcon,
    AddSegmentDrawer,
  },
  data() {
    return {
      loading: false,
      segmentComparisonLoading: false,
      tabOption: 0,
      selectedSegment: null,
      isFilterToggled: false,
      segmentLength: 1,
      addSegmentData: addSegmentData,
      segmentScores: segmentScores,
      overviewData: overviewData,
      attributeData: [
        {
          attribute_name: "humanity",
          attribute_score: 71,
          attribute_description:
            "Humanity is demonstrating empathy and kindness towards customers, and treating everyone fairly. It is scored on a scale between -100 to 100",
          overall_customer_rating: {
            total_customers: 190909,
            rating: {
              agree: { percentage: 0.25, count: 156545 },
              neutral: { percentage: 0.35, count: 13363 },
              disagree: { percentage: 0.4, count: 21001 },
            },
          },
        },
        {
          attribute_name: "transparency",
          attribute_score: 71,
          attribute_description:
            "Transparency is openly sharing all information, motives, and choices in straightforward and plain language. It is scored on a scale between -100 to 100",
          overall_customer_rating: {
            total_customers: 190909,
            rating: {
              agree: { percentage: 0.3, count: 156545 },
              neutral: { percentage: 0.28, count: 13363 },
              disagree: { percentage: 0.48, count: 21001 },
            },
          },
        },
        {
          attribute_name: "capability",
          attribute_score: 78,
          attribute_description:
            "Capability is creating quality products, services, and/or experiences. It is scored on a scale between -100 to 100",
          overall_customer_rating: {
            total_customers: 190909,
            rating: {
              agree: { percentage: 20, count: 168000 },
              neutral: { percentage: 28, count: 3818 },
              disagree: { percentage: 52, count: 19091 },
            },
          },
        },
        {
          attribute_name: "reliability",
          attribute_score: 71,
          attribute_description:
            "Reliability is consistently and dependably delivering on promises. It is scored on a scale between -100 to 100",
          overall_customer_rating: {
            total_customers: 190909,
            rating: {
              agree: { percentage: 0.3, count: 156545 },
              neutral: { percentage: 0.38, count: 13363 },
              disagree: { percentage: 0.32, count: 21001 },
            },
          },
        },
      ],
    }
  },
  computed: {
    ...mapGetters({
      // TODO: enable this once API endpoint available
      // segmentScores: "trustId/getSegmentsComparison",
      // overviewData: "trustId/getTrustOverview",
    }),
    getSegment() {
      return this.segmentScores.map((item) => {
        return item.segment_filter
      })
    },
  },
  async mounted() {
    this.loading = true
    this.segmentComparisonLoading = true
    try {
      await this.getOverview()
      await this.getTrustIdComparison()
    } finally {
      this.loading = false
      this.segmentComparisonLoading = false
    }
  },
  methods: {
    ...mapActions({
      getOverview: "trustId/getTrustIdOverview",
      getTrustIdComparison: "trustId/getTrustIdComparison",
    }),
    getSelectedData(value) {
      this.selectedSegment = value
    },
    filterToggle() {
      this.isFilterToggled = !this.isFilterToggled
    },
    addSegment() {
      this.isFilterToggled = !this.isFilterToggled
    },
  },
}
</script>

<style lang="scss" scoped>
.v-application {
  .hx-trust-id-wrapper {
    ::v-deep .v-breadcrumbs {
      li {
        font-family: Open Sans Light;
        font-size: 28px;
        font-style: normal;
        font-weight: 400 !important;
        line-height: 40px;
        letter-spacing: 0px;
        text-align: left;
      }
    }
    ::v-deep .theme--light.v-tabs {
      .v-tabs-bar .v-tab:not(.v-tab--active) {
        color: var(--v-black-lighten4) !important;
      }
    }
    .tab-slider {
      position: absolute;
      top: 2px;
    }
  }
}
.add-segment {
  height: 60px !important;
  display: inline-table;
  background: var(--v-white-base);
  border: 1px solid var(--v-black-lighten2);
  border-radius: 5px;
}
.no-data-width {
  width: 100%;
}
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
.content-section {
  height: calc(100vh - 200px);
  overflow-y: auto !important;
  overflow-x: hidden !important;
}
.segment-drawer {
  margin-top: -30px;
  margin-right: -30px;
}
::v-deep .hux-filters-drawer {
  width: 320px !important;
}
::v-deep .header-height-fix {
  height: 70px !important;
}
::v-deep .wrapper {
  width: 320px !important;
}
</style>
