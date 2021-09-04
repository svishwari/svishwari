<template>
  <page class="white" max-width="970px">
    <div class="mb-10">
      <h4 class="text-h2 neroBlack--text">Add a destination</h4>
      <p class="neroBlack--text">
        Please fill out the information below to connect a new destination.
      </p>
    </div>

    <label class="d-flex mb-2 neroBlack--text">Select a destination</label>

    <div class="d-flex align-center mb-10">
      <template v-if="selectedDestination">
        <logo :type="selectedDestination.type" />
        <span class="pl-2">{{ selectedDestination.name }}</span>
        <a class="pl-2" color="primary" @click="toggleDrawer()">Change</a>
      </template>
      <template v-else>
        <v-btn fab x-small color="primary" @click="toggleDrawer()">
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

    <hux-footer slot="footer" max-width="850px">
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
        <div class="d-flex align-baseline">
          <h5 class="text-h3 pr-2 neroBlack--text">Select a destination</h5>
          <span class="text-caption gray--text">(select one)</span>
        </div>
      </template>
      <template #footer-left>
        <div class="d-flex align-baseline">
          <span class="text-caption gray--text">
            {{ destinations.length }} results
          </span>
        </div>
      </template>
      <template #default>
        <div class="ma-3 font-weight-light">
          <card-horizontal
            v-for="destination in enabledDestinations"
            :key="destination.id"
            :title="destination.name"
            :icon="destination.type"
            :is-added="destination.is_added || isSelected(destination.id)"
            :is-available="destination.is_enabled"
            :is-already-added="destination.is_added"
            class="my-3"
            @click="onSelectDestination(destination.id)"
          />

          <v-divider style="border-color: var(--v-zircon-base)" />

          <card-horizontal
            v-for="destination in disabledDestinations"
            :key="destination.id"
            :title="destination.name"
            :icon="destination.type"
            :is-added="destination.is_added || isSelected(destination.id)"
            hide-button
            :is-available="destination.is_enabled"
            :is-already-added="destination.is_added"
            class="my-3"
          >
            <i class="font-weight-light letter-spacing-sm">Coming soon</i>
          </card-horizontal>
        </div>
      </template>
    </drawer>
  </page>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import Page from "@/components/Page"
import Drawer from "@/components/common/Drawer"
import CardHorizontal from "@/components/common/CardHorizontal"
import Logo from "@/components/common/Logo"
import huxButton from "@/components/common/huxButton"
import HuxFooter from "@/components/common/HuxFooter"
import TextField from "@/components/common/TextField"

import SFMC from "./Configuration/SFMC.vue"

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
  },

  data() {
    return {
      loading: false,
      drawer: false,
      selectedDestinationId: null,
      authenticationDetails: {},
      isValidated: false,
      isValidating: false,
      validationError: null,
      isFormValid: false,
      rules: {
        required: (value) => !!value || "This is a required field",
      },
      selectedDataExtension: null,
      dataExtensions: [],
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
      return this.destinationConstants[this.selectedDestination.type] || null
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
        ? this.selectedDataExtension !== null
        : this.isValidated
    },
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

    setExtension(data) {
      this.selectedDataExtension = data
    },

    toggleDrawer() {
      this.drawer = !this.drawer
    },

    isSelected(id) {
      return this.selectedDestination && this.selectedDestination.id === id
    },

    onSelectDestination(id) {
      this.selectedDestinationId = id
      this.reset()
      this.authenticationDetails = {}
      this.drawer = false
    },

    reset() {
      this.isValidated = false
      this.selectedDataExtension = null
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
          data.perf_data_extension = this.selectedDataExtension
        }
        await this.addDestination(data)
        this.$router.push({ name: "Connections" })
      } catch (error) {
        console.error(error)
      }
    },

    cancel() {
      // TODO: need to add modal that confirms to leave configuration
      this.$router.push({ name: "Connections" })
    },
  },
}
</script>

<style lang="scss" scoped>
.destination-auth-wrap {
  border: 1px solid var(--v-zircon-base) !important;
}
</style>
