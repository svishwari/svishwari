<template>
  <hux-filters-drawer
    :is-toggled="localDrawer"
    :count="filterLength"
    content-height="300px"
    :style="{ height: viewHeight }"
    @clear="clear"
    @apply="apply"
    @close="close"
  >
    <hux-filter-panels :expanded="[]">
      <v-checkbox
        v-model="selectedFavourite"
        color="primary lighten-6"
        class="text--base-1 px-5 withoutExpansion checkboxFavorite"
        label="My favorites only"
      ></v-checkbox>
      <v-checkbox
        v-model="selectedEngagementsWorkedWith"
        color="primary lighten-6"
        class="text--base-1 px-5 withoutExpansion"
        label="Engagements I’ve worked on"
      ></v-checkbox>
    </hux-filter-panels>
  </hux-filters-drawer>
</template>

<script>
import HuxFiltersDrawer from "@/components/common/FiltersDrawer"
import HuxFilterPanels from "@/components/common/FilterPanels"

export default {
  name: "EngagementFilterDrawer",
  components: {
    HuxFiltersDrawer,
    HuxFilterPanels,
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
      selectedFavourite: false,
      selectedEngagementsWorkedWith: false,
    }
  },

  computed: {
    filterLength() {
      let count = 0
      if (this.selectedFavourite) count++
      if (this.selectedEngagementsWorkedWith) count++
      this.$emit("selected-filters", count)
      return count
    },
  },
  watch: {
    value: function () {
      this.localDrawer = this.value
    },
  },
  methods: {
    clearFilter() {
      this.selectedFavourite = false
      this.selectedEngagementsWorkedWith = false
    },
    clear() {
      this.clearFilter()
      this.apply()
    },
    apply() {
      this.$emit("onSectionAction", {
        selectedFavourite: this.selectedFavourite,
        selectedEngagementsWorkedWith: this.selectedEngagementsWorkedWith,
      })
    },
    cancel() {
      this.clearFilter()
      this.localDrawer = false
    },
    close() {
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
