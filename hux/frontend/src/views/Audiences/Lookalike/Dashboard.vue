<template>
  <div class="audience-lookalike-insight">
    <div class="mb-7 text-body-1">
      This is a lookalike audience of
      <span v-if="audienceData.source_exists === false">
        <router-link
          :to="{
            name: 'AudienceInsight',
            params: { id: audienceData.source_id },
          }"
          class="
            text-body-1
            primary--text
            text--base
            view-all
            text-decoration-none
          "
        >
          {{ audienceData.source_name }}
        </router-link>
      </span>
      <span v-else class="'black--text text--base'">
        {{ audienceData.source_name }}
      </span>
      (the seed audience). The customer list of this lookalike resides in the
      destination itself, not in the Hux interface.
    </div>
    <v-row>
      <v-col cols="7">
        <v-card class="overview-card pt-5 pb-6 pl-6 pr-6 box-shadow-5">
          <v-card-title class="d-flex justify-space-between pa-0 pr-2">
            <h3 class="text-h3 mb-2">Audience overview</h3>
          </v-card-title>
          <div class="mt-1">
            <v-row class="metric-row">
              <v-col cols="3">
                <metric-card
                  title="Destination"
                  :height="75"
                  :interactable="false"
                >
                  <template #subtitle-extended>
                    <div
                      class="
                        mt-1
                        caption
                        black--text
                        text--darken-4
                        font-weight-semi-bold
                      "
                    >
                      <logo type="facebook" :size="24"></logo>
                    </div>
                  </template>
                </metric-card>
              </v-col>
              <v-col cols="3" class="ml-n3">
                <metric-card title="Reach" :height="75" :interactable="false">
                  <template #subtitle-extended>
                    <div
                      class="
                        mt-1
                        caption
                        black--text
                        text--darken-4
                        font-weight-semi-bold
                      "
                    >
                      -
                    </div>
                  </template>
                </metric-card>
              </v-col>
              <v-col cols="3" class="ml-n3">
                <metric-card
                  title="Lookalike size"
                  :height="75"
                  title-tooltip="The number of people in the lookalike audience in the destination platform."
                  :interactable="false"
                >
                  <template #subtitle-extended>
                    <div
                      class="
                        mt-1
                        caption
                        black--text
                        text--darken-4
                        font-weight-semi-bold
                      "
                    >
                      -
                    </div>
                  </template>
                </metric-card>
              </v-col>
              <v-col cols="3" class="ml-n3">
                <metric-card title="Created" :height="75" :interactable="false">
                  <template #subtitle-extended>
                    <div
                      class="
                        mt-1
                        caption
                        black--text
                        text--darken-4
                        font-weight-semi-bold
                      "
                    >
                      {{
                        audienceData.create_time | Date("MM/DD/YY [•] h:mm A")
                      }}
                    </div>
                  </template>
                </metric-card>
              </v-col>
            </v-row>
          </div>
        </v-card>
        <div>
          <lookalike-engagement :headers="columnDefs" :sections="relatedEngagements" />
        </div>
      </v-col>
      <v-col cols="5">
        <v-card class="overview-card pt-5 pb-6 pl-6 pr-6 box-shadow-5">
          <v-card-title class="d-flex justify-space-between pa-0 pr-2">
            <h3 class="text-h3 mb-2">Seed audience overview</h3>
          </v-card-title>
          <div class="mt-1 mb-5">
            <metric-card
              title="Seed audience"
              :height="75"
              :interactable="false"
            >
              <template #subtitle-extended>
                <div class="mt-1">
                  <router-link
                    :to="{
                      name: 'AudienceInsight',
                      params: { id: audienceData.source_id },
                    }"
                    class="
                      text-body-1
                      primary--text
                      text--base
                      font-weight-semi-bold
                      text-decoration-none
                    "
                  >
                    {{ audienceData.source_name | Empty("-") }}
                  </router-link>
                </div>
              </template>
            </metric-card>
          </div>
          <div class="mt-1 mb-5">
            <v-row>
              <v-col cols="7">
                <metric-card
                  title="Seed audience size"
                  :height="75"
                  title-tooltip="The size of original audience this lookalike was created from."
                  :interactable="false"
                >
                  <template #subtitle-extended>
                    <div
                      class="
                        mt-1
                        caption
                        black--text
                        text--darken-4
                        font-weight-semi-bold
                      "
                    >
                      {{
                        audienceData.source_size
                          | Numeric(false, false, true)
                          | Empty("-")
                      }}
                    </div>
                  </template>
                </metric-card>
              </v-col>
              <v-col cols="5" class="ml-n2">
                <metric-card
                  title="Match rate"
                  :height="75"
                  :interactable="false"
                >
                  <template #subtitle-extended>
                    <div
                      class="
                        mt-1
                        caption
                        black--text
                        text--darken-4
                        font-weight-semi-bold
                      "
                    >
                      {{
                        audienceData.match_rate
                          | Numeric(true, false, false, true)
                          | Empty("-")
                      }}
                    </div>
                  </template>
                </metric-card>
              </v-col>
            </v-row>
          </div>
          <div class="mb-1">
            <metric-card
              v-if="Object.keys(appliedFilters).length > 0"
              :title="'Attributes'"
              :height="104"
              :interactable="false"
              class="mt-1"
            >
              <template #extra-item>
                <div class="container pl-0 pt-2 mt-1">
                  <ul class="filter-list">
                    <li
                      v-for="(filterKey, filterIndex) in Object.keys(
                        appliedFilters
                      )"
                      :key="filterKey"
                      class="filter-item ma-0 mr-1 d-flex align-center"
                    >
                      <tooltip
                        v-for="filter in Object.keys(appliedFilters[filterKey])"
                        :key="filter"
                      >
                        <template #label-content>
                          <v-chip
                            v-if="filterIndex < 4"
                            small
                            class="mr-1 ml-0 mt-0 mb-1 text-subtitle-2"
                            text-color="primary"
                            color="var(--v-primary-lighten3)"
                          >
                            {{ appliedFilters[filterKey][filter].name }}
                          </v-chip>
                        </template>
                        <template #hover-content>
                          <span
                            class="text-body-2 black--text text--darken-4"
                            v-html="appliedFilters[filterKey][filter].hover"
                          >
                          </span>
                        </template>
                      </tooltip>
                    </li>
                  </ul>
                </div>
              </template>
            </metric-card>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"

import Breadcrumb from "@/components/common/Breadcrumb.vue"
import MetricCard from "@/components/common/MetricCard.vue"
import DashboardHeader from "@/views/Audiences/Dashboard/Header.vue"
import Delivery from "@/views/Audiences/Dashboard/Delivery.vue"
import Logo from "@/components/common/Logo"
import TimeStamp from "@/components/common/huxTable/TimeStamp.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import LookalikeEngagement from "@/views/Audiences/Lookalike/LookalikeEngagement.vue"

export default {
  name: "AudienceLookalikeDashboard",
  components: {
    Breadcrumb,
    MetricCard,
    Logo,
    DashboardHeader,
    Delivery,
    TimeStamp,
    Tooltip,
    LookalikeEngagement,
  },
  props: {
    audienceData: {
      type: Object,
      required: false,
    },
    appliedFilters: {
      type: Array,
      required: false,
      default: () => [],
    },
    relatedEngagements: {
      type: Array,
      required: false,
      default: () => [],
    },
  },
  data() {
    return {
      columnDefs: [
        {
          text: "Engagement name",
          value: "name",
        },
        {
          text: "Status",
          value: "status",
        },
        {
          text: "Created",
          value: "created",
        },
      ],
    }
  },
  computed: {},
}
</script>
<style lang="scss" scoped>
.audience-lookalike-insight {
  .overview-card {
    border-radius: 12px !important;
  }
  .filter-list {
    padding-left: 0px !important;
  }
  .metric-row {
    margin-right: -46px !important;
  }
}
</style>
