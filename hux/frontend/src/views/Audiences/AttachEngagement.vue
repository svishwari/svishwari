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
              <empty-page>
                <template #icon>mdi-alert-circle-outline</template>
                <template #title>Oops! There’s nothing here yet</template>
                <template #subtitle>
                  No engagements have been created yet. Let’s create one by
                  clicking the new engagement button below.
                </template>
                <template #button>
                  <huxButton
                    variant="primary base"
                    icon-color="white"
                    icon-variant="base"
                    icon="plus"
                    size="small"
                    is-custom-icon
                    class="ma-2 caption"
                    is-tile
                    @click="goToStep2()"
                  >
                    New engagement
                  </huxButton>
                </template>
              </empty-page>
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
            <div class="new-engament-wrap">
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
                      <v-icon color="primary" :size="12" class="ml-1" v-on="on">
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
                <div class="d-flex flex-column delivery-options">
                  <v-btn-toggle
                    v-model="newEngagement.delivery_schedule"
                    mandatory
                  >
                    <v-btn
                      class="active-delivery-option"
                      :class="
                        newEngagement.delivery_schedule == 0
                          ? 'btn-radio-active'
                          : 'btn-radio-inactive'
                      "
                      height="40"
                      width="175"
                      @click="resetSchedule()"
                    >
                      <v-radio
                        :off-icon="
                          newEngagement.delivery_schedule == 0
                            ? '$radioOn'
                            : '$radioOff'
                        "
                      />
                      <v-icon class="ico primary--text" size="16">
                        mdi-gesture-tap
                      </v-icon>
                      Manual
                    </v-btn>
                    <v-btn
                      class="active-delivery-option"
                      :class="
                        isRecurring ? 'btn-radio-active' : 'btn-radio-inactive'
                      "
                      height="40"
                      width="175"
                    >
                      <v-radio
                        :off-icon="isRecurring ? '$radioOn' : '$radioOff'"
                      />
                      <v-icon class="ico primary--text" size="16">
                        mdi-clock-check-outline
                      </v-icon>
                      Recurring
                    </v-btn>
                  </v-btn-toggle>
                </div>
                <v-row v-if="isRecurring" class="delivery-schedule ml-0 mt-6">
                  <div>
                    <span
                      class="
                        date-picker-label
                        black--text
                        text--darken-4 text-caption
                      "
                    >
                      Start date
                    </span>
                    <hux-start-date
                      class=""
                      :label="selectedStartDate"
                      :selected="selectedStartDate"
                      @on-date-select="onStartDateSelect"
                    />
                  </div>
                  <icon class="ml-1 mt-9 mr-2" type="arrow" :size="28" />
                  <div>
                    <span
                      class="
                        date-picker-label
                        black--text
                        text--darken-4 text-caption
                      "
                    >
                      End date
                    </span>
                    <hux-end-date
                      class=""
                      :label="selectedEndDate"
                      :selected="selectedEndDate"
                      :is-sub-menu="true"
                      :min-date="endMinDate"
                      @on-date-select="(val) => (selectedEndDate = val)"
                    />
                  </div>
                </v-row>
                <v-row v-if="isRecurring" class="delivery-schedule ml-0 mt-6">
                  <hux-schedule-picker v-model="schedule" />
                </v-row>
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
          variant="white"
          :is-tile="true"
          height="40"
          width="146"
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
      selectedStartDate: "Select date",
      selectedEndDate: "Select date",
      schedule: JSON.parse(JSON.stringify(deliverySchedule())),
      endMinDate: new Date(
        new Date().getTime() - new Date().getTimezoneOffset() * 60000
      ).toISOString(),
    }
  },

  computed: {
    areEngagementAlreadyCreated() {
      return this.engagements.length > 0
    },
    isRecurring() {
      return this.newEngagement.delivery_schedule == 1
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
        delivery_schedule: this.newEngagement.delivery_schedule,
        audiences: [],
        start_date: this.selectedStartDate,
        end_date: this.selectedEndDate,
      }
      if (this.newEngagement.description) {
        payload["description"] = this.newEngagement.description
      }
      const newEngagement = await this.addEngagementToDB(payload)
      this.engagements.push(newEngagement)
      this.engagements = this.engagements.sort((a, b) => {
        return new Date(b.update_time) - new Date(a.update_time)
      })
      this.showSortIcon = false
      this.onEngagementClick(newEngagement)
      if (this.closeOnAction) {
        this.$emit("onAddEngagement", newEngagement)
        this.loading = false
        this.localDrawer = false
      } else {
        this.goToStep1()
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
</style>
