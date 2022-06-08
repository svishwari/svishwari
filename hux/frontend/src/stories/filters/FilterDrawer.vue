<template>
  <div>
    <hux-button @click="toggleDrawer = !toggleDrawer" >Toggle Filter</hux-button>
    <drawer v-model="toggleDrawer" title="Filter">
      <template #default>
        <div>This will be the filter pannels</div>
      </template>
      <template #footer-left>
        <hux-button @click="toggleDrawer = !toggleDrawer" >Close</hux-button>
      </template>
    </drawer>
  </div>
</template>

<script>
import drawer from "../Drawer/Drawer2.vue"
import huxButton from "../huxButton/huxButton2.vue"

export default {
  name: "Filter Drawer",
  components: { drawer, huxButton },
  data() {
    return {
      toggleDrawer: false,
    }
  }
}
</script>
