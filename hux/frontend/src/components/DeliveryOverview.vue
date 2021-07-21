<template>
  <v-card class="rounded-lg card-style" minHeight="145px" flat>
    <v-card-title class="d-flex justify-space-between pb-4 pl-6 pt-5">
      <slot name="title-left"></slot>
      <slot name="title-right"></slot>
    </v-card-title>
    <v-progress-linear
      v-if="loadingRelationships"
      :active="loadingRelationships"
      :indeterminate="loadingRelationships"
    />
    <v-card-text v-else class="pl-6 pr-6 pb-4 pt-0">
      <v-col class="d-flex flex-row pl-0 pt-0 pr-0 overflow-auto pb-3">
        <status-list
          v-for="item in sections"
          :key="item.id"
          :audience="item"
          :statusIcon="17"
        />
      </v-col>
    </v-card-text>
  </v-card>
</template>

<script>
import StatusList from "./common/StatusList.vue"
export default {
  components: { StatusList },
  name: "DeliveryOverview",
  data() {
    return {
      loadingRelationships: true,
    }
  },
  props: {
    sections: {
      type: Array,
      required: false,
      default: () => [],
    },
  },
}
</script>

<style lang="scss" scoped></style>
