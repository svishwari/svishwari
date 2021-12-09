<template>
  <v-expand-transition>
    <div class="hux-table-filter-bar-container pl-6">
      <div class="d-flex justify-space-between pb-2">
        <v-checkbox
          color="#00a3e0"
          v-model="showMatchRate"
          class="text-h5 px-5 withoutExpansion mt-0 pt-0 pl-0"
          label="Show match rate"
          @click="handleCheckboxValueChange()"
        ></v-checkbox>
        <div class="reset-filter" @click="resetAll()">Clear</div>
      </div>
      <div class="d-flex flex-wrap mb-2">
        <hux-table-filter
          v-for="(filter, i) in filters"
          :key="i"
          v-model="filter.value"
          :name="`${filter.name}${
            filter.value.length > 0 ? ` (${filter.value.length})` : ''
          }`"
          :on-select="filter.onSelect"
          :items="filter.data"
          @onValueChange="handleFilterValueChange(i)"
        />
        <hux-drop-down-search
          v-for="(filter, i) in filters"
          :key="i"
          v-model="filter.value"
          :toggle-drop-down="toggleDropDown"
          :min-selection="0"
          :items="filter.data"
          :is-search-enabled="false"
          :name="`${filter.name}${
            filter.value.length > 0 ? ` (${filter.value.length})` : ''
          }`"
          @onToggle="handleFilterValueChange(i)"
        >
          <template #activator>
            <div class="dropdown-select-activator">
              <v-select
                dense
                readonly
                placeholder="Select engagement(s)"
                outlined
                background-color="white"
                append-icon="mdi-chevron-down"
              />
            </div>
          </template>
        </hux-drop-down-search>
      </div>
      <div class="d-flex justify-space-between align-center">
        <div>
          <span v-for="(filter, filterIndex) in filters" :key="filterIndex">
            <v-chip
              v-for="(selectedValue, valueIndex) in filter.value"
              :key="valueIndex"
              close
              small
              class="mr-1 ml-0 mt-0 mb-1 text-subtitle-2"
              text-color="primary"
              color="var(--v-primary-lighten3)"
              close-icon="mdi-close"
              @click:close="removeValue(filterIndex, valueIndex)"
            >
              {{ selectedValue.name }}
            </v-chip>
          </span>
        </div>
        <!-- <div class="reset-filter" @click="resetAll()">Reset all</div> -->
      </div>
    </div>
  </v-expand-transition>
</template>

<script>
import HuxTableFilter from "@/components/common/TableFilter.vue"
import HuxDropDownSearch from "@/components/common/HuxDropDownSearch"

export default {
  name: "HuxTableFiltersBar",

  components: {
    HuxTableFilter,
    HuxDropDownSearch,
  },

  props: {
    filters: {
      type: Array,
      required: false,
      default: () => [],
    },
  },

  data() {
    return {
      showMatchRate: true,
    }
  },

  methods: {
    removeValue(filterIndex, valueIndex) {
      this.filters[filterIndex].value.splice(valueIndex, 1)
      this.handleFilterValueChange(filterIndex)
    },

    resetAll() {
      this.filters.map((each) => {
        each.value = []
      })
      this.$emit("onReset")
    },

    handleFilterValueChange(filterIndex) {
      if (this.filters[filterIndex].onSelect) {
        this.filters[filterIndex].onSelect(this.filters[filterIndex].value)
      }
    },

    handleCheckboxValueChange() {
       this.$emit("onCheckboxChange", this.showMatchRate)
    }
  },
}
</script>

<style lang="scss" scoped>
.hux-table-filter-bar-container {
  // background: var(--v-primary-lighten2);
  padding: 8px 11px;
  border-bottom: 1px solid var(--v-black-lighten3);
  .reset-filter {
    @extend .cursor-pointer;
    color: var(--v-primary-base);
    min-width: fit-content;
  }

  ::v-deep .v-input__control {
    .v-label {
      color: var(--v-black-base);
    }
  }
}
</style>
