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
        :columns="columns"
        :data-items="items"
        :sort-column="sortColumn"
      >
        <template #row-item="{ item }">
          <td
            v-for="(col, index) in columns"
            :key="index"
            :style="{ width: col.width }"
            class="text-body-1"
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
      <observer v-if="items.length" @intersect="onLazyLoad" />
    </template>

    <template #footer-left>
      <span class="black--text text--darken-1 text-caption">
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
      required: false,
      default: "states",
    },

    results: {
      required: false,
      default: 0,
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
      geoCities: "customers/geoCities",
      geoCountries: "customers/geoCountries",
      geoStates: "customers/geoStates",
    }),

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
      switch (this.geoLevel) {
        case "cities":
          this.columns = [
            {
              value: "city",
              text: "City",
              width: "30%",
            },
            {
              value: "state",
              text: "State",
              width: "20%",
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
              width: "50%",
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
              width: "50%",
            },
            ...this.defaultColumns,
          ]
          this.sortColumn = "state"
          break
      }
      this.loading = true
      this.batchNumber = 1
      await this.refreshData()
      this.loading = false
      this.enableLazyLoad = true
    } else {
      this.enableLazyLoad = false
    }
  },

  methods: {
    ...mapActions({
      getGeoCities: "customers/getGeoCities",
      getGeoCountries: "customers/getGeoCountries",
      getGeoStates: "customers/getGeoStates",
    }),

    async onLazyLoad() {
      if (this.lastBatch > 1 && this.batchNumber <= this.lastBatch) {
        this.batchNumber++
        await this.refreshData()
      } else {
        this.enableLazyLoad = false
      }
    },

    async refreshData() {
      switch (this.geoLevel) {
        case "cities":
          await this.getGeoCities({
            batchNumber: this.batchNumber,
            batchSize: this.batchSize,
          })
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
