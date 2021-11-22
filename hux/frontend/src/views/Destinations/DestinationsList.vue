<template>
  <div class="list-wrapper d-flex justify-start align-start flex-wrap">
    <template v-if="hasAddedDestinations">
      <descriptive-card
        v-for="destination in addedDestinations"
        :key="destination.id"
        :icon="destination.type"
        :icon-color="'white'"
        :title="destination.name"
        :description="destination.category"
        :disabled="['Pending', 'Requested'].includes(destination.status)"
        :action-menu="true"
        :coming-soon="false"
        :logo-option="true"
        :interactable="false"
        height="225"
        width="255"
        class="mr-12 model-desc-card"
        data-e2e="destination-list"
      >
        <template slot="top">
          <status
            :icon-size="18"
            :status="destination.status"
            collapsed
            class="d-flex float-left"
            data-e2e="model-status"
          />
        </template>
        <template slot="action-menu-options">
          <div
            class="px-4 py-2 white d-flex flex-column text-h5"
            data-e2e="destination-list-remove"
            @click="openModal(destination)"
          >
            <span class="d-flex align-center"> Remove </span>
          </div>
        </template>
      </descriptive-card>
    </template>

    <v-row v-else class="pa-4">
      <hux-empty
        v-if="!showError"
        icon-type="destinations-null"
        :icon-size="50"
        title="No destinations to show"
        subtitle="Destinations will appear here once you add them."
      >
        <template #button>
          <router-link
            :to="{ name: 'DestinationConfiguration' }"
            class="text-decoration-none"
            data-e2e="addDestination"
          >
            <huxButton
              button-text="Add a destination"
              variant="primary"
              size="large"
              is-tile
              height="40"
              class="ma-2 font-weight-regular no-shadow mr-0 caption"
            >
              Add a destination
            </huxButton>
          </router-link>
        </template>
      </hux-empty>
      <error
        v-else
        icon-type="error-on-screens"
        :icon-size="50"
        title="Destinations are currently unavailable"
        subtitle="Our team is working hard to fix it. Please be patient and try again soon!"
      >
      </error>
    </v-row>

    <confirm-modal
      v-model="confirmModal"
      icon="sad-face"
      type="error"
      title="You are about to remove"
      :sub-title="`${selectedDestination.name}`"
      right-btn-text="Yes, remove it"
      data-e2e="remove-destination-confirm"
      :is-disabled="
        selectedDestination.status !== 'Requested' ? !enableConfirm : false
      "
      @onCancel="cancelRemoval()"
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
          Are you sure you want to remove this
          <template v-if="selectedDestination.status === 'Requested'">
            pending
          </template>
          destination?
        </div>
        <div
          v-if="selectedDestination.status !== 'Requested'"
          class="black--text text--darken-4 text-subtitle-1 font-weight-regular"
        >
          By removing this destination you will be impacting
          <span class="error--text">ALL</span> audiences and engagements that
          are being delivered to this destination and you will not be able to
          recover its impact.
        </div>
        <br />
        <div v-if="selectedDestination.status !== 'Requested'">
          <text-field
            label-text="For safety reasons please confirm the deletion of the destination:"
            placeholder='Type "confirm" to remove this destination'
            height="40"
            data-e2e="remove-destination-text"
            required
            :value="inputText"
            @input="enableConfirmButton($event)"
          />
        </div>
      </template>
    </confirm-modal>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import sortBy from "lodash/sortBy"

import ConfirmModal from "@/components/common/ConfirmModal"
import DescriptiveCard from "@/components/common/Cards/DescriptiveCard"
import Status from "@/components/common/Status"
import TextField from "@/components/common/TextField"
import HuxEmpty from "@/components/common/screens/Empty"
import Error from "@/components/common/screens/Error"
import huxButton from "@/components/common/huxButton"

export default {
  name: "DestinationsList",

  components: {
    ConfirmModal,
    DescriptiveCard,
    Status,
    TextField,
    HuxEmpty,
    Error,
    huxButton,
  },

  props: {
    showError: {
      type: Boolean,
      required: true,
    },
  },

  data() {
    return {
      selectedDestination: {},
      confirmModal: false,
      enableConfirm: false,
      inputText: null,
    }
  },

  computed: {
    ...mapGetters({
      destinations: "destinations/list",
    }),

    addedDestinations() {
      return sortBy(this.destinations, ["status", "name"]).filter(
        (destination) => destination.is_added
      )
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
          connection_status: "Pending",
        },
      })
      this.confirmModal = false
      this.inputText = null
    },

    enableConfirmButton(val) {
      this.inputText = val
      this.enableConfirm = /confirm/i.test(val)
    },

    cancelRemoval() {
      this.confirmModal = !this.confirmModal
      this.inputText = null
      this.enableConfirm = false
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
::v-deep.descriptive-card {
  &.non-interactable {
    cursor: default;
    &:hover {
      @extend .box-shadow-5;
    }
  }
  .description {
    color: var(--v-black-lighten4) !important;
  }
}
::v-deep.descriptive-card.in-active {
  box-shadow: none !important;
}
</style>
