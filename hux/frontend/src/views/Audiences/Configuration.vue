<template>
  <div>
    <v-progress-linear
      v-if="loading"
      :active="loading"
      :indeterminate="loading"
    />
    <page class="white create-audience-wrap" max-width="100%">
      <div>
        <div class="heading font-weight-light black--text text--darken-4">
          {{ !isEdit ? "Add" : "Update" }} an audience
        </div>
        <div class="sub-heading text-h6 black--text text--darken-4">
          Build a target audience from the data you own. Add the attributes you
          want to involve in this particular audience and where you wish to send
          this audience.
        </div>

        <div
          class="overview font-weight-regular black--text text--darken-4 mt-8"
        >
          Audience overview
        </div>
        <div class="row overview-list mb-0 ml-0 mt-1">
          <metric-card
            v-for="(item, i) in overviewListItems"
            :key="i"
            class="list-item mr-3"
            :grow="i === 0 ? 2 : 1"
            :title="item.title"
            :icon="item.icon"
            :height="80"
          >
            <template #subtitle-extended>
              <tooltip>
                <template #label-content>
                  <span class="text--subtitle-1">
                    {{ getFormattedValue(item) | Empty }}
                  </span>
                </template>
                <template #hover-content>
                  {{ item.subtitle | Empty }}
                </template>
              </tooltip>
            </template>
          </metric-card>
        </div>
        <v-divider class="divider mt-2 mb-9"></v-divider>
      </div>

      <div class="timeline-wrapper">
        <v-form ref="form" v-model="isFormValid" class="ml-0" lazy-validation>
          <!-- TODO: this can be moved Configuration folder -->
          <form-steps>
            <form-step
              :step="1"
              label="General information"
              class="black--text text--darken-4 step-1"
            >
              <v-row class="pt-1 mt-n10">
                <v-col cols="4">
                  <text-field
                    v-model="audience.audienceName"
                    placeholder-text="What is the name for this audience ?"
                    height="40"
                    label-text="Audience name"
                    background-color="white"
                    required
                    class="
                      mt-1
                      text-caption
                      black--text
                      text--darken-4
                      pt-2
                      input-placeholder
                    "
                    data-e2e="audience-name"
                    :rules="audienceNamesRules"
                    help-text="This audience will appear in the delivered destinations as the provided Audience name. In Facebook it will appear as the provided Audience name with the timestamp of delivery."
                    icon="mdi-information-outline"
                  />
                </v-col>
                <v-col cols="8">
                  <div class="mt-3 ml-15 text-h5 black--text text--darken-4">
                    Add to an engagement -
                    <i style="text-h6">you must have at least one</i>
                    <div class="mt-2 d-flex align-center">
                      <span
                        data-e2e="add-engagement"
                        @click="openAttachEngagementsDrawer()"
                      >
                        <icon
                          class="add-icon cursor-pointer"
                          type="add"
                          :size="41"
                        />
                      </span>
                      <div>
                        <v-chip
                          v-for="item in selectedEngagements"
                          :key="item.id"
                          :close="isMinEngagementSelected"
                          small
                          class="mx-2 my-1 font-weight-semi-bold"
                          text-color="primary"
                          color="pillBlue"
                          close-icon="mdi-close"
                          @click:close="detachEngagement(item)"
                        >
                          {{ item.name }}
                        </v-chip>
                      </div>
                    </div>
                  </div>
                </v-col>
              </v-row>
            </form-step>

            <form-step
              :step="2"
              label="Select attribute(s)"
              optional="- Optional"
              class="black--text text--darken-4 step-2"
            >
              <v-col class="pa-0">
                <attribute-rules
                  ref="filters"
                  :rules="attributeRules"
                  @updateOverview="(data) => mapCDMOverview(data)"
                />
              </v-col>
            </form-step>

            <form-step
              v-if="!isEdit"
              :step="3"
              label="Select destination(s)"
              optional="- Optional"
              border="inactive"
              class="black--text text--darken-4 step-3"
            >
              <template slot="label">
                <h5 class="text-h5 d-flex align-start">
                  Select destination(s)
                  <tooltip>
                    <template #label-content>
                      <v-icon color="primary" :size="12" class="ml-1 mb-2 mr-1">
                        mdi-information-outline
                      </v-icon>
                    </template>
                    <template
                      #hover-content
                      class="
                        black--text
                        text--darken-4
                        shadow
                        pa-2
                        text-caption
                      "
                    >
                      <v-sheet max-width="240px">
                        The external platforms where this audience will be
                        delivered.
                      </v-sheet>
                    </template>
                  </tooltip>
                </h5>
              </template>

              <v-row>
                <v-col cols="12" class="pt-2">
                  <div class="d-flex align-center">
                    <span
                      data-e2e="add-destination-audience"
                      @click="openSelectDestinationsDrawer()"
                    >
                      <icon
                        class="add-icon cursor-pointer"
                        type="add"
                        :size="41"
                      />
                    </span>
                    <tooltip
                      v-for="destination in selectedDestinations"
                      :key="destination.id"
                    >
                      <template #label-content>
                        <div class="destination-logo-wrapper">
                          <div class="logo-wrapper">
                            <logo
                              class="added-logo ml-2 svg-icon"
                              :type="destination.type"
                              :size="24"
                            />
                            <logo
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
            </form-step>
          </form-steps>
        </v-form>

        <hux-footer max-width="inherit">
          <template #left>
            <huxButton
              variant="white"
              is-tile
              width="94"
              height="40"
              data-e2e="cancel-audience"
              @click.native="
                flagForModal = true
                $router.go(-1)
              "
            >
              <span class="primary--text">Cancel</span>
            </huxButton>
          </template>
          <template #right>
            <huxButton
              variant="primary"
              is-tile
              height="44"
              :is-disabled="!isAudienceFormValid"
              data-e2e="create-audience"
              @click="createAudience()"
            >
              {{
                !isEdit
                  ? selectedDestinations.length > 0
                    ? "Create &amp; deliver"
                    : "Create"
                  : "Update"
              }}
            </huxButton>
          </template>
        </hux-footer>
      </div>

      <!-- Add destination workflow -->
      <select-destinations-drawer
        ref="selectDestinations"
        v-model="selectedDestinations"
        :toggle="showSelectDestinationsDrawer"
        @onToggle="(val) => (showSelectDestinationsDrawer = val)"
        @onSalesforceAdd="openSalesforceExtensionDrawer"
      />

      <!-- Salesforce extension workflow -->
      <destination-data-extension-drawer
        v-model="selectedDestinations"
        :toggle="showSalesforceExtensionDrawer"
        :destination="salesforceDestination"
        @onToggle="(val) => (showSalesforceExtensionDrawer = val)"
        @onBack="openSelectDestinationsDrawer"
      />

      <!-- Engagement workflow -->
      <attach-engagement
        ref="selectEngagements"
        v-model="engagementDrawer"
        :final-engagements="selectedEngagements"
        @onEngagementChange="setSelectedEngagements"
      />

      <confirm-modal
        v-model="showConfirmModal"
        icon="leave-config"
        title="You are about to leave the configuration process"
        right-btn-text="Yes, leave configuration"
        body=" Are you sure you want to stop the configuration and go to another page? You will not be able to recover it and will need to start the process again."
        @onCancel="showConfirmModal = false"
        @onConfirm="navigateaway()"
      />
    </page>
  </div>
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
import AttributeRules from "@/views/SegmentPlayground/AttributeRules.vue"
import AttachEngagement from "@/views/Audiences/AttachEngagement"
import SelectDestinationsDrawer from "@/views/Audiences/Configuration/Drawers/SelectDestinations"
import DestinationDataExtensionDrawer from "@/views/Audiences/Configuration/Drawers/DestinationDataExtension"
import Logo from "@/components/common/Logo"
import Tooltip from "@/components/common/Tooltip.vue"
import Icon from "@/components/common/Icon"
import ConfirmModal from "@/components/common/ConfirmModal.vue"

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
    AttributeRules,
    Logo,
    AttachEngagement,
    Tooltip,
    SelectDestinationsDrawer,
    DestinationDataExtensionDrawer,
    Icon,
    ConfirmModal,
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
      isEdit: false,
      audienceId: "",
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
      showConfirmModal: false,
      navigateTo: false,
      flagForModal: false,
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

  beforeRouteLeave(to, from, next) {
    if (this.flagForModal == false) {
      this.showConfirmModal = true
      this.navigateTo = to
    } else {
      next()
    }
  },

  async mounted() {
    this.loading = true
    try {
      await this.getOverview()
      this.mapCDMOverview(this.overview)
      if (this.$route.name === "AudienceUpdate") {
        this.audienceId = this.$route.params.id
        this.isEdit = true
        await this.getAudienceById(this.audienceId)
        const data = this.getAudience(this.audienceId)
        this.mapAudienceData(data)
      }
    } finally {
      this.loading = false
    }
  },

  methods: {
    ...mapActions({
      fetchEngagements: "engagements/getAll",
      saveAudience: "audiences/add",
      updateAudience: "audiences/update",
      getAudienceById: "audiences/getAudienceById",
      getOverview: "customers/getOverview",
    }),

    navigateaway() {
      this.showConfirmModal = false
      this.flagForModal = true
      this.$router.push(this.navigateTo)
    },

    closeAllDrawers() {
      this.engagementDrawer = false
      this.showSelectDestinationsDrawer = false
      this.showSalesforceExtensionDrawer = false
    },

    openSelectDestinationsDrawer() {
      this.closeAllDrawers()
      this.$refs.selectDestinations.fetchDependencies()
      this.showSelectDestinationsDrawer = true
    },

    openAttachEngagementsDrawer() {
      this.closeAllDrawers()
      this.$refs.selectEngagements.fetchDependencies()
      this.engagementDrawer = true
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
          return this.$options.filters.Percentage(item.subtitle)
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
      let min_age = data.min_age
      let max_age = data.max_age
      if (min_age && max_age && min_age === max_age) {
        this.overviewListItems[4].subtitle = min_age
      } else if (min_age && max_age) {
        this.overviewListItems[4].subtitle = `${min_age}-${max_age}`
      } else {
        this.overviewListItems[4].subtitle = "-"
      }
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
      let response = {}
      if (!this.isEdit) {
        response = await this.saveAudience(payload)
      } else {
        payload["engagement_ids"] = payload.engagements
        delete payload["engagements"]
        response = await this.updateAudience({
          id: this.audienceId,
          payload: payload,
        })
      }
      this.flagForModal = true
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
    getAttributeOption(attribute_key, options) {
      for (let opt of options) {
        if (opt.menu && opt.menu.length > 0) {
          return opt.menu.filter((menuOpt) => menuOpt.key === attribute_key)[0]
        } else if (opt.key === attribute_key) {
          return opt
        }
      }
    },
    mapAudienceData(data) {
      const _audienceObject = JSON.parse(JSON.stringify(data))
      _audienceObject.audienceName = _audienceObject.name
      // Mapping the filters of audience.
      const attributeOptions = this.$refs.filters.attributeOptions()
      _audienceObject.attributeRules = _audienceObject.filters.map(
        (filter) => ({
          id: Math.floor(Math.random() * 1024).toString(16),
          operand: filter.section_aggregator === "ALL",
          conditions: filter.section_filters.map((cond) => ({
            id: Math.floor(Math.random() * 1024).toString(16),
            attribute: cond.field,
            operator: cond.type === "range" ? "" : cond.type,
            text: cond.type !== "range" ? cond.value : "",
            range: cond.type === "range" ? cond.value : [],
          })),
        })
      )
      _audienceObject.attributeRules.forEach((section) => {
        section.conditions.forEach((cond) => {
          cond.attribute = this.getAttributeOption(
            cond.attribute,
            attributeOptions
          )
          let _operators = this.$refs.filters.operatorOptions(cond)
          cond.operator =
            cond.operator !== "range"
              ? _operators.filter((opt) => opt.key === cond.operator)[0]
              : cond.operator
          this.$refs.filters.triggerSizing(cond, false)
        })
      })
      this.selectedEngagements = _audienceObject.engagements.map((eng) => ({
        id: eng.id,
        name: eng.name,
      }))
      this.selectDestinations = _audienceObject.destinations
        ? _audienceObject.destinations.map((dest) => ({
            id: dest.id,
            type: dest.delivery_platform_type,
            name: dest.name,
          }))
        : []
      this.$set(this, "audience", _audienceObject)
      this.$nextTick(function () {
        this.$refs.filters.getOverallSize()
      })
    },
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
            background: var(--v-black-lighten3);
            .v-timeline-item__inner-dot {
              background-color: var(--v-white-base) !important;
              color: var(--v-black-lighten3);
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
          var(--v-primary-lighten8) 50%,
          rgba(255, 255, 255, 0) 0%
        ),
        linear-gradient(
          var(--v-primary-lighten8) 50%,
          rgba(255, 255, 255, 0) 0%
        ),
        linear-gradient(
          to right,
          var(--v-primary-lighten8) 49%,
          rgba(255, 255, 255, 0) 0%
        ),
        linear-gradient(
          var(--v-primary-lighten8) 50%,
          rgba(255, 255, 255, 0) 0%
        );
      background-position: top, right, bottom, left;
      background-repeat: repeat-x, repeat-y;
      background-size: 12px 0px, 1px 12px;
    }
    .theme--light.v-timeline-item {
      .v-timeline-item__divider {
        .v-timeline-item__dot {
          background: var(--v-primary-lighten8);
          .v-timeline-item__inner-dot {
            background-color: var(--v-white-base) !important;
            color: var(--v-primary-lighten8);
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
          color: var(--v-black-lighten3);
        }
        .v-timeline-item__divider {
          .v-timeline-item__dot {
            color: var(--v-black-lighten3);
            .v-timeline-item__inner-dot {
              background-color: var(--v-white-base) !important;
              color: var(--v-black-lighten3);
            }
          }
        }
      }
    }
    .destination-logo-wrapper {
      display: inline-flex;
      .logo-wrapper {
        position: relative;
        .delete-icon {
          z-index: 1;
          position: absolute;
          left: 8px;
          top: 0px;
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
            color: var(--v-black-darken1) !important;
          }
        }
      }
      label {
        margin-bottom: 2px !important;
      }
    }
    .form-steps {
      .step-1 {
        .form-step__label {
          padding-bottom: 14px;
        }
        .form-step__content {
          padding-bottom: 25px !important;
        }
      }
      .step-2 {
        .form-step__label {
          padding-bottom: 7px;
        }
        .form-step__content {
          padding-top: 0px !important;
          margin-top: 0px;
          padding-bottom: 30px !important;
        }
      }
      .step-3 {
        .form-step__label {
          padding-bottom: 6px;
        }
        .form-step__content {
          padding-top: 0px !important;
          margin-top: 0px;
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
