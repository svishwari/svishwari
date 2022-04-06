<template>
  <v-form>
    <h5 class="text-h3 mb-2">General information</h5>
    <v-row class="pt-2">
      <v-col>
        <text-field
          v-model="value.name"
          label-text="Engagement name"
          placeholder="Give this engagement a name"
          :rules="[(value) => !!value || 'Engagement name is required']"
          :error-messages="errorMessages"
          required
          data-e2e="engagement-name"
          @blur="errorMessages = []"
        />
      </v-col>
      <v-col>
        <text-field
          v-model="value.description"
          label-text="Description"
          placeholder="What is the purpose of this engagement?"
          data-e2e="engagement-description"
        />
      </v-col>
    </v-row>

    <h5 class="text-h3 mb-2">Audience(s) and destination(s)</h5>
    <data-cards
      bordered
      :items="Object.values(value.audiences)"
      card-class="pa-4 body-1"
      :fields="[
        {
          key: 'name',
          label: 'Audience name',
          col: '5',
        },
        {
          key: 'size',
          label: 'Size',
        },
        {
          key: 'destinations',
          label: 'Destination(s)',
        },
        {
          key: 'manage',
        },
      ]"
    >
      <template #field:name="row">
        <span v-if="row.item.is_lookalike" class="d-flex align-items-center"
          ><icon type="lookalike" :size="24" class="mr-1" /><span
            class="body-1"
            >{{ row.value }}</span
          ></span
        >
        <span v-else class="not-lookalike-color body-1">{{ row.value }}</span>
      </template>

      <template #field:size="row">
        <tooltip>
          <template #label-content>
            {{ row.value | Numeric(true, true) | Empty("n/a") }}
          </template>
          <template #hover-content>
            {{ row.value | Numeric | Empty("Size unavailable at this time") }}
          </template>
        </tooltip>
      </template>

      <template #field:destinations="row">
        <div class="destinations-wrap">
          <v-row class="align-center">
            <div>
              <tooltip v-for="destination in row.value" :key="destination.id">
                <template #label-content>
                  <div class="destination-logo-wrapper">
                    <div class="logo-wrapper">
                      <logo
                        class="added-logo svg-icon"
                        :type="destinationType(destination.id)"
                        :size="24"
                      />
                      <logo
                        class="delete-icon"
                        type="delete"
                        @click.native="removeDestination(row, destination.id)"
                      />
                    </div>
                  </div>
                </template>
                <template #hover-content>
                  <div class="d-flex align-center">Remove</div>
                </template>
              </tooltip>
            </div>
            <div v-if="!row.item.is_lookalike">
              <tooltip>
                <template #label-content>
                  <div
                    class="
                      resize-destination-button
                      d-flex
                      align-items-center
                      ml-2
                    "
                    data-e2e="add-destination"
                    @click="openSelectDestinationsDrawer(row.item.id)"
                  >
                    <icon
                      type="plus"
                      :size="12"
                      color="primary"
                      class="mr-1 mt-1"
                    />
                    <icon
                      type="destination"
                      :size="24"
                      color="primary"
                      class="mr-2"
                    />
                  </div>
                </template>
                <template #hover-content>Add destination(s)</template>
              </tooltip>
            </div>
          </v-row>
        </div>
      </template>

      <template #field:manage="row">
        <div class="d-flex align-center justify-end">
          <div @click="removeAudience(row.item)">
            <icon size="19" type="delete-button" />
          </div>
        </div>
      </template>

      <template slot="empty">
        <v-col class="grow pl-2">
          You have not added any audiences, yet.
        </v-col>
      </template>
    </data-cards>
    <v-alert
      color="primary"
      class="empty-card mb-8"
      data-e2e="add-audience"
      @click="openSelectAudiencesDrawer()"
    >
      <v-row align="center">
        <v-col class="grow d-flex align-items-center hover-button"
          ><icon
            type="plus"
            :size="12"
            color="primary"
            class="mr-1 mt-1"
          /><span class="body-1 not-lookalike-color">Audience</span></v-col
        >
      </v-row>
    </v-alert>
    <h5 class="text-h3 mb-2">Setup a delivery schedule</h5>
    <div class="d-flex align-items-center">
      <plain-card
        :icon="!isRecurringFlag ? 'manual-light' : 'manual-dark'"
        title="Manual"
        description="Deliver this engagement when you are ready."
        :style="
          !isRecurringFlag
            ? { float: 'left', color: 'var(--v-primary-lighten6)' }
            : { float: 'left', color: 'var(--v-black-base)' }
        "
        title-color="black--text"
        height="175"
        width="200"
        top-adjustment="mt-3"
        :class="!isRecurringFlag ? 'border-card' : 'model-desc-card mr-0'"
        @onClick="changeSchedule(false)"
      />
      <plain-card
        :icon="!isRecurringFlag ? 'recurring-dark' : 'recurring-light'"
        title="Recurring"
        description="Deliver this engagement during a chosen timeframe."
        :style="
          isRecurringFlag
            ? { float: 'left', color: 'var(--v-primary-lighten6)' }
            : { float: 'left', color: 'var(--v-black-base)' }
        "
        title-color="black--text"
        height="175"
        width="200"
        top-adjustment="mt-3"
        :class="isRecurringFlag ? 'border-card' : 'model-desc-card mr-0'"
        @onClick="changeSchedule(true)"
      />
    </div>
    <div v-if="isRecurringFlag" class="delivery-background px-4 pt-4 pb-6">
      <v-row class="delivery-schedule mt-6 ml-n2">
        <div>
          <span
            class="date-picker-label black--text text--darken-4 text-caption"
          >
            Start date
          </span>
          <hux-start-date
            class="mt-n4"
            :label="selectedStartDate"
            :selected="selectedStartDate"
            @on-date-select="onStartDateSelect"
          />
        </div>
        <icon class="mx-2" type="arrow" :size="28" color="black-lighten3" />
        <div>
          <span
            class="date-picker-label black--text text--darken-4 text-caption"
          >
            End date
          </span>
          <hux-end-date
            class="mt-n4"
            :label="selectedEndDate"
            :selected="selectedEndDate"
            :is-sub-menu="true"
            :min-date="endMinDate"
            @on-date-select="onEndDateSelect"
          />
        </div>
      </v-row>
      <v-row class="delivery-schedule mt-5">
        <hux-schedule-picker
          v-model="localSchedule"
          :start-date="selectedStartDate"
          :end-date="selectedEndDate"
        />
      </v-row>
    </div>

    <hux-footer>
      <template #left>
        <hux-button
          size="large"
          tile
          variant="white"
          height="40"
          class="btn-border box-shadow-none rounded-0"
          @click.native="
            dontShowModal = true
            $router.go(-1)
          "
        >
          <span class="primary--text">Cancel &amp; return</span>
        </hux-button>
      </template>

      <template #right>
        <hux-button
          v-if="isEditable"
          tile
          color="primary"
          height="44"
          class="rounded-0"
          :is-disabled="
            !isValid ||
            (isRecurringFlag &&
              (selectedStartDate == 'Select date' || selectedStartDate == null))
          "
          @click="showUpdateModal = true"
        >
          Update
        </hux-button>

        <hux-button
          v-else-if="hasDestinations && isManualDelivery"
          tile
          color="primary"
          height="44"
          :is-disabled="!isValid || !isDateValid"
          data-e2e="create-engagement"
          @click="deliverNewEngagement()"
        >
          Create &amp; deliver
        </hux-button>

        <hux-button
          v-else
          tile
          color="primary"
          height="44"
          :is-disabled="!isValid || !isDateValid"
          @click="addNewEngagement()"
        >
          Create
        </hux-button>
      </template>
    </hux-footer>

    <select-audiences-drawer
      ref="selectAudiences"
      v-model="value.audiences"
      :toggle="showSelectAudiencesDrawer"
      @onToggle="(val) => (showSelectAudiencesDrawer = val)"
      @onAdd="openAddAudiencesDrawer()"
    />

    <add-audience-drawer
      ref="addNewAudience"
      v-model="value.audiences"
      :toggle="showAddAudiencesDrawer"
      @onToggle="(val) => (showAddAudiencesDrawer = val)"
      @onCancelAndBack="openSelectAudiencesDrawer()"
    />

    <select-destinations-drawer
      ref="selectDestinations"
      v-model="value.audiences"
      :selected-audience-id="selectedAudienceId"
      :toggle="showSelectDestinationsDrawer"
      @onToggle="(val) => (showSelectDestinationsDrawer = val)"
      @onSalesforce="openDataExtensionDrawer"
    />

    <destination-data-extension-drawer
      v-model="value.audiences"
      :selected-destination="selectedDestination"
      :selected-audience-id="selectedAudienceId"
      :toggle="showDataExtensionDrawer"
      @onToggle="(val) => (showDataExtensionDrawer = val)"
      @onBack="openSelectDestinationsDrawer"
    />

    <confirm-modal
      v-model="showUpdateModal"
      icon="alert-edit"
      type="error"
      title="Edit"
      :sub-title="`${value.name}?`"
      left-btn-text="Cancel"
      right-btn-text="Yes, edit"
      body="Are you sure you want to edit this engagement? <br>
By changing the engagement, you may need to reschedule the delivery time and it will impact all associated audiences and destinations."
      @onCancel="showUpdateModal = false"
      @onConfirm="restoreEngagement()"
    />
  </v-form>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import DataCards from "@/components/common/DataCards.vue"
import HuxFooter from "@/components/common/HuxFooter.vue"
import huxButton from "@/components/common/huxButton"
import Logo from "@/components/common/Logo.vue"
import TextField from "@/components/common/TextField.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import AddAudienceDrawer from "./Drawers/AddAudienceDrawer.vue"
import SelectAudiencesDrawer from "./Drawers/SelectAudiencesDrawer.vue"
import SelectDestinationsDrawer from "./Drawers/SelectDestinationsDrawer.vue"
import DestinationDataExtensionDrawer from "./Drawers/DestinationDataExtensionDrawer.vue"
import HuxStartDate from "@/components/common/DatePicker/HuxStartDate"
import HuxEndDate from "@/components/common/DatePicker/HuxEndDate"
import Icon from "@/components/common/Icon.vue"
import HuxSchedulePicker from "@/components/common/DatePicker/HuxSchedulePicker.vue"
import PlainCard from "@/components/common/Cards/PlainCard.vue"
import ConfirmModal from "@/components/common/ConfirmModal.vue"
import { deliverySchedule } from "@/utils"

export default {
  name: "EngagementsForm",

  components: {
    DataCards,
    Logo,
    HuxFooter,
    TextField,
    Tooltip,
    AddAudienceDrawer,
    SelectAudiencesDrawer,
    SelectDestinationsDrawer,
    DestinationDataExtensionDrawer,
    HuxStartDate,
    HuxEndDate,
    Icon,
    HuxSchedulePicker,
    huxButton,
    PlainCard,
    ConfirmModal,
  },

  props: {
    value: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      showSelectAudiencesDrawer: false,
      showAddAudiencesDrawer: false,
      showSelectDestinationsDrawer: false,
      showDataExtensionDrawer: false,
      selectedAudienceId: null,
      selectedDestination: null,
      selectedStartDate: "Select date",
      selectedEndDate: "Select date",
      disableEndDate: true,
      errorMessages: [],
      localSchedule: JSON.parse(JSON.stringify(deliverySchedule())),
      endMinDate: new Date(
        new Date().getTime() - new Date().getTimezoneOffset() * 60000
      ).toISOString(),
      engagementList: {},
      dontShowModal: false,
      isRecurringFlag: false,
      showUpdateModal: false,
    }
  },

  computed: {
    ...mapGetters({
      destination: "destinations/single",
    }),

    getRouteId() {
      return this.$route.params.id
    },

    isEditable() {
      return this.$route.name === "EngagementUpdate" ? true : false
    },

    payload() {
      const requestPayload = {
        name: this.value.name,
        description: this.value.description,
        audiences: Object.values(this.value.audiences).map((audience) => {
          return {
            id: audience.id,
            destinations: audience.destinations,
          }
        }),
      }

      if (this.isRecurringFlag) {
        const recurringConfig = {}
        recurringConfig["every"] = this.localSchedule.every
        recurringConfig["periodicity"] = this.localSchedule.periodicity
        recurringConfig["hour"] = this.localSchedule.hour
        recurringConfig["minute"] = this.localSchedule.minute
        recurringConfig["period"] = this.localSchedule.period
        if (this.localSchedule && this.localSchedule.periodicity == "Weekly") {
          recurringConfig["day_of_week"] = this.localSchedule.day_of_week
        } else if (
          this.localSchedule &&
          this.localSchedule.periodicity == "Monthly"
        ) {
          recurringConfig["monthly_period_items"] = [
            this.localSchedule.monthlyPeriod,
          ]
          recurringConfig["day_of_month"] =
            this.localSchedule.monthlyPeriod === "Day"
              ? this.localSchedule.monthlyDayDate
              : this.localSchedule.monthlyDay
        }
        requestPayload["delivery_schedule"] = {
          start_date:
            this.selectedStartDate !== "Select date"
              ? new Date(this.selectedStartDate).toISOString()
              : null,
          end_date:
            this.selectedEndDate !== "Select date" &&
            this.selectedEndDate !== "No end date"
              ? new Date(this.selectedEndDate).toISOString()
              : null,
          schedule: recurringConfig,
        }
      } else {
        requestPayload["delivery_schedule"] = null
      }

      return requestPayload
    },

    isValid() {
      return this.value.name.length
    },

    isDateValid() {
      if (this.value.delivery_schedule == 1) {
        if (this.selectedStartDate == "Select date") {
          return false
        } else {
          return true
        }
      } else {
        return true
      }
    },

    hasAudiences() {
      return Boolean(this.totalSelectedAudiences > 0)
    },

    hasDestinations() {
      return Object.values(this.value.audiences).find((audience) => {
        return audience.destinations && audience.destinations.length
      })
    },

    isManualDelivery() {
      return this.value.delivery_schedule === 0
    },

    totalSelectedAudiences() {
      return Object.values(this.value.audiences).length
    },

    isRecurring() {
      return this.value.delivery_schedule == 1
    },
  },

  watch: {
    value() {
      if (this.value.schedule) {
        this.localSchedule = JSON.parse(
          JSON.stringify(deliverySchedule(this.value.schedule))
        )
      }
    },
    isRecurring() {
      this.isRecurringFlag = this.isRecurring
    },
  },

  methods: {
    ...mapActions({
      addEngagement: "engagements/add",
      deliverEngagement: "engagements/deliver",
      updateEngagement: "engagements/updateEngagement",
    }),

    resetSchedule() {
      this.localSchedule = JSON.parse(JSON.stringify(deliverySchedule()))
    },

    changeSchedule(val) {
      this.isRecurringFlag = val
      if (this.value.delivery_schedule) {
        this.selectedStartDate = "Select date"
        this.selectedEndDate = "Select date"
        this.disableEndDate = true
        this.endMinDate = new Date(
          new Date().getTime() - new Date().getTimezoneOffset() * 60000
        ).toISOString()
        this.$set(this.value, "recurring", null)
        this.resetSchedule()
      }
    },

    closeAllDrawers() {
      this.showSelectAudiencesDrawer = false
      this.showAddAudiencesDrawer = false
      this.showSelectDestinationsDrawer = false
      this.showDataExtensionDrawer = false
    },

    scrollToTop() {
      window.scrollTo({
        top: 100,
        left: 100,
        behavior: "auto",
      })
    },

    openSelectAudiencesDrawer() {
      this.closeAllDrawers()
      this.$refs.selectAudiences.fetchAudiences()
      this.showSelectAudiencesDrawer = true
    },

    openAddAudiencesDrawer() {
      this.closeAllDrawers()
      this.$refs.addNewAudience.fetchDependencies()
      this.showAddAudiencesDrawer = true
    },

    openSelectDestinationsDrawer(audienceId) {
      // set the selected audience on which we want to manage its destinations
      this.selectedAudienceId = audienceId
      this.$refs.selectDestinations.fetchDependencies()
      this.closeAllDrawers()
      this.showSelectDestinationsDrawer = true
    },

    openDataExtensionDrawer(destination) {
      this.closeAllDrawers()
      this.selectedDestination = destination
      this.showDataExtensionDrawer = true
    },

    removeAudience(audience) {
      this.$delete(this.value.audiences, audience.id)
    },

    isLastItem(index) {
      return Boolean(index === this.totalSelectedAudiences - 1)
    },

    destinationType(id) {
      return this.destination(id) && this.destination(id).type
    },

    async addNewEngagement() {
      try {
        const engagement = await this.addEngagement(this.payload)
        this.dontShowModal = true
        this.$router.push({
          name: "EngagementDashboard",
          params: { id: engagement.id },
        })
      } catch (error) {
        this.errorMessages.push(error.response.data.message)
        this.scrollToTop()
      }
    },

    async deliverNewEngagement() {
      try {
        const engagement = await this.addEngagement(this.payload)
        await this.deliverEngagement(engagement.id)
        this.dontShowModal = true
        this.$router.push({
          name: "EngagementDashboard",
          params: { id: engagement.id },
        })
      } catch (error) {
        this.errorMessages.push(error.response.data.message)
        this.scrollToTop()
      }
    },

    async restoreEngagement() {
      this.showUpdateModal = false
      try {
        const requestPayload = { ...this.payload }
        if (requestPayload.delivery_schedule === 0) {
          delete requestPayload.start_date
          delete requestPayload.end_date
        }
        const payload = { id: this.getRouteId, data: requestPayload }
        await this.updateEngagement(payload)
        this.dontShowModal = true
        this.$router.push({
          name: "EngagementDashboard",
          params: { id: this.getRouteId },
        })
      } catch (error) {
        this.errorMessages.push(error.response.data.message)
        this.scrollToTop()
      }
    },

    removeDestination(deleteAudience, id) {
      const index = this.value.audiences[
        deleteAudience.item.id
      ].destinations.findIndex((destination) => destination.id === id)
      this.value.audiences[deleteAudience.item.id].destinations.splice(index, 1)
    },

    onStartDateSelect(val) {
      this.selectedStartDate = val
      this.$set(this.value, "recurring", {
        start: this.$options.filters.Date(this.selectedStartDate, "MMM D"),
        end: this.$options.filters.Date(this.selectedEndDate, "MMM D") || null,
      })
      this.endMinDate = val
    },

    onEndDateSelect(val) {
      if (!val) {
        this.selectedEndDate = "No end date"
        this.$set(this.value, "recurring", {
          start: this.$options.filters.Date(this.selectedStartDate, "MMM D"),
          end: null,
        })
      } else {
        this.selectedEndDate = val
        this.$set(this.value, "recurring", {
          start: this.$options.filters.Date(this.selectedStartDate, "MMM D"),
          end: this.$options.filters.Date(this.selectedEndDate, "MMM D"),
        })
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.destinations-wrap {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  flex-direction: row-reverse;

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
}
.delivery-schedule {
  margin-left: auto;
  .icon-right {
    transform: scale(1.5);
    margin-left: 12px;
    margin-right: 12px;
    margin-top: -30px;
    color: var(--v-black-lighten3) !important;
  }
}
.date-picker-label {
  position: absolute;
  margin-top: -30px;
  margin-left: 8px;
}
.form-steps {
  ::v-deep .form-step__content {
    padding-top: 0px !important;
  }
}
.resize-destination-button {
  width: 80px;
  height: 24px;
  color: transparent;
  position: relative;
  top: 2px;
  &:hover {
    cursor: pointer;
  }
}
.not-lookalike-color {
  color: var(--v-primary-base);
}
.empty-card {
  border: 1px solid var(--v-black-lighten2) !important;
  background: var(--v-primary-lighten1) !important;
}
.hover-button {
  &:hover {
    cursor: pointer;
  }
}
.border-card {
  border: solid 1px var(--v-primary-lighten6);
}
.delivery-background {
  width: 612px;
  border: solid 1px var(--v-black-lighten2);
  background: #f9fafb;
  position: relative;
  bottom: 25px;
  border-radius: 5px;
}
</style>
