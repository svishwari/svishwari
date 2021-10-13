<template>
  <div class="audience-insight-wrap">
    <page-header class="background-border" :header-height-changes="'py-3'">
      <template #left>
        <breadcrumb :items="breadcrumbItems" />
      </template>
      <template #right>
        <v-icon size="22" color="primary" class="mr-2" @click="refreshEntity()">
          mdi-refresh
        </v-icon>

        <v-icon size="22" color="black lighten-3" class="icon-border pa-2 ma-1">
          mdi-plus-circle-multiple-outline
        </v-icon>
        <v-icon
          size="22"
          color="primary"
          class="icon-border pa-2 ma-1"
          @click="
            $router.push({
              name: 'AudienceUpdate',
              params: { id: audienceId },
            })
          "
        >
          mdi-pencil
        </v-icon>
        <span class="position-relative">
          <v-menu :min-width="100" left offset-y close-on-click>
            <template #activator="{ on }">
              <v-icon
                size="22"
                color="primary"
                class="icon-border pa-2 ma-1 d-none"
                v-on="on"
              >
                mdi-download
              </v-icon>
              <tooltip>
                <template #label-content>
                  <v-icon
                    size="22"
                    color="primary"
                    class="icon-border pa-2 ma-1"
                    v-on="on"
                  >
                    mdi-download
                  </v-icon>
                </template>
                <template #hover-content>
                  <span
                    class="text--caption"
                    style="width: 260px; display: block"
                  >
                    Download a generic .csv of this audience or a hashed file to
                    directly upload to Amazon or Google.
                  </span>
                </template>
              </tooltip>
            </template>
            <v-list>
              <v-list-item
                v-for="option in downloadOptions"
                :key="option.id"
                @click="initiateFileDownload(option)"
              >
                <v-list-item-title class="text-h6 black--text text--darken-4">
                  <div class="d-flex align-center">
                    <logo :type="option.icon" :size="18" class="mr-4" />
                    <span> {{ option.name }}</span>
                  </div>
                </v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
          <tooltip close-on-click>
            <template #label-content> </template>
            <template #hover-content>
              <span class="text--caption" style="width: 260px; display: block">
                Download the hashed customer data file of this audience for
                manual uploads to Amazon or Google.
              </span>
            </template>
          </tooltip>
        </span>
      </template>
    </page-header>
    <v-progress-linear :active="loading" :indeterminate="loading" />

    <div v-if="audienceHistory.length > 0" class="row px-15 my-1">
      <v-card
        v-if="audience && audience.is_lookalike"
        class="rounded-lg card-info-wrapper ma-2 card-shadow no-background"
      >
        <v-card-text>
          <div class="text-caption black--text text--darken-1">
            Original size
            <tooltip position-top>
              <template #label-content>
                <icon type="info" :size="12" />
              </template>
              <template #hover-content>
                Size of original audience that was used to create this
                Lookalike.
              </template>
            </tooltip>
            | Match rate
          </div>

          <div
            class="
              subtitle-slot
              size
              mr-2
              pt-2
              font-audience-text
              black--text
              text--darken-4
              font-weight-semi-bold
            "
          >
            <size :value="audience.source_size" /> |
            <tooltip position-bottom>
              <template #label-content>
                {{ audience.match_rate | Numeric(true, false, false, true) }}
              </template>
              <template #hover-content>
                {{ audience.match_rate }}
              </template>
            </tooltip>
          </div>
        </v-card-text>
      </v-card>

      <metric-card
        v-if="audience && audience.is_lookalike"
        class="ma-2 audience-summary py-2"
        :grow="0"
        :title="'Lookalike size'"
        :height="75"
      >
        <template #subtitle-extended>
          <span class="mr-2 pt-2">
            <span class="black--text text--darken-4 font-weight-semi-bold">
              <size :value="audience.size" />
            </span>
          </span>
        </template>
      </metric-card>

      <metric-card
        v-if="audience && audience.is_lookalike"
        class="ma-2 audience-summary original-audience"
        :grow="0"
        :title="'Original Audience'"
        :height="75"
      >
        <template #subtitle-extended>
          <span class="mr-2 pt-2">
            <span class="original-audience-text">
              <router-link
                :to="{
                  name: 'AudienceInsight',
                  params: { id: audience.source_id },
                }"
                class="text-decoration-none original-audience-text"
                append
                >{{ audience.source_name }}
              </router-link>
            </span>
          </span>
        </template>
      </metric-card>

      <metric-card
        v-for="(item, i) in audienceHistory"
        :key="i"
        class="ma-2 audience-summary"
        :grow="0"
        :title="item.title"
        :icon="item.icon"
        :height="75"
        data-e2e="audience-history"
      >
        <template #subtitle-extended>
          <span class="mr-2 mt-1">
            <tooltip>
              <template #label-content>
                <span class="black--text text--darken-4 font-weight-semi-bold">
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
                        black--text
                        text--darken-4
                        font-weight-semi-bold
                        text-over-2
                        filter-title
                      "
                      v-html="appliedFilters[filterKey][filter].name"
                    />
                  </template>
                  <template #hover-content>
                    <span class="text-caption black--text text--darken-4">
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
                  data-e2e="add-engagement"
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
                  v-if="audience && !audience.is_lookalike"
                  text
                  color="primary"
                  class="body-2 ml-n3"
                  data-e2e="delivery-history"
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
            v-model="lookalikeAudiences"
            :status="isLookalikable"
            @createLookalike="openLookAlikeDrawer"
          />
        </v-col>
      </v-row>
    </div>
    <div class="px-15 my-1">
      <v-card class="rounded pa-5 box-shadow-5">
        <h5 class="text-h5 mb-2">Audience overview</h5>
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
          class="row overview-list mb-0 ml-0 mt-1"
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
            data-e2e="audience-overview"
            @click="item.action ? onClick(item.action) : ''"
          >
            <template #subtitle-extended>
              <tooltip>
                <template #label-content>
                  <span class="font-weight-semi-bold">
                    {{ getFormattedValue(item) | Empty }}
                  </span>
                </template>
                <template #hover-content>
                  <span v-if="percentageColumns.includes(item.title)">{{
                    item.subtitle | Percentage | Empty
                  }}</span>
                  <span v-else>{{ item.subtitle | Numeric | Empty }}</span>
                </template>
              </tooltip>
            </template>
          </metric-card>
        </div>
      </v-card>
    </div>
    <v-row v-if="audience && !audience.is_lookalike" class="px-15 mt-2">
      <v-col md="7">
        <v-card class="mt-3 rounded-lg box-shadow-5" height="386">
          <v-progress-linear
            v-if="loadingDemographics"
            :active="loadingDemographics"
            :indeterminate="loadingDemographics"
          />
          <v-card-title class="pb-2 pl-5 pt-5">
            <div class="mt-2">
              <span class="black--text text--darken-4 text-h5">
                Demographic Overview
              </span>
            </div>
          </v-card-title>
          <map-chart
            v-if="!loadingDemographics"
            :map-data="mapChartData"
            :configuration-data="configurationData"
            data-e2e="map-chart"
          />
          <map-slider
            v-if="!loadingDemographics"
            :map-data="mapChartData"
            :configuration-data="configurationData"
          />
        </v-card>
      </v-col>
      <v-col md="5">
        <v-card class="mt-3 rounded-lg box-shadow-5" height="386">
          <v-progress-linear
            v-if="loadingDemographics"
            :active="loadingDemographics"
            :indeterminate="loadingDemographics"
          />
          <v-card-title class="pb-2 pl-5 pt-5">
            <div class="mt-2">
              <span class="black--text text--darken-4 text-h5">
                United States
              </span>
            </div>
          </v-card-title>
          <v-divider class="ml-5 mr-8 mt-0 mb-1" />
          <map-state-list
            v-if="!loadingDemographics"
            :map-data="mapChartData"
            :configuration-data="configurationData"
          />
        </v-card>
      </v-col>
    </v-row>
    <v-row v-if="audience && !audience.is_lookalike" class="px-15 mt-2">
      <v-col md="3">
        <v-card class="mt-3 rounded-lg box-shadow-5 pl-2 pr-2" height="290">
          <v-progress-linear
            v-if="loadingDemographics"
            :active="loadingDemographics"
            :indeterminate="loadingDemographics"
          />
          <v-card-title v-if="!loadingDemographics" class="pb-0 pl-5 pt-5">
            <div class="mt-2">
              <span class="black--text text--darken-4 text-h5">
                Top location &amp; Income
              </span>
            </div>
          </v-card-title>
          <income-chart
            v-if="!loadingDemographics"
            :data="demographicsData.income"
            data-e2e="income-chart"
          />
        </v-card>
      </v-col>
      <v-col md="6">
        <v-card class="mt-3 rounded-lg box-shadow-5" height="290">
          <v-progress-linear
            v-if="loadingDemographics"
            :active="loadingDemographics"
            :indeterminate="loadingDemographics"
          />
          <v-card-title v-if="!loadingDemographics" class="pb-2 pl-2 pt-5">
            <div class="mt-2 pl-5">
              <span class="black--text text--darken-4 text-h5">
                Gender &sol; monthly spending
              </span>
              <span class="text-body-2 time-frame">(last 6 months)</span>
            </div>
          </v-card-title>
          <gender-spend-chart
            v-if="!loadingDemographics"
            :data="demographicsData.spend"
            data-e2e="gender-spend-chart"
          />
        </v-card>
      </v-col>
      <v-col md="3">
        <v-card class="mt-3 rounded-lg box-shadow-5" height="290">
          <v-progress-linear
            v-if="loadingDemographics"
            :active="loadingDemographics"
            :indeterminate="loadingDemographics"
          />
          <v-card-title v-if="!loadingDemographics" class="pb-0 pl-5 pt-5">
            <div class="mt-2">
              <span class="black--text text--darken-4 text-h5"> Gender </span>
            </div>
          </v-card-title>
          <div v-if="!loadingDemographics" ref="genderChart">
            <doughnut-chart
              :chart-dimensions="genderChartDimensions"
              :data="genderChartData"
              label="Gender"
              data-e2e="gender-chart"
            />
          </div>
        </v-card>
      </v-col>
    </v-row>

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

    <geo-drawer
      geo-level="cities"
      :audience-id="audienceId"
      :results="audienceInsights.total_cities"
      :toggle="geoDrawer.cities"
      @onToggle="(isToggled) => (geoDrawer.cities = isToggled)"
    />

    <geo-drawer
      geo-level="countries"
      :audience-id="audienceId"
      :results="audienceInsights.total_countries"
      :toggle="geoDrawer.countries"
      @onToggle="(isToggled) => (geoDrawer.countries = isToggled)"
    />

    <geo-drawer
      geo-level="states"
      :audience-id="audienceId"
      :results="audienceInsights.total_us_states"
      :toggle="geoDrawer.states"
      @onToggle="(isToggled) => (geoDrawer.states = isToggled)"
    />
  </div>
</template>

<script>
// helpers
import { generateColor, saveFile } from "@/utils"
import { mapGetters, mapActions } from "vuex"
import filter from "lodash/filter"

// common components
import Avatar from "@/components/common/Avatar.vue"
import Breadcrumb from "@/components/common/Breadcrumb.vue"
import ConfirmModal from "@/components/common/ConfirmModal.vue"
import DeliveryOverview from "@/components/DeliveryOverview.vue"
import DoughnutChart from "@/components/common/DoughnutChart/DoughnutChart"
import Icon from "@/components/common/Icon.vue"
import IncomeChart from "@/components/common/incomeChart/IncomeChart.vue"
import LookAlikeCard from "@/components/common/LookAlikeCard.vue"
import MapChart from "@/components/common/MapChart/MapChart"
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
import configurationData from "@/components/common/MapChart/MapConfiguration.json"
import GeoDrawer from "@/views/Shared/Drawers/GeoDrawer.vue"
import Logo from "../../components/common/Logo.vue"

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
    GeoDrawer,
    Logo,
  },
  data() {
    return {
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
          size: 12,
        },
      ],
      downloadOptions: [
        {
          id: "c2b0bf2d9d48",
          name: ".csv",
          type: "amazon_ads",
          title: "Amazon Advertising CSV",
          icon: "amazon-outline",
        },
        {
          id: "5e112c22f1b1",
          name: ".csv",
          type: "google_ads",
          title: "Google Ads CSV",
          icon: "google-ads-outline",
        },
        {
          id: "2349d4353b9f",
          title: "Generic CSV",
          name: ".csv",
          type: "generic_ads",
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
    }
  },
  computed: {
    ...mapGetters({
      getAudience: "audiences/audience",
      demographicsData: "audiences/demographics",
      ruleAttributes: "audiences/audiencesRules",
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
          title: "Target size",
          subtitle: "",
        },
        total_countries: {
          title: "Countries",
          subtitle: "",
          icon: "mdi-earth",
          action: "toggleCountriesDrawer",
        },
        total_us_states: {
          title: "US States",
          subtitle: "",
          icon: "mdi-map",
          action: "toggleStatesDrawer",
        },
        total_cities: {
          title: "Cities",
          subtitle: "",
          icon: "mdi-map-marker-radius",
          action: "toggleCitiesDrawer",
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

    genderChartData() {
      if (
        this.demographicsData.gender &&
        (this.demographicsData.gender.gender_men ||
          this.demographicsData.gender.gender_women ||
          this.demographicsData.gender.gender_other)
      ) {
        return [
          {
            label: "Men",
            population_percentage:
              this.demographicsData.gender.gender_men.population_percentage,
            size: this.demographicsData.gender.gender_men.size,
          },
          {
            label: "Women",
            population_percentage:
              this.demographicsData.gender.gender_women.population_percentage,
            size: this.demographicsData.gender.gender_women.size,
          },
          {
            label: "Other",
            population_percentage:
              this.demographicsData.gender.gender_other.population_percentage,
            size: this.demographicsData.gender.gender_other.size,
          },
        ]
      } else {
        return []
      }
    },
    mapChartData() {
      return this.demographicsData.demo
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
     *
     * @returns {Array} filters
     */
    appliedFilters() {
      try {
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
              const filterObj = {
                name: ruleFilterObject[0]["name"],
                key: sectionFilter.field,
              }

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
            })
          })
        }
        return _filters
      } catch (error) {
        return []
      }
    },
  },
  created() {
    window.addEventListener("resize", this.sizeHandler)
  },
  destroyed() {
    window.removeEventListener("resize", this.sizeHandler)
  },
  async mounted() {
    this.sizeHandler()
    await this.loadAudienceInsights()
    this.fetchDemographics()
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
      downloadAudienceData: "audiences/fetchAudienceData",
      setAlert: "alerts/setAlert",
      getAudiencesRules: "audiences/fetchConstants",
    }),
    attributeOptions() {
      const options = []
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
      return options
    },
    async fetchDemographics() {
      this.loadingDemographics = true
      await this.getDemographics(this.$route.params.id)
      this.loadingDemographics = false
    },
    async initiateFileDownload(option) {
      const audienceName = this.audience.name
      this.setAlert({
        type: "pending",
        message: `Download for the '${audienceName}' with '${option.title}', has started in background, stay tuned.`,
      })
      const fileBlob = await this.downloadAudienceData({
        id: this.audienceId,
        type: option.type,
      })
      saveFile(fileBlob)
    },
    getFormattedTime(time) {
      return this.$options.filters.Date(time, "relative") + " by"
    },
    getColorCode(name) {
      return generateColor(name, 30, 60) + " !important"
    },

    async refreshEntity() {
      this.loading = true
      this.$root.$emit("refresh-notifications")
      await this.loadAudienceInsights()
      this.loading = false
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

    /**
     * Formatting the values to the desired format using predefined application filters.
     *
     * @param {object} item item
     * @param {string} item.title item's title
     * @returns {string} formatted value
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
          await this.deliverAudience({
            id: event.data.id,
            audienceId: this.audienceId,
          })
          this.dataPendingMesssage(event, "engagement")
          break
        case "view delivery history":
          break
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
            this.confirmDialog.title = `Remove ${event.data.name} destination?`
            this.confirmDialog.btnText = "Yes, remove it"
            this.confirmDialog.body =
              "You will not be deleting this destination; this destination will not be attached to this specific engagement anymore."
            this.deleteActionData = {
              engagementId: this.engagementId,
              audienceId: this.audienceId,
              data: { id: event.data.id },
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
      this.refreshAudience = true
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
      this.refreshAudience = false
      this.loading = false
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
    onClick(action) {
      switch (action) {
        case "toggleCitiesDrawer":
          this.toggleGeoDrawer("cities")
          break
        case "toggleCountriesDrawer":
          this.toggleGeoDrawer("countries")
          break
        case "toggleStatesDrawer":
          this.toggleGeoDrawer("states")
          break
      }
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
</style>
