<template>
  <div class="engagement-dash">
    <!-- Page Header -->
    <page-header class="d-flex">
      <template #left>
        <div class="d-flex align-center bread-crumb">
          <breadcrumb :items="breadcrumbItems" />
          <div v-if="engagementList && engagementList.status" class="ml-3">
            <status :status="engagementList.status" :icon-size="17"></status>
          </div>
        </div>
      </template>
      <template #right>
        <v-icon size="22" color="lightGrey" class="mr-2">mdi-refresh</v-icon>
        <v-icon size="22" color="lightGrey" class="icon-border pa-2 ma-1">
          mdi-pencil
        </v-icon>
        <v-icon size="22" color="lightGrey" class="icon-border pa-2 ma-1">
          mdi-download
        </v-icon>
      </template>
    </page-header>
    <v-progress-linear :active="loading" :indeterminate="loading" />
    <!-- Page Content Starts here -->
    <div v-if="!loading" class="inner-wrap px-15 py-8">
      <!-- Summary Cards Wrapper -->
      <div class="summary-wrap d-flex mb-6">
        <metric-card class="mr-3 shrink" :title="summaryCards[0].title">
          <template #subtitle-extended>
            <div class="font-weight-semi-bold neroBlack--text my-2">
              {{ deliverySchedule }}
            </div>
          </template>
        </metric-card>
        <metric-card class="mr-3 shrink" :title="summaryCards[1].title">
          <template v-if="summaryCards[1].subLabel" #subtitle-extended>
            <span class="mr-2">
              <tooltip>
                <template #label-content>
                  <span class="font-weight-semi-bold neroBlack--text">
                    {{ summaryCards[1].value }}
                  </span>
                </template>
                <template #hover-content>
                  {{ summaryCards[1].hoverValue | Date | Empty }}
                </template>
              </tooltip>
            </span>
            <avatar :name="summaryCards[1].subLabel" />
          </template>
        </metric-card>
        <metric-card class="mr-3 shrink" :title="summaryCards[2].title">
          <template v-if="summaryCards[2].subLabel" #subtitle-extended>
            <span class="mr-2">
              <tooltip>
                <template #label-content>
                  <span class="font-weight-semi-bold neroBlack--text">
                    {{ summaryCards[2].value }}
                  </span>
                </template>
                <template #hover-content>
                  {{ summaryCards[2].hoverValue | Date | Empty }}
                </template>
              </tooltip>
            </span>
            <avatar :name="summaryCards[2].subLabel" />
          </template>
        </metric-card>
        <metric-card
          v-if="engagementList && engagementList.description"
          class="mr-3 grow"
          title=""
          :max-width="800"
        >
          <template #subtitle-extended>
            {{ summaryCards[3].title }}
          </template>
        </metric-card>
      </div>

      <div class="audience-summary">
        <!-- Audience Destination Cards Wrapper -->
        <delivery-overview
          :sections="engagementList && engagementList.audiences"
          section-type="audience"
          deliveries-key="destinations"
          :loading-relationships="loadingAudiences"
          @onOverviewSectionAction="triggerOverviewAction($event)"
          @onOverviewDestinationAction="
            triggerOverviewDestinationAction($event)
          "
        >
          <template #title-left>
            <div class="d-flex align-center">
              <icon
                type="audiences"
                :size="24"
                color="neroBlack"
                class="mr-2"
              /><span class="text-h5">Audiences</span>
            </div>
          </template>
          <template #title-right>
            <div class="d-flex align-center">
              <v-btn
                text
                class="d-flex align-center primary--text text-decoration-none"
                @click="triggerSelectAudience()"
              >
                <icon type="audiences" :size="16" class="mr-1" />
                Add an audience
              </v-btn>
              <v-btn text color="primary" @click="openDeliveryHistoryDrawer()">
                <icon type="history" :size="16" class="mr-1" />
                Delivery history
              </v-btn>
            </div>
          </template>
          <template #empty-deliveries="{ sectionId }">
            <div class="pt-1 empty-audience pb-1">
              There are no destinations assigned to this audience.
              <br />
              Add one now.
              <br />
              <v-icon
                size="30"
                class="add-icon cursor-pointer pt-2"
                color="primary"
                @click="triggerSelectDestination(sectionId)"
              >
                mdi-plus-circle
              </v-icon>
            </div>
          </template>
        </delivery-overview>
        <v-tabs v-model="tabOption" class="mt-8">
          <v-tabs-slider color="primary"></v-tabs-slider>

          <v-tab
            key="displayAds"
            class="pa-2"
            color
            @click="fetchCampaignPerformanceDetails('ads')"
          >
            <span style="width: 15px">
              <icon type="display_ads" :size="10" class="mr-2" />
            </span>
            Display ads
          </v-tab>
          <v-tab key="email" @click="fetchCampaignPerformanceDetails('email')">
            @ Email
          </v-tab>
        </v-tabs>
        <v-tabs-items v-model="tabOption" class="mt-2">
          <v-tab-item key="displayAds">
            <v-progress-linear
              :active="loadingTab"
              :indeterminate="loadingTab"
            />
            <campaign-summary
              :summary="displayAdsSummary"
              :campaign-data="audiencePerformanceAdsData"
              :engagement-id="engagementId"
              type="ads"
              @onUpdateCampaignMappings="fetchCampaignPerformanceDetails('ads')"
            />
          </v-tab-item>
          <v-tab-item key="email">
            <v-progress-linear
              :active="loadingTab"
              :indeterminate="loadingTab"
            />
            <campaign-summary
              :summary="emailSummary"
              :campaign-data="audiencePerformanceEmailData"
              type="email"
            />
          </v-tab-item>
        </v-tabs-items>
      </div>
    </div>
    <select-audiences-drawer
      ref="selectAudiences"
      v-model="selectedAudiences"
      :toggle="showSelectAudiencesDrawer"
      enable-multiple
      @onToggle="(val) => (showSelectAudiencesDrawer = val)"
      @onAdd="triggerCreateAudience()"
      @triggerAddAudiences="triggerAttachAudiences($event)"
    />
    <add-audience-drawer
      v-model="selectedAudiences"
      :toggle="showAddAudiencesDrawer"
      @onToggle="(val) => (showAddAudiencesDrawer = val)"
      @onCancelAndBack="triggerSelectAudience()"
      @onCreateAddAudience="triggerAttachAudience($event)"
    />
    <select-destinations-drawer
      v-model="selectedAudiences"
      :selected-audience-id="selectedAudienceId"
      :toggle="showSelectDestinationsDrawer"
      @onToggle="(val) => (showSelectDestinationsDrawer = val)"
      @onSalesforce="triggerDataExtensionDrawer"
      @addedDestination="triggerAttachDestination($event)"
    />

    <destination-data-extension-drawer
      v-model="selectedAudiences"
      :selected-destination="selectedDestination"
      :selected-audience-id="selectedAudienceId"
      :toggle="showDataExtensionDrawer"
      @onToggle="(val) => (showDataExtensionDrawer = val)"
      @updateDestination="triggerAttachDestination($event)"
      @onBack="closeDrawers"
    />
    <delivery-history-drawer
      ref="deliveryHistory"
      :engagement-id="engagementId"
      :toggle="showDeliveryHistoryDrawer"
      @onToggle="(toggle) => (showDeliveryHistoryDrawer = toggle)"
    />
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
      :audience-id="selectedAudienceId"
      :destination="scheduleDestination"
      :engagement-id="engagementId"
    />

    <look-alike-audience
      :toggle="showLookAlikeDrawer"
      :selected-audience="selectedAudience"
      @onBack="reloadAudienceData()"
      @onCreate="onCreated()"
    />
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import { handleError } from "@/utils"
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import Status from "@/components/common/Status"
import MetricCard from "@/components/common/MetricCard"
import Avatar from "@/components/common/Avatar"
import Icon from "@/components/common/Icon"
import Tooltip from "../../components/common/Tooltip.vue"
import CampaignSummary from "../../components/CampaignSummary.vue"
import SelectAudiencesDrawer from "./Configuration/Drawers/SelectAudiencesDrawer.vue"
import AddAudienceDrawer from "./Configuration/Drawers/AddAudienceDrawer.vue"
import SelectDestinationsDrawer from "./Configuration/Drawers/SelectDestinationsDrawer.vue"
import DestinationDataExtensionDrawer from "./Configuration/Drawers/DestinationDataExtensionDrawer.vue"
import DeliveryHistoryDrawer from "./Configuration/Drawers/DeliveryHistoryDrawer.vue"
import DeliveryOverview from "../../components/DeliveryOverview.vue"
import HuxAlert from "../../components/common/HuxAlert.vue"
import ConfirmModal from "@/components/common/ConfirmModal.vue"
import EditDeliverySchedule from "@/views/Engagements/Configuration/Drawers/EditDeliveryScheduleDrawer.vue"
import LookAlikeAudience from "@/views/Audiences/Configuration/Drawers/LookAlikeAudience.vue"

export default {
  name: "EngagementDashboard",
  components: {
    PageHeader,
    Breadcrumb,
    Status,
    MetricCard,
    Avatar,
    Icon,
    Tooltip,
    CampaignSummary,
    AddAudienceDrawer,
    SelectAudiencesDrawer,
    SelectDestinationsDrawer,
    DestinationDataExtensionDrawer,
    DeliveryHistoryDrawer,
    DeliveryOverview,
    HuxAlert,
    ConfirmModal,
    EditDeliverySchedule,
    LookAlikeAudience,
  },
  data() {
    return {
      selectedAudience: null,
      showLookAlikeDrawer: false,
      engagementId: null,
      destinationArr: [],
      audienceMergedData: [],
      loading: false,
      loadingTab: false,
      loadingAudiences: false,
      flashAlert: false,
      alert: {
        type: "success",
        title: "YAY!",
        message: "Successfully triggered delivery.",
      },
      tabOption: 0,
      Tooltips: [
        { acronym: "CPM", description: "Cost per Thousand Impressions" },
        { acronym: "CTR", description: "Click Through Rate" },
        { acronym: "CPA", description: "Cost per Action" },
        { acronym: "CPC", description: "Cost per Click" },
      ],
      // Drawer Data Props
      selectedAudiences: {},
      showSelectAudiencesDrawer: false,
      showAddAudiencesDrawer: false,
      showSelectDestinationsDrawer: false,
      showDataExtensionDrawer: false,
      selectedAudienceId: null,
      selectedDestination: [],
      showDeliveryHistoryDrawer: false,
      // Edit Schedule data props
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
      audiencePerformanceAds: "engagements/audiencePerformanceByAds",
      audiencePerformanceEmail: "engagements/audiencePerformanceByEmail",
      getEngagement: "engagements/engagement",
      getAudience: "audiences/audience",
      getDestinations: "destinations/single",
    }),

    engagementList() {
      return this.getEngagement(this.engagementId)
    },

    breadcrumbItems() {
      const items = [
        {
          text: "Engagements",
          disabled: false,
          href: this.$router.resolve({ name: "Engagements" }).href,
          icon: "engagements",
        },
      ]
      if (this.engagementList) {
        items.push({
          text: this.engagementList.name,
          disabled: false,
        })
      }
      return items
    },
    audiencePerformanceAdsData() {
      return this.audiencePerformanceAds
        ? this.audiencePerformanceAds.audience_performance
        : []
    },
    audiencePerformanceEmailData() {
      return this.audiencePerformanceEmail
        ? this.audiencePerformanceEmail.audience_performance
        : []
    },
    summaryCards() {
      const summary = [
        {
          id: 1,
          title: "Delivery schedule",
          value: this.fetchKey(this.engagementList, "delivery_schedule"),
          subLabel: null,
        },
        {
          id: 2,
          title: "Last updated",
          // TODO: need to remove mapping to created by
          value:
            this.formattedDate(
              this.fetchKey(this.engagementList, "update_time")
            ) !== "-"
              ? this.formattedDate(
                  this.fetchKey(this.engagementList, "update_time")
                )
              : this.formattedDate(
                  this.fetchKey(this.engagementList, "create_time")
                ),
          hoverValue:
            this.fetchKey(this.engagementList, "update_time") !== "-"
              ? this.fetchKey(this.engagementList, "update_time")
              : this.fetchKey(this.engagementList, "create_time"),
          subLabel:
            this.fetchKey(this.engagementList, "updated_by") !== "-"
              ? this.fetchKey(this.engagementList, "updated_by")
              : this.fetchKey(this.engagementList, "created_by"),
          width: "19%",
          minWidth: "164px",
        },
        {
          id: 3,
          title: "Created",
          value: this.formattedDate(
            this.fetchKey(this.engagementList, "create_time")
          ),
          hoverValue: this.fetchKey(this.engagementList, "create_time"),
          subLabel: this.fetchKey(this.engagementList, "created_by"),
          width: "19%",
          minWidth: "164px",
        },
        {
          id: 4,
          title: this.fetchKey(this.engagementList, "description"),
          value: null,
          subLabel: null,
        },
      ]
      return summary.filter((item) => item.title !== null)
    },
    displayAdsSummary() {
      if (
        !this.audiencePerformanceAds ||
        (this.audiencePerformanceAds &&
          this.audiencePerformanceAds.length === 0)
      )
        return []
      return [
        {
          id: 1,
          title: "Spend",
          field: "spend",
          value: this.audiencePerformanceAds
            ? this.audiencePerformanceAds &&
              this.fetchKey(this.audiencePerformanceAds["summary"], "spend")
            : "-",
        },
        {
          id: 2,
          field: "reach",
          title: "Reach",
          value: this.audiencePerformanceAds
            ? this.audiencePerformanceAds &&
              this.fetchKey(this.audiencePerformanceAds["summary"], "reach")
            : "-",
        },
        {
          id: 3,
          title: "Impressions",
          field: "impressions",
          value: this.audiencePerformanceAds
            ? this.audiencePerformanceAds &&
              this.fetchKey(
                this.audiencePerformanceAds["summary"],
                "impressions"
              )
            : "-",
        },
        {
          id: 4,
          title: "Conversions",
          field: "conversions",
          value: this.audiencePerformanceAds
            ? this.audiencePerformanceAds &&
              this.fetchKey(
                this.audiencePerformanceAds["summary"],
                "conversions"
              )
            : "-",
        },
        {
          id: 5,
          title: "Clicks",
          field: "clicks",
          value: this.audiencePerformanceAds
            ? this.audiencePerformanceAds &&
              this.fetchKey(this.audiencePerformanceAds["summary"], "clicks")
            : "-",
        },
        {
          id: 6,
          title: "Frequency",
          field: "frequency",
          value: this.audiencePerformanceAds
            ? this.audiencePerformanceAds &&
              this.fetchKey(this.audiencePerformanceAds["summary"], "frequency")
            : "-",
        },
        {
          id: 7,
          title: "CPM",
          field: "cost_per_thousand_impressions",
          value: this.audiencePerformanceAds
            ? this.audiencePerformanceAds &&
              this.fetchKey(
                this.audiencePerformanceAds["summary"],
                "cost_per_thousand_impressions"
              )
            : "-",
        },
        {
          id: 8,
          title: "CTR",
          field: "click_through_rate",
          value: this.audiencePerformanceAds
            ? this.audiencePerformanceAds &&
              this.fetchKey(
                this.audiencePerformanceAds["summary"],
                "click_through_rate"
              )
            : "-",
        },
        {
          id: 9,
          title: "CPA",
          field: "cost_per_action",
          value: this.audiencePerformanceAds
            ? this.audiencePerformanceAds &&
              this.fetchKey(
                this.audiencePerformanceAds["summary"],
                "cost_per_action"
              )
            : "-",
        },
        {
          id: 10,
          title: "CPC",
          field: "cost_per_click",
          value:
            this.audiencePerformanceAds &&
            this.fetchKey(
              this.audiencePerformanceAds["summary"],
              "cost_per_click"
            ),
        },
        {
          id: 11,
          title: "Engagement rate",
          field: "engagement_rate",
          value:
            this.audiencePerformanceAds &&
            this.fetchKey(
              this.audiencePerformanceAds["summary"],
              "engagement_rate"
            ),
        },
      ]
    },
    emailSummary() {
      if (
        !this.audiencePerformanceEmail ||
        (this.audiencePerformanceEmail &&
          this.audiencePerformanceEmail.length === 0)
      )
        return []
      return [
        {
          id: 1,
          title: "Sent",
          field: "sent",
          value:
            this.audiencePerformanceEmail &&
            this.audiencePerformanceEmail["summary"]
              ? this.audiencePerformanceEmail &&
                this.fetchKey(this.audiencePerformanceEmail["summary"], "sent")
              : "-",
        },
        {
          id: 2,
          title: "Hard bounces / Rate",
          field: "hard_bounces|hard_bounces_rate",
          value: `${`${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "hard_bounces"
                )
              : "-"
          }|${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "hard_bounces_rate"
                )
              : "-"
          }`}`,
        },
        {
          id: 3,
          title: "Delivered / Rate",
          field: "delivered|delivered_rate",
          value: `${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "delivered"
                )
              : "-"
          }|${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "delivered_rate"
                )
              : "-"
          }`,
        },
        {
          id: 4,
          title: "Open / Rate",
          field: "open|open_rate",
          value: `${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(this.audiencePerformanceEmail["summary"], "open")
              : "-"
          }|${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "open_rate"
                )
              : "-"
          }`,
        },
        {
          id: 5,
          title: "Click / CTR",
          field: "clicks|click_through_rate",
          value: `${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "clicks"
                )
              : "-"
          }|${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "click_through_rate"
                )
              : "-"
          }`,
        },
        {
          id: 6,
          title: "Click to open rate  ",
          field: "click_to_open_rate",
          value: this.audiencePerformanceEmail
            ? this.audiencePerformanceEmail &&
              this.fetchKey(
                this.audiencePerformanceEmail["summary"],
                "click_to_open_rate"
              )
            : "-",
        },
        {
          id: 7,
          title: "Unique clicks / Unique opens",
          field: "unique_clicks|unique_opens",
          value: `${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "unique_clicks"
                )
              : "-"
          }|${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "unique_opens"
                )
              : "-"
          }`,
        },
        {
          id: 8,
          title: "Unsubscribe / Rate",
          field: "unsubscribe|unsubscribe_rate",
          value: `${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "unsubscribe"
                )
              : "-"
          }|${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "unsubscribe_rate"
                )
              : "-"
          }`,
        },
      ]
    },
    deliverySchedule() {
      if (this.engagementList && this.engagementList.delivery_schedule) {
        if (
          !this.engagementList.delivery_schedule.start_date &&
          !this.engagementList.delivery_schedule.end_date
        ) {
          return "Now"
        } else {
          if (
            this.engagementList.delivery_schedule.start_date &&
            this.engagementList.delivery_schedule.end_date
          ) {
            return (
              this.$options.filters.Date(
                this.engagementList.delivery_schedule.start_date,
                "MMMM D"
              ) +
              " - " +
              this.$options.filters.Date(
                this.engagementList.delivery_schedule.end_date,
                "MMMM D"
              )
            )
          } else if (this.engagementList.delivery_schedule.start_date) {
            return this.$options.filters.Date(
              this.engagementList.delivery_schedule.start_date,
              "MMMM D"
            )
          } else if (this.engagementList.delivery_schedule.end_date) {
            return this.$options.filters.Date(
              this.engagementList.delivery_schedule.end_date,
              "MMMM D"
            )
          }
        }
      }
      return "Manual"
    },
  },
  async mounted() {
    this.loading = true
    this.engagementId = this.$route.params.id
    await this.loadEngagement(this.$route.params.id)
    this.getAudiences()
    this.getAvailableDestinations()
    this.loading = false
  },
  methods: {
    ...mapActions({
      attachAudience: "engagements/attachAudience",
      attachAudienceDestination: "engagements/attachAudienceDestination",
      deliverAudience: "engagements/deliverAudience",
      deliverAudienceDestination: "engagements/deliverAudienceDestination",
      detachAudience: "engagements/detachAudience",
      detachAudienceDestination: "engagements/detachAudienceDestination",
      getAudiences: "audiences/getAll",
      getAudiencePerformanceById: "engagements/getAudiencePerformance",
      getAvailableDestinations: "destinations/getAll",
      getEngagementById: "engagements/get",
    }),

    // Drawer Section Starts
    closeDrawers() {
      this.showSelectAudiencesDrawer = false
      this.showAddAudiencesDrawer = false
      this.showSelectDestinationsDrawer = false
      this.showDataExtensionDrawer = false
    },

    triggerSelectAudience() {
      this.closeDrawers()
      this.showSelectAudiencesDrawer = true
      this.$refs.selectAudiences.localSelectedAudiences = JSON.parse(
        JSON.stringify(this.selectedAudiences)
      )
    },

    triggerCreateAudience() {
      this.closeDrawers()
      this.showAddAudiencesDrawer = true
    },
    triggerSelectDestination(audienceId) {
      this.closeDrawers()
      this.selectedAudienceId = audienceId
      this.showSelectDestinationsDrawer = true
    },
    triggerDataExtensionDrawer(destination) {
      this.closeDrawers()
      this.selectedDestination = destination || []
      this.showDataExtensionDrawer = true
    },
    async triggerAttachDestination(event) {
      this.loadingAudiences = true
      const payload = event.destination
      await this.attachAudienceDestination({
        engagementId: this.engagementId,
        audienceId: this.selectedAudienceId,
        data: payload,
      })
      await this.loadEngagement(this.engagementId)
    },
    async triggerAttachAudiences(audiences) {
      this.loadingAudiences = true
      if (Object.keys(audiences.added).length > 0) {
        const addPayload = {
          audiences: Object.values(audiences.added).map((aud) => ({
            id: aud.id,
            destinations: [],
          })),
        }
        await this.attachAudience({
          engagementId: this.engagementId,
          data: addPayload,
        })
      }
      if (Object.keys(audiences.removed).length > 0) {
        if (process.env.NODE_ENV === "development") {
          for (const aud of Object.values(audiences.removed)) {
            const removePayload = { audience_ids: [] }
            removePayload.audience_ids.push(aud.id)
            await this.detachAudience({
              engagementId: this.engagementId,
              data: removePayload,
            })
          }
        } else {
          const removePayload = {
            audience_ids: Object.values(audiences.removed).map((aud) => aud.id),
          }

          await this.detachAudience({
            engagementId: this.engagementId,
            data: removePayload,
          })
        }
      }
      await this.loadEngagement(this.engagementId)
    },
    async triggerAttachAudience(aud) {
      this.loadingAudiences = true
      const payload = { audiences: [] }
      payload.audiences.push({
        id: aud.id,
        destinations:
          aud.destinations.map((dest) => ({
            id: dest.id,
          })) || [],
      })
      await this.attachAudience({
        engagementId: this.engagementId,
        data: payload,
      })
      await this.loadEngagement(this.engagementId)
    },
    async triggerDetachAudiences(aud) {
      this.loadingAudiences = true
      const payload = { audience_ids: [] }
      payload.audience_ids.push(aud.id)
      await this.detachAudience({
        engagementId: this.engagementId,
        data: payload,
      })
      await this.loadEngagement(this.engagementId)
    },
    // Drawer Section Ends

    formattedDate(value) {
      if (value) {
        return this.$options.filters.Date(value, "relative") + " by"
      }
      return "-"
    },
    fetchKey(obj, key) {
      return obj && obj[key] ? obj[key] : "-"
    },
    showCard(card) {
      if (card.cardType !== "description") return true
      else {
        return !!card.title
      }
    },
    async fetchCampaignPerformanceDetails(type) {
      this.loadingTab = true
      await this.getAudiencePerformanceById({
        type: type,
        id: this.engagementList.id,
      })
      this.loadingTab = false
    },
    getTooltip(summaryCard) {
      const acronymObject = this.Tooltips.filter(
        (item) => item.acronym === summaryCard.title
      )
      if (acronymObject.length === 0) return null
      return acronymObject[0].description
    },
    mapDeliveries() {
      this.engagementList.audiences.forEach((audience) => {
        this.selectedAudiences[audience.id] = audience
        audience.destinations.map((destination) => {
          if (destination.latest_delivery) {
            destination["status"] = destination.latest_delivery.status
            destination["size"] = destination.latest_delivery.size
            destination["update_time"] = destination.latest_delivery.update_time
          }
          return destination
        })
      })
      this.loadingAudiences = false
    },
    async loadEngagement(engagementId) {
      await this.getEngagementById(engagementId)
      await this.getAudiencePerformanceById({
        type: "ads",
        id: this.engagementList.id,
      })
      this.mapDeliveries()
    },
    //#region Delivery Overview Region
    async triggerOverviewAction(event) {
      try {
        const engagementId = this.engagementId
        switch (event.target.title.toLowerCase()) {
          case "add a destination":
            this.closeDrawers()
            this.triggerSelectDestination(event.data.id)
            break

          case "deliver now":
            try {
              await this.deliverAudience({
                id: engagementId,
                audienceId: event.data.id,
              })
              this.dataPendingMesssage(event.data.name, "engagement")
            } catch (error) {
              this.dataErrorMesssage(event.data.name, "engagement")
              handleError(error)
              throw error
            }
            break

          case "remove audience":
            this.triggerDetachAudiences(event.data)
            break
          default:
            break
        }
      } catch (error) {
        handleError(error)
        throw error
      }
    },

    async triggerOverviewDestinationAction(event) {
      try {
        const engagementId = this.engagementId
        this.selectedAudienceId = event.parent.id
        switch (event.target.title.toLowerCase()) {
          case "deliver now":
            await this.deliverAudienceDestination({
              id: engagementId,
              audienceId: this.selectedAudienceId,
              destinationId: event.data.id,
            })
            this.dataPendingMesssage(event.data.name, "audience")
            break
          case "edit delivery schedule":
            this.showConfirmModal = true
            this.scheduleDestination = event.data
            break
          case "remove destination":
            await this.detachAudienceDestination({
              engagementId: this.engagementId,
              audienceId: this.selectedAudienceId,
              data: { id: event.data.id },
            })
            await this.loadEngagement(this.engagementId)
            break
          case "create lookalike":
            this.openLookAlikeDrawer(event)
            break
          default:
            break
        }
      } catch (error) {
        this.dataErrorMesssage(event.data.name, "audience")
        handleError(error)
        throw error
      }
    },

    //Alert Message
    dataPendingMesssage(name) {
      this.alert.type = "Pending"
      this.alert.title = ""
      this.alert.message = `Your audience, '${name}' , has started delivering.`
      this.flashAlert = true
    },
    dataErrorMesssage(name) {
      this.alert.type = "error"
      this.alert.title = "OH NO!"
      this.alert.message = `Failed to schedule a delivery for '${name}'`
      this.flashAlert = true
    },

    //#endregion
    openDeliveryHistoryDrawer() {
      this.$refs.deliveryHistory.fetchHistory()
      this.showDeliveryHistoryDrawer = true
    },
    openLookAlikeDrawer(event) {
      this.selectedAudience = event.parent
      this.lookalikeCreated = false
      this.showLookAlikeDrawer = true
    },
    async reloadAudienceData() {
      this.showLookAlikeDrawer = false
    },
    onCreated() {
      this.lookalikeCreated = true
      this.alert.message = "Lookalike created successfully"
      this.flashAlert = true
    },
  },
}
</script>

<style lang="scss" scoped>
.engagement-dash {
  .page-header--wrap {
    box-shadow: 0px 1px 0px var(--v-lightGrey-base) !important;
  }
  .empty-audience {
    width: 190px;
    text-align: center;
    margin: 0 auto;
  }
  .empty-state {
    background: var(--v-aliceBlue-base);
    width: 190px;
    margin: 0 auto;
    font-size: 14px;
    line-height: 22px;
    color: var(--v-gray-base);
    border: 1px solid var(--v-lightGrey-base);
    box-sizing: border-box;
    border-radius: 5px;
  }
  .inner-wrap {
    .summary-wrap {
      flex-wrap: wrap;
      .metric-card-wrapper {
        padding: 10px 15px;
      }
    }
    .summary-tab-wrap {
      .metric-card-wrapper {
        border: 1px solid var(--v-zircon-base);
        box-sizing: border-box;
        border-radius: 12px;
        ::v-deep .v-list-item {
          .v-list-item__content {
            padding-top: 15px;
            padding-bottom: 15px;
            margin-left: -5px !important;
            .v-list-item__title {
              font-size: 12px;
              line-height: 16px;
              margin: 0 !important;
            }
            .v-list-item__subtitle {
              margin-bottom: 15px !important;
            }
          }
        }
        &.description {
          ::v-deep .v-list-item__content {
            padding-top: 0px;

            .v-list-item__title {
              font-size: 14px;
              line-height: 22px;

              text-overflow: inherit;
              white-space: inherit;
              color: var(--v-neroBlack-base) !important;
            }
          }
        }
      }
    }

    .v-tabs {
      ::v-deep .v-tabs-bar {
        background: transparent;
        .v-tabs-bar__content {
          border-bottom: 2px solid var(--v-zircon-base);
          .v-tabs-slider-wrapper {
            width: 128px;
            .v-tabs-slider {
              background-color: var(--v-info-base) !important;
              border-color: var(--v-info-base) !important;
            }
          }
          .v-tab {
            text-transform: inherit;
            padding: 8px;
            color: var(--v-primary-base);
            font-size: 15px;
            line-height: 20px;
            svg {
              fill: transparent !important;
              path {
                stroke: var(--v-primary-base);
              }
            }
            &.v-tab--active {
              color: var(--v-info-base);
              svg {
                path {
                  stroke: var(--v-info-base);
                }
              }
            }
          }
        }
      }
    }
    .v-tabs-items {
      overflow: inherit;
      background-color: transparent !important;
      .v-window-item--active {
        background: transparent;
      }
    }
  }
}
.theme--light.v-btn.v-btn--disabled.v-btn--has-bg {
  background-color: white !important;
}
</style>
