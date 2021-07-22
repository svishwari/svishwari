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
      <div class="empty-state pa-5 text--gray" v-if="sections.length == 0">
        <slot name="empty-deliveries"></slot>
      </div>
      <v-col
        class="d-flex flex-row pl-0 pt-0 pr-0 overflow-auto pb-3"
        v-if="sections.length >= 0"
      >
        <status-list
          v-for="item in sections"
          :key="item.id"
          :section="item"
          :statusIcon="17"
        >
          <template #empty-destinations>
            <span
              >This engagement has no destinations yet. Add destinations in the
              submenu located in the right corner above.
            </span>
          </template>
        </status-list>
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
      loadingRelationships: false,
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
