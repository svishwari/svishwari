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
    <v-card-text v-else class="pl-6 pr-6 pb-3 pt-1">
      <div
        v-if="sections.length == 0"
        class="empty-state py-4 black--text text--lighten-4 text-body-1"
      >
        This audience is not part of an engagement. Add it to an engagement
        below.
      </div>
      <div v-else class="pa-0">
        <v-row>
          <v-col
            v-for="(item, index) in availableRelationships"
            :key="item.id"
            :cols="
              availableRelationships.length % 2 != 0 &&
              index == availableRelationships.length - 1
                ? 12
                : 6
            "
          >
            <delivery-details
              :key="item.id"
              :section="item"
              :status-icon="17"
              :menu-items="sectionActions"
              :deliveries-key="deliveriesKey"
              :section-type="sectionType"
              :destination-menu-items="destinationActions"
              :engagement-id="engagementId"
              :headers="headers"
              data-e2e="status-list"
              class="mb-4"
              :audience="audienceData"
              @onAddDestination="$emit('onAddDestination', $event)"
              @engagementDeliverySection="$emit('engagementDeliveries', $event)"
              @refreshEntityDelivery="$emit('refreshEntityDelivery', $event)"
              @triggerSelectAudience="$emit('triggerSelectAudience', $event)"
              @onSectionAction="$emit('onOverviewDestinationAction', $event)"
              @triggerOverviewAction="$emit('triggerOverviewAction', $event)"
            >
              <template #empty-destinations>
                <slot name="empty-deliveries" :sectionId="item.id" />
              </template>
            </delivery-details>
          </v-col>
        </v-row>
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
    engagementId: {
      type: String,
      required: false,
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
    headers: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      engagementMenuOptions: [
        { id: 1, title: "View delivery history", active: false },
        { id: 2, title: "Deliver all", active: true },
        { id: 3, title: "Add a destination", active: true },
        { id: 5, title: "ps.history", active: false },
      ],
      destinationMenuOptions: [
        { id: 1, title: "Deliver now", active: true },
        { id: 3, title: "Edit delivery schedule", active: true },
        { id: 6, title: "Remove destination", active: true },
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
        : this.destinationMenuOptions
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
