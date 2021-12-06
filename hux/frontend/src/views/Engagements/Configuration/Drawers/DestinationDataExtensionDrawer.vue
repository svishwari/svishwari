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
        <div class="add-destination-wrapper ma-6 font-weight-regular">
          <div class="black--text text-body-1">Extension type</div>
          <div class="d-flex align-center mt-2">
            <div
              class="cursor-pointer px-10 py-4 text-center mr-6 rounded-lg"
              :class="[isActive ? 'active' : 'box-shadow-1']"
              @click="toggleClass($event)"
            >
              <icon
                type="new-data-extension"
                :color="isActive ? 'primary' : 'black'"
                :variant="isActive ? 'lighten6' : ''"
                :size="40"
              />
              <div
                class="mt-2 text-button"
                :class="isActive ? 'primary--text text--lighten-6' : ''"
              >
                New data extension
              </div>
              <div class="pt-2 black--text text--lighten-4 text-body-2">
                Create a brand new data extension
              </div>
            </div>
            <div
              class="cursor-pointer px-10 py-4 text-center rounded-lg"
              :class="[!isActive ? 'active' : 'box-shadow-1']"
              @click="toggleClass($event)"
            >
              <icon
                type="existing-data-extension"
                :color="!isActive ? 'primary' : 'black'"
                :variant="!isActive ? 'lighten6' : ''"
                :size="40"
              />
              <div
                class="mt-2 text-button"
                :class="!isActive ? 'primary--text text--lighten-6' : ''"
              >
                Existing data extension
              </div>
              <div class="pt-2 black--text text--lighten-4 text-body-2">
                Select an existing data extension schema
              </div>
            </div>
          </div>

          <div v-if="isActive" class="mt-6">
            <div class="black--text text-body-1">Journey type</div>
            <v-radio-group v-model="journeyType" row>
              <v-radio value="radio-1">
                <template #label>
                  <div class="black--text text-body-1">Batch delivery</div>
                </template>
              </v-radio>
              <v-radio value="radio-2" disabled>
                <template #label>
                  <div class="text-caption">
                    API event - <span class="font-italic">coming soon</span>
                  </div>
                </template>
              </v-radio>
            </v-radio-group>
            <text-field
              v-model="extension"
              label-text="Data extension name"
              icon="mdi-alert-circle-outline"
              placeholder-text="What is the name for this new data extension?"
              :help-text="tooltipText"
              height="40"
              background-color="white"
              class="
                mt-1
                text-caption
                black--text
                text--darken-4
                pt-2
                input-placeholder
              "
              :rules="newExtensionRules"
              required
              data-e2e="new-data-extension"
            />
          </div>

          <div v-else class="mt-6 data-extension">
            <div class="existing-banner-notice">
              <icon type="Bulb" color="yellow" />
              <div class="black--text text-body-1 ml-1">
                Modifying this data extension may impact any independent journey
                in Salesforce.
              </div>
            </div>
            <div class="black--text text-body-1 pb-2">
              Select an existing data extension
            </div>
            <div class="data-extension-filter">
              <icon
                type="search"
                color="black"
                variant="lighten4"
                :size="16"
                class="mr-2"
              />
              <input
                v-model="filterDataExtensionInput"
                placeholder="Find a specific data extension"
              />
            </div>
          </div>
        </div>
        <hux-data-table
          v-show="!isActive"
          :columns="dataExtensionHeaders"
          :data-items="filteredDataExtensions"
        >
          <template #row-item="{ item }">
            <td
              v-for="(col, index) in dataExtensionHeaders"
              :key="index"
              :style="{ width: col.width, height: col.height }"
              class="text-body-1"
            >
              <template v-if="col.value === 'data_extension_id'">
                <input
                  v-model="selectedDataExtension"
                  type="radio"
                  name="selectedDataExtension"
                  class="data-extension-radio"
                  required
                  :checked="item[col.value] === selectedDataExtension"
                  :value="item['name']"
                />
              </template>
              <template v-if="col.value === 'create_time'">
                {{ item[col.value] | Date("relative") | Empty }}
              </template>
              <template v-if="col.value === 'name'">
                {{ item[col.value] }}
              </template>
            </td>
          </template>
        </hux-data-table>
      </v-form>
    </template>

    <template #footer-right>
      <div class="d-flex align-baseline">
        <hux-button
          variant="primary"
          is-tile
          width="80"
          height="40"
          class="ma-2"
          :is-disabled="
            isActive ? !isFormValid : selectedDataExtension === null
          "
          data-e2e="destination-added"
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
          size="large"
          is-tile
          width="80"
          height="40"
          class="ma-2 drawer-back btn-border box-shadow-none"
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
import Icon from "@/components/common/Icon"
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import TextField from "@/components/common/TextField"
export default {
  name: "DestinationDataExtensionDrawer",

  components: {
    Drawer,
    HuxButton,
    Logo,
    TextField,
    HuxDataTable,
    Icon,
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
      filterDataExtensionInput: "",
      selectedDataExtension: null,
      dataExtensionHeaders: [
        {
          text: " ",
          value: "data_extension_id",
          width: "60px",
          height: "40px",
        },
        {
          text: "Data extension name",
          value: "name",
          width: "270px",
          height: "40px",
        },
        {
          text: "Created date",
          value: "create_time",
          width: "250px",
          height: "40px",
        },
      ],
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
            this.dataExtensions.findIndex(
              (each) => each.name === trimmedValue
            ) === -1
          )
        },
      ],
      tooltipText:
        "When creating a new journey in Salesforce Marketing Cloud, look for the name input here when searching Data Extension Entry Source in Salesforce Marketing Cloud.",
    }
  },

  computed: {
    ...mapGetters({
      dataExtensions: "destinations/dataExtensions",
    }),

    filteredDataExtensions() {
      return this.dataExtensions.filter((each) =>
        each.name
          .toLowerCase()
          .includes(this.filterDataExtensionInput.toLowerCase())
      )
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
        this.selectedDataExtension = null
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

      if (this.isActive) {
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
          data_extension_name: this.selectedDataExtension,
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
  .add-destination-wrapper {
    .active {
      border: 1px solid var(--v-primary-lighten6);
    }
    .data-extension {
      ::v-deep .v-input {
        .v-input__control {
          .v-input__slot {
            min-height: 40px;
            fieldset {
              color: var(--v-black-lighten3) !important;
              border-width: 1px !important;
            }
            input::placeholder {
              color: var(--v-black-darken1) !important;
            }
            .v-input__prepend-inner {
              margin-top: 12px;
            }
          }
          .v-text-field__details {
            display: none;
          }
        }
      }
      .existing-banner-notice {
        display: flex;
        background: var(--v-yellow-lighten1);
        border: 1px solid var(--v-black-lighten1);
        align-items: center;
        padding: 14px 22px 14px 16px;
        margin-bottom: 24px;
      }
      .data-extension-filter {
        display: flex;
        align-items: center;
        border: 1px solid var(--v-black-lighten3);
        padding: 8px 16px;
        border-radius: 4px;
        margin-bottom: 16px;
        input {
          outline: none;
          width: 100%;
          &::placeholder {
            color: var(--v-black-lighten4);
          }
        }
      }
    }
    .input-placeholder {
      ::v-deep .v-text-field {
        .v-text-field__slot {
          label {
            color: var(--v-black-darken1) !important;
          }
        }
      }
    }
  }
  .data-extension-radio {
    width: 20px;
    height: 20px;
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;
    border: 1px solid var(--v-black-lighten4);
    border-radius: 50%;

    &:checked {
      &::before {
        content: " \25CF";
        font-size: 24px;
        color: var(--v-primary-base);
        position: relative;
        top: -4px;
        left: 2px;
      }
    }
  }
}
</style>
