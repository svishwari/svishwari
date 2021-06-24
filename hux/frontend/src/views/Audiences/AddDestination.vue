<template>
  <div class="add-destination-wrapper font-weight-regular">
    <v-form
      @input="validateForm()"
      ref="addDestinationRef"
      v-model="newEngagementValid"
    >
      <span class="neroBlack--text text-caption">Extension type</span>
      <div class="d-flex align-center mt-2">
        <div
          class="extension-type mr-4 text-center"
          :class="[isActive ? 'active' : '']"
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
          :class="[!isActive ? 'active' : '']"
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
              <template #activator="{ on, attrs }">
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
              <template #label>
                <div class="darkGreyHeading--text text-caption">
                  Automated (Batched)
                </div>
              </template>
            </v-radio>
            <v-radio value="radio-2" :disabled="true">
              <template #label>
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
          class="mt-1 text-caption neroBlack--text pt-2"
          :rules="newEngagementRules"
          required
        />
      </div>

      <div class="mt-6" v-if="!isActive">
        <label
          class="d-flex align-items-center mb-2 neroBlack--text text-caption"
        >
          Existing data extension
        </label>

        <hux-dropdown
          class="extension-dropdown"
          :label="selectedLabel"
          :items="dropdownOptions"
          @on-select="onSelect($event)"
        />

        <v-card elevation="1">
          <v-card-text>
            <v-row align="center" class="mx-0">
              <v-icon color="info" size="15" class="mr-2">
                mdi-message-alert
              </v-icon>
              <div class="feedback info--text">FEEDBACK</div>
              <div class="mx-2">
                Modifying this data extension may impact any independent
                journey.
              </div>
            </v-row>
          </v-card-text>
        </v-card>
      </div>
    </v-form>
  </div>
</template>
<script>
import TextField from "@/components/common/TextField"
import HuxDropdown from "@/components/common/HuxDropdown.vue"
import extensionInactive1 from "../../assets/logos/extension-inactive-1.svg"
import extensionInactive2 from "../../assets/logos/extension-inactive-2.svg"
export default {
  name: "AddDestination",
  components: {
    TextField,
    extensionInactive1,
    extensionInactive2,
    HuxDropdown,
  },
  props: {
    dropdownItems: Array,
  },
  computed: {
    dropdownOptions() {
      return Object.keys(this.dropdownItems).map((key) => ({
        key: this.dropdownItems[key].data_extension_id,
        name: this.dropdownItems[key].name,
      }))
    },
  },
  data() {
    return {
      isActive: true,
      journeyType: "radio-1", // TODO - with API integration
      extension: null,
      items: ["Item 1", "Item 2", "Item 3", "Item 4"],
      newEngagementValid: false,
      newEngagementRules: [
        (v) => !!v || "Engagement name is required",
        (v) =>
          // eslint-disable-next-line no-useless-escape
          /^[^!@#$%^*()={}\/.<>":?|,_&]*$/.test(v) ||
          // eslint-disable-next-line no-useless-escape
          "You can’t include the following characters in the name and field name of a data extension: ! @ # $ % ^ * ( ) = { } [ ] \ . < > / : ? | , _ &",
      ],
      selectedLabel: "Select an existing data extension",
    }
  },
  methods: {
    toggleClass: function (event) {
      if (!event.currentTarget.classList.contains("active")) {
        this.isActive = !this.isActive
      }
    },
    validateForm() {
      this.$emit("onformchange", this.newEngagementValid)
    },
    onSelect(item) {
      this.selectedLabel = item.name
    },
    resetLabel() {
      this.selectedLabel = "Select an existing data extension"
    },
    resetForm: function () {
      this.resetLabel()
      this.isActive = true
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
      .v-icon {
        margin-top: -3px;
      }
      .label {
        color: var(--v-darkBlue-base);
      }
    }
  }
  .feedback {
    font-weight: 800;
    font-size: 16px;
  }
  ::v-deep .extension-dropdown {
    .main-button {
      min-width: 500px;
      margin: 0px !important;
      margin-bottom: 32px !important;
    }
  }
}
</style>
