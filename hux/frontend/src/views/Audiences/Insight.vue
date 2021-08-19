<template>
  <div class="audience-insight-wrap">
    <page-header class="background-border" :header-height-changes="'py-3'">
      <template #left>
        <breadcrumb :items="breadcrumbItems" />
      </template>
      <template #right>
        <v-icon size="22" color="lightGrey" class="mr-2"> mdi-refresh </v-icon>

        <v-icon size="22" color="lightGrey" class="icon-border pa-2 ma-1">
          mdi-plus-circle-multiple-outline
        </v-icon>
        <v-icon size="22" color="lightGrey" class="icon-border pa-2 ma-1">
          mdi-pencil
        </v-icon>
        <v-icon size="22" color="lightGrey" class="icon-border pa-2 ma-1">
          mdi-download
        </v-icon>
      </template>
    </page-header>
    <v-progress-linear :active="loading" :indeterminate="loading" />

    <div v-if="audienceHistory.length > 0" class="row px-15 my-1">
      <metric-card
        v-for="(item, i) in audienceHistory"
        :key="i"
        class="ma-2 audience-summary"
        :grow="0"
        :title="item.title"
        :icon="item.icon"
        :height="75"
      >
        <template #subtitle-extended>
          <span class="mr-2 mt-1">
            <tooltip>
              <template #label-content>
                <span class="neroBlack--text font-weight-semi-bold">
                  {{ getFormattedTime(item.subtitle) }}
                </span>
              </template>
              <template #hover-content>
                {{ item.subtitle | Date | Empty }}
              </template>
            </tooltip>
          </span>
          <avatar :name="item.fullName" />
        </template>
      </metric-card>
      <metric-card
        v-if="audience.is_lookalike"
        class="ma-2 audience-summary original-audience"
        :grow="0"
        :title="'Original Audience'"
        :height="75"
      >
        <template #subtitle-extended>
          <span class="mr-2 pt-2">
            <span class="original-audience-text">
              {{ audience.name }}
            </span>
          </span>
        </template>
      </metric-card>
      <metric-card
        v-if="audience.is_lookalike"
        class="ma-2 audience-summary"
        :grow="0"
        :title="'Original • Actual size'"
        :height="75"
      >
        <template #subtitle-extended>
          <span class="mr-2 pt-2">
            <span class="neroBlack--text font-weight-semi-bold">
              <size :value="audience.size" /> &bull;
              <size :value="audience.size" />
            </span>
          </span>
        </template>
      </metric-card>

      <metric-card
        v-if="Object.keys(appliedFilters).length > 0"
        class="ma-2 audience-summary"
        :title="'Attributes'"
        :height="75"
      >
        <template #extra-item>
          <div class="container pl-0 pt-2">
            <ul class="filter-list">
              <li
                v-for="filterKey in Object.keys(appliedFilters)"
                :key="filterKey"
                class="filter-item ma-0 mr-1 d-flex align-center"
              >
                <icon
                  :type="filterKey == 'general' ? 'plus' : filterKey"
                  :size="filterKey == 'general' ? 10 : 21"
                  class="mr-1"
                />
                <tooltip
                  v-for="filter in Object.keys(appliedFilters[filterKey])"
                  :key="filter"
                >
                  <template #label-content>
                    <span
                      class="
                        neroBlack--text
                        font-weight-semi-bold
                        text-over-2
                        filter-title
                      "
                      v-html="appliedFilters[filterKey][filter].name"
                    />
                  </template>
                  <template #hover-content>
                    <span class="text-caption neroBlack--text">
                      <div class="mb-2">
                        {{ appliedFilters[filterKey][filter].name }}
                      </div>
                      <span v-html="appliedFilters[filterKey][filter].hover" />
                    </span>
                  </template>
                </tooltip>
              </li>
            </ul>
          </div>
        </template>
      </metric-card>
    </div>
    <div
      v-if="relatedEngagements.length > 0"
      class="px-15 my-1 mb-4 pt-6 relationships"
    >
      <v-row class="pa-3 pb-5" style="min-height: 200px">
        <v-col :md="showLookalike ? 9 : 12" class="pa-0">
          <delivery-overview
            :sections="relatedEngagements"
            section-type="engagement"
            deliveries-key="deliveries"
            :loading-relationships="loadingRelationships"
            @onOverviewSectionAction="triggerOverviewAction($event)"
            @onOverviewDestinationAction="
              triggerOverviewDestinationAction($event)
            "
          >
            <template #title-left>
              <span class="text-h5">Engagement &amp; delivery overview</span>
            </template>
            <template #title-right>
              <div class="d-flex align-center">
                <v-btn
                  text
                  class="
                    d-flex
                    align-center
                    primary--text
                    text-decoration-none
                    body-2
                  "
                  @click="openAttachEngagementDrawer()"
                >
                  <icon
                    type="engagements"
                    :size="14"
                    color="primary"
                    class="mr-2"
                  />
                  Add to an engagement
                </v-btn>
                <v-btn
                  text
                  color="primary"
                  class="body-2 ml-n3"
                  @click="openDeliveryHistoryDrawer()"
                >
                  <icon type="history" :size="14" class="mr-1" />
                  Delivery history
                </v-btn>
              </div>
            </template>
            <template #empty-deliveries>
              <div class="mb-2">
                This engagement has no destinations yet. Add destinations in the
                submenu located in the right corner above.
              </div>
            </template>
          </delivery-overview>
        </v-col>
        <v-col v-if="showLookalike" md="3" class="pl-6 pr-0 py-0">
          <look-alike-card
            :key="lookalikeAudiences"
            v-model="lookalikeAudiences"
            :status="isLookalikable"
            @createLookalike="openLookAlikeDrawer"
          />
        </v-col>
      </v-row>
    </div>
    <div class="px-15 my-1">
      <v-card class="rounded pa-5 box-shadow-5">
        <div class="overview">Audience overview</div>
        <div class="row overview-list mb-0 ml-0 mt-1">
          <metric-card
            v-for="(item, i) in Object.keys(insightInfoItems)"
            :key="i"
            class="mr-3"
            :grow="i === 0 ? 2 : 1"
            :title="insightInfoItems[item].title"
            :icon="insightInfoItems[item].icon"
            :height="80"
          >
            <template #subtitle-extended>
              <tooltip>
                <template #label-content>
                  <span class="font-weight-semi-bold">
                    {{ getFormattedValue(insightInfoItems[item]) | Empty }}
                  </span>
                </template>
                <template #hover-content>
                  {{ insightInfoItems[item].subtitle | Empty }}
                </template>
              </tooltip>
            </template>
          </metric-card>
        </div>
      </v-card>
    </div>
    <v-row class="px-15 mt-2">
      <v-col md="7">
        <v-card class="mt-3 rounded-lg box-shadow-5" height="386">
          <v-card-title class="chart-style pb-2 pl-5 pt-5">
            <div class="mt-2">
              <span class="neroBlack--text text-h5">
                Demographic Overview
              </span>
            </div>
          </v-card-title>
          <map-chart :map-data="mapChartData" />
          <map-slider :map-data="mapChartData" />
        </v-card>
      </v-col>
      <v-col md="5">
        <v-card class="mt-3 rounded-lg box-shadow-5" height="386">
          <v-card-title class="chart-style pb-2 pl-5 pt-5">
            <div class="mt-2">
              <span class="neroBlack--text text-h5"> United States </span>
            </div>
          </v-card-title>
          <v-divider class="ml-5 mr-8 mt-0 mb-1" />
          <map-state-list :map-data="mapChartData" />
        </v-card>
      </v-col>
    </v-row>
    <v-row class="px-15 mt-2">
      <v-col md="3">
        <v-card class="mt-3 rounded-lg box-shadow-5 pl-2 pr-2" height="273">
          <v-card-title class="chart-style pb-0 pl-5 pt-5">
            <div class="mt-2">
              <span class="neroBlack--text text-h5">
                Top location &amp; Income
              </span>
            </div>
          </v-card-title>
          <income-chart />
        </v-card>
      </v-col>
      <v-col md="6">
        <v-card class="mt-3 rounded-lg box-shadow-5" height="273">
          <v-card-title class="chart-style pb-2 pl-5 pt-5">
            <div class="mt-2">
              <span class="neroBlack--text text-h5">
                Gender / monthly spending in 2021
              </span>
            </div>
          </v-card-title>
          <gender-spend-chart />
        </v-card>
      </v-col>
      <v-col md="3">
        <v-card class="mt-3 rounded-lg box-shadow-5" height="273">
          <v-card-title class="chart-style pb-2 pl-5 pt-5">
            <div class="mt-2">
              <span class="neroBlack--text text-h5"> Gender </span>
            </div>
          </v-card-title>
          <doughnut-chart
            :width="250"
            :height="200"
            :data="genderChartData"
            label="Gender"
          />
        </v-card>
      </v-col>
    </v-row>
    <hux-alert
      v-model="flashAlert"
      :type="alert.type"
      :title="alert.title"
      :message="alert.message"
    />

    <confirm-modal
      v-model="showConfirmModal"
      title="You are about to edit delivery schedule."
      right-btn-text="Yes, edit delivery schedule"
      body="This will override the default delivery schedule. However, this action is not permanent, the new delivery schedule can be reset to the default settings at any time."
      @onCancel="showConfirmModal = false"
      @onConfirm="
        showConfirmModal = false
        editDeliveryDrawer = true
      "
    />

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
      @onToggle="(toggle) => (showDeliveryHistoryDrawer = toggle)"
    />
  </div>
</template>

<script>
// helpers
import { generateColor } from "@/utils"
import { mapGetters, mapActions } from "vuex"

// common components
import Avatar from "@/components/common/Avatar.vue"
import Breadcrumb from "@/components/common/Breadcrumb.vue"
import ConfirmModal from "@/components/common/ConfirmModal.vue"
import DeliveryOverview from "@/components/DeliveryOverview.vue"
import DoughnutChart from "@/components/common/DoughnutChart/DoughnutChart"
import genderData from "@/components/common/DoughnutChart/genderData.json"
import HuxAlert from "@/components/common/HuxAlert.vue"
import Icon from "@/components/common/Icon.vue"
import IncomeChart from "@/components/common/incomeChart/IncomeChart.vue"
import LookAlikeCard from "@/components/common/LookAlikeCard.vue"
import MapChart from "@/components/common/MapChart/MapChart"
import mapData from "@/components/common/MapChart/mapData.json"
import mapSlider from "@/components/common/MapChart/mapSlider"
import MapStateList from "@/components/common/MapChart/MapStateList"
import MetricCard from "@/components/common/MetricCard.vue"
import PageHeader from "@/components/PageHeader.vue"
import Size from "@/components/common/huxTable/Size.vue"
import Tooltip from "@/components/common/Tooltip.vue"

// views
import AttachEngagement from "@/views/Audiences/AttachEngagement.vue"
import DeliveryHistoryDrawer from "@/views/Shared/Drawers/DeliveryHistoryDrawer.vue"
import DestinationDataExtensionDrawer from "@/views/Audiences/Configuration/Drawers/DestinationDataExtension.vue"
import EditDeliverySchedule from "@/views/Engagements/Configuration/Drawers/EditDeliveryScheduleDrawer.vue"
import SelectDestinationsDrawer from "@/views/Audiences/Configuration/Drawers/SelectDestinations.vue"
import LookAlikeAudience from "./Configuration/Drawers/LookAlikeAudience.vue"
import GenderSpendChart from "@/components/common/GenderSpendChart/GenderSpendChart"

export default {
  name: "AudienceInsight",
  components: {
    AttachEngagement,
    Avatar,
    Breadcrumb,
    ConfirmModal,
    DeliveryHistoryDrawer,
    DeliveryOverview,
    DestinationDataExtensionDrawer,
    DoughnutChart,
    EditDeliverySchedule,
    HuxAlert,
    Icon,
    IncomeChart,
    LookAlikeAudience,
    LookAlikeCard,
    MapChart,
    mapSlider,
    MapStateList,
    MetricCard,
    PageHeader,
    SelectDestinationsDrawer,
    Size,
    Tooltip,
    GenderSpendChart,
  },
  data() {
    return {
      mapChartData: mapData.demographic_overview,
      showLookAlikeDrawer: false,
      lookalikeCreated: false,
      audienceHistory: [],
      relatedEngagements: [],
      isLookalikable: false,
      is_lookalike: false,
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
          size: 12,
        },
      ],
      loading: false,
      loadingRelationships: false,
      flashAlert: false,
      alert: {
        type: "success",
        title: "YAY!",
        message: "Successfully triggered delivery.",
      },
      insightInfoItems: {
        total_customers: {
          title: "Target size",
          subtitle: "",
        },
        total_countries: {
          title: "Countries",
          subtitle: "",
          icon: "mdi-earth",
        },
        total_us_states: { title: "US States", subtitle: "", icon: "mdi-map" },

        total_cities: {
          title: "Cities",
          subtitle: "",
          icon: "mdi-map-marker-radius",
        },
        age: { title: "Age", subtitle: "", icon: "mdi-cake-variant" },
        gender_women: {
          title: "Women",
          subtitle: "",
          icon: "mdi-gender-female",
        },
        gender_men: { title: "Men", subtitle: "", icon: "mdi-gender-male" },
        gender_other: {
          title: "Other",
          subtitle: "",
          icon: "mdi-gender-male-female",
        },
      },
      modelInitial: [
        { value: "propensity", icon: "model" },
        { value: "lifetime", icon: "lifetime" },
        { value: "churn", icon: "churn" },
      ],
      genderChartData: [
        {
          label: "Men",
          population_percentage:
            genderData.gender.gender_men.population_percentage,
          size: genderData.gender.gender_men.size,
        },
        {
          label: "Women",
          population_percentage:
            genderData.gender.gender_women.population_percentage,
          size: genderData.gender.gender_women.size,
        },
        {
          label: "Other",
          population_percentage:
            genderData.gender.gender_other.population_percentage,
          size: genderData.gender.gender_other.size,
        },
      ],
      selectedEngagements: [],
      selectedDestinations: [],
      showDeliveryHistoryDrawer: false,
      showSelectDestinationsDrawer: false,
      showSalesforceExtensionDrawer: false,
      salesforceDestination: {},

      engagementDrawer: false,
      engagementId: null,
      showConfirmModal: false,
      editDeliveryDrawer: false,
      scheduleDestination: {
        name: null,
        delivery_platform_type: null,
        id: null,
      },
    }
  },
  computed: {
    ...mapGetters({
      getAudience: "audiences/audience",
      getAudienceInsights: "audiences/insights",
    }),
    audience() {
      return this.getAudience(this.$route.params.id)
    },
    audienceId() {
      return this.$route.params.id
    },
    audienceInsights() {
      return this.getAudienceInsights(this.audienceId)
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
            icon: "lookalike",
            size: 12,
          })
        } else {
          items.push({
            text: this.audience.name,
            disabled: true,
            href: this.$route.path,
          })
        }
        return items
      }
      return items
    },
    /**
     * This computed property is converting the audience filters conditions
     * into groups of fiters and having custom keys which are needed
     * on the UI transformation.
     */
    appliedFilters() {
      try {
        let _filters = {}
        if (this.audience && this.audience.filters) {
          this.audience.filters.forEach((section) => {
            section.section_filters.forEach((filter) => {
              const model = this.modelInitial.filter(
                (model) =>
                  typeof filter.field === "string" &&
                  filter.field.includes(model.value)
              )
              const filterObj = {
                name: this.$options.filters.TitleCase(filter.field),
                key: filter.field,
              }

              filterObj.name = filterObj.name.replace(/_/gi, " ")
              if (model.length > 0) {
                filterObj["hover"] = "Between " + filter.value.join("-")
                if (!_filters[model[0].icon]) _filters[model[0].icon] = {}
                if (_filters[model[0].icon][filter.field])
                  _filters[model[0].icon][filter.field]["hover"] +=
                    "<br/> " + filterObj.hover
                else _filters[model[0].icon][filter.field] = filterObj
              } else {
                if (!_filters["general"]) _filters["general"] = {}
                filterObj["hover"] =
                  filter.type === "range"
                    ? "Include " + filter.value.join("-")
                    : filter.value
                if (_filters["general"][filter.field])
                  _filters["general"][filter.field]["hover"] +=
                    "<br/> " + filterObj.hover
                else _filters["general"][filter.field] = filterObj
              }
            })
          })
        }
        return _filters
      } catch (error) {
        return []
      }
    },
  },
  async mounted() {
    await this.loadAudienceInsights()
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
    }),
    getFormattedTime(time) {
      return this.$options.filters.Date(time, "relative") + " by"
    },
    getColorCode(name) {
      return generateColor(name, 30, 60) + " !important"
    },

    /**
     * This is to map the Insight Values from the getter.
     */
    mapInsights() {
      this.insightInfoItems = Object.keys(this.insightInfoItems).map(
        (insight) => {
          return {
            title: this.insightInfoItems[insight].title,
            subtitle:
              insight !== "age"
                ? this.audience.audience_insights[insight]
                : this.getAgeString(
                    this.audience.audience_insights["min_age"],
                    this.audience.audience_insights["max_age"]
                  ),
            icon: this.insightInfoItems[insight].icon,
          }
        }
      )
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

    /**
     * Formatting the values to the desired format using predebfined application filters.
     */
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
    async triggerOverviewAction(event) {
      switch (event.target.title.toLowerCase()) {
        case "add a destination": {
          this.closeAllDrawers()
          this.engagementId = event.data.id
          this.selectedDestinations = []
          this.selectedEngagements.push(event.data)
          this.selectedDestinations.push(
            ...event.data.deliveries.map((dest) => ({ id: dest.id }))
          )
          this.showSelectDestinationsDrawer = true
          break
        }
        case "deliver all":
          try {
            await this.deliverAudience({
              id: event.data.id,
              audienceId: this.audienceId,
            })
            this.dataPendingMesssage(event.data.name, "engagement")
          } catch (error) {
            this.dataErrorMesssage(event, "engagement")
            console.error(error)
          }
          break
        case "view delivery history":
          break
        case "remove engagement": {
          let payload = {
            data: {
              id: event.data.id,
              action: "Detach",
            },
          }
          this.triggerAttachEngagement(payload)
          break
        }
        default:
          break
      }
    },
    async triggerOverviewDestinationAction(event) {
      try {
        switch (event.target.title.toLowerCase()) {
          case "deliver now":
            await this.deliverAudienceDestination({
              id: event.parent.id,
              audienceId: this.audienceId,
              destinationId: event.data.id,
            })
            this.dataPendingMesssage(event, "destination")
            break
          case "edit delivery schedule":
            this.engagementId = event.parent.id
            this.showConfirmModal = true
            this.scheduleDestination = event.data
            break
          case "remove destination":
            this.engagementId = event.parent.id
            await this.detachAudienceDestination({
              engagementId: this.engagementId,
              audienceId: this.audienceId,
              data: { id: event.data.id },
            })
            break
          case "create lookalike":
            this.openLookAlikeDrawer()
            break
          default:
            break
        }
      } catch (error) {
        this.dataErrorMesssage(event, "destination")
        console.error(error)
      }
    },

    //Alert Message
    dataPendingMesssage(event, value) {
      this.alert.type = "Pending"
      this.alert.title = ""
      if (value == "engagement") {
        const engagementName = event.data.name
        const audienceName = this.audience.name
        this.alert.message = `Your engagement '${engagementName}', has started delivering as part of the audience '${audienceName}'.`
      } else if (value == "destination") {
        const engagementName = event.parent.name
        const destinationName = event.data.name
        this.alert.message = `Your engagement '${engagementName}', has started delivering to '${destinationName}'.`
      }
      this.flashAlert = true
    },
    dataErrorMesssage(event, value) {
      this.alert.type = "error"
      this.alert.title = "OH NO!"
      if (value == "engagement") {
        const engagementName = event.data.name
        const audienceName = this.audience.name
        this.alert.message = `Failed to schedule a delivery of your engagement '${engagementName}', from '${audienceName}'.`
      } else if (value == "destination") {
        const engagementName = event.parent.name
        const destinationName = event.data.name
        this.alert.message = `Failed to schedule delivery of your engagement '${engagementName}', to '${destinationName}'.`
      }
      this.flashAlert = true
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
        engagementId: this.engagementId,
        audienceId: this.audienceId,
        data: payload,
      })
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
      } else {
        const payload = { audience_ids: [] }
        payload.audience_ids.push(this.audienceId)
        await this.detachAudience({
          engagementId: event.data.id,
          data: payload,
        })
      }
      await this.loadAudienceInsights()
    },
    async loadAudienceInsights() {
      this.loading = true
      await this.getAudienceById(this.$route.params.id)
      this.audienceHistory = this.audience.audienceHistory
      this.relatedEngagements = this.audience.engagements
      this.lookalikeAudiences = this.audience.lookalike_audiences
      this.isLookalikable = this.audience.lookalikeable
      this.is_lookalike = this.audience.is_lookalike
      this.items[1].text = this.audience.name
      this.mapInsights()
      this.getDestinations()
      this.loading = false
    },
  },
}
</script>
<style lang="scss" scoped>
.audience-insight-wrap {
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
    color: var(--v-neroBlack-base) !important;
    cursor: default !important;
    background: transparent !important;
  }
}
.icon-border {
  cursor: default;
}
.original-audience {
  background: var(--v-white-base) !important;
}
.original-audience-text {
  font-family: Open Sans;
  font-style: normal;
  font-weight: 600;
  font-size: 14px;
  line-height: 19px;
  color: var(--v-primary-base) !important;
}
::v-deep .v-snack__wrapper {
  max-width: 1300px !important;
}
</style>
