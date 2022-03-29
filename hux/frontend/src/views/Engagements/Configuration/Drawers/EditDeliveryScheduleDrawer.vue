<template>
  <drawer
    v-model="localToggle"
    :loading="loading"
    class="edit-delivery-drawer-wrapper rounded-0"
    @onClose="cancel()"
  >
    <template #header-left>
      <div class="d-flex align-center">
        <icon type="clock" :size="32" class="mr-2" />
        <h3 class="pl-1 text-h2 black--text">Edit delivery schedule</h3>
      </div>
    </template>

    <template #default>
      <div class="pt-5 pl-6">
        <div class="body-1 black--text mr-6">
          By editing this audience’s delivery schedule, the default delivery
          schedule will be replaced by your newly created schedule.
        </div>
        <div class="body-2 black--text text--lighten-4 pl-6 mt-6 mb-1">
          Audience
        </div>
        <card-horizontal
          :title="audienceName"
          class="cursor-default body-1 mr-6 pl-4"
          hide-button
        />
        <div class="d-flex justify-end pt-4 pb-6 mr-6 primary--text">
          <span class="cursor-pointer body-2" @click="resetSchedule">
            Reset delivery to default
          </span>
        </div>
        <h5 class="body-1 mb-2">Delivery schedule</h5>
        <div class="d-flex align-items-center">
          <plain-card
            v-for="(schedule, index) in ['Manual', 'Recurring']"
            :key="index"
            :icon="cardIcon(schedule, isRecurringFlag)"
            :title="schedule"
            :description="cardDescription[index]"
            :style="cardStyle(schedule, isRecurringFlag)"
            title-color="black--text"
            height="175"
            width="276"
            top-adjustment="mt-3"
            :class="cardClass(schedule, isRecurringFlag)"
            @onClick="changeSchedule(schedule)"
          />
        </div>
        <div
          v-if="isRecurringFlag"
          class="delivery-background px-4 pt-4 pb-6 mr-6"
        >
          <v-row class="delivery-schedule mt-6 ml-n2">
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
                class="mt-n4"
                :label="selectedStartDate"
                :selected="selectedStartDate"
                @on-date-select="onStartDateSelect"
              />
            </div>
            <icon
              class="mx-2"
              type="arrow"
              :size="19"
              color="primary"
              variant="lighten6"
            />
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
              short
              :start-date="selectedStartDate"
              :end-date="selectedEndDate"
            />
          </v-row>
        </div>
      </div>
    </template>

    <template #footer-left>
      <hux-button
        size="large"
        variant="white"
        is-tile
        height="40"
        class="btn-border box-shadow-25-light primary--text"
        @click="cancel()"
      >
        Cancel
      </hux-button>
    </template>

    <template #footer-right>
      <hux-button
        size="large"
        variant="primary"
        is-tile
        height="40"
        class="box-shadow-25-light"
        @click="onEditDeliverySchedule()"
      >
        Update &amp; save
      </hux-button>
    </template>
  </drawer>
</template>

<script>
import Drawer from "@/components/common/Drawer.vue"
import CardHorizontal from "@/components/common/CardHorizontal.vue"
import HuxButton from "@/components/common/huxButton.vue"
import PlainCard from "@/components/common/Cards/PlainCard.vue"
import HuxStartDate from "@/components/common/DatePicker/HuxStartDate"
import HuxEndDate from "@/components/common/DatePicker/HuxEndDate"
import HuxSchedulePicker from "@/components/common/DatePicker/HuxSchedulePicker.vue"
import { deliverySchedule, endMinDateGenerator } from "@/utils"
import Icon from "@/components/common/Icon.vue"
import { mapActions } from "vuex"

export default {
  name: "EditDeliverySchedule",

  components: {
    Drawer,
    CardHorizontal,
    HuxButton,
    PlainCard,
    HuxStartDate,
    HuxEndDate,
    HuxSchedulePicker,
    Icon,
  },

  props: {
    value: {
      type: Boolean,
      required: true,
    },

    audienceName: {
      type: String,
      required: false,
    },

    audienceId: {
      type: [String, Number],
      required: false,
    },

    currentSchedule: {
      type: Object,
      required: true,
    },

    engagementId: {
      type: [String, Number],
      required: false,
    },
  },

  data() {
    return {
      loading: false,
      localToggle: false,
      localSchedule: JSON.parse(
        JSON.stringify(deliverySchedule(this.currentSchedule.schedule))
      ),
      isRecurringFlag: false,
      selectedStartDate: "Select date",
      selectedEndDate: "Select date",
      disableEndDate: true,
      endMinDate: endMinDateGenerator(),
    }
  },

  computed: {
    cardDescription() {
      return [
        "Deliver this engagement when you are ready.",
        "Deliver this engagement during a chosen timeframe.",
      ]
    },

    scheduleConfig() {
      const recurringConfig = {
        every: this.localSchedule.every,
        periodicity: this.localSchedule.periodicity,
        hour: this.localSchedule.hour,
        minute: this.localSchedule.minute,
        period: this.localSchedule.period,
      }
      if (this.localSchedule) {
        switch (this.localSchedule.periodicity) {
          case "Weekly":
            recurringConfig["day_of_week"] = this.localSchedule.day_of_week
            break
          case "Monthly":
            recurringConfig["day_of_month"] = [
              this.localSchedule.monthlyDayDate,
            ]
            break
          default:
            recurringConfig
        }
      }
      return recurringConfig
    },
  },

  watch: {
    value(value) {
      this.localToggle = value
    },

    localToggle(value) {
      this.$emit("onToggle", value)
    },

    currentSchedule() {
      this.isRecurringFlag = Object.keys(this.currentSchedule).length > 0
      if (this.isRecurringFlag) {
        this.localSchedule = JSON.parse(
          JSON.stringify(deliverySchedule(this.currentSchedule.schedule))
        )
        this.selectedStartDate = new Date(
          this.currentSchedule.start_date,
          "YYYY-MM-DD"
        ).toISOString()
        this.selectedEndDate = new Date(
          this.currentSchedule.end_date,
          "YYYY-MM-DD"
        ).toISOString()
      }
    },
  },

  methods: {
    ...mapActions({
      deliveryScheduleAudience: "engagements/deliveryScheduleAudience",
    }),
    cardIcon(schedule, isRecurringFlag) {
      let colorIcon = ""
      if (
        (schedule == "Manual" && !isRecurringFlag) ||
        (schedule == "Recurring" && isRecurringFlag)
      ) {
        colorIcon = "-light"
      } else {
        colorIcon = "-dark"
      }
      return schedule.charAt(0).toLowerCase() + schedule.slice(1) + colorIcon
    },

    cardStyle(schedule, isRecurringFlag) {
      return (schedule == "Manual" && !isRecurringFlag) ||
        (schedule == "Recurring" && isRecurringFlag)
        ? { float: "left", color: "var(--v-primary-lighten6)" }
        : { float: "left", color: "var(--v-black-base)" }
    },

    cardClass(schedule, isRecurringFlag) {
      return (schedule == "Manual" && !isRecurringFlag) ||
        (schedule == "Recurring" && isRecurringFlag)
        ? "border-card mb-11"
        : "model-desc-card mr-0 mb-11"
    },

    changeSchedule(val) {
      this.isRecurringFlag = val == "Recurring"
      if (this.value.delivery_schedule) {
        this.selectedStartDate = "Select date"
        this.selectedEndDate = "Select date"
        this.disableEndDate = true
        this.endMinDate = endMinDateGenerator()
      }
    },

    cancel() {
      this.$emit("onToggle", false)
      this.localToggle = false
    },

    async onEditDeliverySchedule() {
      const requestPayload = {
        schedule: this.scheduleConfig,
        start_date:
          this.selectedStartDate == "Select date"
            ? new Date().toISOString()
            : new Date(this.selectedStartDate).toISOString(),
        end_date:
          this.selectedEndDate == "Select date" ||
          this.selectedEndDate == "No end date"
            ? null
            : new Date(this.selectedEndDate).toISOString(),
      }
      await this.deliveryScheduleAudience({
        engagementId: this.engagementId,
        audienceId: this.audienceId,
        data: requestPayload,
      })
      this.$emit("onToggle", false)
      this.localToggle = false
    },

    async resetSchedule() {
      await this.deliveryScheduleAudience({
        engagementId: this.engagementId,
        audienceId: this.audienceId,
        data: {},
      })
      this.$emit("onToggle", false)
      this.localToggle = false
    },

    onStartDateSelect(val) {
      this.selectedStartDate = val
      this.endMinDate = val
    },

    onEndDateSelect(val) {
      if (!val) {
        this.selectedEndDate = "No end date"
      } else {
        this.selectedEndDate = val
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.edit-delivery-drawer-wrapper {
  .border-card {
    border: solid 1px var(--v-primary-lighten6);
  }
  .delivery-background {
    border: solid 1px var(--v-black-lighten2);
    background: var(--v-primary-lighten1);
    position: relative;
    bottom: 25px;
    border-radius: 5px;
  }
  .delivery-schedule {
    margin-left: auto;
    ::v-deep .edit-schedule-wrapper {
      .d-flex:nth-child(1) {
        .pr-2:nth-child(1) {
          .select-common {
            width: 207px !important;
            margin-right: 16px !important;
          }
        }
        .pr-2:nth-child(2) {
          .select-common {
            width: 120px !important;
          }
        }
      }
      .d-flex:nth-child(2) {
        .select-common {
          width: 100px !important;
        }
        .pr-2:nth-child(1) {
          .select-common {
            width: 120px !important;
            margin-right: 4px !important;
            &::after {
              content: ":" !important;
              margin-top: 8px !important;
              margin-left: 16px !important;
            }
          }
        }
        .pr-2:nth-child(2) {
          margin-right: 10px !important;
        }
      }
    }
  }
  .date-picker-label {
    position: absolute;
    margin-top: -30px;
    margin-left: 8px;
  }
}
</style>
