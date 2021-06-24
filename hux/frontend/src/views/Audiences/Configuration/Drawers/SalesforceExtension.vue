<template>
  <Drawer v-model="localToggle" :loading="loading">
    <template #header-left>
      <div class="d-flex align-baseline">
        <h3 class="text-h3 pr-2 d-flex align-center">
          <Logo type="salesforce" />
          <div class="pl-2 font-weight-light">Salesforce Marketing Cloud</div>
        </h3>
      </div>
    </template>

    <template #default>
      <v-form ref="salesforceExtensionRef" v-model="isFormValid">
        <div class="add-destination-wrapper pa-2 font-weight-regular">
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
                    <div class="text-caption">
                      Triggered (API) - coming soon
                    </div>
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
              :rules="newExtensionRules"
              required
            />
          </div>

          <div class="mt-6" v-else>
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

            <HuxDropdown
              class="extension-dropdown"
              :label="selectedLabel"
              :items="dropdownOptions"
              @on-select="onSelect($event)"
            />

            <v-text-field
              class="d-none"
              v-model="extension"
              :rules="newExtensionRules"
              required
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
        </div>
      </v-form>
    </template>

    <template #footer-right>
      <div class="d-flex align-baseline">
        <HuxButton
          variant="primary"
          isTile
          width="80"
          height="40"
          class="ma-2"
          :isDisabled="!isFormValid"
          @click="addDestination()"
        >
          Add
        </HuxButton>
      </div>
    </template>

    <template #footer-left>
      <div class="d-flex align-baseline">
        <HuxButton
          variant="white"
          isTile
          width="80"
          height="40"
          class="ma-2 drawer-back"
          @click="onBack()"
        >
          Back
        </HuxButton>
      </div>
    </template>
  </Drawer>
</template>
<script>
import { mapGetters, mapActions } from "vuex"
import Drawer from "@/components/common/Drawer"
import HuxDropdown from "@/components/common/HuxDropdown.vue"
import HuxButton from "@/components/common/huxButton"
import Logo from "@/components/common/Logo"
import TextField from "@/components/common/TextField"
import extensionInactive1 from "@/assets/logos/extension-inactive-1.svg"
import extensionInactive2 from "@/assets/logos/extension-inactive-2.svg"
export default {
  name: "SalesforceExtensionDrawer",

  components: {
    Drawer,
    HuxButton,
    Logo,
    TextField,
    extensionInactive1,
    extensionInactive2,
    HuxDropdown,
  },

  computed: {
    ...mapGetters({
      dataExtensions: "destinations/dataExtensions",
    }),

    dropdownOptions() {
      return this.dataExtensions.map((each) => ({
        key: each.data_extension_id,
        name: each.name,
      }))
    },
  },

  data() {
    return {
      isActive: true,
      journeyType: "radio-1", // TODO - with API integration
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
      ],
      selectedLabel: "Select an existing data extension",
    }
  },
  methods: {
    ...mapActions({
      getDataExtensions: "destinations/dataExtensions",
    }),

    onSelect(item) {
      this.selectedLabel = item.name
      this.extension = item.name
    },

    resetForm() {
      this.selectedLabel = "Select an existing data extension"
      this.extension = null
      this.journeyType = "radio-1"
    },

    toggleClass: function (event) {
      if (!event.currentTarget.classList.contains("active")) {
        this.isActive = !this.isActive
      }
      this.resetForm()
    },

    addDestination() {
      //TODO: this won't work incase there are two data extensions with same name.
      // 1. need to handle with id
      // 2. need to make an api call to create an data extension
      this.value.push(this.destination)
      let id = this.dropdownOptions.findIndex(
        (each) => each.name === this.extension
      )
      this.$emit("onAdd", {
        name: this.extension,
        data_extension_id: id,
      })
      this.onBack()
    },

    onBack() {
      this.$refs.salesforceExtensionRef.reset()
      this.resetForm()
      this.$emit("onBack")
    },
  },

  async mounted() {
    this.loading = true
    await this.getDataExtensions(this.destination.id)
    this.loading = false
  },

  props: {
    value: {
      type: Array,
      required: true,
    },

    toggle: {
      type: Boolean,
      required: false,
      default: false,
    },

    destination: {
      type: Object,
      required: true,
    },
  },

  watch: {
    toggle(value) {
      this.localToggle = value
    },

    localToggle(value) {
      this.$emit("onToggle", value)
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
  ::v-deep .extension-dropdown {
    .main-button {
      min-width: 500px;
      margin: 0px !important;
      margin-bottom: 32px !important;
    }
  }
}
</style>
