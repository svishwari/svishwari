<template>
  <Drawer
    v-model="localToggle"
    :loading="loading"
    class="edit-delivery-drawer-wrapper rounded-0"
  >
    <template #header-left>
      <div class="d-flex">
        <v-icon color="primary" size="27">mdi-clock-time-five-outline</v-icon>
        <h3 class="pl-1 text-h3 darkGrey--text">Edit delivery schedule</h3>
      </div>
    </template>

    <template #default>
      <div class="pt-2 pl-4 pr-3">
        <div class="text-h6 neroBlack--text">
          Override the default delivery schedule for this engagement and setup a
          scheduling pattern for this specific destination.
        </div>
        <div class="text-caption gray--text pt-8 pb-1">Destination</div>
        <CardHorizontal
          :title="destination.name"
          :icon="destination.type"
          hideButton
        />
        <div class="d-flex justify-end py-4 primary--text cursor-pointer">
          Reset delivery to default
        </div>
        <hux-schedule-picker v-model="schedule" />
      </div>
    </template>

    <template #footer-left>
      <HuxButton variant="white" isTile height="40" @click="reset()">
        Cancel
      </HuxButton>
    </template>

    <template #footer-right>
      <HuxButton variant="primary" isTile height="40" @click="onUpdate()">
        Update
      </HuxButton>
    </template>
  </Drawer>
</template>

<script>
import Drawer from "@/components/common/Drawer.vue"
import CardHorizontal from "@/components/common/CardHorizontal.vue"
import HuxButton from "@/components/common/huxButton.vue"
import HuxSchedulePicker from "@/components/common/DatePicker/HuxSchedulePicker.vue"

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
      type: String,
      required: false,
    },

    destination: {
      type: Object,
      required: false,
    },

    engagementId: {
      type: String,
      required: false,
    },
  },

  data() {
    return {
      loading: false,
      localToggle: false,
      schedule: null,
    }
  },

  methods: {
    reset() {
      this.localToggle = false
    },

    onUpdate() {
      this.$emit("onUpdate")
    },
  },

  watch: {
    value(value) {
      this.localToggle = value
    },

    localToggle(value) {
      this.$emit("input", value)
    },
  },
}
</script>
