<template>
  <div class="add-destination-wrapper font-weight-regular">
    <span class="neroBlack--text text-caption">Extension type</span>
    <div class="d-flex align-center mt-2">
      <div
        class="extension-type mr-4 text-center"
        v-bind:class="[isActive ? 'active' : '']"
        @click="toggleClass($event)"
      >
        <div class="child mt-4">
          <div class="icon">
            <v-icon color="info" size="44" class="ml-2" v-if="isActive">
              mdi-check-circle
            </v-icon>
          </div>
          <extensionInactive1 v-if="!isActive" />
          <div class="label primary--text">New data extension</div>
        </div>
      </div>
      <diV
        class="extension-type mr-4 text-center"
        v-bind:class="[!isActive ? 'active' : '']"
        @click="toggleClass($event)"
      >
        <div class="child mt-4">
          <div class="icon">
            <v-icon color="info" size="44" class="ml-2" v-if="!isActive">
              mdi-check-circle
            </v-icon>
          </div>
          <extensionInactive2 v-if="isActive" />
          <div class="label primary--text">Existing data extension</div>
        </div>
      </diV>
    </div>

    <div class="mt-6" v-if="isActive">
      <div>
        <label class="d-flex align-items-center">
          <span class="neroBlack--text text-caption">Journey type</span>
          <v-tooltip top>
            <template v-slot:activator="{ on, attrs }">
              <v-icon
                color="primary"
                size="small"
                class="ml-2"
                v-bind="attrs"
                v-on="on"
              >
                mdi-alert-circle-outline
              </v-icon>
            </template>
            <span> Type of journey </span>
          </v-tooltip>
        </label>
        <v-radio-group v-model="journeyType" row>
          <v-radio value="radio-1">
            <template v-slot:label>
              <div class="darkGreyHeading--text text-caption">
                Automated (Batched)
              </div>
            </template>
          </v-radio>
          <v-radio value="radio-2" :disabled="true">
            <template v-slot:label>
              <div class="text-caption">Triggered (API) - coming soon</div>
            </template>
          </v-radio>
        </v-radio-group>
      </div>
      <TextField
        v-model="extension"
        labelText="Data extension name"
        icon="mdi-alert-circle-outline"
        placeholderText="What is the name for this new data extension?"
        helpText="Extension name"
        height="40"
        backgroundColor="white"
        class="mt-1 aud-name-field text-caption neroBlack--text pt-2"
        required
      ></TextField>
    </div>

    <div class="mt-6" v-if="!isActive">
      <label
        class="d-flex align-items-center mb-2 neroBlack--text text-caption"
      >
        Existing data extension
      </label>
      <v-select
        :items="items"
        placeholder="Select an existing data extension "
        dense
        outlined
      ></v-select>

      <v-card elevation="1">
        <v-card-text>
          <v-row align="center" class="mx-0">
            <v-icon color="info" size="15" class="mr-2">
              mdi-message-alert
            </v-icon>
            <div class="feedback info--text">FEEDBACK</div>
            <div class="mx-2">
              Modifying this data extension may impact any independent journey.
            </div>
          </v-row>
        </v-card-text>
      </v-card>
    </div>
  </div>
</template>
<script>
import TextField from "@/components/common/TextField"
import extensionInactive1 from "../../assets/logos/extension-inactive-1.svg"
import extensionInactive2 from "../../assets/logos/extension-inactive-2.svg"
export default {
  name: "AddDestination",
  components: { TextField, extensionInactive1, extensionInactive2 },
  data() {
    return {
      isActive: true,
      journeyType: "radio-1", // TODO - with API integration
      extension: null,
      items: ["Item 1", "Item 2", "Item 3", "Item 4"],
    }
  },
  methods: {
    toggleClass: function (event) {
      if (!event.currentTarget.classList.contains("active")) {
        this.isActive = !this.isActive
      }
    },
  },
}
</script>
<style lang="scss" scoped>
.add-destination-wrapper {
  .extension-type {
    height: 100px;
    width: 196px;
    left: 24px;
    top: 126px;
    border-radius: 4px;
    background: var(--v-white-base);
    border: 1px solid var(--v-lightGrey-base);
    box-sizing: border-box;
    &.active {
      border: 1px solid var(--v-primary-base);
    }
    .child {
      .label {
        color: var(--v-darkBlue-base);
      }
    }
  }
  .feedback {
    font-weight: 800;
    font-size: 16px;
  }
}
</style>
