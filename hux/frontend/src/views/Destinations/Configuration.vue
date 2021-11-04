<template>
  <page class="white" max-width="970px">
    <div class="mb-10">
      <h4 class="text-h2 black--text text--darken-4">Add a destination</h4>
      <p class="black--text text--darken-4">
        Please fill out the information below to connect a new destination.
      </p>
    </div>

    <label class="d-flex mb-2 black--text text--darken-4"
      >Select a destination</label
    >

    <div class="d-flex align-center mb-10">
      <template v-if="selectedDestination">
        <logo :type="selectedDestination.type" />
        <span class="pl-2">{{ selectedDestination.name }}</span>
        <a class="pl-2" color="primary" @click="toggleDrawer()">Change</a>
      </template>
      <template v-else>
        <v-btn
          fab
          x-small
          color="primary"
          data-e2e="drawerToggle"
          @click="toggleDrawer()"
        >
          <v-icon dark> mdi-plus </v-icon>
        </v-btn>
      </template>
    </div>

    <v-form
      v-if="selectedDestination && destinationFields"
      v-model="isFormValid"
    >
      <div class="destination-auth-wrap primary lighten-1 pa-5 rounded mb-10">
        <v-row>
          <v-col
            v-for="key in Object.keys(destinationFields)"
            :key="key"
            cols="6"
            data-e2e="destinationConfigDetails"
          >
            <text-field
              v-model="authenticationDetails[key]"
              :label-text="destinationFields[key].name"
              :required="destinationFields[key].required"
              :rules="[rules.required]"
              :placeholder-text="
                destinationFields[key].type == 'text'
                  ? `Enter ${destinationFields[key].name}`
                  : `**********`
              "
              :input-type="destinationFields[key].type"
              :help-text="destinationFields[key].description"
              height="40"
              icon="mdi-alert-circle-outline"
              @blur="reset"
            />
          </v-col>
        </v-row>
      </div>
      <div class="d-flex flex-wrap justify-end">
        <hux-button
          v-if="!isValidating"
          :icon="isValidated ? 'mdi-check' : null"
          :icon-position="isValidated ? 'left' : null"
          :variant="isValidated ? 'success' : 'primary'"
          size="large"
          :is-tile="true"
          :is-disabled="!isFormValid"
          data-e2e="validateDestination"
          @click="validate()"
        >
          {{ isValidated ? "Success!" : "Validate connection" }}
        </hux-button>
        <hux-button
          v-if="isValidating"
          class="processing-button"
          variant="primary"
          size="large"
          :is-tile="true"
        >
          Validating...
        </hux-button>
      </div>
      <div v-if="validationError" class="d-flex flex-wrap justify-end pt-2">
        <span class="red--text text-caption">{{ validationError }}</span>
      </div>
      <div
        v-if="isSalesforceSelected && isValidated"
        class="destination-auth-wrap primary lighten-1 pa-4 rounded mt-10"
      >
        <s-f-m-c :data-extensions="dataExtensions" @select="setExtension" />
      </div>
    </v-form>

    <hux-footer slot="footer" max-width="850px" data-e2e="footer">
      <template #left>
        <hux-button
          variant="white"
          size="large"
          :is-tile="true"
          @click="cancel()"
        >
          <span class="primary--text">Cancel</span>
        </hux-button>
      </template>
      <template #right>
        <hux-button
          variant="primary"
          size="large"
          :is-tile="true"
          :is-disabled="!isFullyConfigured"
          @click="add()"
        >
          Add &amp; return
        </hux-button>
      </template>
    </hux-footer>

    <drawer v-model="drawer">
      <template #header-left>
        <div class="d-flex align-center">
          <icon type="map" :size="32" class="mr-3" />
          <h2 class="text-h2 pr-2 black--text text--lighten-4">
            Select a destination
          </h2>
        </div>
      </template>
      <template #footer-left>
        <div class="d-flex align-baseline">
          <span class="text-caption black--text text--darken-1">
            {{ destinations.length }} results
          </span>
        </div>
      </template>
      <template #default>
        <div class="ma-3 font-weight-light px-6">
          <div
            v-for="(value, category, index) in groupByCategory(
              enabledDestinations
            )"
            :key="`active-${index}`"
          >
            <span class="d-block text--body-2 mb-2 mt-6">{{ category }}</span>
            <card-horizontal
              v-for="destination in value"
              :key="destination.id"
              :title="destination.name"
              :icon="destination.type"
              :is-added="destination.is_added || isSelected(destination.id)"
              :is-available="destination.is_enabled"
              :is-already-added="destination.is_added"
              class="mb-2"
              data-e2e="destinationsDrawer"
              @click="onSelectDestination(destination.id)"
            />
          </div>

          <v-divider
            style="border-color: var(--v-black-lighten2)"
            class="my-8"
          />

          <div
            v-for="(value, category, index) in groupByCategory(
              disabledDestinations
            )"
            :key="`nonActive-${index}`"
          >
            <span class="d-block text--body-2 mb-2 mt-6">{{ category }}</span>
            <!-- TODO update the isAddeed with the right logic to fetch the ones already requested -->
            <card-horizontal
              v-for="destination in value"
              :key="destination.id"
              :title="destination.name"
              :icon="destination.type"
              :is-added="requestedDestinations.includes(destination.id)"
              requested-button
              :is-available="destination.is_enabled"
              :is-already-added="destination.is_added"
              class="my-3"
              data-e2e="requestDestinationDrawer"
              @click="onRequestDestination(destination.id)"
            />
          </div>
        </div>
      </template>
    </drawer>
    <confirm-modal
      v-model="showConfirmModal"
      icon="leave-config"
      title="You are about to leave the configuration process"
      right-btn-text="Yes, leave configuration"
      body=" Are you sure you want to stop the configuration and go to another page? You will not be able to recover it and will need to start the process again."
      @onCancel="showConfirmModal = false"
      @onConfirm="navigateaway()"
    />
  </page>
</template>

<script>
import { mapGetters, mapActions } from "vuex"

import { groupBy } from "@/utils"

import Page from "@/components/Page"
import Drawer from "@/components/common/Drawer"
import CardHorizontal from "@/components/common/CardHorizontal"
import Logo from "@/components/common/Logo"
import huxButton from "@/components/common/huxButton"
import HuxFooter from "@/components/common/HuxFooter"
import TextField from "@/components/common/TextField"
import ConfirmModal from "@/components/common/ConfirmModal.vue"

import SFMC from "./Configuration/SFMC.vue"
import Icon from "../../components/common/Icon.vue"

import sortBy from "lodash/sortBy"

export default {
  name: "ConfigureDestination",

  components: {
    Page,
    Drawer,
    CardHorizontal,
    HuxFooter,
    huxButton,
    TextField,
    Logo,
    SFMC,
    ConfirmModal,
    Icon,
  },
  data() {
    return {
      loading: false,
      drawer: false,
      selectedDestinationId: null,
      authenticationDetails: {},
      requestedDestinations: [],
      isValidated: false,
      isValidating: false,
      validationError: null,
      isFormValid: false,
      rules: {
        required: (value) => !!value || "This is a required field",
      },
      selectedDataExtension: {},
      dataExtensions: [],
      showConfirmModal: false,
      navigateTo: false,
      flagForModal: false,
    }
  },

  computed: {
    ...mapGetters({
      destinations: "destinations/list",
      destination: "destinations/single",
      destinationConstants: "destinations/constants",
    }),

    selectedDestination() {
      return this.selectedDestinationId
        ? this.destination(this.selectedDestinationId)
        : null
    },

    destinationFields() {
      return (
        this.destinationConstants[
          this.selectedDestination.type.replace("-", "_")
        ] || null
      )
    },

    enabledDestinations() {
      return this.destinations.filter((each) => each.is_enabled)
    },

    disabledDestinations() {
      return this.destinations.filter((each) => !each.is_enabled)
    },

    isSalesforceSelected() {
      return this.selectedDestination !== null
        ? this.selectedDestination.type === "sfmc"
        : false
    },

    isFullyConfigured() {
      return this.isSalesforceSelected
        ? this.selectedDataExtension.performance_metrics_data_extension
        : this.isValidated
    },
  },

  beforeRouteLeave(to, from, next) {
    if (this.flagForModal == false) {
      this.showConfirmModal = true
      this.navigateTo = to
    } else {
      next()
    }
  },

  async mounted() {
    this.loading = true

    if (this.$route.query.select) {
      this.drawer = true
    }

    await this.getDestinationConstants()
    await this.getDestinations()

    this.loading = false
  },

  methods: {
    ...mapActions({
      getDestinationConstants: "destinations/constants",
      getDestinations: "destinations/getAll",
      getDestination: "destinations/get",
      addDestination: "destinations/add",
      validateDestination: "destinations/validate",
    }),

    navigateaway() {
      this.showConfirmModal = false
      this.flagForModal = true
      this.$router.push(this.navigateTo)
    },

    setExtension(data) {
      this.selectedDataExtension = data
    },

    toggleDrawer() {
      this.drawer = !this.drawer
    },

    isSelected(id) {
      return this.selectedDestination && this.selectedDestination.id === id
    },

    groupByCategory(list) {
      return groupBy(sortBy(list, ["category", "name"]), "category")
    },

    onSelectDestination(id) {
      this.selectedDestinationId = id
      this.reset()
      this.authenticationDetails = {}
      this.drawer = false
    },

    // TODO Need to implement the requesting destination integration with API.
    onRequestDestination(id) {
      if (this.requestedDestinations.includes(id)) {
        this.requestedDestinations.splice(
          this.requestedDestinations.indexOf(id),
          1
        )
      } else {
        this.requestedDestinations.push(id)
      }
    },

    reset() {
      this.isValidated = false
      this.selectedDataExtension = {}
    },

    async validate() {
      this.isValidating = true
      this.validationError = null

      try {
        const response = await this.validateDestination({
          type: this.selectedDestination.type,
          authentication_details: this.authenticationDetails,
        })
        if (this.isSalesforceSelected) {
          this.dataExtensions = response.perf_data_extensions
        }
        this.isValidated = true
      } catch (error) {
        this.validationError = error.response.data.message
      } finally {
        this.isValidating = false
      }
    },

    async add() {
      try {
        let data = {
          id: this.selectedDestination.id,
          authentication_details: this.authenticationDetails,
        }
        if (this.isSalesforceSelected) {
          data.configuration = this.selectedDataExtension
        }
        await this.addDestination(data)
        this.flagForModal = true
        this.$router.push({ name: "Destinations" })
      } catch (error) {
        console.error(error)
      }
    },

    cancel() {
      // TODO: need to add modal that confirms to leave configuration
      this.flagForModal = true
      this.$router.push({ name: "Destinations" })
    },
  },
}
</script>

<style lang="scss" scoped>
.destination-auth-wrap {
  border: 1px solid var(--v-black-lighten2) !important;
}
</style>
