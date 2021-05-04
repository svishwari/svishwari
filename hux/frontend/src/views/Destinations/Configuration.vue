<template>
  <div class="add-destination--wrap font-weight-regular white">
    <div class="mb-10">
      <h4 class="text-h4 font-weight-light">Add a destination</h4>
      <p>Please fill out the information below to connect a new destination.</p>
    </div>

    <label class="d-flex mb-2">Select a destination</label>

    <div class="d-flex align-center mb-10">
      <template v-if="isDestinationSelected">
        <Logo :type="destinations[selectedDestinationIndex].type" />
        <span class="pl-2">
          {{ destinations[selectedDestinationIndex].name }}
        </span>
        <a class="pl-2" color="primary" @click="toggleDrawer()">Change</a>
      </template>
      <template v-else>
        <v-btn fab x-small color="primary" @click="toggleDrawer()">
          <v-icon dark> mdi-plus </v-icon>
        </v-btn>
      </template>
    </div>

    <v-form v-model="isFormValid" v-if="isDestinationSelected">
      <div class="destination-auth-wrap background pa-5 rounded mb-10">
        <v-row>
          <v-col
            v-for="item in Object.values(
              destinations[selectedDestinationIndex].auth_details
            )"
            cols="6"
            :key="item.name"
          >
            <TextField
              :labelText="item.name"
              :rules="[rules.required]"
              :placeholderText="
                item.type == 'text' ? `Enter ${item.name}` : `**********`
              "
              :InputType="item.type"
              :help-text="item.description"
              @blur="changeValidationStatus"
              icon="mdi-alert-circle-outline"
              class="mb-0"
            ></TextField>
          </v-col>
        </v-row>
      </div>
      <div class="d-flex flex-wrap justify-end">
        <hux-button
          v-if="!isValidating"
          :button-text="
            isConnectionValidated ? 'Success!' : 'Validate connection'
          "
          :icon="isConnectionValidated ? 'mdi-check' : null"
          :icon-position="isConnectionValidated ? 'left' : null"
          :variant="isConnectionValidated ? 'success' : 'primary'"
          size="large"
          v-bind:isTile="true"
          v-bind:isDisabled="!isFormValid"
          @click="validate()"
        ></hux-button>
        <hux-button
          v-if="isValidating"
          class="processing-button"
          button-text="Validating..."
          variant="primary"
          size="large"
          v-bind:isTile="true"
        ></hux-button>
      </div>
    </v-form>

    <hux-footer>
      <template v-slot:left>
        <hux-button
          button-text="Cancel"
          variant="tertiary"
          size="large"
          v-bind:isTile="true"
          @click="cancelDestination()"
        ></hux-button>
      </template>
      <template v-slot:right>
        <hux-button
          button-text="Add &amp; return"
          variant="primary"
          size="large"
          v-bind:isTile="true"
          v-bind:isDisabled="!isConnectionValidated"
          @click="addDestination()"
        ></hux-button>
      </template>
    </hux-footer>

    <drawer v-model="drawer">
      <template v-slot:header-left>
        <div class="d-flex align-baseline">
          <h5 class="text-h5 font-weight-light pr-2">Select a destination</h5>
          <div class="font-weight-regular">(select one)</div>
        </div>
      </template>
      <template v-slot:footer-left>
        <div class="d-flex align-baseline">
          <div class="font-weight-regular">
            {{ destinations.length }} results
          </div>
        </div>
      </template>
      <template v-slot:default>
        <div class="ma-5">
          <CardHorizontal
            v-for="(destination, index) in destinations"
            :key="destination.id"
            :title="destination.name"
            :icon="destination.type"
            :isAdded="destination.is_added || index == selectedDestinationIndex"
            :isAvailable="destination.is_enabled"
            :isAlreadyAdded="destination.is_added"
            @click="onSingleDestinationClick(index)"
            class="my-3"
          />
        </div>
      </template>
    </drawer>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import Drawer from "@/components/common/Drawer"
import CardHorizontal from "@/components/common/CardHorizontal"
import Logo from "@/components/common/Logo"
import huxButton from "@/components/common/huxButton"
import HuxFooter from "@/components/common/HuxFooter"
import TextField from "@/components/common/TextField"

export default {
  name: "add-destination",

  components: {
    Drawer,
    CardHorizontal,
    HuxFooter,
    huxButton,
    TextField,
    Logo,
  },

  data() {
    return {
      drawer: false,
      selectedDestinationIndex: "-1",
      isConnectionValidated: false,
      isValidating: false,
      isFormValid: false,
      rules: {
        required: (value) => !!value || "This is a required field",
      },
    }
  },

  computed: {
    ...mapGetters(["destinations"]),

    isDestinationSelected() {
      if (this.selectedDestinationIndex === "-1") {
        return false
      }
      return true
    },
  },

  methods: {
    ...mapActions(["getAllDestinations"]),

    toggleDrawer() {
      this.drawer = !this.drawer
    },

    onSingleDestinationClick(index) {
      this.selectedDestinationIndex = index
      this.isConnectionValidated = false
      setTimeout(() => (this.drawer = false), 470)
    },

    validate() {
      this.isValidating = true
      // This is a TODO need to replace with actual API call
      setTimeout(() => {
        this.isValidating = false
        this.isConnectionValidated = true
      }, 2000)
    },

    changeValidationStatus() {
      this.isConnectionValidated = false
    },

    addDestination() {
      // This is a TODO need to replace with actual API call
      this.$router.push("/connections")
    },

    cancelDestination() {
      // This is a TODO need to add modal that confirms to leave configuration
      this.$router.push("/connections")
    },
  },

  async mounted() {
    await this.getAllDestinations()
  },
}
</script>

<style lang="scss" scoped>
.add-destination--wrap {
  padding: 4rem 10rem;

  .destination-auth-wrap {
    // This is a temporary fix need to find alternative
    border: 1px solid #e2eaec !important;
  }
}
</style>
