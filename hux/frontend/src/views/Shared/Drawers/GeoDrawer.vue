<template>
  <drawer v-model="localToggle" content-padding="pa-0">
    <template #header-left>
      <div class="d-flex align-center">
        <icon :type="title.icon" :size="32" class="mr-2" />
        <h3 class="text-h2">
          {{ title.name }}
          <sup>
            <tooltip v-if="title.toolTipText" position-top>
              <template #label-content>
                <icon
                  v-if="title.toolTipText"
                  type="info"
                  :size="8"
                  color="primary"
                  variant="base"
                  class="mb-1"
                />
              </template>
              <template #hover-content>
                {{ title.toolTipText }}
              </template>
            </tooltip>
          </sup>
        </h3>
      </div>
    </template>

    <template #loading>
      <v-progress-linear :active="loading" :indeterminate="loading" />
    </template>

    <template #default>
      <hux-data-table
        v-if="!loading"
        :columns="columns"
        :data-items="items"
        :sort-column="sortColumn"
        :data-e2e="`geo-drawer-table-${geoLevel}`"
      >
        <template #row-item="{ item }">
          <td v-for="(col, index) in columns" :key="index" class="text-body-1">
            <tooltip v-if="['city', 'country', 'state'].includes(col.value)">
              {{ item[col.value] }}
              <template #tooltip> {{ item[col.value] }} </template>
            </tooltip>
            <tooltip v-if="col.value === 'size'">
              {{ item[col.value] | Numeric(false, true) }}
              <template #tooltip>
                {{ item[col.value] | Numeric(true) }}
              </template>
            </tooltip>
            <tooltip v-if="col.value === 'revenue'">
              {{ item[col.value] | Currency }}
              <template #tooltip>
                {{ item[col.value] | Currency }}
              </template>
            </tooltip>
            <span v-if="col.value === 'id'">
              {{ item[col.value] }}
            </span>
          </td>
        </template>
      </hux-data-table>
      <v-progress-linear v-if="enableLazyLoad" active indeterminate />
      <observer v-if="items && items.length" @intersect="onLazyLoad" />
    </template>

    <template #footer-left>
      <span class="black--text text--darken-1 text-body-2">
        {{ results | Numeric }} results
      </span>
    </template>
  </drawer>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import Drawer from "@/components/common/Drawer.vue"
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import Observer from "@/components/common/Observer.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import { arrayHasFieldWithMultipleValues } from "@/utils"
import Icon from "@/components/common/Icon.vue"

export default {
  name: "GeoDrawer",

  components: {
    Drawer,
    HuxDataTable,
    Observer,
    Tooltip,
    Icon,
  },

  props: {
    toggle: {
      type: Boolean,
      required: false,
      default: false,
    },

    geoLevel: {
      type: String,
      required: false,
      default: "states",
    },

    results: {
      type: Number,
      required: false,
      default: 0,
    },

    audienceId: {
      required: false,
      default: null,
    },
  },

  data() {
    return {
      localToggle: false,
      loading: false,
      enableLazyLoad: false,
      batchSize: 100,
      batchNumber: 1,
      columns: [],
      defaultColumns: [
        {
          value: "size",
          text: "Size",
        },
        {
          value: "revenue",
          text: "Revenue",
        },
      ],
      sortColumn: "state",
    }
  },

  computed: {
    ...mapGetters({
      customersGeoCities: "customers/geoCities",
      customersGeoCountries: "customers/geoCountries",
      customersGeoStates: "customers/geoStates",
      audienceGeoCities: "audiences/geoCities",
      audienceGeoCountries: "audiences/geoCountries",
      audienceGeoStates: "audiences/geoStates",
    }),

    geoCities() {
      if (this.audienceId) return this.audienceGeoCities
      else return this.customersGeoCities
    },

    geoStates() {
      if (this.audienceId) return this.audienceGeoStates
      else return this.customersGeoStates
    },

    geoCountries() {
      if (this.audienceId) return this.audienceGeoCountries
      else return this.customersGeoCountries
    },

    items() {
      switch (this.geoLevel) {
        case "cities":
          return this.geoCities
        case "states":
          return this.geoStates
        case "countries":
          return this.geoCountries
        default:
          return this.geoStates
      }
    },

    lastBatch() {
      return Math.ceil(this.results / this.batchSize) || 1
    },

    title() {
      return {
        countries: { name: "Countries", icon: "country" },
        states: {
          name: "States",
          icon: "state",
          toolTipText:
            "US states or regions equivalent to US state-level , eg. counties, districts, departments, divisions, parishes, provinces etc.",
        },
        cities: { name: "Cities", icon: "city" },
      }[this.geoLevel]
    },
  },

  watch: {
    toggle(value) {
      this.localToggle = value
    },

    localToggle(value) {
      this.$emit("onToggle", value)
    },
  },

  async updated() {
    if (this.toggle) {
      this.loading = true
      this.batchNumber = 1
      try {
        await this.refreshData()
        switch (this.geoLevel) {
          case "cities":
            this.columns = [
              {
                value: "city",
                text: "City",
              },
              {
                value: "state",
                text: "State",
                hoverTooltip:
                  "US states or regions equivalent to US state-level , eg. counties, districts, departments, divisions, parishes, provinces etc.",
              },
              ...this.defaultColumns,
            ]
            if (arrayHasFieldWithMultipleValues(this.geoCities, "country")) {
              this.columns.splice(2, 0, {
                value: "country",
                text: "Country",
              })
            }
            this.sortColumn = "city"
            break
          case "countries":
            this.columns = [
              {
                value: "country",
                text: "Country",
              },
              ...this.defaultColumns,
            ]
            this.sortColumn = "country"
            break
          case "states":
            this.columns = [
              {
                value: "state",
                text: "State",
              },
              ...this.defaultColumns,
            ]
            if (arrayHasFieldWithMultipleValues(this.geoStates, "country")) {
              this.columns.splice(1, 0, {
                value: "country",
                text: "Country",
              })
            }
            this.sortColumn = "state"
            break
        }
      } catch (error) {
        this.enableLazyLoad = false
      } finally {
        this.loading = false
        this.enableLazyLoad = true
      }
    } else {
      this.enableLazyLoad = false
    }
  },

  methods: {
    ...mapActions({
      getCustomersGeoCities: "customers/getGeoCities",
      getCustomersGeoCountries: "customers/getGeoCountries",
      getCustomersGeoStates: "customers/getGeoStates",
      getAudienceGeoCities: "audiences/getGeoCities",
      getAudienceGeoCountries: "audiences/getGeoCountries",
      getAudienceGeoStates: "audiences/getGeoStates",
    }),

    async onLazyLoad() {
      if (this.lastBatch > 1 && this.batchNumber <= this.lastBatch) {
        this.batchNumber++
        try {
          await this.refreshData()
        } catch (error) {
          this.enableLazyLoad = false
        }
      } else {
        this.enableLazyLoad = false
      }
    },

    async getGeoCities() {
      if (this.audienceId)
        await this.getAudienceGeoCities({
          id: this.audienceId,
          batchNumber: this.batchNumber,
          batchSize: this.batchSize,
        })
      else
        await this.getCustomersGeoCities({
          batchNumber: this.batchNumber,
          batchSize: this.batchSize,
        })
    },

    async getGeoCountries() {
      if (this.audienceId) await this.getAudienceGeoCountries(this.audienceId)
      else await this.getCustomersGeoCountries()
    },

    async getGeoStates() {
      if (this.audienceId) await this.getAudienceGeoStates(this.audienceId)
      else await this.getCustomersGeoStates()
    },

    async refreshData() {
      switch (this.geoLevel) {
        case "cities":
          await this.getGeoCities()
          break
        case "countries":
          await this.getGeoCountries()
          break
        case "states":
          await this.getGeoStates()
          break
      }
    },
  },
}
</script>
<style lang="scss" scoped>
.hux-data-table {
  ::v-deep table {
    table-layout: auto !important;
  }
}
</style>
