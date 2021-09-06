<template>
  <v-card class="rounded-lg card-style delivery-overview" flat height="100%">
    <v-card-title class="d-flex justify-space-between pb-2 pl-6 pt-3">
      <slot name="title-left"></slot>
      <slot name="title-right"></slot>
    </v-card-title>
    <v-progress-linear
      v-if="loadingRelationships"
      :active="loadingRelationships"
      :indeterminate="loadingRelationships"
    />
    <v-card-text v-else class="pl-6 pr-6 pb-4 pt-0">
      <div v-if="sections.length == 0" class="empty-state pa-5 black--text text--darken-1">
        <slot name="empty-sections"></slot>
      </div>
      <v-col v-else class="d-flex flex-row pl-0 pt-0 pr-0 overflow-auto pb-3">
        <status-list
          v-for="item in sections"
          :key="item.id"
          :section="item"
          :status-icon="17"
          :menu-items="sectionActions"
          :deliveries-key="deliveriesKey"
          :section-type="sectionType"
          :destination-menu-items="destinationActions"
          @onSectionAction="$emit('onOverviewSectionAction', $event)"
          @onDestinationAction="$emit('onOverviewDestinationAction', $event)"
        >
          <template #empty-destinations>
            <slot name="empty-deliveries" :sectionId="item.id" />
          </template>
        </status-list>
      </v-col>
    </v-card-text>
  </v-card>
</template>

<script>
import StatusList from "./common/StatusList.vue"
export default {
  name: "DeliveryOverview",
  components: { StatusList },
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
    deliveriesKey: {
      type: String,
      required: true,
      default: "destinations",
    },
    loadingRelationships: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    return {
      engagementMenuOptions: [
        { id: 1, title: "View delivery history", active: false },
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
      audienceMenuOptions: [
        {
          id: 1,
          title: "Deliver now",
          active: false,
        },
        { id: 2, title: "Add a destination", active: true },
        { id: 3, title: "Create lookalike", active: false },
        { id: 4, title: "Pause all delivery", active: false },
        { id: 5, title: "Remove audience", active: true },
      ],
    }
  },
  computed: {
    sectionActions() {
      return this.sectionType === "engagement"
        ? this.engagementMenuOptions
        : this.audienceMenuOptions
    },
    destinationActions() {
      return this.sectionType === "engagement"
        ? this.destinationMenuOptions
        : []
    },
  },
}
</script>

<style lang="scss" scoped></style>
