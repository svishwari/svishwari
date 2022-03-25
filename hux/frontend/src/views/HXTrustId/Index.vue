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
                  v-if="loading"
                  :active="loading"
                  :indeterminate="loading"
                />
                <v-card-title class="pb-2 pl-6 pt-5">
                  <span class="d-flex">
                    <h3 class="text-h3">HX TrustID scores across segments</h3>
                  </span>
                </v-card-title>
                <trust-comparison-chart
                  :segment-scores="segmentScores"
                  data-e2e="trust-comparison-chart"
                />
              </v-card>
            </v-col>
          </v-row>
        </v-tab-item>
        <v-tab-item key="attributes" class="tab-item">
          <trustID-attributes :data="attributeData"> </trustID-attributes>
        </v-tab-item>
      </v-tabs-items>
    </div>
    <div>
      <link-dropdown
        :data-list="getSegment"
        :width="245"
        @onselect="getSelectedData"
      ></link-dropdown>
    </div>
  </page>
</template>

<script>
import Breadcrumb from "@/components/common/Breadcrumb.vue"
import LinkDropdown from "@/components/common/LinkDropdown.vue"
import Page from "@/components/Page.vue"
import PageHeader from "@/components/PageHeader.vue"
import segmentScores from "@/api/mock/fixtures/segmentComparisonScores.js"
import TrustComparisonChart from "@/components/common/TrustIDComparisonChart/TrustComparisonChart"
import TrustIDAttributes from "./AttributeTable.vue"

export default {
  name: "HXTrustID",
  components: {
    Breadcrumb,
    LinkDropdown,
    Page,
    PageHeader,
    TrustComparisonChart,
    TrustIDAttributes,
  },
  data() {
    return {
      loading: false,
      tabOption: 0,
      segmentScores: segmentScores,
      selectedSegment: null,
      attributeData: [
        {
            "attribute_name": "humanity",
            "attribute_score": 71,
            "attribute_description": "Humanity is demonstrating empathy and kindness towards customers, and treating everyone fairly. It is scored on a scale between -100 to 100",
            "overall_customer_rating":{
                    "total_customers": 190909,
                    "rating":{
                        "agree": {"percentage": 0.25, "count":156545},
                        "neutral": {"percentage": 0.35, "count":13363},
                        "disagree": {"percentage": 0.40, "count":21001},
                    }
            }
        },
        {
            "attribute_name": "transparency",
            "attribute_score": 71,
            "attribute_description": "Transparency is openly sharing all information, motives, and choices in straightforward and plain language. It is scored on a scale between -100 to 100",
            "overall_customer_rating":{
                    "total_customers": 190909,
                    "rating":{                        
                        "agree": {"percentage": 0.30, "count":156545},
                        "neutral": {"percentage": 0.28, "count":13363},
                        "disagree": {"percentage": 0.48, "count":21001},
                    }
            }
        },
        {
            "attribute_name": "capability",
            "attribute_score": 78,
            "attribute_description": "Capability is creating quality products, services, and/or experiences. It is scored on a scale between -100 to 100",
            "overall_customer_rating":{
                    "total_customers": 190909,
                    "rating":{
                        "agree": {"percentage": 20, "count":168000},
                        "neutral": {"percentage": 28, "count":3818},
                        "disagree": {"percentage": 52, "count":19091},
                    }
            }
        },
        {
            "attribute_name": "reliability",
            "attribute_score": 71,
            "attribute_description": "Reliability is consistently and dependably delivering on promises. It is scored on a scale between -100 to 100",
            "overall_customer_rating":{
                    "total_customers": 190909,
                     "rating":{                        
                        "agree": {"percentage": 0.30, "count":156545},
                        "neutral": {"percentage": 0.38, "count":13363},
                        "disagree": {"percentage": 0.32, "count":21001},
                    }
             }
        }
    ]
    }
  },
  computed: {
    getSegment() {
      return this.segmentScores.map((item) => {
        return item.segment_filter
      })
    },
  },
  methods: {
    getSelectedData(value) {
      this.selectedSegment = value
    },
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
