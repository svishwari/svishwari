<template>
  <hux-filters-drawer
    :is-toggled="localDrawer"
    :count="filterLength"
    content-height="262px"
    :disable-clear="filterLength === 1 && selectedTimeType === 'Last week'"
    @clear="clearAndReload"
    @apply="apply"
    @close="close"
  >
    <div class="filter-body">
      <hux-filter-panels>
        <hux-filter-panel title="Alert type" :count="selectedAlertType.length">
          <v-checkbox
            v-for="data in alertType"
            :key="data.id"
            v-model="selectedAlertType"
            multiple
            color="primary lighten-6"
            class="text--base-1"
            :label="data.title"
            :value="data.title"
          ></v-checkbox>
        </hux-filter-panel>
        <hux-filter-panel title="Category" :count="selectedCategory.length">
          <v-checkbox
            v-for="data in category"
            :key="data.id"
            v-model="selectedCategory"
            multiple
            color="primary lighten-6"
            :label="data.title"
            :value="data.title"
          ></v-checkbox>
        </hux-filter-panel>
        <hux-filter-panel title="Time" :count="1">
          <v-radio-group v-model="selectedTimeType">
            <v-radio
              v-for="data in time"
              :key="data.id"
              :label="data.title"
              color="primary lighten-6"
              :value="data.title"
            ></v-radio>
          </v-radio-group>
        </hux-filter-panel>
        <hux-filter-panel title="User" :count="selectedUsers.length">
          <v-checkbox
            v-for="data in users"
            :key="data"
            v-model="selectedUsers"
            multiple
            color="primary lighten-6"
            :label="data"
            :value="data"
          ></v-checkbox>
        </hux-filter-panel>
      </hux-filter-panels>
    </div>
  </hux-filters-drawer>
</template>

<script>
import HuxFiltersDrawer from "@/components/common/FiltersDrawer"
import HuxFilterPanels from "@/components/common/FilterPanels"
import HuxFilterPanel from "@/components/common/FilterPanel"
export default {
  name: "AlertFilterDrawer",
  components: {
    HuxFiltersDrawer,
    HuxFilterPanels,
    HuxFilterPanel,
  },
  props: {
    value: {
      type: Boolean,
      required: true,
      default: false,
    },
    users: {
      type: Array,
      required: false,
    },
  },
  data() {
    return {
      localDrawer: this.value,
      alertType: [
        {
          id: 1,
          title: "Success",
        },
        {
          id: 2,
          title: "Critical",
        },
        {
          id: 3,
          title: "Informational",
        },
      ],
      category: [
        {
          id: 1,
          title: "Data Sources",
        },
        {
          id: 2,
          title: "Destinations",
        },
        {
          id: 3,
          title: "Engagements",
        },
        {
          id: 4,
          title: "Delivery",
        },
        {
          id: 5,
          title: "Orchestration",
        },
        {
          id: 6,
          title: "Customers",
        },
        {
          id: 7,
          title: "Models",
        },
      ],
      time: [
        {
          id: 1,
          title: "All time",
        },
        {
          id: 2,
          title: "Today",
        },
        {
          id: 3,
          title: "Last week",
        },
        {
          id: 4,
          title: "Last month",
        },
        {
          id: 5,
          title: "Last 3 months",
        },
        {
          id: 6,
          title: "Last 6 months",
        },
      ],
      selectedAlertType: [],
      selectedCategory: [],
      selectedTimeType: "Last week",
      selectedUsers: [],
      selectedTimeCount: 1,
      pendingAlertType: [],
      pendingCategory: [],
      pendingTimeType: "Last week",
      pendingUsers: [],
    }
  },

  computed: {
    filterLength() {
      let alert = this.selectedAlertType.length
      let category = this.selectedCategory.length
      let time = 1
      let users = this.selectedUsers.length
      let totalFiltersCount =
        this.selectedAlertType.length +
        this.selectedCategory.length +
        this.selectedUsers.length +
        time
      this.$emit("selected-filters", totalFiltersCount)
      return alert + category + time + users
    },
  },
  watch: {
    value: function () {
      this.localDrawer = this.value
    },
    localDrawer: function () {
      this.$emit("input", this.localDrawer)
    },
  },
  methods: {
    getTime(value) {
      let today_date = new Date()
      return new Date(
        today_date.getFullYear(),
        today_date.getMonth(),
        today_date.getDate() - value
      )
    },
    clearFilter() {
      this.selectedAlertType = []
      this.selectedCategory = []
      this.selectedTimeType = "Last week"
      this.selectedUsers = []
    },
    clearAndReload() {
      this.clearFilter()
      this.pendingAlertType = []
      this.pendingCategory = []
      this.pendingTimeType = "Last week"
      this.pendingUsers = []
      this.apply()
    },
    apply() {
      this.pendingAlertType = [...this.selectedAlertType]
      this.pendingCategory = [...this.selectedCategory]
      this.pendingTimeType = this.selectedTimeType
      this.pendingUsers = [...this.selectedUsers]

      let getTime
      switch (this.selectedTimeType) {
        case "Today":
          getTime = this.getTime(0)
          break
        case "Last week":
          getTime = this.getTime(7)
          break
        case "Last month":
          getTime = this.getTime(30)
          break
        case "Last 3 months":
          getTime = this.getTime(90)
          break
        case "Last 6 months":
          this.getTime(180)
          break
        default:
          this.getTime(7)
          break
      }

      this.$emit("onSectionAction", {
        getTime: this.$options.filters.Date(getTime, "YYYY-MM-DD"),
        selectedAlertType: this.selectedAlertType,
        selectedCategory: this.selectedCategory,
        selectedUsers: this.selectedUsers,
        filterApplied: this.filterLength,
      })
    },
    close() {
      this.selectedAlertType = [...this.pendingAlertType]
      this.selectedCategory = [...this.pendingCategory]
      this.selectedTimeType = this.pendingTimeType
      this.selectedUsers = [...this.pendingUsers]
      this.localDrawer = false
    },
  },
}
</script>
<style lang="scss" scoped>
::v-deep.v-input--selection-controls {
  margin-top: 0px !important;
  padding-top: 0px !important;
}
::v-deep.input__slot {
  margin: 0px !important;
}
::v-deep .v-input--selection-controls .v-input__slot {
  margin-bottom: 0px !important;
}
::v-deep.theme--light .v-messages {
  min-height: 6px !important;
  color: var(--v-black-base);
}
.clear-btn {
  padding-left: 7.9rem !important;
  padding-top: 10px;
  padding-right: 0px !important;
}
::v-deep.theme--light .v-label {
  font-size: 16px;
  font-weight: 400;
  line-height: 22px;
  letter-spacing: 0;
  color: var(--v-black-base);
}
::v-deep .drawer-header > .v-toolbar__content {
  height: 40px !important;
}
.filter-body {
  ::v-deep .v-expansion-panel-content__wrap {
    padding: 14px 24px 14px 24px !important;
  }
}
</style>
