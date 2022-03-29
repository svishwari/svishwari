<template>
  <drawer v-model="localDrawer" :loading="loading" @onClose="goToStep1()">
    <template #header-left>
      <div class="d-flex align-center">
        <icon
          v-if="viewStep == '1'"
          type="engagements"
          :size="18"
          color="black-darken4"
        />
        <h3
          v-if="viewStep == '1'"
          class="text-h3 ml-2 black--text text--darken-4"
        >
          Add to an engagement
        </h3>
        <h3 v-else class="text-h3 ml-2 black--text text--darken-4">
          Add a new engagement
        </h3>
      </div>
    </template>
    <template #default>
      <v-stepper v-if="!loading" v-model="viewStep">
        <v-stepper-items>
          <v-stepper-content step="1">
            <div v-if="!areEngagementAlreadyCreated">
              <v-row class="no-engagement-frame py-14 mx-7">
                <empty-page type="no-engagement-found" :size="50">
                  <template #title>
                    <div class="h2">No engagements</div>
                  </template>
                  <template #subtitle>
                    <div class="body-2">
                      Engagements will appear here once you start creating them.
                    </div>
                  </template>
                  <template #button>
                    <huxButton
                      variant="primary base"
                      icon-color="white"
                      icon-variant="base"
                      size="small"
                      is-custom-icon
                      class="ma-2 caption"
                      is-tile
                      data-e2e="first-engagement-create"
                      @click="goToStep2()"
                    >
                      Create an engagement
                    </huxButton>
                  </template>
                </empty-page>
              </v-row>
            </div>
            <div v-else class="ma-1">
              <h6 class="mb-6 text-h6 black--text text--darken-4">
                Select an existing engagement or create a new one. You are
                required to have at least one selected.
              </h6>
              <huxButton
                variant="primary base"
                icon-color="white"
                icon-variant="base"
                icon="plus"
                size="small"
                is-custom-icon
                class="ma-2 caption"
                is-tile
                height="40"
                @click="goToAddNewEngagement()"
              >
                New engagement
              </huxButton>
              <div class="engagement-list-wrap mt-6">
                <div>
                  <span class="text-caption">Engagement name</span>
                  <v-icon
                    v-if="showSortIcon"
                    :class="{ 'rotate-icon-180': toggleSortIcon }"
                    class="ml-1"
                    color="primary lighten-8"
                    size="12"
                    @click="onSortIconClick()"
                  >
                    mdi-arrow-down
                  </v-icon>
                </div>
                <card-horizontal
                  v-for="engagement in engagements"
                  :key="engagement.id"
                  :is-added="isEngagementSelected(engagement)"
                  :enable-blue-background="isEngagementSelected(engagement)"
                  class="my-3 mb-4 mt-1"
                  data-e2e="engagement-list"
                  @click="onEngagementClick(engagement)"
                >
                  <v-menu open-on-hover offset-x offset-y :max-width="177">
                    <template #activator="{ on }">
                      <div class="pl-2 font-weight-regular" v-on="on">
                        {{ engagement.name }}
                      </div>
                    </template>
                    <template #default>
                      <div class="px-4 py-2 white">
                        <div class="black--text text--darken-4 text-caption">
                          Name
                        </div>
                        <div
                          class="black--text text--lighten-3 text-caption mt-1"
                        >
                          {{ engagement.name }}
                        </div>
                        <div
                          class="black--text text--darken-4 text-caption mt-3"
                        >
                          Description
                        </div>
                        <div
                          class="black--text text--lighten-3 text-caption mt-1"
                        >
                          {{ engagement.description }}
                        </div>
                      </div>
                    </template>
                  </v-menu>
                </card-horizontal>
              </div>
            </div>
          </v-stepper-content>
          <v-stepper-content step="2">
            <div class="new-engament-wrap content-section">
              <h6 class="mb-8 text-h6 black--text text--darken-4">
                Build a new engagement to see performance information on this
                audience.
              </h6>
              <v-form ref="newEngagementRef" v-model="newEngagementValid">
                <text-field
                  v-model="newEngagement.name"
                  label-text="Engagement name"
                  placeholder="Give this engagement a name"
                  height="40"
                  :rules="newEngagementRules"
                  data-e2e="new-engagement-name"
                  required
                />
                <text-field
                  v-model="newEngagement.description"
                  label-text="Description"
                  placeholder="What is the purpose of this engagement?"
                  height="40"
                />
                <div class="mb-2">
                  <span class="black--text text--darken-4 text-caption">
                    Delivery schedule
                  </span>
                  <v-menu max-width="240" open-on-hover offset-y>
                    <template #activator="{ on }">
                      <v-icon
                        color="primary"
                        :size="8"
                        class="ml-1 mb-1"
                        v-on="on"
                      >
                        mdi-information-outline
                      </v-icon>
                    </template>
                    <template #default>
                      <div class="px-4 py-2 white">
                        <div class="black--text text--darken-4 text-caption">
                          Manual delivery
                        </div>
                        <div
                          class="black--text text--darken-1 text-caption mt-1"
                        >
                          Choose this option if you want the engagement
                          delivered immediately or at a future date and time.
                        </div>
                        <div
                          class="black--text text--darken-4 text-caption mt-3"
                        >
                          Recurring delivery
                        </div>
                        <div
                          class="black--text text--darken-1 text-caption mt-1"
                        >
                          Choose this option if you want the engagement
                          delivered on a specific recurring basis you selected.
                        </div>
                      </div>
                    </template>
                  </v-menu>
                </div>
                <div class="d-flex">
                  <div
                    class="
                      cursor-pointer
                      text-center
                      rounded-lg
                      manual
                      py-5
                      px-5
                      mr-2
                      ml-2
                    "
                    :class="[isActive ? 'active' : 'box-shadow-1']"
                    @click="toggleClass($event), resetSchedule()"
                  >
                    <icon
                      type="manual"
                      :color="isActive ? 'primary' : 'black'"
                      :variant="isActive ? 'lighten6' : ''"
                      :size="40"
                    />
                    <div
                      class="mt-2 text-button"
                      :class="isActive ? 'primary--text text--lighten-6' : ''"
                    >
                      Manual
                    </div>
                    <div class="pt-2 black--text text--lighten-4 text-body-2">
                      Deliver this engagement when you are ready.
                    </div>
                  </div>
                  <div
                    class="
                      cursor-pointer
                      text-center
                      rounded-lg
                      recurring
                      py-5
                      px-5
                      ml-2
                    "
                    :class="[!isActive ? 'active' : 'box-shadow-1']"
                    @click="toggleClass($event)"
                  >
                    <icon
                      type="recurring"
                      :color="!isActive ? 'primary' : 'black'"
                      :variant="!isActive ? 'lighten6' : ''"
                      :size="40"
                    />
                    <div
                      class="mt-2 text-button"
                      :class="!isActive ? 'primary--text text--lighten-6' : ''"
                    >
                      Recurring
                    </div>
                    <div class="pt-2 black--text text--lighten-4 text-body-2">
                      Deliver this engagement during a chosen timeframe.
                    </div>
                  </div>
                </div>
                <div v-if="!isActive" class="schedule-recurring mt-6 px-6 py-5">
                  <div class="d-flex align-center">
                    <div>
                      <div class="text-body-2 pl-2 mb-n2">Start date</div>
                      <hux-start-date
                        :label="selectedStartDate"
                        :selected="selectedStartDate"
                        @on-date-select="onStartDateSelect"
                      />
                    </div>
                    <div>
                      <icon
                        class="ml-2 mr-1 mt-3"
                        type="arrow"
                        :size="19"
                        color="primary"
                        variant="lighten6"
                      />
                    </div>
                    <div>
                      <div class="text-body-2 pl-2 mb-n2">End date</div>
                      <hux-end-date
                        :label="selectedEndDate"
                        :selected="selectedEndDate"
                        :is-sub-menu="true"
                        :min-date="endMinDate"
                        @on-date-select="onEndDateSelect"
                      />
                    </div>
                  </div>
                  <div class="mx-2 mt-2">
                    <hux-schedule-picker
                      v-model="schedule"
                      short
                      :colon-sign="true"
                      :start-date="selectedStartDate"
                      :end-date="selectedEndDate"
                    />
                  </div>
                </div>
              </v-form>
            </div>
          </v-stepper-content>
        </v-stepper-items>
      </v-stepper>
    </template>
    <template #footer-right>
      <div v-if="viewStep == 2" class="d-flex align-baseline">
        <huxButton
          variant="primary"
          :is-tile="true"
          height="40"
          width="146"
          :is-disabled="!newEngagementValid"
          data-e2e="create-engagement-new"
          @click.native="addEngagement()"
        >
          Create &amp; add
        </huxButton>
      </div>
    </template>

    <template #footer-left>
      <div
        v-if="viewStep == 1 && areEngagementAlreadyCreated"
        class="d-flex align-baseline black--text text--darken-1 text-caption"
      >
        {{ engagements.length }} results
      </div>
      <div v-if="viewStep == 2" class="d-flex align-baseline">
        <huxButton
          size="large"
          variant="white"
          :is-tile="true"
          height="40"
          width="146"
          class="btn-border box-shadow-none"
          @click.native="goToStep1()"
        >
          <span class="primary--text">Cancel &amp; back</span>
        </huxButton>
      </div>
    </template>
  </drawer>
</template>

<script>
import { mapActions } from "vuex"

import huxButton from "@/components/common/huxButton"
import TextField from "@/components/common/TextField"
import EmptyPage from "@/components/common/EmptyPage"
import Drawer from "@/components/common/Drawer"
import CardHorizontal from "@/components/common/CardHorizontal"
import Icon from "@/components/common/Icon"

import sortBy from "lodash/sortBy"
import HuxStartDate from "@/components/common/DatePicker/HuxStartDate"
import HuxEndDate from "@/components/common/DatePicker/HuxEndDate"

import HuxSchedulePicker from "@/components/common/DatePicker/HuxSchedulePicker.vue"
import { deliverySchedule } from "@/utils"

export default {
  name: "AttachEngagement",

  components: {
    Drawer,
    huxButton,
    TextField,
    CardHorizontal,
    EmptyPage,
    Icon,
    HuxStartDate,
    HuxEndDate,
    HuxSchedulePicker,
  },

  props: {
    value: {
      type: Boolean,
      required: true,
      default: false,
    },
    finalEngagements: {
      type: Array,
      required: true,
      default: () => [],
    },
    closeOnAction: {
      type: Boolean,
      required: false,
      default: false,
    },
  },

  data() {
    return {
      localDrawer: this.value,
      toggleSortIcon: true,
      showSortIcon: true,
      engagements: [],
      loading: false,
      viewStep: 1,
      selectedEngagements: [],
      newEngagement: {
        name: "",
        description: "",
        delivery_schedule: 0,
      },
      newEngagementValid: false,
      newEngagementRules: [(v) => !!v || "Engagement name is required"],
      sortBy: sortBy,
      selectedStartDate: new Date(
        Date.now() - new Date().getTimezoneOffset() * 60000
      )
        .toISOString()
        .substr(0, 10),
      selectedEndDate: "Select date",
      schedule: JSON.parse(JSON.stringify(deliverySchedule())),
      endMinDate: new Date(
        new Date().getTime() - new Date().getTimezoneOffset() * 60000
      ).toISOString(),
      isActive: true,
    }
  },

  computed: {
    areEngagementAlreadyCreated() {
      return this.engagements.length > 0
    },
    isRecurring() {
      return this.newEngagement.delivery_schedule == 1
    },
    scheduleConfig() {
      const recurringConfig = {
        every: this.schedule.every,
        periodicity: this.schedule.periodicity,
        hour: this.schedule.hour,
        minute: this.schedule.minute,
        period: this.schedule.period,
      }
      if (this.schedule) {
        switch (this.schedule.periodicity) {
          case "Weekly":
            recurringConfig["day_of_week"] = this.schedule.day_of_week
            break
          case "Monthly":
            recurringConfig["day_of_month"] = [this.schedule.monthlyDayDate]
            break
          default:
            recurringConfig
        }
      }
      return recurringConfig
    },
  },

  watch: {
    value: function () {
      this.localDrawer = this.value
    },
    localDrawer: function () {
      this.$emit("input", this.localDrawer)
      if (!this.localDrawer) {
        this.$emit("onClose")
        this.showSortIcon = true
      }
    },
    finalEngagements: function (newVal) {
      this.selectedEngagements = newVal
    },
  },

  methods: {
    ...mapActions({
      fetchEngagements: "engagements/getAll",
      addEngagementToDB: "engagements/add",
    }),
    async fetchDependencies() {
      this.loading = true
      await this.fetchEngagements()
      this.engagements = JSON.parse(
        JSON.stringify(this.$store.getters["engagements/list"])
      )
      this.sortEngagements()
      this.loading = false
    },
    onStartDateSelect(val) {
      this.selectedStartDate = val
      this.selectedEndDate = null
      this.endMinDate = val
    },
    onEndDateSelect(val) {
      if (!val) {
        this.selectedEndDate = "No end date"
      } else {
        this.selectedEndDate = val
      }
    },
    initializeDate(date, defaultDate) {
      return date == "Select date" || date == "No end date"
        ? defaultDate
        : new Date(date).toISOString()
    },
    resetSchedule() {
      this.schedule = JSON.parse(JSON.stringify(deliverySchedule()))
      this.endMinDate = new Date(
        new Date().getTime() - new Date().getTimezoneOffset() * 60000
      ).toISOString()
      this.selectedStartDate = "Select date"
      this.selectedEndDate = "Select date"
    },
    isEngagementSelected: function (engagement) {
      return (
        this.selectedEngagements.filter((eng) => eng.id === engagement.id)
          .length > 0
      )
    },
    goToAddNewEngagement: function () {
      this.resetNewEngagement()
      this.goToStep2()
    },
    resetNewEngagement: function () {
      this.$refs.newEngagementRef.reset()
      this.newEngagement.delivery_schedule = 0
    },
    goToStep1: function () {
      this.viewStep = 1
    },
    goToStep2: function () {
      this.viewStep = 2
      this.resetSchedule()
    },
    addEngagement: async function () {
      this.loading = true
      const payload = {
        name: this.newEngagement.name,
        audiences: [],
        delivery_schedule: !this.isActive
          ? {
              schedule: this.scheduleConfig,
              start_date: this.initializeDate(
                this.selectedStartDate,
                new Date().toISOString()
              ),
              end_date: this.initializeDate(this.selectedEndDate, null),
            }
          : null,
      }
      if (this.newEngagement.description) {
        payload["description"] = this.newEngagement.description
      }
      try {
        const newEngagement = await this.addEngagementToDB(payload)
        this.engagements.push(newEngagement)
        this.engagements = this.engagements.sort((a, b) => {
          return new Date(b.update_time) - new Date(a.update_time)
        })
        this.showSortIcon = false
        this.onEngagementClick(newEngagement)
        if (this.closeOnAction) {
          this.$emit("onAddEngagement", newEngagement)
          this.localDrawer = false
        } else {
          this.goToStep1()
        }
        this.loading = false
      } finally {
        this.loading = false
      }
    },
    onEngagementClick: function (engagement) {
      if (
        this.selectedEngagements.filter((eng) => eng.id === engagement.id)
          .length > 0
      ) {
        if (this.selectedEngagements.length !== 1) {
          const deselectedId = this.selectedEngagements.findIndex(
            (eng) => eng.id === engagement.id
          )

          this.selectedEngagements.splice(deselectedId, 1)
          if (this.closeOnAction) {
            this.$emit("onAddEngagement", {
              data: engagement,
              action: "Detach",
            })
            this.localDrawer = false
          }
          this.$emit("onEngagementChange", this.selectedEngagements)
        }
      } else {
        this.selectedEngagements.push(engagement)
        if (this.closeOnAction) {
          this.$emit("onAddEngagement", { data: engagement, action: "Attach" })
          this.localDrawer = false
        }
        this.$emit("onEngagementChange", this.selectedEngagements)
      }
    },
    sortEngagements: function () {
      if (this.toggleSortIcon) {
        this.engagements = this.sortBy(this.engagements, ["name"])
      } else {
        this.engagements = this.sortBy(this.engagements, ["name"]).reverse()
      }
    },
    toggleSort: function () {
      this.toggleSortIcon = !this.toggleSortIcon
    },
    onSortIconClick: function () {
      this.toggleSort()
      this.sortEngagements()
    },
    toggleClass: function (event) {
      if (!event.currentTarget.classList.contains("active")) {
        this.isActive = !this.isActive
      }
      if (this.isActive) {
        this.resetSchedule()
      } else {
        this.selectedStartDate = new Date(
          Date.now() - new Date().getTimezoneOffset() * 60000
        )
          .toISOString()
          .substr(0, 10)

        this.selectedEndDate = "No end date"
      }
    },
  },
}
</script>

<style lang="scss" scoped>
::v-deep .v-stepper {
  box-shadow: none !important;
}
.new-engament-wrap {
  height: 650px;
  .delivery-options {
    ::v-deep button {
      background: var(--v-white-base);
      box-sizing: border-box;
      border-radius: 4px;
      border-left-width: 1px !important;
      width: 175px;
      height: 40px;
      padding: 10px;
      margin-right: 10px;
      .v-icon {
        &.ico {
          width: 13.44px;
          height: 12.5px;
          margin-right: 9px;
        }
      }
      .v-btn__content {
        justify-content: start;
        color: var(--v-primary-base) !important;
      }
      &.v-btn--active {
        border: 1px solid var(--v-primary-base) !important;
        &::before {
          opacity: 0;
        }
        .v-icon {
          &.ico {
            margin-right: 9px;
          }
        }
        .theme--light {
          color: var(--v-primary-base) !important;
        }
      }
    }
    .active-delivery-option.v-btn.v-item--active {
      border-color: var(--v-primary-base) !important;
    }
    .active-delivery-option.v-btn.btn-radio-inactive {
      border-color: var(--v-black-lighten3) !important;
      .v-btn__content {
        .v-radio.theme--light {
          ::v-deep .v-input--selection-controls__input {
            .v-icon.notranslate.mdi.mdi-radiobox-blank.theme--light {
              color: var(--v-black-darken1) !important;
            }
          }
        }
      }
    }
    .disabled-white-background {
      background: white !important;
      &.v-btn.v-item--active {
        border-color: var(--v-primary-base) !important;
      }
    }
  }
  .delivery-schedule {
    margin: 0;
    .hux-date-picker {
      ::v-deep .main-button {
        margin-left: 0px !important;
      }
    }
    .icon-right {
      transform: scale(1.5);
      margin-left: 8px;
      margin-right: 12px;
      margin-top: 20px;
      color: var(--v-black-lighten3) !important;
    }
    ::v-deep.v-icon {
      color: var(--v-black-lighten3) !important;
    }
  }
}
.no-engagement-frame {
  background-image: url("../../assets/images/no-alert-frame.png");
  background-position: center;
  background-size: 100%;
}
.manual,
.recurring {
  height: 175px;
  width: 260px;
  border-radius: 12px;
}
.manual.active,
.recurring.active {
  border: 1px solid var(--v-primary-lighten4);
}
.schedule-recurring {
  background: var(--v-primary-lighten1);
  border: 1px solid var(--v-black-lighten2);
  border-radius: 5px;
  .hux-date-picker {
    ::v-deep .main-button {
      min-width: 153px !important;
      width: 200px !important;
    }
  }
}
::-webkit-scrollbar {
  width: 5px;
}
::-webkit-scrollbar-track {
  box-shadow: inset 0 0 5px var(--v-white-base);
  border-radius: 10px;
}
::-webkit-scrollbar-thumb {
  background: var(--v-black-lighten3);
  border-radius: 5px;
}
::-webkit-scrollbar-thumb:hover {
  background: var(--v-black-lighten3);
}
.content-section {
  overflow-y: auto !important;
  overflow-x: hidden !important;
}
::v-deep .edit-schedule-wrapper {
  .periodicity-select {
    width: 207px !important;
  }
  .every-select {
    width: 120px !important;
  }
  .hour-select,
  .minute-select,
  .period-select {
    width: 100px !important;
  }
}
</style>
