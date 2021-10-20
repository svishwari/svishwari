<template>
  <v-expansion-panel class="hux-filter-panel">
    <v-expansion-panel-header class="header">
      <h4 class="text-body-1 primary--text text--lighten-6">
        <slot name="title">{{ title }}</slot>
        <span v-if="count" class="ml-1">({{ count }})</span>
      </h4>
      <template #actions>
        <v-icon color="blue"> $expand </v-icon>
      </template>
    </v-expansion-panel-header>

    <v-expansion-panel-content class="content">
      <slot name="default">
        <!-- filter options and selections (radio, checkbox, dropdown, etc) -->
      </slot>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import { defineComponent } from "@vue/composition-api"

export default defineComponent({
  props: {
    title: {
      type: String,
      required: true,
    },

    count: {
      type: Number,
      required: false,
      default: 0,
    },
  },
})
</script>

<style lang="scss" scoped>
$padding: 20px;
$headerHeight: 40px;

.hux-filter-panel {
  .header {
    height: $headerHeight;
    padding: 0 $padding;
    border-top: 1px solid var(--v-black-lighten2);
    border-bottom: 1px solid var(--v-black-lighten2);
  }

  .content {
    ::v-deep .v-expansion-panel-content__wrap {
      padding: $padding;
    }
  }
}
</style>
