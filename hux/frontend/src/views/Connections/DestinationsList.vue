<template>
  <div class="list-wrapper">
    <div class="d-flex align-end mb-4">
      <icon type="destinations" :size="20" color="black-darken4" />
      <h5 class="text-h4 ml-2 mt-1">Destinations</h5>
      <router-link
        :to="{ name: 'DestinationConfiguration' }"
        class="text-decoration-none"
        data-e2e="addDestination"
      >
        <icon class="add-icon cursor-pointer" type="add" :size="27" />
      </router-link>
    </div>
    <template v-if="hasAddedDestinations">
      <card-horizontal
        v-for="destination in addedDestinations"
        :key="destination.id"
        :title="destination.name"
        :icon="destination.type"
        hide-button
        data-e2e="destinationsList"
        class="mb-3 list pr-7"
      >
        <v-menu left offset-y close-on-click>
          <template #activator="{ on }">
            <v-icon color="black darken-4" v-on="on">
              mdi-dots-vertical
            </v-icon>
          </template>
          <div
            class="black--text text-darken-4 cursor-pointer px-4 py-2 white"
            @click="openModal(destination)"
          >
            Remove
          </div>
        </v-menu>
      </card-horizontal>
    </template>
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
      @onCancel="confirmModal = !confirmModal"
      @onConfirm="confirmRemoval()"
    >
      <template #body>
        <div class="pt-4">
          Are you sure you want to remove this destination?
        </div>
        <div class="mb-4">
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

import CardHorizontal from "@/components/common/CardHorizontal"
import ConfirmModal from "@/components/common/ConfirmModal"
import EmptyStateData from "@/components/common/EmptyStateData"
import Icon from "@/components/common/Icon"

export default {
  name: "DestinationsList",

  components: {
    CardHorizontal,
    ConfirmModal,
    EmptyStateData,
    Icon,
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
