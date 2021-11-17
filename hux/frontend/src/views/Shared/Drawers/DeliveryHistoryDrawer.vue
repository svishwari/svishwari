<template>
  <drawer v-model="localToggle" content-padding="pa-0">
    <template #header-left>
      <div class="d-flex align-center">
        <icon type="clock" :size="32" class="mr-2" />
        <h3 class="text-h3">Delivery history</h3>
      </div>
    </template>

    <template #default>
      <v-progress-linear :active="loading" :indeterminate="loading" />

      <page-header header-height="40">
        <template #left>
          <v-icon
            size="21"
            class="cursor-pointer"
            :class="
              isFilterToggled ? 'primary--text text--darken-2' : 'black--text'
            "
            @click="isFilterToggled = !isFilterToggled"
          >
            mdi-filter-variant
          </v-icon>
        </template>
      </page-header>

      <hux-table-filters-bar
        v-if="!loading"
        v-show="isFilterToggled"
        :filters="filters"
        @onReset="resetFilters"
      />

      <hux-data-table
        v-if="!loading"
        :columns="columns"
        :data-items="items"
        sort-column="delivered"
        sort-desc="false"
        class="delivery-list"
        data-e2e="delivery-list-items"
      >
        <template #row-item="{ item }">
          <td
            v-for="(col, index) in columns"
            :key="index"
            :style="{ width: col.width }"
            class="text-body-1"
          >
            <tooltip>
              <router-link
                v-if="['audience', 'engagement'].includes(col.value)"
                :to="{
                  name:
                    col.value === 'audience'
                      ? 'AudienceInsight'
                      : 'EngagementDashboard',
                  params: { id: item[col.value].id },
                }"
                class="
                  d-inline-block
                  mw-100
                  text-truncate text-decoration-none
                  primary--text
                "
              >
                {{ item[col.value].name }}
              </router-link>
              <template #tooltip>
                {{ item[col.value].name }}
              </template>
            </tooltip>
            <tooltip v-if="col.value === 'destination' && item[col.value]">
              <template #label-content>
                <logo
                  :key="item[col.value].type"
                  :type="item[col.value].type"
                  :size="18"
                  class="mb-0"
                >
                </logo>
              </template>
              <template #hover-content>
                {{ item[col.value].name }}
              </template>
            </tooltip>
            <tooltip v-if="col.value === 'size'">
              <template #label-content>
                {{ item[col.value] | Numeric(true, true) }}
              </template>
              <template #hover-content>
                {{ item[col.value] | Numeric(true) }}
              </template>
            </tooltip>
            <tooltip v-if="col.value === 'match_rate'">
              <template #label-content>
                <span v-if="item[col.value] == null">N/A</span>
                <span v-else>{{ item[col.value] | Percentage }}</span>
              </template>
              <template #hover-content>
                {{ item[col.value] | Percentage }}
              </template>
            </tooltip>
            <tooltip v-if="col.value === 'delivered'">
              <template #label-content>
                <span class="d-inline-block mw-100 text-truncate">
                  {{ item[col.value] | Date("relative") }}
                </span>
              </template>
              <template #hover-content>
                {{ item[col.value] | Date }}
              </template>
            </tooltip>
          </td>
        </template>
      </hux-data-table>
    </template>

    <template #footer-left>
      <span class="black--text text--darken-1 text-caption"
        >{{ items.length }} results</span
      >
    </template>
  </drawer>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import HuxTableFiltersBar from "@/components/common/TableFiltersBar"
import PageHeader from "@/components/PageHeader"
import Drawer from "@/components/common/Drawer.vue"
import Icon from "@/components/common/Icon.vue"
import Logo from "@/components/common/Logo.vue"
import Tooltip from "@/components/common/Tooltip.vue"

import { uniqBy } from "lodash"

export default {
  name: "DeliveryHistoryDrawer",

  components: {
    HuxDataTable,
    HuxTableFiltersBar,
    PageHeader,
    Drawer,
    Icon,
    Logo,
    Tooltip,
  },

  props: {
    audienceId: {
      required: false,
      default: null,
    },

    engagementId: {
      required: false,
      default: null,
    },

    toggle: {
      type: Boolean,
      required: false,
      default: false,
    },
  },

  data() {
    return {
      localToggle: false,
      loading: false,
      isFilterToggled: false,
      filters: [],
      items: [],
      destinationQuery: "",
      audienceQuery: "",
      engagementQuery: "",
      nonCompliantMatchRatePlatforms: [
        "salesforce",
        "sendgrid",
        "qualtrics",
        "sfmc",
      ],
      columns: [
        {
          value: "destination",
          text: "Destination",
          width: "20%",
        },
        {
          value: "size",
          text: "Target size",
          width: "20%",
        },
        {
          value: "match_rate",
          text: "Match Rate",
          width: "20%",
        },
        {
          value: "delivered",
          text: "Delivered",
          width: "20%",
        },
      ],
    }
  },

  computed: {
    ...mapGetters({
      audienceDeliveries: "audiences/deliveries",
      audienceFilteredDeliveries: "audiences/filteredDeliveries",
      engagementDeliveries: "engagements/deliveries",
      engagementFilteredDeliveries: "engagements/filteredDeliveries",
      getDestination: "destinations/single",
    }),

    allDeliveries() {
      if (this.audienceId) return this.audienceDeliveries(this.audienceId)
      else return this.engagementDeliveries(this.engagementId)
    },
  },

  watch: {
    toggle(value) {
      this.localToggle = value
    },

    localToggle(value) {
      this.$emit("onToggle", value)
      if (!value) {
        this.isFilterToggled = value
      }
    },
  },

  async updated() {
    if (this.toggle) {
      await this.fetchHistory()
    }
  },

  mounted() {
    if (this.engagementId !== null)
      this.columns.unshift({
        value: "audience",
        text: "Audience name",
        width: "25%",
      })

    if (this.audienceId !== null)
      this.columns.unshift({
        value: "engagement",
        text: "Engagement name",
        width: "30%",
      })
  },

  methods: {
    ...mapActions({
      getAudienceDeliveries: "audiences/getDeliveries",
      getAudienceFilteredDeliveries: "audiences/getFilteredDeliveries",
      getEngagementDeliveries: "engagements/getDeliveries",
      getEngagementFilteredDeliveries: "engagements/getFilteredDeliveries",
    }),

    resetFilters() {
      this.items = this.allDeliveries
    },

    async fetchHistory() {
      this.loading = true
      try {
        if (this.engagementId) {
          await this.getEngagementDeliveries(this.engagementId)

          let allAudiences = this.allDeliveries.map((each) => each.audience)
          let allDestinations = this.allDeliveries.map(
            (each) => each.destination
          )

          let uniqueAudiences = uniqBy(allAudiences, "id")
          let uniqueDestinations = uniqBy(allDestinations, "id")
          this.filters = [
            {
              name: "Audience name",
              data: uniqueAudiences,
              value: [],
              onSelect: async (value) => {
                let audienceIds = ""
                value.map((each, index) => {
                  if (index !== value.length - 1) {
                    audienceIds += `engagement=${each.id}&`
                  } else {
                    audienceIds += `engagement=${each.id}`
                  }
                })

                this.audienceQuery = audienceIds

                let query = `${audienceIds}${
                  this.destinationQuery !== "" ? "&" : ""
                }${this.destinationQuery}`

                await this.getEngagementFilteredDeliveries({
                  id: this.engagementId,
                  query: query,
                })
                this.items = this.engagementFilteredDeliveries
              },
            },
            {
              name: "Destination",
              data: uniqueDestinations,
              value: [],
              onSelect: async (value) => {
                let destintaionIds = ""
                value.map((each, index) => {
                  if (index !== value.length - 1) {
                    destintaionIds += `destination=${each.id}&`
                  } else {
                    destintaionIds += `destination=${each.id}`
                  }
                })

                this.destinationQuery = destintaionIds

                let query = `${destintaionIds}${
                  this.audienceQuery !== "" ? "&" : ""
                }${this.audienceQuery}`

                await this.getEngagementFilteredDeliveries({
                  id: this.engagementId,
                  query: query,
                })
                this.items = this.engagementFilteredDeliveries
              },
            },
          ]
        }

        if (this.audienceId) {
          await this.getAudienceDeliveries(this.audienceId)
          let allEngagements = this.allDeliveries.map((each) => each.engagement)
          let allDestinations = this.allDeliveries.map(
            (each) => each.destination
          )

          let uniqueEngagements = uniqBy(allEngagements, "id")
          let uniqueDestinations = uniqBy(allDestinations, "id")
          this.filters = [
            {
              name: "Engagement name",
              data: uniqueEngagements,
              value: [],
              onSelect: async (value) => {
                let engagementIds = ""
                value.map((each, index) => {
                  if (index !== value.length - 1) {
                    engagementIds += `engagement=${each.id}&`
                  } else {
                    engagementIds += `engagement=${each.id}`
                  }
                })

                this.engagementQuery = engagementIds

                let query = `${engagementIds}${
                  this.destinationQuery !== "" ? "&" : ""
                }${this.destinationQuery}`

                await this.getAudienceFilteredDeliveries({
                  id: this.audienceId,
                  query: query,
                })
                this.items = this.audienceFilteredDeliveries
              },
            },
            {
              name: "Destination",
              data: uniqueDestinations,
              value: [],
              onSelect: async (value) => {
                let destintaionIds = ""
                value.map((each, index) => {
                  if (index !== value.length - 1) {
                    destintaionIds += `destination=${each.id}&`
                  } else {
                    destintaionIds += `destination=${each.id}`
                  }
                })

                this.destinationQuery = destintaionIds

                let query = `${destintaionIds}${
                  this.engagementQuery !== "" ? "&" : ""
                }${this.engagementQuery}`

                await this.getAudienceFilteredDeliveries({
                  id: this.audienceId,
                  query: query,
                })
                this.items = this.audienceFilteredDeliveries
              },
            },
          ]
        }

        this.items = this.allDeliveries
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
<style lang="scss" scoped>
.hux-data-table {
  ::v-deep .v-data-table__wrapper {
    .v-data-table-header {
      th {
        &:first-child {
          padding: 9px 10px 9px 25px !important;
        }
        padding: 9px 10px !important;
        &:last-child {
          padding: 9px 20px 9px 10px !important;
        }
      }
    }
    tbody {
      tr {
        td {
          &:first-child {
            padding: 9px 10px 9px 25px !important;
          }
          padding: 9px 10px !important;
          &:last-child {
            padding: 9px 20px 9px 10px !important;
          }
        }
      }
    }
  }
}
</style>
