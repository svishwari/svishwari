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
        <div class="d-flex align-center">
          <tooltip>
            <template #label-content>
              <icon
                type="pencil"
                :size="18"
                class="cursor-pointer mr-7"
                color="black-darken4"
                @click.native="editEngagement()"
              />
            </template>
            <template #hover-content>
              <span>
                <span> Click to edit this engagement </span>
              </span>
            </template>
          </tooltip>

        </div>
      </template>
    </page-header>
    <v-progress-linear :active="loading" :indeterminate="loading" />
    <!-- Page Content Starts here -->
    <div v-if="!loading" class="inner-wrap px-15 py-8">
      <div>
        <!-- Summary Cards Wrapper -->
        <engagement-overview-summary
          data-e2e="overview-summary"
          :data="engagementList"
        />
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
                color="black-darken4"
                class="mr-2"
              /><span class="text-h5">Audiences</span>
            </div>
          </template>
          <template #title-right>
            <div class="d-flex align-center">
              <v-btn
                text
                class="d-flex align-center primary--text text-decoration-none mr-9"
                @click="triggerSelectAudience()"
              >
                <icon
                  type="audiences"
                  color="primary"
                  :size="16"
                  class="mr-1"
                />
                Add an audience
              </v-btn>
              <v-btn
                text
                color="primary"
                data-e2e="deliver-history"
                @click="openDeliveryHistoryDrawer()"
              >
                <icon type="history" color="primary" :size="16" class="mr-1" />
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
        <engagement-performance-metrics
          :engagement-id="engagementId"
          :ad-data="audiencePerformanceAds"
          :email-data="audiencePerformanceEmail"
          :loading-metrics="loadingTab"
          @fetchMetrics="fetchCampaignPerformanceDetails($event)"
        />
      </div>
    </div>
    <!-- Select Audience Drawer -->
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
      ref="addNewAudience"
      v-model="selectedAudiences"
      :toggle="showAddAudiencesDrawer"
      @onToggle="(val) => (showAddAudiencesDrawer = val)"
      @onCancelAndBack="triggerSelectAudience()"
      @onCreateAddAudience="triggerAttachAudience($event)"
    />
    <select-destinations-drawer
      ref="selectDestinations"
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
      :engagement-id="engagementId"
      :toggle="showDeliveryHistoryDrawer"
      @onToggle="(toggle) => (showDeliveryHistoryDrawer = toggle)"
    />

    <confirm-modal
      v-model="showConfirmModal"
      :title="confirmDialog.title"
      :right-btn-text="confirmDialog.btnText"
      :body="confirmDialog.body"
      :type="confirmDialog.type"
      :sub-title="confirmDialog.subtitle"
      :icon="confirmDialog.icon"
      @onCancel="showConfirmModal = false"
      @onConfirm="onConfirmAction()"
    />

    <edit-delivery-schedule
      v-model="editDeliveryDrawer"
      :schedule="currentSchedule"
      :audience-id="selectedAudienceId"
      :destination="scheduleDestination"
      :engagement-id="engagementId"
      @onUpdate="refreshEntity()"
    />

    <look-alike-audience
      ref="lookalikeWorkflow"
      :toggle="showLookAlikeDrawer"
      :selected-audience="selectedAudience"
      @onBack="reloadAudienceData()"
      @onCreate="onCreated()"
    />
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import Status from "@/components/common/Status"
import Icon from "@/components/common/Icon"
import SelectAudiencesDrawer from "./Configuration/Drawers/SelectAudiencesDrawer.vue"
import AddAudienceDrawer from "./Configuration/Drawers/AddAudienceDrawer.vue"
import SelectDestinationsDrawer from "./Configuration/Drawers/SelectDestinationsDrawer.vue"
import DestinationDataExtensionDrawer from "./Configuration/Drawers/DestinationDataExtensionDrawer.vue"
import DeliveryHistoryDrawer from "@/views/Shared/Drawers/DeliveryHistoryDrawer.vue"
import DeliveryOverview from "../../components/DeliveryOverview.vue"
import ConfirmModal from "@/components/common/ConfirmModal.vue"
import EditDeliverySchedule from "@/views/Engagements/Configuration/Drawers/EditDeliveryScheduleDrawer.vue"
import LookAlikeAudience from "@/views/Audiences/Configuration/Drawers/LookAlikeAudience.vue"
import EngagementOverviewSummary from "./Overview.vue"
import EngagementPerformanceMetrics from "./PerformanceMetrics.vue"
import Tooltip from "@/components/common/Tooltip.vue"

export default {
  name: "EngagementDashboard",
  components: {
    PageHeader,
    EngagementOverviewSummary,
    EngagementPerformanceMetrics,
    Breadcrumb,
    Status,
    Icon,
    AddAudienceDrawer,
    SelectAudiencesDrawer,
    SelectDestinationsDrawer,
    DestinationDataExtensionDrawer,
    DeliveryHistoryDrawer,
    DeliveryOverview,
    ConfirmModal,
    EditDeliverySchedule,
    LookAlikeAudience,
    Tooltip,
  },
  data() {
    return {
      engagementList: {},
      currentSchedule: {},
      selectedAudience: null,
      showLookAlikeDrawer: false,
      engagementId: "",
      destinationArr: [],
      audienceMergedData: [],
      loading: false,
      loadingTab: false,
      loadingAudiences: false,
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
      deleteActionData: {},
      confirmDialog: {
        title: "Remove  audience?",
        icon: "sad-face",
        btnText: "Yes, remove it",
        body: "You will not be deleting this audience; this audience will not be attached to this specific engagement anymore.",
        actionType: "remove-audience",
      },
    }
  },
  computed: {
    ...mapGetters({
      audiencePerformanceAds: "engagements/audiencePerformanceByAds",
      audiencePerformanceEmail: "engagements/audiencePerformanceByEmail",
      getEngagementObject: "engagements/engagement",
    }),

    breadcrumbItems() {
      const items = [
        {
          text: "Engagements",
          disabled: false,
          href: this.$router.resolve({ name: "Engagements" }).href,
          icon: "speaker_down",
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

    getRouteId() {
      return this.$route.params.id
    },
  },
  async mounted() {
    this.loading = true
    this.engagementId = this.getRouteId
    try {
      await this.loadEngagement(this.getRouteId)
    } finally {
      this.currentSchedule = this.engagementList.delivery_schedule?.schedule
      this.loading = false
    }
  },
  methods: {
    ...mapActions({
      attachAudience: "engagements/attachAudience",
      attachAudienceDestination: "engagements/attachAudienceDestination",
      deliverAudience: "engagements/deliverAudience",
      deliverAudienceDestination: "engagements/deliverAudienceDestination",
      detachAudience: "engagements/detachAudience",
      detachAudienceDestination: "engagements/detachAudienceDestination",
      getAudiencePerformanceById: "engagements/getAudiencePerformance",
      getEngagementById: "engagements/get",
      setAlert: "alerts/setAlert",
    }),
    async refreshEntity() {
      this.loading = true
      this.$root.$emit("refresh-notifications")
      try {
        await this.loadEngagement(this.engagementId)
      } finally {
        this.loading = false
      }
      this.$forceUpdate()
      this.$nextTick(() => {
        this.$forceUpdate()
      })
    },
    async onConfirmAction() {
      this.showConfirmModal = false
      switch (this.confirmDialog.actionType) {
        case "edit-schedule":
          this.editDeliveryDrawer = true
          break
        case "remove-audience":
          this.triggerDetachAudiences(this.deleteActionData)
          break
        case "remove-destination":
          await this.detachAudienceDestination(this.deleteActionData)
          await this.loadEngagement(this.engagementId)
          break
        default:
          break
      }
    },
    // Drawer Section Starts
    closeDrawers() {
      this.showSelectAudiencesDrawer = false
      this.showAddAudiencesDrawer = false
      this.showSelectDestinationsDrawer = false
      this.showDataExtensionDrawer = false
    },

    triggerSelectAudience() {
      this.closeDrawers()
      this.$refs.selectAudiences.fetchAudiences()
      this.showSelectAudiencesDrawer = true
      this.$refs.selectAudiences.localSelectedAudiences = JSON.parse(
        JSON.stringify(this.selectedAudiences)
      )
    },

    triggerCreateAudience() {
      this.closeDrawers()
      this.$refs.addNewAudience.fetchDependencies()
      this.showAddAudiencesDrawer = true
    },
    triggerSelectDestination(audienceId) {
      this.closeDrawers()
      this.selectedAudienceId = audienceId
      this.$refs.selectDestinations.fetchDependencies()
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
      try {
        await this.attachAudienceDestination({
          engagementId: this.engagementId,
          audienceId: this.selectedAudienceId,
          data: payload,
        })
        await this.loadEngagement(this.engagementId)
      } catch (error) {
        this.loadingAudiences = false
      }
    },
    async triggerAttachAudiences(audiences) {
      this.loadingAudiences = true
      try {
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
              audience_ids: Object.values(audiences.removed).map(
                (aud) => aud.id
              ),
            }

            await this.detachAudience({
              engagementId: this.engagementId,
              data: removePayload,
            })
          }
        }
        await this.loadEngagement(this.engagementId)
      } catch (error) {
        this.loadingAudiences = false
      }
    },
    async triggerAttachAudience(aud) {
      this.loadingAudiences = true
      try {
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
      } catch (error) {
        this.loadingAudiences = false
      }
    },
    async triggerDetachAudiences(aud) {
      this.loadingAudiences = true
      try {
        const payload = { audience_ids: [] }
        payload.audience_ids.push(aud.id)
        await this.detachAudience({
          engagementId: this.engagementId,
          data: payload,
        })
        await this.loadEngagement(this.engagementId)
      } catch (error) {
        this.loadingAudiences = false
      }
    },
    // Drawer Section Ends
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
      try {
        await this.getAudiencePerformanceById({
          type: type,
          id: this.engagementList.id,
        })
      } finally {
        this.loadingTab = false
      }
    },
    getTooltip(summaryCard) {
      const acronymObject = this.Tooltips.filter(
        (item) => item.acronym === summaryCard.title
      )
      if (acronymObject.length === 0) return null
      return acronymObject[0].description
    },
    mapDeliveries() {
      this.selectedAudiences = {}
      this.engagementList.audiences.forEach((audience) => {
        this.selectedAudiences[audience.id] = audience
        audience.destinations.map((destination) => {
          if (destination.latest_delivery) {
            destination["status"] = destination.latest_delivery.status
            destination["size"] = destination.latest_delivery.size
            destination["update_time"] = destination.latest_delivery.update_time
            destination["match_rate"] = destination.latest_delivery.match_rate
          }
          return destination
        })
      })
      this.loadingAudiences = false
    },
    async loadEngagement(engagementId) {
      await this.getEngagementById(engagementId)
      this.engagementList = JSON.parse(
        JSON.stringify(this.getEngagementObject(this.engagementId))
      )
      await this.getAudiencePerformanceById({
        type: "ads",
        id: this.engagementList.id,
      })
      this.mapDeliveries()
    },
    //#region Delivery Overview Region
    async triggerOverviewAction(event) {
      const engagementId = this.engagementId
      switch (event.target.title.toLowerCase()) {
        case "add a destination":
          this.closeDrawers()
          this.triggerSelectDestination(event.data.id)
          break

        case "deliver now":
          await this.deliverAudience({
            id: engagementId,
            audienceId: event.data.id,
          })
          this.dataPendingMesssage(event, "audience")
          this.refreshEntity()
          break

        case "remove audience":
          this.showConfirmModal = true
          this.confirmDialog.actionType = "remove-audience"
          this.confirmDialog.title = "You are about to remove"
          this.confirmDialog.icon = "modal-remove"
          this.confirmDialog.type = "primary"
          this.confirmDialog.subtitle = event.data.name
          this.confirmDialog.btnText = "Yes, remove audience"
          this.confirmDialog.body =
            "Are you sure you want to remove this audience? By removing this audience, it will not be deleted, but it will become unattached from this engagement."
          this.deleteActionData = event.data
          break
        default:
          break
      }
    },

    async triggerOverviewDestinationAction(event) {
      const engagementId = this.engagementId
      this.selectedAudienceId = event.parent.id
      switch (event.target.title.toLowerCase()) {
        case "deliver now":
          await this.deliverAudienceDestination({
            id: engagementId,
            audienceId: this.selectedAudienceId,
            destinationId: event.data.id,
          })
          this.dataPendingMesssage(event, "destination")
          break
        case "edit delivery schedule":
          this.confirmDialog.icon = "edit"
          this.confirmDialog.type = "primary"
          this.confirmDialog.subtitle = ""
          this.confirmDialog.actionType = "edit-schedule"
          this.confirmDialog.title = "You are about to edit delivery schedule."
          this.confirmDialog.btnText = "Yes, edit delivery schedule"
          this.confirmDialog.body =
            "This will override the default delivery schedule. However, this action is not permanent, the new delivery schedule can be reset to the default settings at any time."
          this.showConfirmModal = true
          this.scheduleDestination = event.data
          this.currentSchedule = event.data["delivery_schedule"]
          break
        case "remove destination":
          this.confirmDialog.actionType = "remove-destination"
          this.confirmDialog.title = `Remove ${event.data.name} destination?`
          this.confirmDialog.btnText = "Yes, remove it"
          this.confirmDialog.icon = "sad-face"
          this.confirmDialog.subtitle = ""
          this.confirmDialog.type = "error"
          this.confirmDialog.body =
            "You will not be deleting this destination; this destination will not be attached to this specific audience anymore."
          this.deleteActionData = {
            engagementId: this.engagementId,
            audienceId: this.selectedAudienceId,
            data: { id: event.data.id },
          }
          this.showConfirmModal = true
          break
        case "create lookalike":
          this.openLookAlikeDrawer(event)
          break
        default:
          break
      }
    },

    //Alert Message
    dataPendingMesssage(event, value) {
      if (value == "audience") {
        const engagementName = this.engagementList.name
        const audienceName = event.data.name
        this.setAlert({
          type: "pending",
          message: `Your audience '${audienceName}', has started delivering as part of the engagement '${engagementName}'.`,
        })
      } else if (value == "destination") {
        const audienceName = event.parent.name
        const destinationName = event.data.name
        this.setAlert({
          type: "pending",
          message: `Your audience '${audienceName}', has started delivering to '${destinationName}'.`,
        })
      }
    },

    //#endregion
    openDeliveryHistoryDrawer() {
      this.showDeliveryHistoryDrawer = true
    },
    openLookAlikeDrawer(event) {
      this.selectedAudience = event.parent
      this.$refs.lookalikeWorkflow.prefetchLookalikeDependencies()
      this.lookalikeCreated = false
      this.showLookAlikeDrawer = true
    },
    async reloadAudienceData() {
      this.refreshEntity()
      this.showLookAlikeDrawer = false
    },
    onCreated() {
      this.lookalikeCreated = true
      this.setAlert({
        type: "teal",
        message: "Lookalike created successfully",
      })
    },
    editEngagement() {
      this.$router.push({
        name: "EngagementUpdate",
        params: { id: this.getRouteId },
      })
    },
  },
}
</script>

<style lang="scss" scoped>
.engagement-dash {
  .empty-audience {
    width: 190px;
    text-align: center;
    margin: 0 auto;
  }
  .empty-state {
    background: var(--v-primary-lighten2);
    width: 190px;
    margin: 0 auto;
    font-size: 14px;
    line-height: 22px;
    color: var(--v-black-darken1);
    border: 1px solid var(--v-black-lighten3);
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
        border: 1px solid var(--v-black-lighten2);
        box-sizing: border-box;
        border-radius: 12px;
        ::v-deep .v-list-item {
          .v-list-item__content {
            padding-top: 15px;
            padding-bottom: 15px;
            margin-left: -5px !important;
            .v-list-item__title {
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
              color: var(--v-black-darken4) !important;
            }
          }
        }
      }
    }
  }
}
.theme--light.v-btn.v-btn--disabled.v-btn--has-bg {
  background-color: white !important;
}
::v-deep .v-snack__wrapper {
  max-width: 1300px !important;
}
</style>
