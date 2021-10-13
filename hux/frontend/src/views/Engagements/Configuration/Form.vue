<template>
  <v-form>
    <form-steps>
      <form-step :step="1" label="General information">
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
      </form-step>

      <form-step :step="2">
        <template slot="label">
          <h5 class="text-h5 d-flex align-start">
            Setup a delivery schedule

            <tooltip>
              <template #label-content>
                <v-icon color="primary" :size="12" class="ml-1">
                  mdi-information-outline
                </v-icon>
              </template>
              <template #hover-content>
                <v-sheet max-width="240px">
                  <h6 class="text-caption mb-2">Manual delivery</h6>
                  <p class="black--text text--darken-1">
                    Choose this option if you want the engagement delivered
                    immediately or at a future date and time.
                  </p>
                  <h6 class="text-caption mb-2">Recurring delivery</h6>
                  <p class="black--text text--darken-1">
                    Choose this option if you want the engagement delivered on a
                    specific recurring basis you selected.
                  </p>
                </v-sheet>
              </template>
            </tooltip>
          </h5>
        </template>

        <v-row class="delivery-schedule mt-2">
          <v-radio-group
            v-model="value.delivery_schedule"
            row
            class="ma-0 radio-div"
            @change="changeSchedule()"
          >
            <v-radio
              :value="0"
              selected
              :class="
                value.delivery_schedule == 0
                  ? 'btn-radio-active'
                  : 'btn-radio-inactive'
              "
            >
              <template #label>
                <v-icon small color="primary" class="mr-1">
                  mdi-gesture-tap
                </v-icon>
                <span class="primary--text">Manual</span>
              </template>
            </v-radio>

            <v-radio
              :value="1"
              :class="isRecurring ? 'btn-radio-active' : 'btn-radio-inactive'"
            >
              <template #label>
                <v-icon small color="primary" class="mr-1"
                  >mdi-clock-check-outline</v-icon
                >
                <span class="primary--text">Recurring</span>
              </template>
            </v-radio>
          </v-radio-group>
        </v-row>
        <v-row v-if="isRecurring" class="delivery-schedule mt-10 ml-n2">
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
          <hux-schedule-picker v-if="isRecurring" v-model="schedule" />
        </v-row>
      </form-step>

      <form-step :step="3" label="Select audience(s) and destination(s)">
        <p v-if="hasAudiences" class="text-h6">
          First add and deliver an audience to Facebook in order to create a
          lookalike audience from this engagement’s dashboard.
        </p>

        <data-cards
          bordered
          :items="Object.values(value.audiences)"
          :fields="[
            {
              key: 'name',
              label: 'Audience name',
            },
            {
              key: 'size',
              label: 'Target size',
            },
            {
              key: 'destinations',
              label: 'Destinations',
            },
            {
              key: 'manage',
            },
          ]"
        >
          <template #field:size="row">
            <tooltip>
              <template #label-content>
                {{ row.value | Numeric(true, true) | Empty }}
              </template>
              <template #hover-content>
                {{
                  row.value | Numeric | Empty("Size unavailable at this time")
                }}
              </template>
            </tooltip>
          </template>

          <template #field:destinations="row">
            <div class="destinations-wrap">
              <v-row class="align-center">
                <div>
                  <tooltip
                    v-for="destination in row.value"
                    :key="destination.id"
                  >
                    <template #label-content>
                      <div class="destination-logo-wrapper">
                        <div class="logo-wrapper">
                          <logo
                            class="added-logo ml-2 svg-icon"
                            :type="destinationType(destination.id)"
                            :size="24"
                          />
                          <logo
                            class="delete-icon"
                            type="delete"
                            @click.native="
                              removeDestination(row, destination.id)
                            "
                          />
                        </div>
                      </div>
                    </template>
                    <template #hover-content>
                      <div class="d-flex align-center">Remove</div>
                    </template>
                  </tooltip>
                </div>
                <div>
                  <tooltip>
                    <template #label-content>
                      <v-btn
                        x-small
                        fab
                        class="primary ml-2 box-shadow-25"
                        data-e2e="add-destination"
                        @click="openSelectDestinationsDrawer(row.item.id)"
                      >
                        <v-icon size="16">mdi-plus</v-icon>
                      </v-btn>
                    </template>
                    <template #hover-content>Add destination(s)</template>
                  </tooltip>
                </div>
              </v-row>
            </div>
          </template>

          <template #field:manage="row">
            <div class="d-flex align-center justify-end">
              <tooltip v-if="isLastItem(row.index)">
                <template #label-content>
                  <v-btn
                    x-small
                    fab
                    class="primary mr-2 box-shadow-25"
                    @click="openSelectAudiencesDrawer()"
                  >
                    <v-icon>mdi-plus</v-icon>
                  </v-btn>
                </template>
                <template #hover-content>Add another audience</template>
              </tooltip>

              <v-btn icon color="primary" @click="removeAudience(row.item)">
                <v-icon>mdi-delete-outline</v-icon>
              </v-btn>
            </div>
          </template>

          <template slot="empty">
            <v-col class="shrink pl-5">
              <v-btn
                x-small
                fab
                color="primary box-shadow-25"
                elevation="0"
                data-e2e="add-audience"
                @click="openSelectAudiencesDrawer()"
              >
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </v-col>
            <v-col class="grow pl-2">
              You have not added any audiences, yet.
            </v-col>
          </template>
        </data-cards>
      </form-step>
    </form-steps>

    <hux-footer>
      <template #left>
        <v-btn
          tile
          color="white"
          height="40"
          @click.native="
            dontShowModal = true
            $router.go(-1)
          "
        >
          <span class="primary--text">Cancel</span>
        </v-btn>
      </template>

      <template #right>
        <v-btn
          v-if="isEditable"
          tile
          color="primary"
          height="44"
          :disabled="!isValid"
          @click="restoreEngagement()"
        >
          Update
        </v-btn>

        <v-btn
          v-else-if="hasDestinations && isManualDelivery"
          tile
          color="primary"
          height="44"
          :disabled="!isValid"
          data-e2e="create-engagement"
          @click="deliverNewEngagement()"
        >
          Create &amp; deliver
        </v-btn>

        <v-btn
          v-else
          tile
          color="primary"
          height="44"
          :disabled="!isValid || !isDateValid"
          @click="addNewEngagement()"
        >
          Create
        </v-btn>
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
  </v-form>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import DataCards from "@/components/common/DataCards.vue"
import FormStep from "@/components/common/FormStep.vue"
import FormSteps from "@/components/common/FormSteps.vue"
import HuxFooter from "@/components/common/HuxFooter.vue"
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
import { deliverySchedule } from "@/utils"

export default {
  name: "EngagementsForm",

  components: {
    DataCards,
    FormStep,
    FormSteps,
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
      schedule: JSON.parse(JSON.stringify(deliverySchedule())),
      endMinDate: new Date(
        new Date().getTime() - new Date().getTimezoneOffset() * 60000
      ).toISOString(),
      engagementList: {},
      dontShowModal: false,
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
      const recurringConfig = {}
      recurringConfig["every"] = this.schedule.every
      recurringConfig["periodicity"] = this.schedule.periodicity
      if (this.schedule && this.schedule.periodicity == "Daily") {
        recurringConfig["hour"] = this.schedule.hour
        recurringConfig["minute"] = this.schedule.minute
        recurringConfig["period"] = this.schedule.period
      } else if (this.schedule && this.schedule.periodicity == "Weekly") {
        recurringConfig["day_of_week"] = this.schedule.days.map((item) => {
          return item.substring(0, 3).toUpperCase()
        })
      } else if (this.schedule && this.schedule.periodicity == "Monthly") {
        recurringConfig["day_of_month"] = this.schedule.monthlyDayDate
      }

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

      if (this.value.delivery_schedule == 1) {
        requestPayload["delivery_schedule"] = {
          start_date: !this.isManualDelivery
            ? new Date(this.selectedStartDate).toISOString()
            : null,
          end_date:
            !this.isManualDelivery && this.selectedEndDate
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
        let deliverySchedule = this.value.schedule
        for (let prop in deliverySchedule) {
          this.schedule[prop] = deliverySchedule.hasOwnProperty(prop)
            ? deliverySchedule[prop]
            : this.schedule[prop]
        }
      }
    },
  },

  methods: {
    ...mapActions({
      addEngagement: "engagements/add",
      deliverEngagement: "engagements/deliver",
      updateEngagement: "engagements/updateEngagement",
    }),

    resetSchedule() {
      this.schedule = JSON.parse(JSON.stringify(deliverySchedule()))
    },

    changeSchedule() {
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
.btn-radio {
  padding: 8px 16px;
  border-radius: 4px;

  &.v-radio--is-disabled {
    border-color: var(--v-black-lighten3);
  }
}
.btn-radio-inactive {
  border: 1px solid var(--v-black-lighten3);
  @extend .btn-radio;
}
.btn-radio-active {
  border: 1px solid var(--v-primary-base);
  @extend .btn-radio;
}
.radio-div {
  margin-top: -11px !important;
  .v-radio {
    width: 175px;
  }
}
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
</style>
