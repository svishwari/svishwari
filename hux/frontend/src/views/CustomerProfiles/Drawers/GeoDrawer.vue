<template>
  <drawer v-model="localToggle" content-padding="pa-0">
    <template #header-left>
      <div class="d-flex align-center">
        <h3 class="text-h3">{{ title }}</h3>
      </div>
    </template>

    <template #default>
      <v-progress-linear :active="loading" :indeterminate="loading" />

      <hux-data-table
        :columns="columns"
        :data-items="!loading ? items : []"
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
          </td>
        </template>
      </hux-data-table>
    </template>

    <template #footer-left>
      <span class="gray--text text-caption">
        {{ results | Numeric }} results
      </span>
    </template>
  </drawer>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import Drawer from "@/components/common/Drawer.vue"
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import Tooltip from "@/components/common/Tooltip.vue"

export default {
  name: "GeoDrawer",

  components: {
    Drawer,
    HuxDataTable,
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
      if (this.geoLevel === "cities") return this.geoCities
      if (this.geoLevel === "states") return this.geoStates
      if (this.geoLevel === "countries") return this.geoCountries
      return this.geoStates
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
      if (this.geoLevel === "cities") {
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
      }

      if (this.geoLevel === "countries") {
        this.columns = [
          {
            value: "country",
            text: "Country",
            width: "50%",
          },
          ...this.defaultColumns,
        ]
        this.sortColumn = "country"
      }

      if (this.geoLevel === "states") {
        this.columns = [
          {
            value: "state",
            text: "State",
            width: "50%",
          },
          ...this.defaultColumns,
        ]
        this.sortColumn = "state"
      }

      await this.refreshData()
    }
  },

  methods: {
    ...mapActions({
      getGeoCities: "customers/getGeoCities",
      getGeoCountries: "customers/getGeoCountries",
      getGeoStates: "customers/getGeoStates",
    }),

    async refreshData() {
      this.loading = true
      if (this.geoLevel === "cities") await this.getGeoCities()
      if (this.geoLevel === "countries") await this.getGeoCountries()
      if (this.geoLevel === "states") await this.getGeoStates()
      this.loading = false
    },
  },
}
</script>
