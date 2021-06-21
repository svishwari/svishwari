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
            <v-row class="pt-1 pr-0">
              <attribute-rules :rules="attributeRules"></attribute-rules>
            </v-row>
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
                    @click="toggleDrawer()"
                  >
                    mdi-plus-circle
                  </v-icon>
                  <tooltip>
                    <template #label-content>
                      <Logo
                        class="added-logo ml-2"
                        v-for="destination in audience.destinations"
                        :key="destination.id"
                        :type="destination.type"
                        :size="18"
                        @mouseover.native="hoverItem = destination.name"
                      />
                    </template>
                    <template #hover-content>
                      <div class="d-flex align-center">
                        Remove {{ hoverItem }}
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
      <!-- Add destination workflow -->
      <drawer v-model="destinationDrawer.insideFlow" class="destination-drawer">
        <template #header-left>
          <div
            class="d-flex align-baseline"
            v-if="destinationDrawer.viewStep == 1"
          >
            <h3 class="text-h3 font-weight-light pr-2">
              Select a destination to add
            </h3>
          </div>
          <div
            class="d-flex align-baseline"
            v-if="destinationDrawer.viewStep == 2"
          >
            <h3 class="text-h3 pr-2 d-flex align-center">
              <Logo :type="destinationDrawer.selectedDestination[0].type" />
              <div class="pl-2 font-weight-light">
                {{ destinationDrawer.selectedDestination[0].name }}
              </div>
            </h3>
          </div>
        </template>

        <template #default>
          <v-stepper v-model="destinationDrawer.viewStep" class="stepper mt-1">
            <v-stepper-items>
              <v-stepper-content step="1">
                <div>
                  <CardHorizontal
                    v-for="destination in destinationsList"
                    :key="destination.id"
                    :title="destination.name"
                    :icon="destination.type"
                    :isAdded="
                      destination.is_added ||
                      isDestinationAdded(destination.type)
                    "
                    :isAvailable="destination.is_enabled"
                    :isAlreadyAdded="destination.is_added"
                    @click="onSelectDestination(destination)"
                    class="my-3"
                  />
                </div>
              </v-stepper-content>
              <v-stepper-content step="2">
                <AddDestination />
              </v-stepper-content>
            </v-stepper-items>
          </v-stepper>
        </template>

        <template #footer-right>
          <div
            class="d-flex align-baseline"
            v-if="destinationDrawer.viewStep == 2"
          >
            <huxButton
              variant="primary"
              isTile
              width="80"
              height="40"
              class="ma-2"
              @click="addDestinationToAudience()"
            >
              Add
            </huxButton>
          </div>
        </template>

        <template #footer-left>
          <div
            class="d-flex align-baseline"
            v-if="destinationDrawer.viewStep == 1"
          >
            {{ destinationsList.length }} results
          </div>
          <div
            class="d-flex align-baseline"
            v-if="destinationDrawer.viewStep == 2"
          >
            <huxButton
              variant="white"
              isTile
              width="80"
              height="40"
              class="ma-2 drawer-back"
              @click.native="destinationDrawer.viewStep = 1"
            >
              Back
            </huxButton>
          </div>
        </template>
      </drawer>
      <!-- Engagement workflow -->
      <AttachEngagement
        v-model="engagementDrawer"
        :finalEngagements="selectedEngagements"
        @onEngagementChange="setSelectedEngagements"
      />
    </div>
  </page>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import Page from "@/components/Page"
import MetricCard from "@/components/common/MetricCard"
import HuxFooter from "@/components/common/HuxFooter"
import huxButton from "@/components/common/huxButton"
import TextField from "@/components/common/TextField"
import Drawer from "@/components/common/Drawer"
import AttributeRules from "./AttributeRules.vue"
import CardHorizontal from "@/components/common/CardHorizontal"
import AddDestination from "@/views/Audiences/AddDestination"
import AttachEngagement from "@/views/Audiences/AttachEngagement"
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
    Drawer,
    AttributeRules,
    CardHorizontal,
    AddDestination,
    Logo,
    AttachEngagement,
    Tooltip,
  },
  data() {
    return {
      // selectedDestinationIndex: -1,
      // selectedDestination: null,
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

      engagementDrawer: false,
      audience: {
        name: null,
        attributeRules: [],
        destinations: [],
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
      destinationDrawer: {
        insideFlow: false,
        viewStep: 1,
        selectedDestination: [],
      },
      hoverItem: "",
      loading: false,
    }
  },

  computed: {
    ...mapGetters({
      destinations: "destinations/enabledDestination",
      AudiencesRules: "audiences/audiencesRules",
      getAudience: "audiences/audience",
      overview: "customers/overview",
      availableDestinations: "destinations/availableDestinations",
    }),

    destinationsList() {
      return this.availableDestinations
    },

    destination() {
      return this.destinations[this.selectedDestinationIndex] || null
    },

    isDestinationSelected() {
      return Boolean(this.destination)
    },

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
      getDestinations: "destinations/getAll",
      fetchEngagements: "engagements/getAll",
      addAudienceToDB: "audiences/add",
      getAudiencesRules: "audiences/fetchConstants",
      getAudienceById: "audiences/getAudienceById",
      getOverview: "customers/getOverview",
      getAvailableDestinations: "destinations/getAvailableDestinations",
    }),

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

    // Destinations
    toggleDrawer() {
      this.destinationDrawer.insideFlow = !this.destinationDrawer.insideFlow
    },

    onSelectDestination(selected) {
      // check to avoid duplicate destination
      if (!this.isDestinationAdded(selected.type)) {
        if (selected && selected.type === "salesforce") {
          if (!this.isDestinationAddedOnDrawer(selected)) {
            this.destinationDrawer.selectedDestination.push(selected)
          }
          this.destinationDrawer.viewStep = 2
        } else {
          this.audience.destinations.push(selected)
          this.toggleDrawer()
        }
      } else {
        var idx = this.audience.destinations.findIndex(
          (item) => item.id == selected.id
        )
        if (idx > -1) {
          this.audience.destinations.splice(idx, 1)
        }
      }
    },

    addDestinationToAudience() {
      this.audience.destinations.push(
        ...this.destinationDrawer.selectedDestination
      )
      this.destinationDrawer.insideFlow = false
      this.destinationDrawer.viewStep = 1
    },
    isDestinationAddedOnDrawer(selected) {
      if (
        this.destinationDrawer &&
        this.destinationDrawer.selectedDestination
      ) {
        const existingIndex =
          this.destinationDrawer.selectedDestination.findIndex(
            (destination) => destination.type === selected.type
          )
        return existingIndex > -1
      }
    },

    isDestinationAdded(title) {
      if (this.audience && this.audience.destinations) {
        const existingIndex = this.audience.destinations.findIndex(
          (destination) => destination.type === title
        )
        return existingIndex > -1
      }
    },
    async createAudience() {
      const destinationIdArray = this.audience.destinations.map(
        (destination) => destination.id
      )
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
        destinations: destinationIdArray,
        engagements: engagementIdArray,
        filters: filtersArray,
        name: this.audience.audienceName,
      }
      await this.addAudienceToDB(payload)
      this.$router.push({ name: "Audiences" })
    },
  },
  async mounted() {
    this.loading = true
    await this.getOverview()
    if (this.$route.params.id) await this.getAudienceById(this.$route.params.id)
    await this.getDestinations()
    await this.getAudiencesRules()
    this.mapCDMOverview()
    this.loading = false
    await this.getAvailableDestinations()
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
    .added-logo {
      margin-top: 6px;
      &:hover {
        width: 18px;
        height: 18px;
        background-image: url("../../assets/images/delete_outline.png");
        background-size: 18px 18px;
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
