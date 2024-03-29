<template>
  <page class="white add-destination-container" max-width="912px">
    <div class="mb-10">
      <h4 class="text-h1 black--text text--darken-4">Add a destination</h4>
      <p class="text-body-1 black--text text--darken-4">
        Please fill out the information below to connect a new destination.
      </p>
    </div>

    <label class="d-flex text-body-2 mb-2 black--text text--darken-4">
      Select a destination
    </label>

    <div class="d-flex align-center mb-2">
      <template v-if="!(selectedDestination || selectedDestinationNotListed)">
        <v-btn
          text
          min-width="7rem"
          :ripple="false"
          height="3rem"
          class="primary--text text-body-1"
          data-e2e="drawerToggle"
          @click.native="toggleDrawer()"
        >
          <hux-icon type="plus" :size="16" color="primary" class="mr-4" />
          <hux-icon
            type="destination"
            :size="32"
            color="primary"
            class="mr-2 box-shadow-25"
            :style="{ 'border-radius': '50%' }"
          />
          Destination
        </v-btn>
      </template>
      <p v-else class="text-body-1 mb-0 d-inline-flex">
        <template v-if="selectedDestinationNotListed">
          Destination not on list
        </template>
        <template v-else>
          <logo :type="selectedDestination.type" :size="26" />
          <span class="pl-2">{{ selectedDestination.name }}</span>
        </template>
        <a
          class="pl-6 text-body-2 mt-1"
          color="primary"
          @click="toggleDrawer()"
        >
          Change
        </a>
      </p>
    </div>

    <!-- add destination form -->
    <v-form v-if="showAddForm" v-model="isAddFormValid" class="mt-10">
      <div
        class="
          primary
          lighten-1
          border-all
          black--border
          border--lighten-2
          pa-5
          rounded
          mb-10
        "
      >
        <v-row class="pt-4 pl-3">
          <v-col
            v-for="key in Object.keys(destinationFields)"
            :key="key"
            cols="6"
            data-e2e="destinationConfigDetails"
            class="py-0"
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
          :is-disabled="!isAddFormValid"
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
        v-if="isSFMCSelected && isValidated"
        class="
          primary
          lighten-1
          black--border
          border--lighten-2
          pa-4
          rounded
          mt-10
        "
      >
        <s-f-m-c :data-extensions="dataExtensions" @select="setExtension" />
      </div>
      <v-col cols="6" class="py-0">
        <text-field
          v-model="DestinationUrl"
          label-text="Destination URL"
          icon="mdi-alert-circle-outline"
          placeholder-text="URL"
          help-text="Get directed to a specific destination to open and view your audiences. Input the domain/URL where you want to go."
          required
        ></text-field>
      </v-col>
    </v-form>

    <!-- request destination form -->
    <v-form v-if="showRequestForm" v-model="isRequestFormValid">
      <v-alert
        outlined
        tile
        class="
          pa-3
          pl-2
          yellow
          lighten-1
          black--border
          border--lighten-2
          black--text
        "
      >
        <div class="d-flex justify-space-between">
          <div class="mr-3">
            <icon type="bulb" :size="36" color="yellow" />
          </div>
          <p class="text-body-1 ma-0">
            The destination you have selected is currently not available to
            connect through the Hux interface. By requesting, our Hux team will
            explore building an API connector with this destination. In the
            meantime, consider downloading the data files for manual uploads.
          </p>
        </div>
      </v-alert>

      <v-row class="firstRow">
        <v-col cols="8" class="pt-5">
          <text-field
            v-model="requestDetails['contact_email']"
            label-text="Your contact email"
            placeholder-text="Enter an email address"
            required
            :rules="[rules.required, rules.validEmail]"
            input-type="text"
            height="40"
          />
        </v-col>
      </v-row>

      <v-row v-if="selectedDestinationNotListed" class="firstRow">
        <v-col cols="8">
          <text-field
            v-model="requestDetails['name']"
            label-text="Destination name"
            placeholder-text="Enter the destination name"
            required
            :rules="[rules.required]"
            input-type="text"
            height="40"
          />
        </v-col>
      </v-row>

      <v-row class="thirdRow mb-0 mt-3">
        <v-col cols="8" class="py-6">
          <label class="text-h5 mb-0">
            Did the Client request to have this destination available?
          </label>
          <v-radio-group
            v-model="requestDetails['client_request']"
            column
            mandatory
            class="mt-0"
          >
            <v-radio value="true" color="primary darken-1" :ripple="false">
              <template #label>
                <span class="black--text">Yes</span>
              </template>
            </v-radio>
            <v-radio value="false" color="primary darken-1" :ripple="false">
              <template #label>
                <span class="black--text">No</span>
              </template>
            </v-radio>
          </v-radio-group>
        </v-col>
      </v-row>

      <v-row class="fourthRow">
        <v-col cols="8" class="pt-5">
          <label class="text-h5 mb-0">
            Does the Client have an account for this destination?
          </label>
          <v-radio-group
            v-model="requestDetails['client_account']"
            column
            mandatory
            class="mt-0"
          >
            <v-radio value="true" color="primary darken-1" :ripple="false">
              <template #label>
                <span class="black--text">Yes</span>
              </template>
            </v-radio>
            <v-radio value="false" color="primary darken-1" :ripple="false">
              <template #label>
                <span class="black--text">No</span>
              </template>
            </v-radio>
          </v-radio-group>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" class="textAreaDiv pt-6">
          <div
            class="
              primary
              lighten-1
              border-all
              black--border
              border--lighten-2
              rounded
              pa-5
            "
          >
            <label class="d-flex text-h5 mb-2">
              What is the use case for this destination?
            </label>

            <v-textarea
              v-model="requestDetails['use_case']"
              solo
              flat
              hide-details
              class="text-body-2"
              placeholder="Please explain the specifics around this request"
            />
          </div>
        </v-col>
      </v-row>
    </v-form>

    <hux-footer slot="footer" max-width="850px" data-e2e="footer">
      <template #left>
        <hux-button
          size="large"
          variant="white"
          is-tile
          class="
            text-button
            ml-auto
            primary--text
            mr-3
            btn-border
            box-shadow-none
          "
          data-e2e="cancel-destination-request"
          @click="cancel()"
        >
          Cancel & return
        </hux-button>
      </template>
      <template #right>
        <hux-button
          v-if="!showRequestForm"
          variant="primary"
          size="large"
          :is-tile="true"
          :is-disabled="!isFullyConfigured"
          @click="add()"
        >
          Add &amp; return
        </hux-button>

        <hux-button
          v-if="showRequestForm"
          variant="primary"
          size="large"
          :is-tile="true"
          :is-disabled="!isRequestFormValid"
          @click="request()"
        >
          Request
        </hux-button>
      </template>
    </hux-footer>

    <drawer v-model="drawer">
      <template #header-left>
        <div class="d-flex align-center">
          <hux-icon type="map" :size="32" class="ml-2 mr-3" />
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
        <div class="ma-3 font-weight-light px-3 pb-1">
          <div
            v-for="(value, category, index) in groupByCategory(
              enabledDestinations
            )"
            :key="`active-${index}`"
          >
            <label
              class="d-block text-body-2 black--text text--lighten-4 mb-2 mt-6"
            >
              {{ category }}
            </label>

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
              @click="onAddDestination(destination.id)"
            />
          </div>

          <v-divider class="black--border border--lighten-2 mt-7 mb-2" />

          <div
            v-for="(value, category, index) in groupByCategory(
              disabledDestinations
            )"
            :key="`nonActive-${index}`"
          >
            <label class="d-block text--body-2 mb-2 mt-6">{{ category }}</label>

            <card-horizontal
              v-for="destination in value"
              :key="destination.id"
              :title="destination.name"
              :icon="destination.type"
              :is-added="destination.is_added || isSelected(destination.id)"
              requested-button
              :is-available="destination.is_enabled"
              :is-already-added="destination.is_added"
              class="my-3"
              data-e2e="requestDestinationDrawer"
              @click="onRequestDestination(destination.id)"
            />
          </div>
          <div>
            <label class="d-block text--body-2 mb-2 mt-6"> Other </label>
            <card-horizontal
              title="Request a destination not on the list"
              :is-added="false"
              :is-available="false"
              :is-already-added="false"
              requested-button
              class="my-3"
              @click="onRequestDestination"
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
      @onConfirm="navigateAway()"
    />
  </page>
</template>

<script>
import { mapGetters, mapActions } from "vuex"

import { groupBy } from "@/utils"

import Page from "@/components/Page"
import CardHorizontal from "@/components/common/CardHorizontal"
import ConfirmModal from "@/components/common/ConfirmModal.vue"
import Drawer from "@/components/common/Drawer"
import huxButton from "@/components/common/huxButton"
import HuxFooter from "@/components/common/HuxFooter"
import HuxIcon from "@/components/common/Icon.vue"
import Logo from "@/components/common/Logo"
import TextField from "@/components/common/TextField"

import SFMC from "./Configuration/SFMC.vue"

import sortBy from "lodash/sortBy"
import Icon from "../../components/common/Icon.vue"

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
    HuxIcon,
    Icon,
  },
  data() {
    return {
      loading: false,
      drawer: false,
      selectedDestinationId: null,
      selectedDestinationNotListed: null,
      authenticationDetails: {},
      isValidated: false,
      isValidating: false,
      validationError: null,
      isAddFormValid: false,
      requestDetails: {
        contact_email: null,
        client_request: null,
        client_account: null,
        use_case: null,
      },
      isRequestFormValid: false,
      rules: {
        required: (value) => !!value || "This is a required field",
        validEmail: (value) =>
          /.+@.+\..+/.test(value) || "Please enter a valid email address",
      },
      selectedDataExtension: {},
      dataExtensions: [],
      showConfirmModal: false,
      navigateTo: false,
      flagForModal: false,
      DestinationUrl: null,
    }
  },

  computed: {
    ...mapGetters({
      destinations: "destinations/list",
      destination: "destinations/single",
      destinationConstants: "destinations/constants",
      userEmail: "users/getEmailAddress",
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

    isSFMCSelected() {
      return this.selectedDestination !== null
        ? this.selectedDestination.type === "sfmc"
        : false
    },

    isFullyConfigured() {
      return this.isSFMCSelected
        ? this.selectedDataExtension.performance_metrics_data_extension
        : this.isValidated
    },

    showAddForm() {
      return Boolean(
        this.selectedDestination &&
          this.destinationFields &&
          this.selectedDestination["is_enabled"]
      )
    },

    showRequestForm() {
      return Boolean(
        (this.selectedDestination && !this.selectedDestination["is_enabled"]) ||
          this.selectedDestinationNotListed
      )
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

    this.resetAddForm()
    this.resetRequestForm()

    this.loading = false
  },

  methods: {
    ...mapActions({
      getDestinationConstants: "destinations/constants",
      getDestinations: "destinations/getAll",
      getDestination: "destinations/get",
      addDestination: "destinations/add",
      validateDestination: "destinations/validate",
      requestDestination: "destinations/request",
    }),

    navigateAway() {
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

    onAddDestination(id) {
      this.selectedDestinationId = id
      this.resetAddForm()
      this.authenticationDetails = {}
      this.drawer = false
    },

    onRequestDestination(id) {
      this.resetRequestForm()
      if (id) {
        this.selectedDestinationId = id
      } else {
        this.selectedDestinationNotListed = true
      }
      this.drawer = false
    },

    resetAddForm() {
      this.isValidated = false
      this.selectedDataExtension = {}
    },

    resetRequestForm() {
      this.selectedDestinationId = null
      this.selectedDestinationNotListed = null
      this.requestDetails = {
        contact_email: this.userEmail,
        client_request: null,
        client_account: null,
        use_case: null,
      }
    },

    async validate() {
      this.isValidating = true
      this.validationError = null

      try {
        const response = await this.validateDestination({
          type: this.selectedDestination.type,
          authentication_details: this.authenticationDetails,
        })
        if (this.isSFMCSelected) {
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
          link: this.DestinationUrl,
        }
        if (this.isSFMCSelected) {
          data.configuration = this.selectedDataExtension
        }
        await this.addDestination(data)
        this.flagForModal = true
        this.$router.push({ name: "Destinations" })
      } catch (error) {
        console.error(error)
      }
    },

    async request() {
      try {
        let requestedDestination = {}
        if (this.selectedDestination) {
          requestedDestination = {
            name: this.selectedDestination.name,
          }
        }
        const data = {
          ...requestedDestination,
          ...this.requestDetails,
        }
        await this.requestDestination(data)
        this.flagForModal = true
        this.$router.push({ name: "Destinations" })
      } catch (error) {
        console.error(error)
      }
    },

    cancel() {
      this.flagForModal = true
      this.$router.push({ name: "Destinations" })
    },
  },
}
</script>

<style lang="scss" scoped>
.add-destination-container {
  height: calc(100vh - 150px) !important;
  overflow: auto;
  ::v-deep .container {
    padding-bottom: 37px !important;
    margin-bottom: 24px !important;
    height: auto !important;
    overflow: hidden !important;
  }
}
.firstRow {
  height: 80px;
}
.thirdRow {
  height: 96px;
}
.fourthRow {
  height: 102px;
}
.textAreaDiv {
  height: 200px;
}
::v-deep .theme--light.v-input {
  color: var(--v-black-lighten4) !important;
}
::v-deep .theme--light.v-input input {
  color: var(--v-black-lighten4) !important;
}
::v-deep .v-text-field__slot textarea {
  font-size: 16px !important;
  color: var(--v-black-lighten4) !important;
}
</style>
