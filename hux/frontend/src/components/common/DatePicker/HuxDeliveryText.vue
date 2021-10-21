<template>
  <div class="black--text text-body-2">
    <span v-if="deliveryType"> Delivery takes place </span>
    <span v-if="deliveryType">every</span>
    <span v-else>Every</span>
    {{ schedule.every !== 1 ? schedule.every : "" }}
    {{ timeFrame }}{{ schedule.every !== 1 ? "s" : "" }}
    <span v-if="schedule.periodicity !== 'Daily'">on </span>
    <span v-if="schedule.periodicity === 'Weekly'">
      <span v-if="selectedDaysString !== ''">
        {{ selectedDaysString }}
      </span>
    </span>
    <span v-if="schedule.periodicity === 'Monthly'">
      <span v-if="schedule.monthlyPeriod === 'Day'">
        Day {{ schedule.monthlyDayDate }}
      </span>
      <span v-else>
        the {{ schedule.monthlyPeriod }} {{ schedule.monthlyDay }}
      </span>
    </span>
    starting at
    <span>{{ schedule.hour }}:{{ schedule.minute }}{{ schedule.period }}</span>
    <span v-if="deliveryType && startDate && startDate !== 'Select date'">
      <span> between {{ startDate | Date("MMMM D, YYYY") }} and</span>
      <span
        v-if="endDate && endDate !== 'Select date' && endDate !== 'No end date'"
      >
        {{ endDate | Date("MMMM D, YYYY") }}
      </span>
      <span v-else> No end</span>
    </span>
    <span>.</span>
  </div>
</template>

<script>
import { abbrDayToFullName } from "@/utils"
export default {
  name: "HuxDeliveryText",

  props: {
    schedule: {
      type: Object,
      required: true,
    },
    type: {
      type: String,
      required: false,
      default: "engagement",
    },
    startDate: {
      type: String,
      required: false,
    },
    endDate: {
      type: String,
      required: false,
    },
  },

  computed: {
    deliveryType() {
      return this.type === "engagement"
    },
    timeFrame() {
      return this.schedule.periodicity === "Daily"
        ? "day"
        : this.schedule.periodicity === "Weekly"
        ? "week"
        : "month"
    },

    selectedDaysString() {
      let string = ""
      this.schedule.day_of_week.forEach((day, index) => {
        if (index === 0) {
          string += " " + abbrDayToFullName(day)
        } else {
          string += " and " + abbrDayToFullName(day)
        }
      })
      string += ""
      return string
    },
  },
}
</script>
