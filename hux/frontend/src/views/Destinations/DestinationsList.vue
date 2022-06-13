<template>
  <div class="list-wrapper d-flex justify-start align-start flex-wrap">
    <template v-if="hasAddedDestinations">
      <descriptive-card
        v-for="destination in addedDestinations"
        :key="destination.id"
        :icon="destination.type"
        :icon-color="'white'"
        :logo-size="45"
        :title="destination.name"
        :description="destination.category"
        :disabled="['Pending', 'Requested'].includes(destination.status)"
        :action-menu="true"
        :coming-soon="false"
        :logo-option="true"
        :interactable="false"
        logo-box-padding="8px"
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
          <v-list class="py-0">
            <v-list-item
              class="text-body-1 action-menu-item"
              data-e2e="destination-list-remove"
              @click="openEditModal(destination)"
            >
              Edit destination URL
            </v-list-item>
            <v-list-item
              v-if="getAccess('destinations', 'delete')"
              class="text-body-1 action-menu-item"
              data-e2e="destination-list-remove"
              @click="openModal(destination)"
            >
              Remove
            </v-list-item>
          </v-list>
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

    <confirm-modal
      v-model="editConfirmModal"
      right-btn-text="Save changes"
      left-btn-text="Nevermind!"
      :is-disabled="newURL === ''"
      @onCancel="editConfirmModal = false"
      @onConfirm="updateDestinationURL()"
    >
      <template #body>
        <div class="mx-4">
          <icon type="edit" :size="42" color="primary" variant="lighten6" />
          <div class="text-h2 mb-4">Editing destination URL</div>
          <text-field
            v-model="newURL"
            label-text="Edit destination URL"
            placeholder="Destination URL"
            class="pt-5"
            height="40"
            required
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
import Icon from "@/components/common/Icon"
import { getAccess } from "@/utils.js"

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
    Icon,
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
      editConfirmModal: false,
      enableConfirm: false,
      inputText: null,
      newURL: "",
      DestinationMessage: false,
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
      updateDestination: "destinations/update",
      setAlert: "alerts/setAlert",
    }),

    openModal(destination) {
      this.selectedDestination = destination
      this.confirmModal = true
    },

    openEditModal(destination) {
      this.newURL = destination.link
      this.selectedDestination = destination
      this.editConfirmModal = true
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

    async updateDestinationURL() {
      try {
        await this.updateDestination({
          id: this.selectedDestination.id,
          payload: {
            link: this.newURL,
          },
        })
        this.editConfirmModal = false
        this.inputText = null
        this.setAlert({
          type: "success",
          message: "Destination URL has been updated successfully.",
        })
      } catch (error) {
        this.editConfirmModal = false
        this.inputText = null
      }
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
    getAccess: getAccess,
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
::v-deep circle {
  stroke: rgb(255, 255, 255) !important;
}
.action-menu-item {
  min-height: 32px !important;
  min-width: 180px !important;
}
</style>
