<template>
  <div class="list-wrapper">
    <v-row v-if="hasAddedDestinations">
      <template>
        <descriptive-card
          v-for="destination in addedDestinations"
          :key="destination.id"
          :icon="destination.type"
          :icon-color="'white'"
          :title="destination.name"
          :description="''"
          :disabled="destination.status !== 'Succeeded'"
          :action-menu="true"
          :coming-soon="false"
          :logo-option="true"
          height="225"
          width="255"
          class="mr-10 model-desc-card"
        >
          <template slot="top">
            <status
              :icon-size="18"
              :status="destination.status || ''"
              collapsed
              class="d-flex float-left"
              data-e2e="model-status"
            />
          </template>
          <template slot="action-menu-options">
            <v-list class="list-wrapper pa-0">
              <v-list-item-group>
                <v-list-item @click="openModal(destination)">
                  <v-list-item-title> Remove </v-list-item-title>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </template>
        </descriptive-card>
      </template>
    </v-row>

    <empty-state-data v-else>
      <template #icon> mdi-alert-circle-outline </template>
      <template #title> Oops! There’s nothing here yet </template>
      <template #subtitle>
        To create a connection, you need to select a destination!
        <br />
        Begin by selecting the plus button above.
      </template>
    </empty-state-data>

    <confirm-modal
      v-model="confirmModal"
      icon="sad-face"
      type="error"
      title="You are about to remove"
      :sub-title="`${selectedDestination.name}`"
      right-btn-text="Yes, remove it"
      data-e2e="remove-destination-confirm"
      @onCancel="confirmModal = !confirmModal"
      @onConfirm="confirmRemoval()"
    >
      <template #body>
        <div
          class="
            black--text
            text--darken-4 text-subtitle-1
            pt-6
            font-weight-regular
          "
        >
          Are you sure you want to remove this destination?
        </div>
        <div
          class="black--text text--darken-4 text-subtitle-1 font-weight-regular"
        >
          By removing this destination you will be impacting
          <span class="error--text">ALL</span> audiences and engagements that
          are being delivered to this destination and you will not be able to
          recover its impact.
        </div>
      </template>
    </confirm-modal>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"

import ConfirmModal from "@/components/common/ConfirmModal"
import EmptyStateData from "@/components/common/EmptyStateData"
import DescriptiveCard from "@/components/common/Cards/DescriptiveCard"
import Status from "@/components/common/Status"

export default {
  name: "DestinationsList",

  components: {
    ConfirmModal,
    EmptyStateData,
    DescriptiveCard,
    Status,
  },

  data() {
    return {
      selectedDestination: {},
      confirmModal: false,
    }
  },

  computed: {
    ...mapGetters({
      destinations: "destinations/list",
    }),

    addedDestinations() {
      return this.destinations.filter((destination) => destination.is_added)
    },

    hasAddedDestinations() {
      return Boolean(this.addedDestinations && this.addedDestinations.length)
    },
  },

  methods: {
    ...mapActions({
      removeDestination: "destinations/remove",
    }),
    openModal(destination) {
      this.selectedDestination = destination
      this.confirmModal = true
    },
    async confirmRemoval() {
      await this.removeDestination({
        id: this.selectedDestination.id,
        data: {
          added: false,
        },
      })
      this.confirmModal = false
    },
  },
}
</script>
<style lang="scss" scoped>
.list-wrapper {
  .add-icon {
    display: block;
    margin-left: 7px;
    position: relative;
    top: 3px;
  }
  .list {
    &:hover {
      cursor: auto;
    }
  }
}
</style>
