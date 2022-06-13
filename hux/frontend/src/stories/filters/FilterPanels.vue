<template>
  <v-expansion-panels>
    <v-expansion-panel v-for="(item, i) in filterOptions" :key="i">
      <v-expansion-panel-header hide-actions>
        <v-checkbox prepend-icon="$expand">
          <template #label
            ><span class="text-body-1">{{ item.name }}</span></template
          >
        </v-checkbox>
        <v-spacer />
        <span class="panel-count">1</span>
      </v-expansion-panel-header>
      <v-expansion-panel-content>
        <v-list>
          <v-list-item
            v-for="(subItem, j) in item.options"
            :key="j"
            class="list-items"
          >
            <v-checkbox>
              <template #label
                ><span class="text-body-1">{{ subItem }}</span></template
              >
            </v-checkbox>
          </v-list-item>
        </v-list>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-expansion-panels>
</template>

<script>
export default {
  name: "Filter Panel",
  data() {
    return {
      selected: [],
    }
  },
  props: {
    filterOptions: {
      type: Array,
      required: true,
    },
  },
}
</script>

<style lang="scss" scoped>
::v-deep .v-expansion-panel-content__wrap {
  border-top: 1px solid var(--v-black-lighten3) !important;
  padding: 0px 8px;
}
::v-deep .v-input--selection-controls {
  margin-top: 0px;
  padding-top: 4px;
  padding-bottom: 4px;
}
::v-deep .v-input__control {
  height: 24px;
}
::v-deep .v-expansion-panel {
  margin-top: 0px;
}
.list-items {
  min-height: 24px;
}
.panel-count {
  text-align: right;
}
</style>
