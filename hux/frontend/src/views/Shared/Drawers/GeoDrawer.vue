<template>
  <drawer v-model="localToggle" content-padding="pa-0">
    <template #header-left>
      <div class="d-flex align-center">
        <h3 class="text-h3">{{ title }}</h3>
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
          <td
            v-for="(col, index) in columns"
            :key="index"
            :style="{ width: col.width }"
            class="text-body-2"
          >
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
            <tooltip v-if="col.value === 'spending'">
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
import { isMultiValColumn } from "../../../utils"

export default {
  name: "GeoDrawer",

  components: {
    Drawer,
    HuxDataTable,
    Observer,
    Tooltip,
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
      defaultColumnsWithCountry: [
        {
          value: "size",
          text: "Size",
          width: "20%",
        },
        {
          value: "spending",
          text: "Spending $",
          width: "20%",
        },
      ],
      defaultColumns: [
        {
          value: "size",
          text: "Size",
          width: "25%",
        },
        {
          value: "spending",
          text: "Spending $",
          width: "25%",
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
        countries: "Countries",
        states: "US States",
        cities: "Cities",
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
      await this.refreshData()
      switch (this.geoLevel) {
        case "cities":
          this.columns = isMultiValColumn(this.geoCities, "country")
            ? [
                {
                  value: "city",
                  text: "City",
                  width: "25%",
                },
                {
                  value: "state",
                  text: "State",
                  width: "15%",
                },
                {
                  value: "country",
                  text: "Country",
                  width: "20%",
                },
                ...this.defaultColumnsWithCountry,
              ]
            : [
                {
                  value: "city",
                  text: "City",
                  width: "35%",
                },
                {
                  value: "state",
                  text: "State",
                  width: "25%",
                },
                ...this.defaultColumns,
              ]
          this.sortColumn = "city"
          break
        case "countries":
          this.columns = [
            {
              value: "country",
              text: "Country",
              width: "60%",
            },
            ...this.defaultColumns,
          ]
          this.sortColumn = "country"
          break
        case "states":
          this.columns = isMultiValColumn(this.geoStates, "country")
            ? [
                {
                  value: "state",
                  text: "State",
                  width: "30%",
                },
                {
                  value: "country",
                  text: "Country",
                  width: "30%",
                },
                ...this.defaultColumnsWithCountry,
              ]
            : [
                {
                  value: "state",
                  text: "State",
                  width: "60%",
                },
                ...this.defaultColumns,
              ]
          this.sortColumn = "state"
          break
      }
      this.loading = false
      this.enableLazyLoad = true
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
        await this.refreshData()
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
