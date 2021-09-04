<template>
  <drawer
    v-model="localToggle"
    class="data-extension-drawer"
    :loading="loading"
  >
    <template #header-left>
      <div class="d-flex align-baseline">
        <h3 class="text-h3 pr-2 d-flex align-center">
          <logo type="sfmc" />
          <div class="pl-2 font-weight-light">Salesforce Marketing Cloud</div>
        </h3>
      </div>
    </template>

    <template #default>
      <v-form ref="extensionRef" v-model="isFormValid">
        <div class="add-destination-wrapper pa-2 font-weight-regular">
          <span class="neroBlack--text text-caption">Extension type</span>
          <div class="d-flex align-center mt-2">
            <div
              class="extension-type mr-4 text-center"
              :class="[isActive ? 'active' : '']"
              @click="toggleClass($event)"
            >
              <div class="child mt-4">
                <div class="icon d-flex justify-center">
                  <div v-if="isActive" class="check-wrap d-flex align-center">
                    <v-icon color="white" size="21"> mdi-check-bold </v-icon>
                  </div>
                </div>
                <extensionInactive1 v-if="!isActive" />
                <div
                  class="label primary--text"
                  :class="[isActive ? 'mt-2' : 'mt-1']"
                >
                  New data extension
                </div>
              </div>
            </div>
            <diV
              class="extension-type mr-4 text-center"
              :class="[!isActive ? 'active' : '']"
              @click="toggleClass($event)"
            >
              <div class="child mt-4">
                <div class="icon d-flex justify-center">
                  <div v-if="!isActive" class="check-wrap d-flex align-center">
                    <v-icon color="white" size="21"> mdi-check-bold </v-icon>
                  </div>
                </div>
                <extensionInactive2 v-if="isActive" />
                <div
                  class="label primary--text"
                  :class="[!isActive ? 'mt-2' : 'mt-1']"
                >
                  Existing data extension
                </div>
              </div>
            </diV>
          </div>

          <div v-if="isActive" class="mt-6">
            <div>
              <label class="d-flex align-items-center">
                <span class="neroBlack--text text-caption">Journey type</span>
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
                    <div class="text-caption">
                      Triggered (API) - coming soon
                    </div>
                  </template>
                </v-radio>
              </v-radio-group>
            </div>
            <text-field
              v-model="extension"
              label-text="Data extension name"
              icon="mdi-alert-circle-outline"
              placeholder="What is the name for this new data extension?"
              :help-text="tooltipText"
              height="40"
              background-color="white"
              class="mt-1 text-caption neroBlack--text pt-2"
              :rules="newExtensionRules"
              required
            />
          </div>

          <div v-else class="mt-6 data-extension">
            <label
              class="
                d-flex
                align-items-center
                mb-2
                neroBlack--text
                text-caption
              "
            >
              Existing data extension
            </label>

            <v-select
              v-model="extension"
              :items="dataExtensionNames"
              placeholder="Select an existing data extension"
              dense
              outlined
              background-color="white"
              append-icon="mdi-chevron-down"
              required
            />
          </div>
        </div>
      </v-form>
      <v-card
        v-if="!isActive"
        height="56"
        class="feedback-card shadow mt-5 rounded-0"
      >
        <v-card-text class="mt-4">
          <v-row align="center" class="mx-0">
            <v-icon color="info" size="15" class="mr-2">
              mdi-message-alert
            </v-icon>
            <div class="text-body-1 primary--text text--lighten-8 font-weight-bold">
              FEEDBACK
            </div>
            <div class="mx-2 darkGrey--text text-caption">
              Modifying this data extension may impact any independent journey.
            </div>
          </v-row>
        </v-card-text>
      </v-card>
    </template>

    <template #footer-right>
      <div class="d-flex align-baseline">
        <hux-button
          variant="primary"
          is-tile
          width="80"
          height="40"
          class="ma-2"
          :is-disabled="isActive ? !isFormValid : !extension"
          @click="addDestination()"
        >
          Add
        </hux-button>
      </div>
    </template>

    <template #footer-left>
      <div class="d-flex align-baseline">
        <hux-button
          variant="white"
          is-tile
          width="80"
          height="40"
          class="ma-2 drawer-back"
          @click="onBack()"
        >
          Back
        </hux-button>
      </div>
    </template>
  </drawer>
</template>
<script>
import { mapGetters, mapActions } from "vuex"
import Drawer from "@/components/common/Drawer"
import HuxButton from "@/components/common/huxButton"
import Logo from "@/components/common/Logo"
import TextField from "@/components/common/TextField"
import extensionInactive1 from "@/assets/logos/extension-inactive-1.svg"
import extensionInactive2 from "@/assets/logos/extension-inactive-2.svg"
export default {
  name: "DestinationDataExtensionDrawer",

  components: {
    Drawer,
    HuxButton,
    Logo,
    TextField,
    extensionInactive1,
    extensionInactive2,
  },

  props: {
    value: {
      type: Object,
      required: true,
    },

    toggle: {
      type: Boolean,
      required: false,
      default: false,
    },

    selectedDestination: {
      required: true,
    },

    selectedAudienceId: {
      required: true,
    },
  },

  data() {
    return {
      isActive: true,
      journeyType: "radio-1", // TODO: HUS-546  with API integration
      extension: null,
      loading: false,
      localToggle: false,
      isFormValid: false,
      newExtensionRules: [
        (v) => !!v || "Data extension name is required",
        (v) =>
          // eslint-disable-next-line no-useless-escape
          /^[^!@#$%^*()={}\/.<>":?|,_&]*$/.test(v) ||
          // eslint-disable-next-line no-useless-escape
          "You can’t include the following characters in the name and field name of a data extension: ! @ # $ % ^ * ( ) = { } [ ] \ . < > / : ? | , _ &",
        (v) => {
          // Checks if data extension name is unique
          let trimmedValue = v ? v.trim() : ""
          return (
            this.dataExtensionNames.findIndex(
              (each) => each.text === trimmedValue
            ) === -1
          )
        },
      ],
      existingExtensionRules: [(v) => !!v || "Select any one Data extension"],
      tooltipText:
        "When creating a new journey in Salesforce Marketing Cloud, look for the name input here when searching Data Extension Entry Source in Salesforce Marketing Cloud.",
    }
  },

  computed: {
    ...mapGetters({
      dataExtensions: "destinations/dataExtensions",
    }),

    dataExtensionNames() {
      return this.dataExtensions.map((each) => {
        return {
          text: each.name,
          value: each,
        }
      })
    },
  },

  watch: {
    toggle(value) {
      this.localToggle = value
    },

    async localToggle(value) {
      this.$emit("onToggle", value)
      if (value) {
        await this.getDataExtensions(this.selectedDestination.id)
      }
    },
  },
  methods: {
    ...mapActions({
      getDataExtensions: "destinations/dataExtensions",
      addDataExtension: "destinations/addDataExtension",
    }),

    resetForm() {
      this.$nextTick(() => {
        this.extension = null
        this.journeyType = "radio-1"
      })
    },

    toggleClass: function (event) {
      if (!event.currentTarget.classList.contains("active")) {
        this.isActive = !this.isActive
      }
      this.resetForm()
    },

    async addDestination() {
      let destinationWithDataExtension = JSON.parse(
        JSON.stringify(this.selectedDestination)
      )

      if (typeof this.extension !== "object") {
        const requestBody = {
          id: destinationWithDataExtension.id,
          data_extension: this.extension,
        }
        let response = await this.addDataExtension(requestBody)
        destinationWithDataExtension.delivery_platform_config = {
          data_extension_name: response.name,
        }
      } else {
        destinationWithDataExtension.delivery_platform_config = {
          data_extension_name: this.extension.name,
        }
      }
      this.value[this.selectedAudienceId].destinations.push({
        id: destinationWithDataExtension.id,
        delivery_platform_config: {
          data_extension_name:
            destinationWithDataExtension.delivery_platform_config
              .data_extension_name,
        },
      })
      this.$emit("updateDestination", {
        destination: {
          id: destinationWithDataExtension.id,
          delivery_platform_config: {
            data_extension_name:
              destinationWithDataExtension.delivery_platform_config
                .data_extension_name,
          },
        },
      })
      this.onBack()
    },

    onBack() {
      this.$refs.extensionRef.reset()
      this.resetForm()
      this.$emit("onBack", this.selectedAudienceId)
    },
  },
}
</script>
<style lang="scss" scoped>
.data-extension-drawer {
  .check-wrap {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    background: var(--v-primary-lighten8);
    padding: 11px;
  }
  .add-destination-wrapper {
    .check-wrap {
      width: 42px;
      height: 42px;
      border-radius: 50%;
      background: var(--v-primary-lighten8);
      padding: 11px;
    }
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
    .data-extension {
      ::v-deep .v-input {
        .v-input__control {
          .v-input__slot {
            min-height: 40px;
            fieldset {
              color: var(--v-lightGrey-base) !important;
              border-width: 1px !important;
            }
          }
          .v-text-field__details {
            display: none;
          }
        }
      }
    }
    .v-input {
      ::v-deep ::placeholder {
        color: var(--v-gray-base) !important;
      }
    }
  }
  .feedback-card {
    left: 0;
    position: absolute;
    width: 100%;
  }
}
</style>
