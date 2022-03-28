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
    <div>
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
                    <h3 class="text-h3">HX TrustID scores across segments</h3>
                  </span>
                </v-card-title>
                <trust-comparison-chart
                  v-if="!segmentComparisonLoading"
                  :segment-scores="segmentScores"
                  data-e2e="trust-comparison-chart"
                />
                <link-dropdown
                  v-if="!segmentComparisonLoading"
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
                        !['segment_name', 'attribute_filters'].includes(
                          header.key
                        )
                      "
                      :key="header.key"
                      :value="row.value"
                      :text-color="
                        row.value < 0 ? 'error--text' : 'black--text'
                      "
                    ></rhombus-number>

                    <span
                      v-else-if="header.key == 'attribute_filters'"
                      :key="header.key"
                    >
                      <span v-if="row.value.length != 0">
                        <v-chip
                          v-for="(filter, filterIndex) in row.value"
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
                    <div class="d-flex align-center justify-end mr-2">
                      <icon
                        type="trash"
                        class="cursor-pointer"
                        :size="18"
                        color="black"
                        @click.native="removeAudience(row.item)"
                      />
                    </div>
                  </template>
                </data-cards>
              </v-card>
            </v-col>
          </v-row>
        </v-tab-item>
        <v-tab-item key="attributes" class="tab-item"> </v-tab-item>
      </v-tabs-items>
    </div>
  </page>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import Breadcrumb from "@/components/common/Breadcrumb.vue"
import LinkDropdown from "@/components/common/LinkDropdown.vue"
import Page from "@/components/Page.vue"
import PageHeader from "@/components/PageHeader.vue"
import segmentScores from "@/api/mock/fixtures/segmentComparisonScores.js"
import TrustComparisonChart from "@/components/common/TrustIDComparisonChart/TrustComparisonChart"
import DataCards from "@/components/common/DataCards.vue"
import { formatText } from "@/utils"
import RhombusNumber from "@/components/common/RhombusNumber.vue"
import Icon from "@/components/common/Icon.vue"

export default {
  name: "HXTrustID",
  components: {
    Breadcrumb,
    LinkDropdown,
    Page,
    PageHeader,
    TrustComparisonChart,
    DataCards,
    RhombusNumber,
    Icon,
  },
  data() {
    return {
      loading: false,
      segmentComparisonLoading: false,
      tabOption: 0,
      selectedSegment: null,
      segmentScores: segmentScores,
    }
  },
  computed: {
    ...mapGetters({
      // TODO: enable this once API endpoint available
      // segmentScores: "trustId/getSegmentsComparison",
    }),
    getSegment() {
      return this.segmentScores.map((item) => {
        return item.segment_filter
      })
    },
    getSegmentTableData() {
      return this.segmentScores[0].segments.map((x) => {
        let segment = {
          segment_name: x.segment_name,
          attribute_filters: x.attribute_filters,
        }

        x.attributes.forEach((item) => {
          segment[item.attribute_type] = item.attribute_score
        })
        return segment
      })
    },
    getSegmentTableHeaders() {
      let headers = Object.keys(this.getSegmentTableData[0]).map((item) => {
        return {
          key: item,
          label: formatText(item),
        }
      })

      headers.push({
        key: "delete",
      })

      return headers
    },
  },
  async mounted() {
    this.segmentComparisonLoading = true
    try {
      await this.getTrustIdComparison()
    } finally {
      this.segmentComparisonLoading = false
    }
  },
  methods: {
    ...mapActions({
      getTrustIdComparison: "trustId/getTrustIdComparison",
    }),
    getSelectedData(value) {
      this.selectedSegment = value
    },
    formatText: formatText,
  },
}
</script>

<style lang="scss" scoped>
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

  .overview-card {
    border-radius: 12px !important;
  }
}
</style>
