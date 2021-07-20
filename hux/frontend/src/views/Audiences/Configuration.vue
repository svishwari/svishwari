<template>
  <page class="white create-audience-wrap" maxWidth="100%">
    <div>
      <div class="heading font-weight-light neroBlack--text">
        Add an audience
      </div>
      <div class="sub-heading text-h6 neroBlack--text">
        Build a target audience from the data you own. Add the attributes you
        want to involve in this particular audience and where you wish to send
        this audience.
      </div>

      <div class="overview font-weight-regular neroBlack--text mt-15">
        Audience overview
      </div>
      <div class="row overview-list mb-0 ml-0 mt-1">
        <MetricCard
          class="list-item mr-3"
          v-for="(item, i) in overviewListItems"
          :key="i"
          :grow="i === 0 ? 2 : 1"
          :title="item.title"
          :icon="item.icon"
        >
          <template #subtitle-extended>
            <tooltip>
              <template #label-content>
                <span class="font-weight-semi-bold">
                  {{ getFormattedValue(item) }}
                </span>
              </template>
              <template #hover-content>
                {{ item.subtitle | Empty }}
              </template>
            </tooltip>
          </template>
        </MetricCard>
      </div>
      <v-divider class="divider mt-2 mb-9"></v-divider>
    </div>

    <div class="timeline-wrapper">
      <v-form ref="form" class="ml-0" v-model="isFormValid" lazy-validation>
        <!-- TODO: this can be moved Configuration folder -->
        <FormSteps>
          <FormStep :step="1" label="General information">
            <v-row class="pt-1">
              <v-col cols="4">
                <TextField
                  placeholderText="What is the name for this audience ?"
                  height="40"
                  labelText="Audience name"
                  backgroundColor="white"
                  required
                  v-model="audience.audienceName"
                  class="
                    mt-1
                    text-caption
                    neroBlack--text
                    pt-2
                    input-placeholder
                  "
                  :rules="audienceNamesRules"
                />
              </v-col>
              <v-col cols="8">
                <div class="mt-3 ml-15 text-caption neroBlack--text">
                  Add to an engagement -
                  <i style="tilt">you must have at least one</i>
                  <div class="mt-2 d-flex align-center">
                    <v-icon
                      size="30"
                      class="add-icon cursor-pointer"
                      color="primary"
                      @click="engagementDrawer = !engagementDrawer"
                      >mdi-plus-circle</v-icon
                    >
                    <div>
                      <v-chip
                        v-for="item in selectedEngagements"
                        :close="isMinEngagementSelected"
                        small
                        class="mx-2 my-1 font-weight-semi-bold"
                        text-color="primary"
                        color="pillBlue"
                        close-icon="mdi-close"
                        @click:close="detachEngagement(item)"
                        :key="item.id"
                      >
                        {{ item.name }}
                      </v-chip>
                    </div>
                  </div>
                </div>
              </v-col>
            </v-row>
          </FormStep>

          <FormStep :step="2" label="Select attribute(s)" optional="- Optional">
            <v-col class="pt-1 pa-0">
              <attribute-rules
                :rules="attributeRules"
                @updateOveriew="(data) => mapCDMOverview(data)"
              />
            </v-col>
          </FormStep>

          <FormStep
            :step="3"
            label="Select destination(s)"
            optional="- Optional"
            :border="!isLookAlikeCreateable ? 'inactive' : ''"
          >
            <v-row class="pt-1">
              <v-col cols="12">
                <div class="d-flex align-center">
                  <v-icon
                    size="30"
                    class="add-icon mt-1"
                    color="primary"
                    @click="openSelectDestinationsDrawer()"
                  >
                    mdi-plus-circle
                  </v-icon>
                  <tooltip
                    v-for="destination in selectedDestinations"
                    :key="destination.id"
                  >
                    <template #label-content>
                      <div class="destination-logo-wrapper">
                        <div class="logo-wrapper">
                          <Logo
                            class="added-logo ml-2 svg-icon"
                            :type="destination.type"
                            :size="24"
                          />
                          <Logo
                            class="delete-icon"
                            type="delete"
                            @click.native="removeDestination(destination)"
                          />
                        </div>
                      </div>
                    </template>
                    <template #hover-content>
                      <div class="d-flex align-center">
                        Remove {{ destination.name }}
                      </div>
                    </template>
                  </tooltip>
                </div>
              </v-col>
            </v-row>
          </FormStep>

          <FormStep
            :step="4"
            label="Create a lookalike audience"
            :optional="
              !isLookAlikeCreateable
                ? '- Enabled if Facebook is added as a destination'
                : ''
            "
            :disabled="!isLookAlikeCreateable"
          >
            <div class="dark--text" v-if="isLookAlikeCreateable">
              Would you like to create a lookalike audience from this audience?
              This will create a one-off new audience in Facebook when this<br />
              audience is first delivered.
            </div>
            <v-row v-if="isLookAlikeCreateable">
              <v-col col="12">
                <v-radio-group v-model="isLookAlikeNeeeded" column mandatory>
                  <v-radio
                    :value="0"
                    color="pantoneBlue"
                    class="pb-3"
                    :ripple="false"
                  >
                    <template #label>
                      <span class="neroBlack--text">Nope! Not interested</span>
                    </template>
                  </v-radio>
                  <v-radio :value="1" color="pantoneBlue" :ripple="false">
                    <template #label>
                      <span class="neroBlack--text">
                        Auto-create a lookalike based on this audience
                      </span>
                    </template>
                  </v-radio>
                </v-radio-group>
              </v-col>
            </v-row>
            <v-row
              v-if="isLookAlikeCreateable && isLookAlikeNeeeded"
              class="mt-0"
            >
              <v-col col="6" class="pr-14">
                <TextField
                  placeholderText="What is the name for this new lookalike audience?"
                  height="40"
                  labelText="Lookalike audience name"
                  backgroundColor="white"
                  required
                  v-model="lookalikeAudience.name"
                  class="text-caption neroBlack--text"
                />
              </v-col>
              <v-col col="6" class="pr-14">
                <div class="neroBlack--text text-caption">Audience reach</div>
                <LookAlikeSlider v-model="lookalikeAudience.value" />
                <div class="gray--text text-caption pt-4">
                  Audience reach ranges from 1% to 10% of the combined
                  population of your selected locations. A 1% lookalike consists
                  of the people most similar to your lookalike source.
                  Increasing the percentage creates a bigger, broader audience.
                </div>
              </v-col>
            </v-row>
          </FormStep>
        </FormSteps>
      </v-form>

      <HuxFooter maxWidth="inherit">
        <template #left>
          <huxButton
            variant="white"
            isTile
            width="94"
            height="40"
            @click.native="$router.go(-1)"
          >
            <span class="primary--text">Cancel</span>
          </huxButton>
        </template>
        <template #right>
          <huxButton
            variant="primary"
            isTile
            width="94"
            height="44"
            @click="createAudience()"
            :isDisabled="!isAudienceFormValid"
          >
            Create
          </huxButton>
        </template>
      </HuxFooter>
    </div>

    <!-- Add destination workflow -->
    <SelectDestinationsDrawer
      v-model="selectedDestinations"
      :toggle="showSelectDestinationsDrawer"
      @onToggle="(val) => (showSelectDestinationsDrawer = val)"
      @onSalesforceAdd="openSalesforceExtensionDrawer"
    />

    <!-- Salesforce extension workflow -->
    <DestinationDataExtensionDrawer
      v-model="selectedDestinations"
      :toggle="showSalesforceExtensionDrawer"
      :destination="salesforceDestination"
      @onToggle="(val) => (showSalesforceExtensionDrawer = val)"
      @onBack="openSelectDestinationsDrawer"
    />

    <!-- Engagement workflow -->
    <AttachEngagement
      v-model="engagementDrawer"
      :finalEngagements="selectedEngagements"
      @onEngagementChange="setSelectedEngagements"
    />
  </page>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import Page from "@/components/Page"
import MetricCard from "@/components/common/MetricCard"
import HuxFooter from "@/components/common/HuxFooter"
import huxButton from "@/components/common/huxButton"
import TextField from "@/components/common/TextField"
import FormSteps from "@/components/common/FormSteps"
import FormStep from "@/components/common/FormStep"
import LookAlikeSlider from "@/components/common/LookAlikeSlider"
import AttributeRules from "./AttributeRules.vue"
import AttachEngagement from "@/views/Audiences/AttachEngagement"
import SelectDestinationsDrawer from "@/views/Audiences/Configuration/Drawers/SelectDestinations"
import DestinationDataExtensionDrawer from "@/views/Audiences/Configuration/Drawers/DestinationDataExtension"
import Logo from "@/components/common/Logo"
import Tooltip from "@/components/common/Tooltip.vue"

export default {
  name: "Configuration",
  components: {
    Page,
    MetricCard,
    HuxFooter,
    huxButton,
    TextField,
    FormSteps,
    FormStep,
    LookAlikeSlider,
    AttributeRules,
    Logo,
    AttachEngagement,
    Tooltip,
    SelectDestinationsDrawer,
    DestinationDataExtensionDrawer,
  },
  data() {
    return {
      overviewListItems: [
        { title: "Target size", subtitle: "" },
        { title: "Countries", subtitle: "", icon: "mdi-earth" },
        { title: "US States", subtitle: "", icon: "mdi-map" },
        { title: "Cities", subtitle: "", icon: "mdi-map-marker-radius" },
        { title: "Age", subtitle: "", icon: "mdi-cake-variant" },
        { title: "Women", subtitle: "", icon: "mdi-gender-female" },
        { title: "Men", subtitle: "", icon: "mdi-gender-male" },
        { title: "Other", subtitle: "", icon: "mdi-gender-male-female" },
      ],
      selectedDestinations: [],
      showSelectDestinationsDrawer: false,
      showSalesforceExtensionDrawer: false,
      salesforceDestination: {},

      engagementDrawer: false,
      audience: {
        name: null,
        attributeRules: [],
      },
      selectedEngagements: [],
      newEngagementValid: true,
      engagement: {
        name: "",
        description: "",
        deliveryType: 0,
      },
      audienceNamesRules: [(v) => !!v || "Audience name is required"],
      isFormValid: false,
      hoverItem: "",
      loading: false,
      addDestinationFormValid: false,
      // TODO: API integration HUS-649
      isLookAlikeNeeeded: 0,
      lookalikeAudience: {
        name: null,
        value: 5,
      },
    }
  },

  computed: {
    ...mapGetters({
      destinations: "destinations/enabledDestination",
      AudiencesRules: "audiences/audiencesRules",
      getAudience: "audiences/audience",
      overview: "customers/overview",
    }),

    attributeRules() {
      return this.audience ? this.audience.attributeRules : []
    },

    isMinEngagementSelected() {
      return this.selectedEngagements.length > 1
    },

    isLookAlikeCreateable() {
      return (
        this.selectedDestinations.filter((each) => each.type === "facebook")
          .length > 0
      )
    },

    isAudienceFormValid() {
      return !!this.audience.audienceName && this.selectedEngagements.length > 0
    },

    selectedEngagementIds() {
      // This will be used when sending data to create an audience
      return this.selectedEngagements.map((each) => {
        return each["id"]
      })
    },
  },

  methods: {
    ...mapActions({
      fetchEngagements: "engagements/getAll",
      saveAudience: "audiences/add",
      getAudiencesRules: "audiences/fetchConstants",
      getAudienceById: "audiences/getAudienceById",
      getOverview: "customers/getOverview",
    }),

    closeAllDrawers() {
      this.engagementDrawer = false
      this.showSelectDestinationsDrawer = false
      this.showSalesforceExtensionDrawer = false
    },

    openSelectDestinationsDrawer() {
      this.closeAllDrawers()
      this.showSelectDestinationsDrawer = true
    },

    openSalesforceExtensionDrawer(destination) {
      this.closeAllDrawers()
      this.salesforceDestination = destination
      this.showSalesforceExtensionDrawer = true
    },

    getFormattedValue(item) {
      switch (item.title) {
        case "Target size":
        case "Countries":
        case "US States":
        case "Cities":
          return this.$options.filters.Numeric(
            item.subtitle,
            false,
            false,
            true
          )
        case "Women":
        case "Men":
        case "Other":
          return this.$options.filters.percentageConvert(
            item.subtitle,
            true,
            true
          )
        default:
          return item.subtitle
      }
    },

    // Mapping Overview Data
    mapCDMOverview(data) {
      this.overviewListItems[0].subtitle = data.total_customers
      this.overviewListItems[1].subtitle = data.total_countries
      this.overviewListItems[2].subtitle = data.total_us_states
      this.overviewListItems[3].subtitle = data.total_cities
      this.overviewListItems[4].subtitle = data.max_age
      this.overviewListItems[5].subtitle = data.gender_women
      this.overviewListItems[6].subtitle = data.gender_men
      this.overviewListItems[7].subtitle = data.gender_other
    },

    // Engagements
    detachEngagement(engagement) {
      const existingIndex = this.selectedEngagements.findIndex(
        (each) => engagement.id === each.id
      )
      if (existingIndex > -1) {
        this.selectedEngagements.splice(existingIndex, 1)
      }
    },

    setSelectedEngagements(engagementsList) {
      this.selectedEngagements = engagementsList
    },

    async createAudience() {
      let filteredDestinations = []

      for (let i = 0; i < this.selectedDestinations.length; i++) {
        if (this.selectedDestinations[i].type !== "sfmc") {
          filteredDestinations.push({
            id: this.selectedDestinations[i].id,
          })
        } else {
          filteredDestinations.push({
            id: this.selectedDestinations[i].id,
            delivery_platform_config:
              this.selectedDestinations[i].delivery_platform_config,
          })
        }
      }

      const engagementIdArray = this.selectedEngagements.map(
        (engagement) => engagement.id
      )
      const filtersArray = []
      for (
        let ruleIndex = 0;
        ruleIndex < this.audience.attributeRules.length;
        ruleIndex++
      ) {
        var filter = {
          section_aggregator: this.audience.attributeRules[ruleIndex].operand
            ? "ALL"
            : "ANY",
          section_filters: [],
        }
        for (
          let conditionIndex = 0;
          conditionIndex <
          this.audience.attributeRules[ruleIndex].conditions.length;
          conditionIndex++
        ) {
          filter.section_filters.push({
            field:
              this.audience.attributeRules[ruleIndex].conditions[conditionIndex]
                .attribute.key,
            type: this.audience.attributeRules[ruleIndex].conditions[
              conditionIndex
            ].operator
              ? this.audience.attributeRules[ruleIndex].conditions[
                  conditionIndex
                ].operator.key
              : "range",
            value: this.audience.attributeRules[ruleIndex].conditions[
              conditionIndex
            ].operator
              ? this.audience.attributeRules[ruleIndex].conditions[
                  conditionIndex
                ].text
              : this.audience.attributeRules[ruleIndex].conditions[
                  conditionIndex
                ].range,
          })
        }
        filtersArray.push(filter)
      }
      const payload = {
        destinations: filteredDestinations,
        engagements: engagementIdArray,
        filters: filtersArray,
        name: this.audience.audienceName,
      }
      const response = await this.saveAudience(payload)
      this.$router.push({
        name: "AudienceInsight",
        params: { id: response.id },
      })
    },
    removeDestination(destination) {
      let index = this.selectedDestinations.indexOf(destination)
      this.selectedDestinations.splice(index, 1)
    },
    validateForm(value) {
      this.addDestinationFormValid = value
    },
  },
  async mounted() {
    this.loading = true
    await this.getOverview()
    if (this.$route.params.id) await this.getAudienceById(this.$route.params.id)
    await this.getAudiencesRules()
    this.mapCDMOverview(this.overview)
    this.loading = false
  },
}
</script>

<style lang="scss" scoped>
.create-audience-wrap {
  .heading {
    font-size: 24px;
    line-height: 40px;
  }
  .sub-heading {
    line-height: 22px;
    max-width: 910px;
  }
  .overview {
    font-size: 15px;
    line-height: 20px;
  }
  .divider {
    width: 100%;
  }
  ::v-deep .timeline-wrapper {
    max-width: 1230px;
    padding-right: 30px;
    .theme--light.v-timeline {
      padding-top: 0px;
      left: -30px;
      .theme--light.v-timeline-item:last-child {
        padding-bottom: 0px;
      }
      .theme--light.v-timeline-item.disabled {
        .v-timeline-item__divider {
          .v-timeline-item__dot {
            background: var(--v-lightGrey-base);
            .v-timeline-item__inner-dot {
              background-color: var(--v-white-base) !important;
              color: var(--v-lightGrey-base);
              height: 34.2px;
              margin: 2.1px;
              width: 34.2px;
            }
          }
        }
      }
    }
    .theme--light.v-timeline:before {
      background: linear-gradient(
          to right,
          var(--v-secondary-base) 50%,
          rgba(255, 255, 255, 0) 0%
        ),
        linear-gradient(var(--v-secondary-base) 50%, rgba(255, 255, 255, 0) 0%),
        linear-gradient(
          to right,
          var(--v-secondary-base) 49%,
          rgba(255, 255, 255, 0) 0%
        ),
        linear-gradient(var(--v-secondary-base) 50%, rgba(255, 255, 255, 0) 0%);
      background-position: top, right, bottom, left;
      background-repeat: repeat-x, repeat-y;
      background-size: 12px 0px, 1px 12px;
    }
    .theme--light.v-timeline-item {
      .v-timeline-item__divider {
        .v-timeline-item__dot {
          background: var(--v-info-base);
          .v-timeline-item__inner-dot {
            background-color: var(--v-white-base) !important;
            color: var(--v-info-base);
            height: 34.2px;
            margin: 2.1px;
            width: 34.2px;
          }
        }
      }
    }
    .theme--light.v-timeline-item {
      &.disabled {
        .v-timeline-item__body {
          color: var(--v-lightGrey-base);
        }
        .v-timeline-item__divider {
          .v-timeline-item__dot {
            color: var(--v-lightGrey-base);
            .v-timeline-item__inner-dot {
              background-color: var(--v-white-base) !important;
              color: var(--v-lightGrey-base);
            }
          }
        }
      }
    }
    .destination-logo-wrapper {
      display: inline-flex;
      .logo-wrapper {
        position: relative;
        .added-logo {
          margin-top: 8px;
        }
        .delete-icon {
          z-index: 1;
          position: absolute;
          left: 8px;
          top: 8px;
          background: var(--v-white-base);
          display: none;
        }
        &:hover {
          .delete-icon {
            display: block;
          }
        }
      }
    }
    .input-placeholder {
      .v-text-field {
        .v-text-field__slot {
          label {
            color: var(--v-lightGrey-base) !important;
          }
        }
      }
    }
  }

  .destination-drawer {
    .stepper {
      box-shadow: none !important;
    }
    .drawer-back {
      @extend .box-shadow-25;
    }
  }
}
</style>
