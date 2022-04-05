<template>
  <div class="audience-insight-wrap">
    <dashboard-header
      :breadcrumb-items="breadcrumbItems"
      :audience-data="audience"
      data-e2e="audience-breadcrumb"
      @onRefresh="refresh()"
      @removeAudience="(data) => removeAudience(data)"
      @favoriteAudience="(data) => favoriteAudience(data)"
      @openDownloadDrawer="() => openDownloadDrawer()"
      @openLookalikeEditModal="() => openLookalikeEditModal()"
      @editAudience="(data) => editAudience(data)"
    />
    <v-progress-linear :active="loading" :indeterminate="loading" />
    <div v-if="audience && audience.is_lookalike === true" class="pa-8">
      <audience-lookalike-dashboard
        :audience-data="audience"
        :applied-filters="appliedFilters"
        :audience-id="audienceId"
        :related-engagements="relatedEngagements"
        @onRefresh="refresh()"
      />
    </div>
    <div v-else v-cloak class="pa-8">
      <v-card class="overview-card pt-5 pb-6 pl-6 pr-6 box-shadow-5">
        <v-card-title class="d-flex justify-space-between pa-0 pr-2">
          <h3 class="text-h3 mb-2">Audience overview</h3>
          <div class="d-flex align-center">
            <v-btn
              v-if="audience && !audience.is_lookalike"
              :disabled="relatedEngagements.length == 0"
              text
              :color="relatedEngagements.length == 0 ? 'black' : 'primary'"
              class="body-1 ml-n3 mt-n2"
              data-e2e="delivery-history"
              @click="openDeliveryHistoryDrawer()"
            >
              <icon
                class="mr-1"
                :class="relatedEngagements.length == 0 ? 'icon_grey' : ''"
                :type="
                  relatedEngagements.length == 0 ? 'history_grey' : 'history'
                "
                :size="24"
                :color="relatedEngagements.length == 0 ? 'black' : 'primary'"
                :variant="relatedEngagements.length == 0 ? 'lighten3' : 'base'"
              />
              Delivery history
            </v-btn>
          </div>
        </v-card-title>

        <div
          v-if="audience && audience.is_lookalike"
          class="row overview-list lookalike-aud mb-0 ml-0 mr-1 mt-4"
        >
          <metric-card :height="60" :title="''" class="lookalikeMessageCard">
            <template #subtitle-extended>
              <span
                >This is a lookalike audience. Go to the original
                audience,&nbsp;</span
              >
              <router-link
                :to="{
                  name: 'AudienceInsight',
                  params: { id: audience.source_id },
                }"
                class="text-decoration-none colorLink"
                append
                >{{ audience.source_name }}
              </router-link>
              <span>,&nbsp;to see insights.</span></template
            >
          </metric-card>
        </div>
        <div
          v-if="audience && !audience.is_lookalike"
          class="row overview-list mb-0 ml-0 mt-1 mr-1"
        >
          <metric-card
            v-for="(item, i) in Object.values(audienceOverview)"
            :key="i"
            class="mr-3"
            :grow="i === 0 ? 2 : 1"
            :title="item.title"
            :icon="item.icon"
            :height="80"
            :interactable="item.action ? true : false"
            :title-tooltip="item.titleTooltip"
            max-width="170"
            data-e2e="audience-overview"
          >
            <template #subtitle-extended>
              <tooltip>
                <template #label-content>
                  <span class="font-weight-semi-bold">
                    {{ getFormattedValue(item) | Empty }}
                  </span>
                </template>
                <template #hover-content>
                  <span v-if="percentageColumns.includes(item.title)">
                    {{ item.subtitle | Percentage | Empty }}
                  </span>
                  <span v-else>{{ item.subtitle | Numeric | Empty }}</span>
                </template>
              </tooltip>
            </template>
          </metric-card>

          <metric-card
            class="mr-3"
            title="Gender"
            :height="80"
            max-width="220"
            :interactable="false"
          >
            <template #subtitle-extended>
              <tooltip>
                <template #label-content>
                  <div class="men mr-1">
                    M: {{ audienceInsights.gender_men | Percentage | Empty }}
                  </div>
                </template>
                <template #hover-content>
                  <span>
                    {{ audienceInsights.gender_men | Percentage | Empty }}
                  </span>
                </template>
              </tooltip>

              <tooltip>
                <template #label-content>
                  <div class="women mx-1">
                    W: {{ audienceInsights.gender_women | Percentage | Empty }}
                  </div>
                </template>
                <template #hover-content>
                  <span>
                    {{ audienceInsights.gender_women | Percentage | Empty }}
                  </span>
                </template>
              </tooltip>

              <tooltip>
                <template #label-content>
                  <div class="other mx-1">
                    O: {{ audienceInsights.gender_other | Percentage | Empty }}
                  </div>
                </template>
                <template #hover-content>
                  <span>
                    {{ audienceInsights.gender_other | Percentage | Empty }}
                  </span>
                </template>
              </tooltip>
            </template>
          </metric-card>

          <metric-card
            v-if="Object.keys(appliedFilters).length > 0"
            class="audience-summary"
            :title="'Attributes'"
            :height="80"
          >
            <template #extra-item>
              <div class="container pl-0 pt-2">
                <ul class="filter-list">
                  <li
                    v-for="(filterKey, filterIndex) in Object.keys(
                      appliedFilters
                    )"
                    :key="filterKey"
                    class="filter-item ma-0 mr-1 d-flex align-center"
                  >
                    <tooltip
                      v-for="filter in Object.keys(appliedFilters[filterKey])"
                      :key="filter"
                    >
                      <template #label-content>
                        <v-chip
                          v-if="filterIndex < 4"
                          small
                          class="mr-1 ml-0 mt-0 mb-1 text-subtitle-2"
                          text-color="primary"
                          color="var(--v-primary-lighten3)"
                        >
                          {{ appliedFilters[filterKey][filter].name }}
                        </v-chip>
                      </template>
                      <template #hover-content>
                        <span
                          class="text-body-2 black--text text--darken-4"
                          v-bind.prop="
                            formatInnerHTML(
                              appliedFilters[filterKey][filter].hover
                            )
                          "
                        />
                      </template>
                    </tooltip>
                  </li>
                </ul>
              </div>
            </template>
          </metric-card>
        </div>
      </v-card>
      <v-tabs v-model="tabOption" class="mt-8">
        <v-tabs-slider color="primary"></v-tabs-slider>
        <div class="d-flex">
          <v-tab
            key="delivery"
            class="pa-2 mr-3 text-h3"
            color
            data-e2e="delivery-tab"
            @click="loadCustomersList = false"
          >
            Delivery
          </v-tab>
          <v-tab
            key="insights"
            class="text-h3"
            data-e2e="insights-tab"
            @click="loadCustomersList = true"
          >
            Insights
          </v-tab>
        </div>
      </v-tabs>
      <v-tabs-items v-model="tabOption" class="tabs-item">
        <v-tab-item key="delivery" class="delivery-tab">
          <v-row class="">
            <div
              class="mt-3 ml-3"
              :style="{ transition: '0.5s', width: deliveryCols + '%' }"
            >
              <delivery
                :sections="relatedEngagements"
                section-type="engagement"
                deliveries-key="deliveries"
                :audience-data="audience"
                data-e2e="engagement-delivery-details"
                @onOverviewSectionAction="triggerOverviewAction($event)"
                @onOverviewDestinationAction="
                  triggerOverviewDestinationAction($event)
                "
                @onAddDestination="addDestination($event)"
                @engagementDeliveries="deliverEngagement($event)"
                @addEngagement="openAttachEngagementDrawer()"
                @refreshEntityInsight="refreshEntity()"
              >
                <template #title-left>
                  <div class="d-flex align-center">
                    <span class="text-h3">Engagement delivery details</span>
                  </div>
                </template>
              </delivery>
              <standalone-delivery
                :audience="audience"
                data-e2e="standalone-delivery"
                @onAddStandaloneDestination="addStandaloneDestination($event)"
                @onDeliveryStandaloneDestination="refreshEntity()"
                @onRemoveStandaloneDestination="
                  onRemoveStandaloneDestination($event, data)
                "
                @onOpenStandaloneDestination="
                  onOpenStandaloneDestination($event, data)
                "
              />
            </div>
            <div :style="{ width: '1.5%' }"></div>
            <div class="mt-3" :style="{ width: advertisingCols + '%' }">
              <div
                class="collapsible-bar"
                :class="{
                  open: showAdvertising,
                  close: !showAdvertising,
                  'float-right': !showAdvertising,
                }"
                :style="{
                  height:
                    showAdvertising &&
                    audienceData.lookalike_audiences.length > 0
                      ? advertisingHeight
                      : '380px',
                }"
                @click="toggleAd()"
              >
                <span class="bar-text"> Digital advertising </span>
                <icon
                  type="expand-arrow"
                  :size="14"
                  :color="showAdvertising ? 'primary' : 'white'"
                  :class="{ 'rotate-icon-180': !showAdvertising }"
                  class="collapse-icon ml-1 mr-2"
                />
              </div>
              <v-card v-if="showAdvertising" class="digital-adv ml-6 mt-4" flat>
                <v-card-title v-if="showAdvertising" class="ml-2 text-h3">
                  Digital advertising
                </v-card-title>
                <v-card-text v-if="showAdvertising">
                  <div class="mx-2 my-1">
                    <matchrate
                      :match-rate="
                        audienceData.digital_advertising &&
                        audienceData.digital_advertising.match_rates
                          ? audienceData.digital_advertising.match_rates
                          : []
                      "
                      data-e2e="audience-matchrates"
                    />
                  </div>
                  <div ref="advertisingcard" class="lookalikes mx-2 my-6">
                    <lookalikes
                      :lookalike-data="audienceData.lookalike_audiences"
                      :standalone-data="audience.standalone_deliveries"
                      @openCreateLookalike="lookalikePageRedirect()"
                    />
                  </div>
                </v-card-text>
              </v-card>
              <v-card
                v-if="false"
                class="rounded-lg card-style mt-4 empty-adv"
                flat
                height="100%"
              >
                <error
                  class="background-empty"
                  icon-type="error-on-screens"
                  :icon-size="50"
                  title="Lookalike table is currently unavailable"
                  subtitle="Our team is working hard to fix it. Please be patient and try again soon!"
                >
                </error>
              </v-card>
            </div>
          </v-row>
        </v-tab-item>
        <v-tab-item key="insights" class="insights-tab">
          <insight-tab></insight-tab>
        </v-tab-item>
      </v-tabs-items>
    </div>

    <confirm-modal
      v-model="showConfirmModal"
      :type="confirmDialog.type"
      :icon="confirmDialog.icon"
      :title="confirmDialog.title"
      :sub-title="confirmDialog.subtitle"
      :right-btn-text="confirmDialog.btnText"
      :body="confirmDialog.body"
      @onCancel="showConfirmModal = false"
      @onConfirm="onConfirmAction()"
    />

    <confirm-modal
      v-model="showEditConfirmModal"
      right-btn-text="Save"
      left-btn-text="Cancel"
      :is-disabled="newAudienceName === ''"
      @onCancel="showEditConfirmModal = false"
      @onConfirm="updateLookalike()"
    >
      <template #body>
        <div class="mx-4">
          <icon type="audiences" color="black" :size="38" />
          <div class="text-h2 mb-4">Edit lookalike audience name</div>
          <div class="text-body-1 mb-7">
            <div>The updated name will be reflected in Hux only;</div>
            <div>in the lookalike destination.</div>
          </div>
          <text-field
            v-model="newAudienceName"
            placeholder="Type new name for [Facebook lookalike - Seed audience]"
            height="40"
            required
          />
        </div>
      </template>
    </confirm-modal>

    <edit-delivery-schedule
      v-model="editDeliveryDrawer"
      :audience-id="audienceId"
      :destination="scheduleDestination"
      :engagement-id="engagementId"
    />
    <!-- Add destination workflow -->
    <select-destinations-drawer
      v-model="selectedDestinations"
      close-on-action
      :toggle="showSelectDestinationsDrawer"
      @onToggle="(val) => (showSelectDestinationsDrawer = val)"
      @onSalesforceAdd="openSalesforceExtensionDrawer"
      @onAddDestination="triggerAttachDestination($event)"
      @onRemoveDestination="triggerRemoveDestination($event)"
    />
    <!-- Salesforce extension workflow -->
    <destination-data-extension-drawer
      v-model="selectedDestinations"
      close-on-action
      :toggle="showSalesforceExtensionDrawer"
      :destination="salesforceDestination"
      @onToggle="(val) => (showSalesforceExtensionDrawer = val)"
      @onBack="openSelectDestinationsDrawer"
      @updateDestination="triggerAttachDestination($event)"
    />

    <!-- Engagement workflow -->
    <attach-engagement
      ref="selectEngagements"
      v-model="engagementDrawer"
      close-on-action
      :final-engagements="selectedEngagements"
      @onEngagementChange="setSelectedEngagements"
      @onAddEngagement="triggerAttachEngagement($event)"
    />
    <look-alike-audience
      ref="lookalikeWorkflow"
      :toggle="showLookAlikeDrawer"
      :selected-audience="audience"
      @onBack="reloadAudienceData()"
      @onCreate="lookalikeCreated = true"
    />

    <delivery-history-drawer
      :audience-id="audienceId"
      :toggle="showDeliveryHistoryDrawer"
      data-e2e="delivery-history-drawer"
      @onToggle="(toggle) => (showDeliveryHistoryDrawer = toggle)"
    />

    <download-audience-drawer
      :audience-data="audience"
      :toggle="toggleDownloadAudienceDrawer"
      @onToggle="(isToggled) => (toggleDownloadAudienceDrawer = isToggled)"
    />
  </div>
</template>

<script>
import Vue from "vue"

// helpers
import { mapGetters, mapActions } from "vuex"
import filter from "lodash/filter"
import { formatInnerHTML } from "@/utils"

// common components
import ConfirmModal from "@/components/common/ConfirmModal.vue"
import Icon from "@/components/common/Icon.vue"
import MetricCard from "@/components/common/MetricCard.vue"
import Tooltip from "@/components/common/Tooltip.vue"

// views
import AttachEngagement from "@/views/Audiences/AttachEngagement.vue"
import DeliveryHistoryDrawer from "@/views/Shared/Drawers/DeliveryHistoryDrawer.vue"
import DestinationDataExtensionDrawer from "@/views/Audiences/Configuration/Drawers/DestinationDataExtension.vue"
import EditDeliverySchedule from "@/views/Engagements/Configuration/Drawers/EditDeliveryScheduleDrawer.vue"
import SelectDestinationsDrawer from "@/views/Audiences/Configuration/Drawers/SelectDestinations.vue"
import LookAlikeAudience from "@/views/Audiences/Configuration/Drawers/LookAlikeAudience.vue"
import configurationData from "@/components/common/MapChart/MapConfiguration.json"
import Delivery from "@/views/Audiences/Dashboard/Delivery.vue"
import Lookalikes from "@/views/Audiences/Dashboard/Lookalikes.vue"
import DashboardHeader from "@/views/Audiences/Dashboard/Header.vue"
import StandaloneDelivery from "@/views/Audiences/Dashboard/StandaloneDelivery.vue"
import Matchrate from "@/views/Audiences/Dashboard/Matchrate.vue"
import Error from "@/components/common/screens/Error"
import InsightTab from "@/views/Audiences/Dashboard/InsightTab.vue"
import DownloadAudienceDrawer from "@/views/Shared/Drawers/DownloadAudienceDrawer.vue"
import AudienceLookalikeDashboard from "@/views/Audiences/Lookalike/Dashboard.vue"
import TextField from "@/components/common/TextField"

export default {
  name: "AudienceInsight",
  components: {
    AttachEngagement,
    ConfirmModal,
    DeliveryHistoryDrawer,
    DestinationDataExtensionDrawer,
    EditDeliverySchedule,
    Icon,
    LookAlikeAudience,
    MetricCard,
    SelectDestinationsDrawer,
    Tooltip,
    Delivery,
    Lookalikes,
    DashboardHeader,
    StandaloneDelivery,
    Matchrate,
    Error,
    InsightTab,
    DownloadAudienceDrawer,
    AudienceLookalikeDashboard,
    TextField,
  },
  data() {
    return {
      advertisingHeight: "280",
      engagementList: {},
      showEditConfirmModal: false,
      newAudienceName: "",
      showAdvertising: true,
      deliveryCols: "57",
      advertisingCols: "40",

      tabOption: 0,
      showLookAlikeDrawer: false,
      lookalikeCreated: false,
      audienceHistory: [],
      relatedEngagements: [],
      isLookalikable: false,
      refreshAudience: false,
      audienceData: {},
      is_lookalike: false,
      percentageColumns: ["Women", "Men", "Other"],
      items: [
        {
          text: "Audiences",
          disabled: false,
          href: "/audiences",
          icon: "audiences",
        },
        {
          text: "",
          disabled: true,
          href: this.$route.path,
          icon: "lookalike",
          statusSize: 21,
          size: 12,
        },
      ],
      loading: false,
      loadingRelationships: false,
      loadingDemographics: true,
      configurationData: configurationData,
      modelInitial: [
        { value: "propensity", icon: "model" },
        { value: "ltv", icon: "lifetime" },
        { value: "churn", icon: "churn" },
      ],
      selectedEngagements: [],
      selectedDestinations: [],
      showDeliveryHistoryDrawer: false,
      showSelectDestinationsDrawer: false,
      showSalesforceExtensionDrawer: false,
      salesforceDestination: {},
      geoDrawer: {
        cities: false,
        countries: false,
        states: false,
      },
      engagementDrawer: false,
      engagementId: null,
      showConfirmModal: false,
      editDeliveryDrawer: false,
      scheduleDestination: {
        name: null,
        delivery_platform_type: null,
        id: null,
      },
      genderChartDimensions: {
        width: 269,
        height: 200,
      },
      deleteActionData: {},
      confirmDialog: {
        icon: "sad-face",
        type: "error",
        subtitle: "",
        title: "Remove  audience?",
        btnText: "Yes, remove it",
        body: "You will not be deleting this audience; this audience will not be attached to this specific engagement anymore.",
        actionType: "remove-audience",
      },
      toggleDownloadAudienceDrawer: false,
      matchrateStyles: {},
    }
  },
  computed: {
    ...mapGetters({
      getAudience: "audiences/audience",
      demographicsData: "audiences/demographics",
      ruleAttributes: "audiences/audiencesRules",
      getEngagementObject: "engagements/engagement",
    }),
    audience() {
      return this.audienceData
    },
    audienceId() {
      return this.$route.params.id
    },
    audienceInsights() {
      return this.audience && this.audience.audience_insights
        ? this.audience.audience_insights
        : {}
    },
    audienceOverview() {
      const metrics = {
        total_customers: {
          title: "Size",
          subtitle: "",
          icon: "targetsize",
          titleTooltip:
            "Current number of customers who fit the selected attributes.",
          tooltipWidth: "231",
        },
        age: { title: "Age range", subtitle: "", icon: "birth" },
      }

      const insights = this.audienceInsights
      return Object.keys(metrics).map((metric) => {
        return {
          ...metrics[metric],
          ...{
            subtitle:
              metric === "age"
                ? this.getAgeString(insights["min_age"], insights["max_age"])
                : insights[metric],
          },
        }
      })
    },

    showLookalike() {
      return !this.is_lookalike &&
        this.isLookalikable &&
        this.isLookalikable != "Disabled"
        ? true
        : false
    },
    breadcrumbItems() {
      const items = [
        {
          text: "Audiences",
          disabled: false,
          href: "/audiences",
          icon: "audiences",
        },
      ]
      if (this.audience) {
        if (this.audience.is_lookalike) {
          items.push({
            text: this.audience.name,
            disabled: true,
            href: this.$route.path,
            status: this.audience.status,
            icon: "lookalike",
            iconColor: "white",
            statusSize: 21,
            iconSize: 24,
            size: 12,
          })
        } else {
          items.push({
            text: this.audience.name,
            disabled: true,
            href: this.$route.path,
            status: this.audience.status,
            statusSize: 21,
          })
        }
        return items
      }
      return items
    },
    appliedFilters() {
      // try {
      let _filters = {}
      const attributeOptions = this.attributeOptions()
      if (this.audience && this.audience.filters) {
        this.audience.filters.forEach((section) => {
          section.section_filters.forEach((sectionFilter) => {
            const model = this.modelInitial.filter(
              (model) =>
                typeof sectionFilter.field === "string" &&
                sectionFilter.field.includes(model.value)
            )
            // TODO for the nestd filter check
            let ruleFilterObject = filter(attributeOptions, {
              key: sectionFilter.field.toLowerCase(),
            })

            const filterObj = {}
            if (ruleFilterObject.length > 0) {
              filterObj["name"] = ruleFilterObject[0]["name"]
              filterObj["key"] = sectionFilter.field

              filterObj.name = filterObj.name.replace(/_/gi, " ")
              if (model.length > 0) {
                filterObj["hover"] = "Between " + sectionFilter.value.join("-")
                if (!_filters[model[0].icon]) _filters[model[0].icon] = {}
                if (_filters[model[0].icon][sectionFilter.field])
                  _filters[model[0].icon][sectionFilter.field]["hover"] +=
                    "<br/> " + filterObj.hover
                else _filters[model[0].icon][sectionFilter.field] = filterObj
              } else {
                if (!_filters["general"]) _filters["general"] = {}
                filterObj["hover"] =
                  sectionFilter.type === "range"
                    ? "Include " + sectionFilter.value.join("-")
                    : sectionFilter.value
                if (_filters["general"][sectionFilter.field])
                  _filters["general"][sectionFilter.field]["hover"] +=
                    "<br/> " + filterObj.hover
                else _filters["general"][sectionFilter.field] = filterObj
              }
            }
          })
        })
      }
      return _filters
      // } catch (error) {
      //   return []
      // }
    },
  },
  async mounted() {
    await this.loadAudienceInsights()
    this.sizeHandler()
    this.matchHeight()
  },

  updated() {
    if (
      this.$refs.advertisingcard &&
      this.$refs.advertisingcard.parentElement &&
      this.$refs.advertisingcard.parentElement.parentElement
    ) {
      this.advertisingHeight =
        this.$refs.advertisingcard.parentElement.parentElement.clientHeight +
        21 +
        "px"
    }
  },

  methods: {
    ...mapActions({
      getAudienceById: "audiences/getAudienceById",
      getDestinations: "destinations/getAll",
      attachAudience: "engagements/attachAudience",
      detachAudience: "engagements/detachAudience",
      deliverAudience: "engagements/deliverAudience",
      deliverAudienceDestination: "engagements/deliverAudienceDestination",
      attachAudienceDestination: "engagements/attachAudienceDestination",
      detachAudienceDestination: "engagements/detachAudienceDestination",
      getDemographics: "audiences/getDemographics",
      setAlert: "alerts/setAlert",
      getAudiencesRules: "audiences/fetchConstants",
      getEngagementById: "engagements/get",
      deleteAudience: "audiences/remove",
      markFavorite: "users/markFavorite",
      detachStandaloneDestination: "audiences/removeStandaloneDestination",
      updateLookalikeAudience: "audiences/updateLookalike",
    }),
    formatInnerHTML: formatInnerHTML,
    attributeOptions() {
      const options = []
      if (this.ruleAttributes && this.ruleAttributes.rule_attributes) {
        Object.values(this.ruleAttributes.rule_attributes).forEach((attr) => {
          Object.keys(attr).forEach((optionKey) => {
            if (
              Object.values(attr[optionKey])
                .map((o) => typeof o === "object" && !Array.isArray(o))
                .includes(Boolean(true))
            ) {
              Object.keys(attr[optionKey]).forEach((att) => {
                if (typeof attr[optionKey][att] === "object") {
                  options.push({
                    key: att,
                    name: attr[optionKey][att]["name"],
                  })
                }
              })
            } else {
              options.push({
                key: optionKey,
                name: attr[optionKey]["name"],
              })
            }
          })
        })
      }
      return options
    },
    async refresh() {
      await this.loadAudienceInsights()
      this.sizeHandler()
    },
    addDestination(event) {
      this.closeAllDrawers()
      this.engagementId = event.id
      this.selectedDestinations = []
      this.selectedEngagements.push(event)
      this.selectedDestinations.push(
        ...event.deliveries.map((dest) => ({ id: dest.delivery_platform_id }))
      )
      this.showSelectDestinationsDrawer = true
    },
    addStandaloneDestination() {
      this.closeAllDrawers()
      this.showSelectDestinationsDrawer = true
    },
    async deliverEngagement(event) {
      switch (event.target.title.toLowerCase()) {
        case "Open destination":
          break

        case "deliver now":
          await this.deliverAudienceDestination({
            id: event.parent.id,
            audienceId: this.audienceId,
            destinationId: event.data.delivery_platform_id,
          })
          this.dataPendingMesssage(event, "destination")
          this.refresh()
          this.refreshEntity()
          break

        case "remove destination":
          this.showConfirmModal = true
          this.confirmDialog.actionType = "remove-destination"
          this.confirmDialog.title = `Remove ${event.data.name} destination?`
          this.confirmDialog.btnText = "Yes, remove it"
          this.confirmDialog.icon = "sad-face"
          this.confirmDialog.subtitle = ""
          this.confirmDialog.type = "error"
          this.confirmDialog.body =
            "You will not be deleting this destination; this destination will not be attached to this specific audience anymore."
          this.deleteActionData = {
            engagementId: event.parent.id,
            audienceId: this.audienceId,
            data: { id: event.data.delivery_platform_id },
          }
          this.showConfirmModal = true
          break
        default:
          break
      }
    },
    getAgeString(min_age, max_age) {
      if (min_age && max_age && min_age === max_age) {
        return min_age
      } else if (min_age && max_age) {
        return `${min_age}-${max_age}`
      } else {
        return "-"
      }
    },
    async loadEngagement(engagementId) {
      await this.getEngagementById(engagementId)
      this.engagementList = JSON.parse(
        JSON.stringify(this.getEngagementObject(this.engagementId))
      )
    },
    async refreshEntity() {
      this.loading = true
      this.$root.$emit("refresh-notifications")
      try {
        await this.loadAudienceInsights()
      } finally {
        this.loading = false
      }
    },
    async onConfirmAction() {
      this.showConfirmModal = false
      switch (this.confirmDialog.actionType) {
        case "edit-schedule":
          this.editDeliveryDrawer = true
          break
        case "remove-engagement":
          this.triggerAttachEngagement(this.deleteActionData)
          break
        case "remove-destination":
          await this.detachAudienceDestination(this.deleteActionData)
          break
        case "remove audience":
          await this.deleteAudience({ id: this.audience.id })
          break
        case "remove-standalone-destination":
          await this.detachStandaloneDestination({
            deleteActionData: this.deleteActionData,
            audienceId: this.audienceId,
          })
          break
        case "edit audience":
          this.$router.push({
            name: "AudienceUpdate",
            params: { id: this.audienceId },
          })
          break
        default:
          break
      }
      if (this.confirmDialog.actionType === "remove audience") {
        this.$router.push({ name: "Audiences" })
      } else {
        await this.loadAudienceInsights()
      }
    },

    /**
     * Formatting the values to the desired format using predefined application filters.
     *
     * @param {object} item item
     * @param {string} item.title item's title
     * @returns {number | string } formatted value
     */
    getFormattedValue(item) {
      switch (item.title) {
        case "Size":
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
    async triggerOverviewAction(event) {
      switch (event.target.title.toLowerCase()) {
        case "remove engagement": {
          this.confirmDialog.actionType = "remove-engagement"
          this.confirmDialog.title = "You are about to remove"
          this.confirmDialog.subtitle = event.data.name
          this.confirmDialog.icon = "sad-face"
          this.confirmDialog.type = "error"
          this.confirmDialog.btnText = "Yes, remove it"
          this.confirmDialog.body =
            "Are you sure you want to remove this engagement? By removing this engagement, it will not be deleted, but it will become unattached from this audience."
          this.deleteActionData = {
            data: {
              id: event.data.id,
              action: "Detach",
            },
          }
          this.showConfirmModal = true
          break
        }
        default:
          break
      }
    },

    async updateLookalike() {
      let payload = {
        name: this.newAudienceName,
      }
      try {
        this.audienceData = await this.updateLookalikeAudience({
          id: this.audienceId,
          payload: payload,
        })
      } finally {
        this.showEditConfirmModal = false
      }
    },

    async triggerOverviewDestinationAction(event) {
      try {
        switch (event.target.title.toLowerCase()) {
          case "deliver now":
            await this.deliverAudienceDestination({
              id: event.parent.id,
              audienceId: this.audienceId,
              destinationId: event.data.delivery_platform_id,
            })
            this.dataPendingMesssage(event, "destination")
            this.refreshEntity()
            break
          case "edit delivery schedule":
            this.confirmDialog.actionType = "edit-schedule"
            this.confirmDialog.title =
              "You are about to edit delivery schedule."
            this.confirmDialog.icon = "edit"
            this.confirmDialog.type = "primary"
            this.confirmDialog.btnText = "Yes, edit delivery schedule"
            this.confirmDialog.body =
              "This will override the default delivery schedule. However, this action is not permanent, the new delivery schedule can be reset to the default settings at any time."
            this.showConfirmModal = true
            this.engagementId = event.parent.id
            this.scheduleDestination = event.data
            break
          case "remove destination":
            this.engagementId = event.parent.id
            this.confirmDialog.actionType = "remove-destination"
            this.confirmDialog.icon = "sad-face"
            this.confirmDialog.type = "error"
            this.confirmDialog.subtitle = ""
            this.confirmDialog.title = `Remove ${event.data.name} destination?`
            this.confirmDialog.btnText = "Yes, remove it"
            this.confirmDialog.body =
              "You will not be deleting this destination; this destination will not be attached to this specific engagement anymore."
            this.deleteActionData = {
              engagementId: this.engagementId,
              audienceId: this.audienceId,
              data: { id: event.data.delivery_platform_id },
            }
            this.showConfirmModal = true
            break
          case "create lookalike":
            this.openLookAlikeDrawer()
            break
          default:
            break
        }
      } catch (error) {
        console.error(error)
      }
    },

    //Alert Message
    dataPendingMesssage(event, value) {
      if (value == "engagement") {
        const engagementName = event.data.name
        const audienceName = this.audience.name
        this.setAlert({
          type: "pending",
          message: `Your engagement '${engagementName}', has started delivering as part of the audience '${audienceName}'.`,
        })
      } else if (value == "destination") {
        const engagementName = event.parent.name
        const destinationName = event.data.name
        this.setAlert({
          type: "pending",
          message: `Your engagement '${engagementName}', has started delivering to '${destinationName}'.`,
        })
      }
    },

    // Drawer Section Starts
    setSelectedEngagements(engagementsList) {
      this.selectedEngagements = engagementsList
    },
    closeAllDrawers() {
      this.engagementDrawer = false
      this.showSelectDestinationsDrawer = false
      this.showSalesforceExtensionDrawer = false
    },
    openAttachEngagementDrawer() {
      this.closeAllDrawers()
      this.$refs.selectEngagements.fetchDependencies()
      this.selectedEngagements = this.relatedEngagements.map((eng) => ({
        id: eng.id,
      }))
      this.engagementDrawer = true
    },
    openLookAlikeDrawer() {
      this.$refs.lookalikeWorkflow.prefetchLookalikeDependencies()
      this.lookalikeCreated = false
      this.showLookAlikeDrawer = true
    },
    openDeliveryHistoryDrawer() {
      this.showDeliveryHistoryDrawer = true
    },
    async reloadAudienceData() {
      this.showLookAlikeDrawer = false
      if (this.lookalikeCreated) {
        await this.loadAudienceInsights()
      }
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
    triggerSelectDestination() {
      this.closeDrawers()
      this.showSelectDestinationsDrawer = true
    },
    triggerDataExtensionDrawer(destination) {
      this.closeDrawers()
      this.selectedDestination = destination || []
      this.showDataExtensionDrawer = true
    },
    async triggerAttachDestination(event) {
      const payload = event.destination
      await this.attachAudienceDestination({
        audienceId: this.audienceId,
        data: payload,
      })
      await this.loadAudienceInsights()
    },
    async triggerRemoveDestination(event) {
      this.deleteActionData = {
        audienceId: this.audienceId,
        data: { id: event.destination.id },
      }
      await this.detachAudienceDestination(this.deleteActionData)

      await this.loadAudienceInsights()
    },
    async triggerAttachEngagement(event) {
      if (event.action === "Attach") {
        const payload = {
          audiences: [
            {
              id: this.audienceId,
              destinations: [],
            },
          ],
        }
        await this.attachAudience({
          engagementId: event.data.id,
          data: payload,
        })
        this.refresh()
        this.refreshEntity()
      } else {
        const payload = { audience_ids: [] }
        payload.audience_ids.push(this.audienceId)
        await this.detachAudience({
          engagementId: event.data.id,
          data: payload,
        })
        // this.$router.push({
        //   name: "AudienceUpdate",
        // })
        this.refresh()
        this.refreshEntity()
      }
    },
    async loadAudienceInsights() {
      this.loading = true
      this.refreshAudience = true
      try {
        this.getAudiencesRules()
        await this.getAudienceById(this.$route.params.id)
        const _getAudience = this.getAudience(this.$route.params.id)
        if (_getAudience && this.refreshAudience) {
          this.audienceData = JSON.parse(JSON.stringify(_getAudience))
        }
        if (this.audience && this.audience.is_lookalike) {
          this.audienceHistory = this.audience.audienceHistory.filter(
            (e) => e.title == "Created"
          )
        } else {
          this.audienceHistory = this.audience.audienceHistory
        }
        this.relatedEngagements = this.audience.engagements
        this.lookalikeAudiences = this.audience.lookalike_audiences
        this.isLookalikable = this.audience.lookalikeable
        this.is_lookalike = this.audience.is_lookalike
        this.items[1].text = this.audience.name
        this.getDestinations()
      } finally {
        this.refreshAudience = false
        this.loading = false
      }
    },
    sizeHandler() {
      if (this.$refs.genderChart) {
        this.genderChartDimensions.width = this.$refs.genderChart.clientWidth
        this.genderChartDimensions.height = 200
      }
    },
    toggleGeoDrawer(geoLevel = "states") {
      this.geoDrawer[geoLevel] = !this.geoDrawer[geoLevel]
    },
    toggleAd() {
      if (this.showAdvertising) {
        this.deliveryCols = "96"
        this.advertisingCols = "1.5"
        this.showAdvertising = false
      } else {
        this.deliveryCols = "57"
        this.advertisingCols = "40"
        this.showAdvertising = true
      }
    },
    removeAudience(data) {
      this.showConfirmModal = true
      ;(this.confirmDialog.title = "You are about to delete"),
        (this.confirmDialog.btnText = "Yes, remove it")
      this.confirmDialog.icon = "sad-face"
      this.confirmDialog.subtitle = data.name
      this.confirmDialog.type = "error"
      this.confirmDialog.body =
        "By deleting this audience you will not be able to recover it and it may impact any associated engagements."
      this.confirmDialog.actionType = "remove audience"
      this.showConfirmModal = true
    },
    editAudience(data) {
      this.showConfirmModal = true
      this.confirmDialog.title = "Edit"
      this.confirmDialog.btnText = "Yes, edit"
      this.confirmDialog.icon = "edit"
      this.confirmDialog.subtitle = data.name
      this.confirmDialog.type = "error"
      this.confirmDialog.body = "Are you sure you want to edit this audience?"
      this.confirmDialog.actionType = "edit audience"
    },
    favoriteAudience(data) {
      let param
      if (data.is_lookalike === true) {
        param = { id: data.id, type: "lookalike" }
      } else {
        param = { id: data.id, type: "audiences" }
      }
      this.markFavorite(param)
      this.refreshEntity()
    },
    openDownloadDrawer() {
      this.toggleDownloadAudienceDrawer = true
    },
    onRemoveStandaloneDestination(data) {
      this.audienceId = data.delivery_platform_id
      this.confirmDialog.actionType = "remove-standalone-destination"
      this.confirmDialog.icon = "sad-face"
      this.confirmDialog.type = "error"
      this.confirmDialog.subtitle = ""
      this.confirmDialog.title = `Remove ${data.delivery_platform_name} destination?`
      this.confirmDialog.btnText = "Yes, remove it"
      this.confirmDialog.body =
        "You will not be deleting this destination; this destination will not be attached to this specific engagement anymore."
      this.deleteActionData = {
        destination_id: data.delivery_platform_id,
      }
      this.showConfirmModal = true
    },
    onOpenStandaloneDestination(data) {
      if (data && data.link) {
        window.open(data.link, "_blank")
      }
    },
    matchHeight() {
      var heightString = this.$refs.infoBox.$el.clientHeight + "px"
      Vue.set(this.matchrateStyles, "height", heightString)
    },
    openLookalikeEditModal() {
      this.showEditConfirmModal = true
    },
    lookalikePageRedirect() {
      this.$router.push({
        name: "LookalikeAudiences",
        params: { id: this.audienceId },
      })
    },
  },
}
</script>
<style lang="scss" scoped>
.audience-insight-wrap {
  .position-relative {
    position: relative;
  }
  .position-absolute {
    position: absolute;
    top: -7px;
    right: 6px;
  }
  .container {
    ul {
      padding: 0;
      margin: 0;
      list-style-type: none;
    }
  }
  .audience-summary {
    padding: 10px 15px;
  }
  .container {
    .filter-list {
      .filter-item {
        width: fit-content;
        height: auto;
        float: left;
        margin-left: 2%;
        span {
          .filter-title {
            &::after {
              content: ",\00a0";
            }
          }
          &:last-child {
            .filter-title {
              &::after {
                content: "";
                margin-right: 8px;
              }
            }
          }
        }
      }
    }
  }
  .blue-grey {
    border-width: 2px;
    border-style: solid;
    border-radius: 50%;
    font-size: 14px;
    width: 35px;
    height: 35px;
    line-height: 22px;
    color: var(--v-black-darken4) !important;
    cursor: default !important;
    background: transparent !important;
  }

  .tabs-item {
    .delivery-tab {
      .digital-adv {
        height: auto !important;
        .lookalikes {
          border-radius: 12px !important;
        }
      }
      .empty-adv {
        padding-top: 73px;
        padding-left: 16px;
        padding-right: 16px;
        .background-empty {
          background-image: url("../../../assets/images/lookalike_unavailable.png") !important;
          background-size: cover !important;
        }
      }
    }
  }
}
.icon-border {
  cursor: default;
}
.original-audience {
  background: var(--v-white-base) !important;
}
.font-audience-text {
  font-family: Open Sans;
  font-style: normal;
  font-weight: 600;
  font-size: 14px;
  line-height: 19px;
}
.original-audience-text {
  @extend .font-audience-text;
  color: var(--v-primary-base) !important;
}
::v-deep .v-snack__wrapper {
  max-width: 1300px !important;
}
.font-lookalike {
  font-family: Open Sans;
  font-style: normal;
  font-weight: normal;
}

.lookalikeMessageCard {
  @extend .font-lookalike;
  border-radius: 5px !important;
  background-color: var(--v-primary-lighten2) !important;
  font-size: 14px;
  color: var(--v-grey-base) !important;
}
.headingOverviewCard {
  @extend .font-lookalike;
  font-size: 15px !important;
}
.no-background {
  background: transparent;
}
.colorLink {
  color: var(--v-primary-base) !important;
}

.collapsible-bar {
  margin-top: 16px;
  width: 24px;
  cursor: pointer;
  float: left;
  position: relative;
  display: flex;
  &.open {
    border-top-left-radius: 12px;
    border-bottom-left-radius: 12px;
    background-color: var(--v-primary-lighten2) !important;
    .bar-text {
      display: none;
    }
  }
  &.close {
    border-top-right-radius: 12px;
    border-bottom-right-radius: 12px;
    background-color: var(--v-primary-base) !important;
  }
  .bar-text {
    writing-mode: vertical-rl;
    transform: scale(-1);
    color: var(--v-white-base) !important;
    position: absolute;
    top: 6%;
  }
  .collapse-icon {
    margin: 0;
    position: absolute;
    top: 50%;
  }
}
.overview-card {
  border-radius: 12px !important;
}
::v-deep .theme--light.v-tabs > .v-tabs-bar .v-tab:not(.v-tab--active) {
  color: var(--v-black-lighten4) !important;
}
::v-deep
  .v-tabs
  .v-tabs-bar
  .v-tabs-bar__content
  .v-tabs-slider-wrapper
  .v-tabs-slider {
  margin-top: 2px !important;
}
.icon_grey {
  margin-top: 10px;
}
</style>
