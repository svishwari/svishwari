<template>
  <div>
    <hux-button @click="toggleDrawer = !toggleDrawer">Toggle Filter</hux-button>
    <drawer v-model="toggleDrawer" title="Filter" width="320">
      <template #header-right>
        <icon-button :raised="false" variant="secondary">Clear all</icon-button>
      </template>
      <template #default>
        <filter-panels :filterOptions="filterOptions"></filter-panels>
      </template>
      <template #footer-left>
        <hux-button @click="toggleDrawer = !toggleDrawer">Close</hux-button>
      </template>
    </drawer>
  </div>
</template>

<script>
import FilterPanels from "./FilterPanels.vue"
import drawer from "../Drawer/Drawer2.vue"
import huxButton from "../huxButton/huxButton2.vue"
import IconButton from "../iconButton/plainButton.vue"

export default {
  name: "Filter Drawer",
  components: { drawer, huxButton, FilterPanels, IconButton },
  data() {
    return {
      toggleDrawer: false,
    }
  },
  props: {
    filterOptions: {
      type: Array,
      required: true,
      default: () => [],
    },
  },
}
</script>
