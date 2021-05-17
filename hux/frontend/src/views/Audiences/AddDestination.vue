<template>
  <diV class="add-destination-wrapper font-weight-regular">
    Extension type
    <div class="d-flex align-center mt-2">
      <diV
        class="extension-type mr-4 text-center"
        v-bind:class="[isActive ? 'active' : '']"
        @click="toggleClass($event)"
      >
        <div class="child mt-4">
          <div class="icon">
            <v-icon
                color="info"
                size="44"
                class="ml-2"
                v-if="isActive"
              >
                mdi-check-circle
              </v-icon>
          </div>
          <extensionInactive1  v-if="!isActive" />
          <div class="label">New data extension</div>
        </div>
      </diV>
      <diV
        class="extension-type mr-4 text-center"
        v-bind:class="[!isActive ? 'active' : '']"
        @click="toggleClass($event)"
      >
        <div class="child mt-4">
          <div class="icon">
            <v-icon
                color="info"
                size="44"
                class="ml-2"
                v-if="!isActive"
              >
                mdi-check-circle
              </v-icon>
          </div>
          <extensionInactive2  v-if="isActive" />
          <div class="label">Existing data extension</div>
        </div>
      </diV>
    </div>

    <div class="mt-6" v-if="isActive">
      <div>
        <label class="d-flex align-items-center">
          Journey type
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
          <v-radio label="Automated (Batched)" value="radio-1"></v-radio>
          <v-radio
            label="Triggered (API) - coming soon"
            value="radio-2"
            :disabled="true"
          ></v-radio>
        </v-radio-group>
      </div>
      <TextField
        v-model="Extension"
        labelText="Data extension name"
        icon="mdi-alert-circle-outline"
        placeholderText="What is the name for this new data extension?"
        helpText="Extension name"
      ></TextField>
    </div>

    <div class="mt-6" v-if="!isActive">
      <label class="d-flex align-items-center mb-2">
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
            <v-icon color="info" size="15" class="mr-2"> mdi-message-alert </v-icon>
            <div class="feedback info--text">FEEDBACK</div>
            <div class="mx-2">
              Modifying this data extension may impact any independent journey.
            </div>
          </v-row>
        </v-card-text>
      </v-card>
    </div>
  </diV>
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
      journeyType: null,
      Extension: null,
      items: ['Item 1', 'Item 2', 'Item 3', 'Item 4'],
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
    background: #ffffff;
    border: 1px solid #d0d0ce;
    box-sizing: border-box;
    &.active {
      border: 1px solid #005587;
    }
    .child {
      .label {
        color: #005587;
      }
    }
  }
  .feedback {
    font-weight: 800;
    font-size: 16px;
  }
}
</style>
