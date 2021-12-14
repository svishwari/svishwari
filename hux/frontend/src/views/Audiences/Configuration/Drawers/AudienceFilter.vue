<template>
  <hux-filters-drawer
    :is-toggled="localDrawer"
    :count="filterLength"
    content-height="300px"
    :style="{ height: viewHeight }"
    data-e2e="audienceFilters"
    @clear="clear"
    @apply="apply"
    @close="close"
  >
    <div class="filter-body">
      <hux-filter-panels :expanded="selectedAttributes.length > 0 ? [0] : []">
        <v-checkbox
          v-model="selectedFavourite"
          color="primary lighten-6"
          class="text--base-1 px-5 withoutExpansion checkboxFavorite"
          label="My favorites only"
        ></v-checkbox>
        <v-checkbox
          v-model="selectedAudienceWorkedWith"
          color="primary lighten-6"
          class="text--base-1 px-5 withoutExpansion"
          label="Audiences I’ve worked on"
        ></v-checkbox>
        <hux-filter-panel title="Attributes" :count="selectedAttributes.length">
          <div class="text-body-1 black--text text--lighten-4 pb-2">MODELS</div>
          <div v-for="data in filterOptions" :key="data.key">
            <v-checkbox
              v-if="data.category == 'model_scores'"
              v-model="selectedAttributes"
              multiple
              color="primary lighten-6"
              class="text--base-1"
              :label="data.name"
              :value="data.key"
            ></v-checkbox>
          </div>
          <br />
          <div class="text-body-1 black--text text--lighten-4 pb-2">
            GENERAL
          </div>
          <div v-for="data in filterOptions" :key="data.key">
            <v-checkbox
              v-if="data.category == 'general'"
              v-model="selectedAttributes"
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
  name: "AudienceFilterDrawer",
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
      selectedAttributes: [],
      selectedFavourite: false,
      selectedAudienceWorkedWith: false,
    }
  },

  computed: {
    filterLength() {
      let count = 0
      count = this.selectedAttributes.length
      if (this.selectedFavourite) count++
      if (this.selectedAudienceWorkedWith) count++

      return count
    },
  },
  watch: {
    value: function () {
      this.localDrawer = this.value
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
      this.selectedAttributes = []
      this.selectedFavourite = false
      this.selectedAudienceWorkedWith = false
    },
    clear() {
      this.clearFilter()
      this.apply()
    },
    apply() {
      this.$emit("onSectionAction", {
        selectedAttributes: this.selectedAttributes,
        selectedFavourite: this.selectedFavourite,
        selectedAudienceWorkedWith: this.selectedAudienceWorkedWith,
      })
    },
    cancel() {
      this.clearFilter()
      this.localDrawer = false
    },
    close() {
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
  ::v-deep .v-expansion-panel-content__wrap {
    padding: 14px 24px 14px 24px !important;
  }
}
</style>
