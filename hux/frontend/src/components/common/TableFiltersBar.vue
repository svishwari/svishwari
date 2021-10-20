<template>
  <v-expand-transition>
    <div class="hux-table-filter-bar-container">
      <div class="d-flex flex-wrap">
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
      </div>
      <div class="d-flex justify-space-between align-center">
        <div>
          <span v-for="(filter, filterIndex) in filters" :key="filterIndex">
            <v-chip
              v-for="(selectedValue, valueIndex) in filter.value"
              :key="valueIndex"
              close
              small
              class="mr-2 my-2 text--subtitle-1"
              text-color="primary"
              color="primary lighten-4"
              close-icon="mdi-close"
              @click:close="removeValue(filterIndex, valueIndex)"
            >
              {{ selectedValue.name }}
            </v-chip>
          </span>
        </div>
        <div class="reset-filter" @click="resetAll()">Reset all</div>
      </div>
    </div>
  </v-expand-transition>
</template>

<script>
import HuxTableFilter from "@/components/common/TableFilter.vue"

export default {
  name: "HuxTableFiltersBar",

  components: {
    HuxTableFilter,
  },

  props: {
    filters: {
      type: Array,
      required: false,
      default: () => [],
    },
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
  },
}
</script>

<style lang="scss" scoped>
.hux-table-filter-bar-container {
  background: var(--v-primary-lighten2);
  padding: 8px 11px;
  border-bottom: 1px solid var(--v-black-lighten3);
  .reset-filter {
    @extend .cursor-pointer;
    color: var(--v-primary-base);
    min-width: fit-content;
  }
}
</style>
