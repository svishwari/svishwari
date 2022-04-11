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
                  superscript: 'TM',
                  disabled: true,
                  href: '/hx-trustid',
                  icon: 'hx-trustid-header',
                  iconSize: 36,
                  iconColor: 'black',
                  iconColorVariant: 'base',
                },
              ]"
            />
          </div>
          <div class="text-subtitle-1 font-weight-regular pt-0 pl-0">
            Measure the signals of trust, predict how trust sentiment will
            impact customer &amp; employee behaviors, and identify actions to
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
          <overview v-if="!loading" :data="trustIdOverview" />
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
              <link-dropdown
                :data-list="getSegment"
                :width="245"
                @onselect="getSelectedData"
              ></link-dropdown>
              <data-cards
                bordered
                class="mr-4"
                card-class="py-5 pa-4"
                :items="getSegmentTableData"
                :fields="getSegmentTableHeaders"
              >
                <template
                  v-for="header in getSegmentTableHeaders"
                  #[`field:${header.key}`]="row"
                >
                  <rhombus-number
                    v-if="
                      !['segment_name', 'attribute_filters', 'colors'].includes(
                        header.key
                      )
                    "
                    :key="header.key"
                    :value="row.value"
                    :text-color="row.value < 0 ? 'error--text' : 'black--text'"
                    :border-image="header.key == 'trust_id'"
                    :color="
                      colColorArr[header.key] && colColorArr[header.key].stroke
                    "
                    :variant="
                      colColorArr[header.key] && colColorArr[header.key].variant
                    "
                    class="ml-4"
                  ></rhombus-number>

                  <span
                    v-else-if="header.key == 'attribute_filters'"
                    :key="header.key"
                  >
                    <span v-if="row.value.length != 0">
                      <v-chip
                        v-for="(filter, filterIndex) in Object.keys(
                          row.value[0]
                        )"
                        :key="filterIndex"
                        small
                        class="mr-1 ml-0 mt-0 mb-1 text-subtitle-2"
                        text-color="primary"
                        color="var(--v-primary-lighten3)"
                      >
                        {{ formatText(filter) }}
                      </v-chip>
                    </span>
                    <span v-else>
                      <v-chip
                        small
                        class="mr-1 ml-0 mt-0 mb-1 text-subtitle-2"
                        text-color="primary"
                        color="var(--v-primary-lighten3)"
                      >
                        All customers
                      </v-chip>
                    </span>
                  </span>
                </template>

                <template #field:delete="row">
                  <div
                    v-if="getSelectedSegment.segments.length > 1"
                    class="d-flex align-center justify-end mr-2"
                  >
                    <hux-icon
                      type="trash"
                      class="cursor-pointer"
                      :size="18"
                      color="black"
                      @click.native="removeSegment(row.item)"
                    />
                  </div>
                </template>
              </data-cards>
              <div v-if="getSelectedSegment.segments.length < 5">
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
              <div v-else>
                <v-card class="empty-text">
                  <hux-icon
                    type="critical"
                    :size="21"
                    color="error"
                    class="mr-4 ml-6"
                  />
                  <span
                    class="error--text text-subtitle-1 mr-4"
                    :style="{ fontWeight: 800 }"
                    >OH NO!</span
                  >
                  <span class="text-body-2 error--text"
                    >You’ve reached the limit for the number of comparisons.
                    Remove a comparison to add a new one.
                  </span>
                </v-card>
              </div>
            </v-tab-item>
            <v-tab-item key="attributes" class="tab-item">
              <trust-id-attributes :data="overviewData.attributes" />
            </v-tab-item>
          </v-tabs-items>
        </div>
        <div class="ml-auto segment-drawer">
          <add-segment-drawer
            ref="filters"
            v-model="isFilterToggled"
            view-height="calc(100vh - 180px)"
            :segment-data="addSegmentData"
            :segment-length="segmentScores.length"
            @onSectionAction="addSegment($event)"
          />
        </div>
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
import DataCards from "@/components/common/DataCards.vue"
import { formatText } from "@/utils"
import RhombusNumber from "@/components/common/RhombusNumber.vue"
import TrustIdAttributes from "./AttributeTable.vue"
import HuxIcon from "@/components/common/Icon.vue"
import AddSegmentDrawer from "@/views/HXTrustId/Drawers/AddSegmentDrawer.vue"
// TODO: will romve after checking in dev
// import addSegmentData from "@/api/mock/fixtures/addSegmentData.js"
import overviewData from "@/api/mock/fixtures/trustIdAttribute.js"
import segmentComparisonScores from "@/api/mock/fixtures/segmentComparisonScores.js"

export default {
  name: "HXTrustID",
  components: {
    Overview,
    Breadcrumb,
    LinkDropdown,
    Page,
    PageHeader,
    TrustComparisonChart,
    DataCards,
    RhombusNumber,
    TrustIdAttributes,
    HuxIcon,
    AddSegmentDrawer,
  },
  data() {
    return {
      loading: false,
      segmentComparisonLoading: false,
      tabOption: 0,
      selectedSegment: "composite & signal scores",
      isFilterToggled: false,
      segmentLength: 1,
      addSegments: [],
      overviewData: overviewData,
      segmentScores: segmentComparisonScores,
      borderColorArr: [
        {
          color: "primary",
          variant: "darken1",
        },
        {
          color: "primary",
          variant: "lighten4",
        },
        {
          color: "primary",
          variant: "lighten6",
        },
        {
          color: "info",
          variant: "base",
        },
        {
          color: "secondary",
          variant: "darken1",
        },
      ],
      colColorArr: {
        // Humanity
        humanity: { stroke: "primary", variant: "darken6" },
        quickly_resolves_issues: { stroke: "primary", variant: "darken6" },
        values_respects_everyone: { stroke: "primary", variant: "darken6" },
        values_society_environment: { stroke: "primary", variant: "darken6" },
        takes_care_of_employees: { stroke: "primary", variant: "darken6" },

        // Transparency
        transparency: { stroke: "yellow", variant: "darken1" },
        honesty_marketing_comms: { stroke: "yellow", variant: "darken1" },
        upfront_on_how_they_make_money: {
          stroke: "yellow",
          variant: "darken1",
        },
        plain_language_data_policy: { stroke: "yellow", variant: "darken1" },
        clear_fees_costs: { stroke: "yellow", variant: "darken1" },

        // Reliability
        reliability: { stroke: "secondary", variant: "lighten2" },
        continuous_product_improvement: {
          stroke: "secondary",
          variant: "lighten2",
        },
        consistent_quality: { stroke: "secondary", variant: "lighten2" },
        smooth_digital_interactions: {
          stroke: "secondary",
          variant: "lighten2",
        },
        timely_issue_resolution: { stroke: "secondary", variant: "lighten2" },

        //Capability
        capability: { stroke: "primary", variant: "darken5" },
        product_quality: { stroke: "primary", variant: "darken5" },
        good_value: { stroke: "primary", variant: "darken5" },
        competent_leaders_employess: { stroke: "primary", variant: "darken5" },
        long_term_solutions_improvements: {
          stroke: "primary",
          variant: "darken5",
        },
      },
      tooltips: {
        trust_id: "TrustID is scored on a scale between -100 to 100",
        humanity:
          "Humanity is demonstrating empathy and kindness towards customers, and treating everyone fairly. It is scored on a scale between -100 to 100",
        transparency:
          "Transparency is openly sharing all information, motives, and choices in straightforward and plain language. It is scored on a scale between -100 to 100",
        reliability:
          "Reliability is consistently and dependably delivering on promises. It is scored on a scale between -100 to 100",
        capability:
          "Capability is creating quality products, services, and/or experiences. It is scored on a scale between -100 to 100",
        product_quality:
          "Products are good quality, accessible and safe to use",
        good_value:
          "Prices of products, services, and experiences are good value for money",
        competent_leaders_employess:
          "Employees and leadership are competent and understand how to respond to needs",
        long_term_solutions_improvements:
          "Creates long-term solutions and improvements that work well for me",
        quickly_resolves_issues:
          "Quickly resolves issues with safety, security and satisfaction top of mind",
        values_respects_everyone:
          "Values and respects everyone, regardless of background, identity or beliefs",
        values_society_environment:
          "Values the good of society and the environment, not just profit",
        takes_care_of_employees: "Takes care of employees",
        honesty_marketing_comms:
          "Marketing and communications are accurate and honest",
        upfront_on_how_they_make_money:
          "Upfront about how they make and spend money from interactions",
        plain_language_data_policy:
          "How and why my data is used is communicated in plain and easy to understand language",
        clear_fees_costs:
          "Clear and upfront about fees and costs of products, services and experiences",
        continuous_product_improvement:
          "Can be counted on to improve the quality of products and services",
        consistent_quality:
          "Consistently delivers products, services and experiences with quality",
        smooth_digital_interactions:
          "Facilitates digital interactions that run smoothly and work when needed",
        timely_issue_resolution:
          "Resolves issues in an adequate and timely manner",
      },
    }
  },
  computed: {
    ...mapGetters({
      // segmentScores: "trustId/getSegmentsComparison",
      // TODO: enable this once API endpoint available
      trustIdOverview: "trustId/getTrustOverview",
      addSegmentData: "trustId/getAddSegment",
      attributeData: "trustId/getTrustAttributes",
    }),
    getSegment() {
      return this.segmentScores.map((item) => {
        return item.segment_filter
      })
    },

    getSegmentTableData() {
      return this.getSelectedSegment.segments.map((x, index) => {
        let segment = {
          segment_name: x.segment_name,
          attribute_filters: x.attribute_filters,
        }

        x.attributes.forEach((item) => {
          segment[item.attribute_type] = item.attribute_score
        })

        segment.colors = this.borderColorArr[index]

        return segment
      })
    },

    getSegmentTableHeaders() {
      let headers = [
        {
          key: "segment_name",
          label: "Segment",
          col: 2,
        },
        {
          key: "attribute_filters",
          label: "Segment filters",
          col: 4,
        },
      ]

      this.getSelectedSegment.segments[0].attributes.forEach((item) => {
        headers.push({
          key: item.attribute_type,
          label: item.attribute_name,
          col: 1,
          tooltip: this.tooltips[item.attribute_type],
        })
      })

      headers.push({
        key: "delete",
        col: 1,
      })

      return headers
    },

    getSelectedSegment() {
      return this.segmentScores.find(
        (x) => x.segment_filter == this.selectedSegment?.toLowerCase()
      )
    },
  },
  async mounted() {
    this.loading = true
    this.segmentComparisonLoading = true
    try {
      await this.getOverview()
      //   await this.getTrustIdComparison()
      await this.getSegmentData()
      await this.getTrustIdAttribute()
    } finally {
      this.loading = false
      this.segmentComparisonLoading = false
    }
  },
  methods: {
    ...mapActions({
      getOverview: "trustId/getTrustIdOverview",
      // getTrustIdComparison: "trustId/getTrustIdComparison",
      addNewSegment: "trustId/addSegment",
      getSegmentData: "trustId/getSegmentData",
      getTrustIdAttribute: "trustId/getTrustAttributes",
    }),
    getSelectedData(value) {
      this.selectedSegment = value
    },
    formatText: formatText,
    filterToggle() {
      this.isFilterToggled = !this.isFilterToggled
    },
    async addSegment(event) {
      this.loading = true
      try {
        await this.addNewSegment(event)
      } finally {
        this.loading = false
      }
      this.isFilterToggled = !this.isFilterToggled
      this.$router.go()
    },
    removeSegment(item) {
      this.getSelectedSegment.segments.splice(
        this.getSelectedSegment.segments.findIndex(
          (x) => x.segment_name == item.segment_name
        ),
        1
      )
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
  height: calc(100vh - 240px);
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
.empty-text.empty-text {
  height: 60px;
  align-items: center;
  display: flex;
}
</style>
