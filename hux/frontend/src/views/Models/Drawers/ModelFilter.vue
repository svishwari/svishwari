<template>
  <hux-filters-drawer
    :is-toggled="localDrawer"
    :count="filterLength"
    :enable-apply="enableApply"
    content-height="300px"
    :style="{ height: viewHeight }"
    data-e2e="audienceFilters"
    @clear="clear"
    @apply="apply"
    @close="close"
  >
      <div class="filter-body">
      <hux-filter-panels :expanded="[0]">
      <hux-filter-panel :hide-actions="true" :disabled="true" title="Industry" :count="selectedTags.length">
          <div v-for="data in filterOptions" :key="data.key">
            <v-checkbox
              v-model="selectedTags"
              multiple
              color="primary lighten-6"
              class="text--base-1"
              :label="data.name"
              :value="data.key"
            ></v-checkbox>
          </div>
        </hux-filter-panel>
      </hux-filter-panels>
      </div>
  </hux-filters-drawer>
</template>

<script>
import HuxFiltersDrawer from "@/components/common/FiltersDrawer"
import HuxFilterPanels from "@/components/common/FilterPanels"
import HuxFilterPanel from "@/components/common/FilterPanel"
import { formatText } from "@/utils.js"

export default {
  name: "ModelFilter",
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
    viewHeight: {
      type: String,
      required: false,
      default: "auto",
    },
    filterOptions: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      localDrawer: this.value,
      selectedTags: [],
      enableApply: false,
      isFilterToggled: false,
      pendingTags: [],
    }
  },

  computed: {
    filterLength() {
      let count = 0
      count = this.selectedTags.length
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
      this.selectedTags = []
    },
    clear() {
      this.clearFilter()
      this.pendingTags = []
      this.apply()
    },
    apply() {
      this.pendingTags = [...this.selectedTags]
      this.$emit("onSectionAction", {
        selectedTags: this.selectedTags,
        filterApplied: this.filterLength,
      })
    },
    cancel() {
      this.clearFilter()
      this.localDrawer = false
    },
    close() {
    this.selectedTags = [...this.pendingTags]
    this.localDrawer = false
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
    width: 100%;
  ::v-deep .v-expansion-panel-content__wrap {
    padding: 14px 24px 14px 24px !important;
  }
}
::v-deep.hux-filters-drawer .footer {
  height: 70px !important;
}
</style>
