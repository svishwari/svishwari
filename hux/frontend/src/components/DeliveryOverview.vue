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
          :menuItems="sectionActions"
          :destinationMenuItems="destinationActions"
          @onSectionAction="$emit('onOverviewSectionAction', $event)"
          @onDestinationAction="$emit('onOverviewDestinationAction', $event)"
        >
          <template #empty-destinations>
            <div class="text--caption mb-13">
              This engagement has no destinations yet. Add destinations in the
              submenu located in the right corner above.
            </div>
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
      engagementMenuOptions: [
        { id: 1, title: "View delivery history", active: true },
        { id: 2, title: "Deliver all", active: true },
        { id: 3, title: "Add a destination", active: true },
        { id: 5, title: "Remove engagement", active: false },
      ],
      destinationMenuOptions: [
        { id: 2, title: "Create lookalike", active: false },
        { id: 1, title: "Deliver now", active: true },
        { id: 3, title: "Edit delivery schedule", active: true },
        { id: 4, title: "Pause delivery", active: false },
        { id: 5, title: "Open destination", active: false },
        { id: 6, title: "Remove destination", active: false },
      ],
    }
  },
  computed: {
    sectionActions() {
      return this.sectionType === "engagement" ? this.engagementMenuOptions : []
    },
    destinationActions() {
      return this.sectionType === "engagement"
        ? this.destinationMenuOptions
        : []
    },
  },
  props: {
    sections: {
      type: Array,
      required: false,
      default: () => [],
    },
    sectionType: {
      type: String,
      required: true,
      default: "engagement",
    },
  },
}
</script>

<style lang="scss" scoped></style>
