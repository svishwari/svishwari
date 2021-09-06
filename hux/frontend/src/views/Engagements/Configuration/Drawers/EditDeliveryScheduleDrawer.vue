<template>
  <drawer
    v-model="localToggle"
    :loading="loading"
    class="edit-delivery-drawer-wrapper rounded-0"
    @onClose="reset()"
  >
    <template #header-left>
      <div class="d-flex">
        <v-icon color="primary" size="27">mdi-clock-time-five-outline</v-icon>
        <h3 class="pl-1 text-h3 black--text text--darken-3">Edit delivery schedule</h3>
      </div>
    </template>

    <template #default>
      <div class="pt-2 pl-4 pr-3">
        <div class="text-h6 black--text text--darken-4">
          Override the default delivery schedule for this engagement and setup a
          scheduling pattern for this specific destination.
        </div>
        <div class="text-caption black--text text--darken-1 pt-8 pb-1">Destination</div>
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
        <hux-schedule-picker v-model="schedule" />
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

export default {
  name: "EditDeliverySchedule",

  components: {
    Drawer,
    CardHorizontal,
    HuxButton,
    HuxSchedulePicker,
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
  },

  data() {
    return {
      loading: false,
      localToggle: false,
      schedule: JSON.parse(JSON.stringify(deliverySchedule())),
    }
  },

  watch: {
    value(value) {
      this.localToggle = value
    },

    localToggle(value) {
      this.$emit("input", value)
    },
  },

  methods: {
    reset() {
      this.localToggle = false
      this.resetSchedule()
    },

    onUpdate() {
      this.$emit("onUpdate")
    },

    resetSchedule() {
      this.schedule = JSON.parse(JSON.stringify(deliverySchedule()))
    },
  },
}
</script>
