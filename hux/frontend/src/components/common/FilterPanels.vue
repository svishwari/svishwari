<template>
  <v-expansion-panels
    v-model="localExpanded"
    flat
    tile
    multiple
    accordion
    class="hux-filter-panels"
  >
    <slot name="default">
      <!-- individual `FilterPanel` items live here -->
    </slot>
  </v-expansion-panels>
</template>

<script>
import { defineComponent, computed } from "@vue/composition-api"

export default defineComponent({
  props: {
    expanded: {
      type: Array,
      required: false,
      default: () => [],
    },
  },

  emits: ["input"],

  setup(props, { emit }) {
    const localExpanded = computed({
      get: () => props.expanded,
      set: (value) => {
        emit("input", value)
      },
    })

    return {
      localExpanded,
    }
  },
})
</script>

<style lang="scss" scoped>
.hux-filter-panels {
  ::v-deep .hux-filter-panel:first-child {
    .header {
      border-top: 0;
    }
  }
}
</style>
