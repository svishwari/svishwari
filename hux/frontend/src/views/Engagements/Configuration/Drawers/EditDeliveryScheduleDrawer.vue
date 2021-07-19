<template>
  <Drawer v-model="localToggle" :loading="loading" class="rounded-0">
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

        <div class="edit-schedule-wrapper">
          <span class="pr-2">
            <span class="neroBlack--text text-caption">Repeat</span>
            <v-select
              v-model="schedule.periodicity"
              :items="repeatItems"
              dense
              outlined
              background-color="white"
              class="select-common"
              append-icon="mdi-chevron-down"
            />
          </span>
          <span class="pr-2">
            <span class="neroBlack--text text-caption">Every</span>
            <v-select
              v-model="schedule.every"
              :items="everyItems"
              dense
              outlined
              background-color="white"
              class="select-common"
              append-icon="mdi-chevron-down"
            />
          </span>
          <span class="neroBlack--text text-h6 pt-3 pr-4">
            {{ timeFrame }}(s) at
          </span>
          <span class="pr-2">
            <v-select
              v-model="schedule.hour"
              :items="hourItems"
              dense
              outlined
              background-color="white"
              class="select-common"
              append-icon="mdi-chevron-down"
            />
          </span>
          <span class="pr-2">
            <v-select
              v-model="schedule.hour"
              :items="minItems"
              dense
              outlined
              background-color="white"
              class="select-common"
              append-icon="mdi-chevron-down"
            />
          </span>
          <span>
            <v-select
              v-model="schedule.period"
              :items="periodItems"
              dense
              outlined
              background-color="white"
              class="select-common"
              append-icon="mdi-chevron-down"
            />
          </span>
        </div>
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

export default {
  name: "EditDeliverySchedule",

  components: {
    Drawer,
    CardHorizontal,
    HuxButton,
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
      repeatItems: ["Daily", "Weekly", "Monthly"],
      hourItems: Array.from({ length: 12 }, (_, i) => i + 1),
      minItems: Array.from({ length: 4 }, (_, i) => i + 15),
      periodItems: ["AM","PM"],
      schedule: {
        periodicity: "Daily",
        every: 1,
        hour: 12,
        minute: 15,
        period: "AM",
      },
    }
  },

  computed: {
    everyItems() {
      return this.schedule.periodicity === "Daily"
        ? Array.from({ length: 7 }, (_, i) => i + 1)
        : this.schedule.periodicity === "Weekly"
        ? Array.from({ length: 4 }, (_, i) => i + 1)
        : Array.from({ length: 12 }, (_, i) => i + 1)
    },

    timeFrame() {
      return this.schedule.periodicity === "Daily"
        ? "day"
        : this.schedule.periodicity === "Weekly"
        ? "week"
        : "month"
    },
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
<style lang="scss" scoped>
.edit-schedule-wrapper {
  display: flex;
  align-items: center;
  ::v-deep .select-common {
    .v-input__control {
      .v-input__slot {
        min-height: 40px;
        fieldset {
          color: var(--v-lightGrey-base) !important;
          border-width: 1px !important;
        }
        input::placeholder {
          color: var(--v-lightGrey-base) !important;
        }
      }
      .v-text-field__details {
        display: none;
      }
    }
  }
}
</style>
