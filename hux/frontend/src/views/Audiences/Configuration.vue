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
        <v-timeline align-top dense class="">
          <v-timeline-item color="blue" class="timeline-section mb-7">
            <template #icon class="timeline-icon-section">
              <span>1</span>
            </template>
            <v-row class="pt-1">
              <v-col cols="4">
                <strong class="text-h5 neroBlack--text"
                  >General information</strong
                >
                <TextField
                  placeholderText="What is the name for this audience ?"
                  height="40"
                  labelText="Audience name"
                  backgroundColor="white"
                  required
                  v-model="audience.audienceName"
                  class="mt-1 text-caption neroBlack--text pt-2"
                  :rules="audienceNamesRules"
                />
              </v-col>
              <v-col cols="8">
                <div class="mt-8 ml-15 text-caption neroBlack--text">
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
          </v-timeline-item>
          <v-timeline-item color="blue" class="timeline-section mb-7">
            <template #icon class="timeline-icon-section">
              <span>2</span>
            </template>
            <v-col class="pt-1 pa-0">
              <attribute-rules :rules="attributeRules"></attribute-rules>
            </v-col>
          </v-timeline-item>
          <v-timeline-item
            color="blue"
            class="timeline-section disable-down-timeline mb-15"
          >
            <template #icon class="timeline-icon-section">
              <span>3</span>
            </template>
            <v-row class="pt-1">
              <v-col cols="12">
                <strong class="text-h5 neroBlack--text">
                  Select destination(s) -
                  <i style="font-size: 12px">Optional</i>
                </strong>
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
                            :size="18"
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
          </v-timeline-item>
          <v-timeline-item class="timeline-section disabled">
            <template #icon class="timeline-icon-section">
              <span>4</span>
            </template>
            <v-row class="pt-1">
              <v-col cols="12">
                <strong class="text-h5"
                  >Create a lookalike audience -
                  <i>This feature will be coming soon</i>
                </strong>
              </v-col>
            </v-row>
          </v-timeline-item>
        </v-timeline>
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
      @onSalesforceRemove="deleteSalesforceExtension"
    />

    <!-- Salesforce extension workflow -->
    <SalesforceExtensionDrawer
      v-model="selectedDestinations"
      :toggle="showSalesforceExtensionDrawer"
      :destination="salesforceDestination"
      @onToggle="(val) => (showSalesforceExtensionDrawer = val)"
      @onAdd="addDataExtension"
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
import AttributeRules from "./AttributeRules.vue"
import AttachEngagement from "@/views/Audiences/AttachEngagement"
import SelectDestinationsDrawer from "@/views/Audiences/Configuration/Drawers/SelectDestinations"
import SalesforceExtensionDrawer from "@/views/Audiences/Configuration/Drawers/SalesforceExtension"
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
    AttributeRules,
    Logo,
    AttachEngagement,
    Tooltip,
    SelectDestinationsDrawer,
    SalesforceExtensionDrawer,
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
      salesforceDestinations: [],

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
    }
  },

  computed: {
    ...mapGetters({
      destinations: "destinations/enabledDestination",
      AudiencesRules: "audiences/audiencesRules",
      getAudience: "audiences/audience",
      overview: "customers/overview",
      dataExtensions: "destinations/dataExtensions",
    }),

    attributeRules() {
      return this.audience ? this.audience.attributeRules : []
    },

    isMinEngagementSelected() {
      return this.selectedEngagements.length > 1
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
      addAudienceToDB: "audiences/add",
      getAudiencesRules: "audiences/fetchConstants",
      getAudienceById: "audiences/getAudienceById",
      getOverview: "customers/getOverview",
      dataExtensionLists: "destinations/dataExtensions",
    }),

    addDataExtension(data) {
      this.salesforceDestinations.push(data)
    },

    deleteSalesforceExtension(destination) {
      let index = this.salesforceDestinations.findIndex((each) => {
        each.id === destination.id
      })
      this.salesforceDestinations.splice(index, 1)
    },

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
    mapCDMOverview() {
      this.overviewListItems[0].subtitle = this.overview.total_customers
      this.overviewListItems[1].subtitle = this.overview.total_countries
      this.overviewListItems[2].subtitle = this.overview.total_us_states
      this.overviewListItems[3].subtitle = this.overview.total_cities
      this.overviewListItems[4].subtitle = this.overview.max_age
      this.overviewListItems[5].subtitle = this.overview.gender_women
      this.overviewListItems[6].subtitle = this.overview.gender_men
      this.overviewListItems[7].subtitle = this.overview.gender_other
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
        if (this.selectedDestinations[i].type !== "salesforce") {
          filteredDestinations.push({
            id: this.selectedDestinations[i].id,
          })
        }
      }

      filteredDestinations.push(...this.salesforceDestinations)

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
      await this.addAudienceToDB(payload)
      this.$router.push({ name: "Audiences" })
    },
    removeDestination(destination) {
      if (destination.type === "salesforce") {
        this.deleteSalesforceExtension(destination)
      }
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
    this.mapCDMOverview()
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
          left: 3px;
          top: 5px;
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
