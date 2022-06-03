<template>
  <hux-filters-drawer
    :is-toggled="localDrawer"
    :count="filterLength"
    content-height="261px"
    :style="{ height: viewHeight }"
    data-e2e="dataFeedsFilters"
    @clear="clearFilter"
    @apply="apply"
    @close="close"
  >
    <div class="filter-body">
      <hux-filter-panels>
        <hux-filter-panel
          title="Time"
          :count="getTimeCount"
          :expanded="getTimeCount > 0 ? [0] : []"
        >
          <v-checkbox
            v-model="selectedToday"
            color="primary lighten-6"
            class="text--base-1 pb-1"
            label="Today"
            @click="updateTime('checkbox')"
          ></v-checkbox>
          <v-checkbox
            v-model="selectedYesterday"
            color="primary lighten-6"
            class="text--base-1 pb-2"
            label="Yesterday"
            @click="updateTime('checkbox')"
          ></v-checkbox>
          <v-divider class="pb-4" />
          <v-radio-group v-model="selectedTimeType">
            <v-radio
              v-for="data in time"
              :key="data.id"
              color="primary lighten-6"
              class="text--base-1"
              :label="data.title"
              :value="data.title"
              @click="updateTime('radio')"
            ></v-radio>
          </v-radio-group>
        </hux-filter-panel>
        <hux-filter-panel
          title="Status"
          :count="selectedStatus.length"
          :expanded="selectedStatus.length > 0 ? [1] : []"
        >
          <v-checkbox
            v-for="data in status"
            :key="data.id"
            v-model="selectedStatus"
            multiple
            color="primary lighten-6"
            class="text--base-1"
            :value="data.title"
          >
            <template v-slot:label>
              <status
                :status="data.title == 'Success' ? 'Completed' : data.title"
                :show-label="false"
                class="d-flex"
                :class="{
                  'data-feed-filter-status': ['Failed', 'Running'].includes(
                    data.title
                  ),
                }"
                :icon-size="data.title == 'Failed' ? '15' : '18'"
              />
              {{ data.title }}
            </template>
          </v-checkbox>
        </hux-filter-panel>
      </hux-filter-panels>
    </div>
  </hux-filters-drawer>
</template>

<script>
import HuxFiltersDrawer from "@/components/common/FiltersDrawer"
import HuxFilterPanels from "@/components/common/FilterPanels"
import HuxFilterPanel from "@/components/common/FilterPanel"
import Status from "@/components/common/Status.vue"
import { formatText } from "@/utils.js"

export default {
  name: "DataFeedsTableFilter",
  components: {
    HuxFiltersDrawer,
    HuxFilterPanels,
    HuxFilterPanel,
    Status,
  },
  props: {
    value: {
      type: Boolean,
      required: true,
      default: false,
    },
    viewHeight: {
      type: String,
      required: false,
      default: "auto",
    },
  },
  data() {
    return {
      localDrawer: this.value,
      selectedToday: false,
      selectedYesterday: false,
      selectedTimeType: "All time",
      selectedStatus: [],
      time: [
        {
          id: 1,
          title: "All time",
        },
        {
          id: 2,
          title: "Last week",
        },
        {
          id: 3,
          title: "Last month",
        },
      ],
      status: [
        {
          id: 1,
          title: "Success",
        },
        {
          id: 2,
          title: "Canceled",
        },
        {
          id: 3,
          title: "Failed",
        },
        {
          id: 4,
          title: "Running",
        },
      ],
    }
  },

  computed: {
    getTimeCount() {
      let count = 0
      if (this.selectedToday) count++
      if (this.selectedYesterday) count++
      if (this.selectedTimeType) count++
      return count
    },
    filterLength() {
      let count = 0
      count = this.selectedStatus.length
      count += this.getTimeCount
      this.$emit("selected-filters", count)
      return count
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
    clearFilter() {
      this.selectedToday = false
      this.selectedYesterday = false
      this.selectedTimeType = "All time"
      this.selectedStatus = []
    },
    apply() {
      this.$emit("onSectionAction", {
        selectedToday: this.selectedToday,
        selectedYesterday: this.selectedYesterday,
        selectedTimeType: this.selectedTimeType,
        selectedStatus: this.selectedStatus,
        filterLength: this.filterLength,
      })
      this.localDrawer = false
    },
    cancel() {
      this.clearFilter()
      this.localDrawer = false
    },
    close() {
      this.localDrawer = false
    },
    updateTime(val) {
      if (val == "radio") {
        this.selectedToday = false
        this.selectedYesterday = false
      } else {
        this.selectedTimeType = null
      }
    },
    formatText: formatText,
  },
}
</script>
<style lang="scss" scoped>
::v-deep.v-input--selection-controls {
  margin-top: 0px !important;
  padding-top: 0px !important;
}
::v-deep.v-input--selection-controls.v-input {
  flex: 1 1 auto !important;
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
.withoutExpansion {
  height: 34px;
  align-items: center;
  margin-top: 6px !important;
}
::v-deep.theme--light .v-label {
  font-size: 16px;
  font-weight: 400;
  line-height: 22px;
  letter-spacing: 0;
  color: var(--v-black-base);
}
.checkboxFavorite {
  border-bottom: 1px solid var(--v-black-lighten2);
}
.filter-body {
  ::v-deep .v-expansion-panel-content__wrap {
    padding: 16px 24px 10px 24px !important;
  }
  width: 100%;
}
.data-feed-filter-status {
  margin-left: 2px !important;
}
</style>
