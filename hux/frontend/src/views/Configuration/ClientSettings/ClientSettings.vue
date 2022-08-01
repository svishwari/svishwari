<template>
  <div class="brand-settings-wrapper">
    <v-row>
      <v-col>
        <v-card class="rounded-lg box-shadow-5 mt-3">
          <div class="px-6 py-5">
            <div class="pb-1 d-flex justify-space-between">
              <div class="black--text text-h3">Industry</div>
            </div>
            <div class="black--text text-h6 d-flex mt-4">
              <h3 class="text-body-1">Demo mode</h3>
              <tooltip max-width="24%" position-top>
                <template #label-content>
                  <icon
                    type="info"
                    :size="10"
                    class="mb-1 ml-1"
                    color="primary"
                    variant="base"
                  />
                </template>
                <template #hover-content>
                  <div>
                    Switching on demo mode will change the look and feel based
                    on a selected industry. This will only apply to you.
                  </div>
                  <div class="mt-4">
                    Switching off demo mode will return the client’s look and
                    feel back to default.
                  </div>
                </template>
              </tooltip>
              <hux-switch
                v-model="showConfiguration"
                false-color="var(--v-black-lighten4)"
                width="64px"
                :switch-labels="toggleSwitchLabels"
                class="w-53"
                @change="toggleMainSwitch($event)"
              />
            </div>
            <div v-if="enableSelection" class="black--text text-h6 mt-4">
              <label class="mb-1">Industry</label>
              <hux-dropdown
                :label="currentIndustrySelection"
                :selected="currentIndustrySelection"
                :show-hover="false"
                :items="configOptions['industryOptions']"
                min-width="360"
                @on-select="onSelectMenuItem"
              />
            </div>
            <div v-if="showSubCategories" class="divider-class mt-2"></div>
            <div v-if="showSubCategories" class="black--text text-h6 mt-6">
              <div
                v-for="option in labelOptions"
                :key="option.key"
                class="mt-4"
              >
                <label class="mb-1">{{ option.label }}</label>
                <hux-dropdown
                  class="ml-0"
                  :label="finalSelection[option.key]"
                  :selected="finalSelection[option.key]"
                  :show-hover="false"
                  :items="
                    configOptions[option.key][
                      currentIndustrySelection.toLowerCase()
                    ]
                  "
                  min-width="360"
                  @on-select="onSelectSubMenuItem($event, option.key)"
                />
              </div>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>
    <hux-footer slot="footer" data-e2e="footer" max-width="100%">
      <template #left>
        <hux-button
          size="large"
          variant="white"
          is-tile
          class="
            text-button
            ml-auto
            primary--text
            mr-3
            submit-button
            btn-border
            box-shadow-none
          "
          @click="restoreState"
        >
          Cancel
        </hux-button>
      </template>
      <template #right>
        <hux-button
          size="large"
          height="40"
          is-tile
          variant="primary base"
          data-e2e="action-audience"
          :is-disabled="isPrePopulate || isDisabled()"
          @click="updatedConfigSettings"
        >
          Update
        </hux-button>
      </template>
    </hux-footer>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import Icon from "@/components/common/Icon.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import HuxSwitch from "@/components/common/Switch.vue"
import HuxButton from "@/components/common/huxButton"
import HuxFooter from "@/components/common/HuxFooter"
import HuxDropdown from "@/components/common/HuxDropdown.vue"
import industryOptions from "./demo_config_options.json"

export default {
  name: "BrandSettings",
  components: {
    HuxSwitch,
    Icon,
    Tooltip,
    HuxButton,
    HuxFooter,
    HuxDropdown,
  },
  data() {
    return {
      toggleSwitchLabels: [
        {
          condition: true,
          label: "ON",
        },
        {
          condition: false,
          label: "OFF",
        },
      ],
      labelOptions: [
        {
          label: "What business category does this client belong to?",
          key: "retailOptions",
        },
        {
          label: "Who is this client’s end consumer?",
          key: "customerOptions",
        },
        {
          label: "What end consumer activity would you like to track? ",
          key: "conversionOptions",
        },
      ],
      configOptions: industryOptions,
      enableSelection: false,
      industrySelected: false,
      showSubCategories: false,
      showConfiguration: false,
      isPrePopulate: true,
      currentIndustrySelection: "Select",
      finalSelection: {
        retailOptions: "Select",
        customerOptions: "Select",
        conversionOptions: "Select",
      },
    }
  },
  computed: {
    ...mapGetters({
      existingDemoConfiguration: "users/getDemoConfiguration",
    }),
  },
  mounted() {
    if (this.existingDemoConfiguration) {
      this.prepopulateConfiguration()
    }
  },
  methods: {
    ...mapActions({
      updateDemoConfig: "users/updateDemoConfig",
    }),
    toggleMainSwitch(value) {
      this.enableSelection = value
      this.showSubCategories = false
      this.currentIndustrySelection = "Select"
      this.resetSubCategories()
    },
    onSelectMenuItem(item) {
      if (item.name !== ("Select" && this.currentIndustrySelection)) {
        this.currentIndustrySelection = item.name
        this.showSubCategories = true
        this.resetSubCategories()
      }
    },
    resetSubCategories() {
      this.finalSelection = {
        retailOptions: "Select",
        customerOptions: "Select",
        conversionOptions: "Select",
      }
      this.isPrePopulate = false
    },
    onSelectSubMenuItem(value, item) {
      this.finalSelection[item] = value.name
      this.isPrePopulate = false
    },
    isDisabled() {
      if (this.showConfiguration) {
        return this.finalSelection.retailOptions !== "Select" &&
          this.finalSelection.customerOptions !== "Select" &&
          this.finalSelection.conversionOptions !== "Select"
          ? false
          : true
      } else return false
    },
    restoreState() {
      this.prepopulateConfiguration()
      this.isPrePopulate = true
    },
    async updatedConfigSettings() {
      await this.updateDemoConfig({
        demo_mode: this.showConfiguration,
        industry: this.currentIndustrySelection,
        description: this.finalSelection.retailOptions,
        target: this.finalSelection.customerOptions,
        track: this.finalSelection.conversionOptions,
      })
      this.$root.$emit("update-config-settings")
    },
    prepopulateConfiguration() {
      this.showConfiguration = this.existingDemoConfiguration.demo_mode
      if (this.showConfiguration) {
        this.enableSelection = true
        this.showSubCategories = true
        this.currentIndustrySelection = this.existingDemoConfiguration.industry
        this.finalSelection = {
          retailOptions: this.existingDemoConfiguration.description,
          customerOptions: this.existingDemoConfiguration.target,
          conversionOptions: this.existingDemoConfiguration.track,
        }
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.brand-settings-wrapper {
  ::v-deep.v-input--selection-controls {
    margin-top: 0px !important;
    padding-top: 0px !important;
    margin-left: 21px !important;
  }
  ::v-deep .hux-dropdown {
    button {
      margin-top: 0px !important;
      margin-left: 0px !important;
    }
  }
  ::v-deep .rounded-lg {
    .hux-dropdown {
      button {
        .v-btn__content {
          .text-ellipsis {
            position: relative;
            bottom: 2px !important;
          }
        }
      }
    }
  }
  .divider-class {
    border-bottom: 1px solid var(--v-black-lighten2) !important;
  }
}
</style>
