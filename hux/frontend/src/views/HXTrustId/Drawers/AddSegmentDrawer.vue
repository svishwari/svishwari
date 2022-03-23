<template>
  <hux-filters-drawer
    :is-toggled="localDrawer"
    headerName="Add segment"
    :count="1"
    content-height="300px"
    submitButtonWidth="79"
    submitButton="Add"
    :style="{ height: viewHeight }"
    @clear="clear"
    @apply="apply"
    @close="close"
  >
    <div class="filter-body">
      <hux-filter-panels :expanded="selectedAttributes.length > 0 ? [0] : []">
        <div class="checkboxFavorite">
          <text-field
            class="mt-4 ml-5 mb-n3 input-box-Field"
            label-text="Segment name"
            placeholder="Segment"
            :rules="lookalikeNameRules"
            required
          />
        </div>
        <v-checkbox
          v-model="selectedFavourite"
          color="primary lighten-6"
          class="text--base-1 px-5 withoutExpansion checkboxFavorite"
          :label="'Households with children under 18'"
        ></v-checkbox>
        <v-checkbox
          v-model="selectedAudienceWorkedWith"
          color="primary lighten-6"
          class="text--base-1 px-5 withoutExpansion checkboxFavorite"
          :label="'Households with seniors over 65'"
        ></v-checkbox>
        <hux-filter-panels>
          <hux-filter-panel
            v-for="(data, ind) in filterData"
            :key="ind"
            :title="data.description"
          >
            <v-checkbox
              v-for="(dataVal, indx) in data.values"
              :key="indx"
              v-model="segementDataObj[data.type]"
              multiple
              color="primary lighten-6"
              class="text--base-1"
              :label="dataVal"
              :value="dataVal"
            ></v-checkbox>
          </hux-filter-panel>
        </hux-filter-panels>
      </hux-filter-panels>
    </div>
  </hux-filters-drawer>
</template>

<script>
import HuxFiltersDrawer from "@/components/common/FiltersDrawer"
import HuxFilterPanels from "@/components/common/FilterPanels"
import HuxFilterPanel from "@/components/common/FilterPanel"
import { formatText } from "@/utils.js"
import TextField from "@/components/common/TextField"

export default {
  name: "AddSegmentDrawer",
  components: {
    HuxFiltersDrawer,
    HuxFilterPanels,
    HuxFilterPanel,
    TextField,
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
    segmentData: {
      type: Array,
      required: true,
      default: false,
    },
  },
  data() {
    return {
      localDrawer: this.value,
      selectedAttributes: [],
      lookalikeNameRules: "",
      selectedFavourite: false,
      selectedAudienceWorkedWith: false,
      enableApply: false,
      segementDataObj: {},
    }
  },

  computed: {
    filterData() {
      return this.segmentData.filter(
        (element) =>
          element.type != "households_with_children_under_18" &&
          element.type != "households_with_children_above_18"
      )
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
    // getTime(value) {
    //   let today_date = new Date()
    //   return new Date(
    //     today_date.getFullYear(),
    //     today_date.getMonth(),
    //     today_date.getDate() - value
    //   )
    // },
    clearFilter() {
      this.selectedAttributes = []
      this.selectedFavourite = false
      this.selectedAudienceWorkedWith = false
    },
    clear() {
      this.enableApply = true
      this.clearFilter()
    },
    clearAndReload() {
      this.enableApply = false
      this.clearFilter()
      this.apply()
    },
    apply() {
      this.$emit("onSectionAction", {
        selectedAttributes: this.selectedAttributes,
        selectedFavourite: this.selectedFavourite,
        selectedAudienceWorkedWith: this.selectedAudienceWorkedWith,
        filterApplied: this.filterLength,
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
  height: 40px;
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
::v-deep .submit-button {
  margin-right: 110px !important;
}
::v-deep .v-expansion-panels {
  justify-content: initial !important;
}
.input-box-Field {
  width: 280px !important;
}
</style>
