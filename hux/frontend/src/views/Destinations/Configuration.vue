<template>
  <div class="add-destination--wrap font-weight-regular">
    <div class="mb-10">
      <h4 class="text-h4 font-weight-light">Add a destination</h4>
      <p>Please fill out the information below to connect a new destination.</p>
    </div>

    <label class="d-flex mb-2">Select a destination</label>

    <div class="d-flex align-center mb-10">
      <template v-if="isDestinationSelected">
        <Logo :type="destination.type" />
        <span class="pl-2">
          {{ destination.name }}
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
            cols="6"
            v-for="item in Object.values(destination.auth_details)"
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
              @blur="resetValidation"
              icon="mdi-alert-circle-outline"
              class="mb-0"
            ></TextField>
          </v-col>
        </v-row>
      </div>
      <div class="d-flex flex-wrap justify-end">
        <hux-button
          v-if="!isValidating"
          :button-text="isValidated ? 'Success!' : 'Validate connection'"
          :icon="isValidated ? 'mdi-check' : null"
          :icon-position="isValidated ? 'left' : null"
          :variant="isValidated ? 'success' : 'primary'"
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
          @click="cancel()"
        ></hux-button>
      </template>
      <template v-slot:right>
        <hux-button
          button-text="Add &amp; return"
          variant="primary"
          size="large"
          v-bind:isTile="true"
          v-bind:isDisabled="!isValidated"
          @click="add()"
        ></hux-button>
      </template>
    </hux-footer>

    <drawer v-model="drawer">
      <template v-slot:header-left>
        <div class="d-flex align-baseline">
          <h5 class="text-h5 font-weight-regular pr-2">Select a destination</h5>
          <p class="mb-0">(select one)</p>
        </div>
      </template>
      <template v-slot:footer-left>
        <div class="d-flex align-baseline">
          <p class="font-weight-regular mb-0">
            {{ destinations.length }} results
          </p>
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
            @click="onSelectDestination(index)"
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
      selectedDestinationIndex: -1,
      isValidated: false,
      isValidating: false,
      isFormValid: false,
      rules: {
        required: (value) => !!value || "This is a required field",
      },
    }
  },

  computed: {
    ...mapGetters({
      destinations: "destinations/list",
    }),

    destination() {
      return this.destinations[this.selectedDestinationIndex] || null
    },

    isDestinationSelected() {
      return Boolean(this.destination)
    },
  },

  methods: {
    ...mapActions({
      getDestinations: "destinations/getAll",
      getDestination: "destinations/get",
      addDestination: "destinations/add",
      validateDestination: "destinations/validate",
    }),

    toggleDrawer() {
      this.drawer = !this.drawer
    },

    onSelectDestination(index) {
      this.selectedDestinationIndex = index
      this.isValidated = false
      setTimeout(() => (this.drawer = false), 470)
    },

    resetValidation() {
      this.isValidated = false
    },

    async validate() {
      this.isValidating = true

      try {
        await this.validateDestination(this.destination)
        this.isValidated = true
      } catch (error) {
        // TODO we probably want to do more here when things arent valid
        console.error(error)
      } finally {
        this.isValidating = false
      }
    },

    async add() {
      try {
        await this.addDestination(this.destination)
        this.$router.push({ name: "connections" })
      } catch (error) {
        console.error(error)
      }
    },

    cancel() {
      // TODO: need to add modal that confirms to leave configuration
      this.$router.push({ name: "connections" })
    },
  },

  async mounted() {
    await this.getDestinations()
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
