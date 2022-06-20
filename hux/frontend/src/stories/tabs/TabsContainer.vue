<template>
  <div>
    <v-tabs v-model="tab">
      <v-tab v-for="item in items" :key="item" class="text-body-1">
        {{ item }}
      </v-tab>
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item v-for="item in items" :key="item">
        <div>
          <slot :name="item" />
        </div>
      </v-tab-item>
    </v-tabs-items>
  </div>
</template>

<script>
export default {
  name: "TabsContainer",
  components: {},
  props: {
    items: {
      type: Array,
      required: true,
      default: () => ["web", "shopping", "videos", "images", "news"],
    },
  },
  data() {
    return {
      tab: null,
    }
  },
}
</script>

<style lang="scss" scoped>
::v-deep .v-tabs {
  .v-tabs-bar {
    .v-tabs-bar__content {
      justify-content: left;
    }
  }
}
</style>
