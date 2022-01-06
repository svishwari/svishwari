<template>
  <v-card class="rounded-lg card-style delivery-overview mt-4" flat>
    <v-card-title class="d-flex justify-space-between pb-2 pl-6 pr-6">
      <slot name="title-left"></slot>
      <slot name="title-right"></slot>
    </v-card-title>
    <v-progress-linear
      v-if="loadingRelationships"
      :active="loadingRelationships"
      :indeterminate="loadingRelationships"
    />
    <v-card-text v-else class="pl-6 pr-6 pb-6 pt-0">
      <div
        v-if="sections.length == 0"
        class="empty-state py-4 black--text text--lighten-4 text-body-1"
      >
        This audience is not part of an engagement. Add it to an engagement
        below.
      </div>
      <div v-else class="pl-0 pt-0 pr-0 overflow-auto pb-0">
        <delivery-details
          v-for="item in availableRelationships"
          :key="item.id"
          :section="item"
          :status-icon="17"
          :menu-items="sectionActions"
          :deliveries-key="deliveriesKey"
          :section-type="sectionType"
          :destination-menu-items="destinationActions"
          data-e2e="status-list"
          class="mb-4"
          :audience="audienceData"
          @onSectionAction="$emit('onOverviewSectionAction', $event)"
          @onDestinationAction="$emit('onOverviewDestinationAction', $event)"
          @onAddDestination="$emit('onAddDestination', $event)"
          @engagementDeliverySection="$emit('engagementDeliveries', $event)"
          @refreshEntityDelivery="$emit('refreshEntityInsight')"
        >
          <template #empty-destinations>
            <slot name="empty-deliveries" :sectionId="item.id" />
          </template>
        </delivery-details>
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
import DeliveryDetails from "./DeliveryDetails.vue"

export default {
  name: "Delivery",
  components: { DeliveryDetails },
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
    audienceData: {
      type: Object,
      required: false,
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
    availableRelationships() {
      return this.sections
    },
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

<style lang="scss" scoped>
.delivery-overview {
  .add-engagement {
    height: 60px !important;
    display: inline-table;
    width: 100%;
    background: var(--v-primary-lighten1);
    border: 1px solid var(--v-black-lighten2);
    border-radius: 5px;
  }
}
</style>
