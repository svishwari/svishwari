<template>
  <drawer
    v-model="localToggle"
    :loading="loading"
    class="edit-delivery-drawer-wrapper rounded-0"
    @onClose="reset()"
  >
    <template #header-left>
      <div class="d-flex">
        <icon type="clock" :size="32" class="mr-2" />
        <h3 class="pl-1 text-h3 black--text text--darken-3">
          Edit delivery schedule
        </h3>
      </div>
    </template>

    <template #default>
      <div class="pt-2 pl-4 pr-3">
        <div class="text-h6 black--text text--darken-4">
          Override the default delivery schedule for this engagement and setup a
          scheduling pattern for this specific destination.
        </div>
        <div class="text-caption black--text text--darken-1 pt-8 pb-1">
          Destination
        </div>
        <card-horizontal
          :title="destination.name"
          :icon="destination.delivery_platform_type"
          class="cursor-default"
          hide-button
        />
        <div class="d-flex justify-end py-4 primary--text">
          <span class="cursor-pointer" @click="resetSchedule">
            Reset delivery to default
          </span>
        </div>
        <!-- <hux-schedule-picker v-model="localSchedule" /> -->
        <h5 class="text-h3 mb-2">Delivery schedule</h5>
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
      </div>
    </template>

    <template #footer-left>
      <hux-button
        size="large"
        variant="white"
        is-tile
        height="40"
        class="btn-border box-shadow-none"
        @click="reset()"
      >
        Cancel
      </hux-button>
    </template>

    <template #footer-right>
      <hux-button variant="primary" is-tile height="40" @click="onUpdate()">
        Update
      </hux-button>
    </template>
  </drawer>
</template>

<script>
import Drawer from "@/components/common/Drawer.vue"
import CardHorizontal from "@/components/common/CardHorizontal.vue"
import HuxButton from "@/components/common/huxButton.vue"
import HuxSchedulePicker from "@/components/common/DatePicker/HuxSchedulePicker.vue"
import { deliverySchedule } from "@/utils"
import Icon from "@/components/common/Icon.vue"
import { mapActions } from "vuex"

export default {
  name: "EditDeliverySchedule",

  components: {
    Drawer,
    CardHorizontal,
    HuxButton,
    HuxSchedulePicker,
    Icon,
  },

  props: {
    value: {
      type: Boolean,
      required: true,
    },

    audienceId: {
      type: [String, Number],
      required: false,
    },

    destination: {
      type: Object,
      required: false,
    },

    engagementId: {
      type: [String, Number],
      required: false,
    },

    schedule: {
      type: Object,
      required: false,
    },
  },

  data() {
    return {
      loading: false,
      localToggle: false,
      localSchedule: JSON.parse(JSON.stringify(deliverySchedule())),
      initialSchedule: JSON.parse(JSON.stringify(deliverySchedule())),
    }
  },

  computed: {
    scheduleConfig() {
      const recurringConfig = {}
      recurringConfig["every"] = this.localSchedule.every
      recurringConfig["periodicity"] = this.localSchedule.periodicity
      recurringConfig["hour"] = this.localSchedule.hour
      recurringConfig["minute"] = this.localSchedule.minute
      recurringConfig["period"] = this.localSchedule.period
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
      this.$emit("input", value)
    },

    schedule() {
      this.localSchedule = JSON.parse(
        JSON.stringify(deliverySchedule(this.schedule))
      )
      this.initialSchedule = JSON.parse(
        JSON.stringify(deliverySchedule(this.schedule))
      )
      console.log(this.localSchedule)
    },
  },

  methods: {
    ...mapActions({
      scheduleDelivery: "engagements/deliverySchedule",
    }),
    reset() {
      this.localToggle = false
      this.resetSchedule()
    },

    async onUpdate() {
      const requestPayload = {
        id: this.engagementId,
        audienceId:
          this.audienceId == null
            ? "000000000000000000000000"
            : this.audienceId,
        destinationId: this.destination.id,
        recurringConfig: this.scheduleConfig,
      }

      await this.scheduleDelivery(requestPayload)
      this.$emit("onUpdate")
      this.localToggle = false
    },

    resetSchedule() {
      this.localSchedule = JSON.parse(JSON.stringify(deliverySchedule(this.initialSchedule)))
    },
  },
}
</script>
