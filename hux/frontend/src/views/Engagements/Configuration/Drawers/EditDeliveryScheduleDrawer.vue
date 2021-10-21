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
        <hux-schedule-picker v-model="localSchedule" />
      </div>
    </template>

    <template #footer-left>
      <hux-button variant="white" is-tile height="40" @click="reset()">
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
    }
  },

  computed: {
    scheduleConfig() {
      const recurringConfig = {}
      recurringConfig["every"] = this.localSchedule.every
      recurringConfig["periodicity"] = this.localSchedule.periodicity
      if (this.localSchedule) {
        switch (this.localSchedule.periodicity) {
          case "Daily":
            recurringConfig["hour"] = this.localSchedule.hour
            recurringConfig["minute"] = this.localSchedule.minute
            recurringConfig["period"] = this.localSchedule.period
          case "Weekly":
            recurringConfig["day_of_week"] = this.localSchedule.day_of_week
          case "Monthly":
            recurringConfig["day_of_month"] = this.localSchedule.monthlyDayDate
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
        audienceId: this.audienceId,
        destinationId: this.destination.id,
        recurringConfig: this.scheduleConfig,
      }

      this.$emit("onUpdate")
      await this.scheduleDelivery(requestPayload)
      this.localToggle = false
    },

    resetSchedule() {
      this.localSchedule = JSON.parse(JSON.stringify(deliverySchedule()))
    },
  },
}
</script>
