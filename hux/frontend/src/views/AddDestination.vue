<template>
  <div class="add-destination--wrap">
    <div class="pb-10">
      <h5 class="text-h5 font-weight-light">Add a destination</h5>
      <div class="font-weight-regular">
        Please fill out the information below to connect a new destination.
      </div>
    </div>
    <div>
      Select a destination
      <div v-if="isDestinationSelected" class="d-flex align-center">
        <Logo :type="destinations[selectedDestinationIndex].logo" />
        <div class="pl-2">
          {{ destinations[selectedDestinationIndex].title }}
        </div>
        <a class="pl-2" color="primary" @click="drawer = !drawer">Change</a>
      </div>
      <div v-else>
        <v-btn fab x-small color="primary" @click="drawer = !drawer">
          <v-icon dark> mdi-plus </v-icon>
        </v-btn>
      </div>
      <drawer style="transition-duration: 1s" v-model="drawer">
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
              v-for="(item, index) in destinations"
              :key="item.title"
              :title="item.title"
              :icon="item.logo"
              :isAdded="
                item.isAlreadyAdded || index == selectedDestinationIndex
              "
              :isAvailable="item.isAvailable"
              :isAlreadyAdded="item.isAlreadyAdded"
              @click="onSingleDestinationClick(index)"
              class="my-3"
            />
          </div>
        </template>
      </drawer>
      <div
        v-if="isDestinationSelected"
        class="d-flex flex-wrap background destination-auth-wrap mt-11 px-7 py-6 rounded-lg"
      >
        <v-form v-model="isFormValid" class="d-flex flex-wrap">
          <TextField
            v-for="item in destinations[selectedDestinationIndex].auth_details"
            :labelText="item.name"
            :key="item.name"
            :rules="[rules.required]"
            icon="mdi-alert-circle-outline"
            :placeholderText="item.type == 'text' ? item.name : '**********'"
            :InputType="item.type"
            @blur="changeValidationStatus"
            class="pa-2 validation-field"
          ></TextField>
        </v-form>
      </div>
      <div
        v-if="isDestinationSelected"
        class="d-flex flex-wrap justify-end mt-4"
      >
        <huxButton
          v-if="!isValidating"
          :ButtonText="
            isConnectionValidated ? 'Success!' : 'Validate connection'
          "
          :icon="isConnectionValidated ? 'mdi-check' : null"
          :iconPosition="isConnectionValidated ? 'left' : null"
          :variant="isConnectionValidated ? 'success' : 'primary'"
          size="large"
          v-bind:isTile="true"
          v-bind:isDisabled="!isFormValid"
          @click="validate()"
        ></huxButton>
        <huxButton
          v-if="isValidating"
          class="validating-connection"
          ButtonText="Validating..."
          variant="primary"
          size="large"
          v-bind:isTile="true"
        ></huxButton>
      </div>
    </div>
    <HuxFooter>
      <template v-slot:left>
        <huxButton
          ButtonText="Cancel"
          variant="tertiary"
          size="large"
          v-bind:isTile="true"
          @click="cancelDestination()"
        ></huxButton>
      </template>
      <template v-slot:right>
        <huxButton
          ButtonText="Add &amp; return"
          variant="primary"
          size="large"
          v-bind:isTile="true"
          v-bind:isDisabled="!isConnectionValidated"
          @click="addDestination"
        ></huxButton>
      </template>
    </HuxFooter>
  </div>
</template>

<script>
import Drawer from "@/components/common/Drawer"
import CardHorizontal from "@/components/common/CardHorizontal"
import Logo from "@/components/common/Logo"
import huxButton from "@/components/common/huxButton"
import HuxFooter from "@/components/common/HuxFooter"
import TextField from "@/components/common/TextField"
import { mapGetters } from "vuex"
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
    ...mapGetters({
      destinations: "AllDestinations",
    }),
    isDestinationSelected() {
      if (this.selectedDestinationIndex === "-1") {
        return false
      }
      return true
    },
  },
  methods: {
    onSingleDestinationClick: function (index) {
      this.selectedDestinationIndex = index
      this.isConnectionValidated = false
      setTimeout(() => (this.drawer = false), 470)
    },
    validate: function () {
      this.isValidating = true
      // This is a TODO need to replace with actual API call
      setTimeout(() => {
        this.isValidating = false
        this.isConnectionValidated = true
      }, 2000)
    },
    changeValidationStatus: function () {
      this.isConnectionValidated = false
    },
    addDestination: function () {
      // This is a TODO need to replace with actual API call
      this.$router.push("/connections")
    },
    cancelDestination: function () {
      // This is a TODO need to add modal that confirms to leave configuration
      this.$router.push("/connections")
    },
  },
}
</script>

<style lang="scss" scoped>
.add-destination--wrap {
  padding: 40px 13vw;
  .destination-auth-wrap {
    // This is a temporary fix need to find alternative
    border: 1px solid #e2eaec !important;
    .validation-field {
      min-width: 50%;
    }
  }
  .validating-connection {
    background-size: 300%;
    background-image: linear-gradient(
      270deg,
      #43b02a 11.98%,
      #00a3e0 50%,
      #005587 88%
    );
    animation: bg-animation 2s infinite;
    @keyframes bg-animation {
      0% {
        background-position: left;
      }
      50% {
        background-position: right;
      }
      100% {
        background-position: left;
      }
    }
  }
}
</style>
