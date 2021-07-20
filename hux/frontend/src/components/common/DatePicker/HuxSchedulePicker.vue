<template>
  <div>
    <div class="edit-schedule-wrapper">
      <span class="pr-2">
        <span class="neroBlack--text text-caption">Repeat</span>
        <v-select
          v-model="schedule.periodicity"
          @input="$emit('input', schedule)"
          :items="repeatItems"
          dense
          outlined
          background-color="white"
          class="select-common periodicity-select"
          append-icon="mdi-chevron-down"
        />
      </span>
      <span class="pr-2">
        <span class="neroBlack--text text-caption">Every</span>
        <v-select
          v-model="schedule.every"
          @input="$emit('input', schedule)"
          :items="everyItems"
          dense
          outlined
          background-color="white"
          class="select-common every-select"
          append-icon="mdi-chevron-down"
        />
      </span>
      <span class="neroBlack--text text-h6 pt-3 pr-4">
        {{ timeFrame }}(s) at
      </span>
      <span class="pr-2">
        <v-select
          v-model="schedule.hour"
          @input="$emit('input', schedule)"
          :items="hourItems"
          dense
          outlined
          background-color="white"
          class="select-common hour-select pt-5"
          append-icon="mdi-chevron-down"
        />
      </span>
      <span class="pr-2">
        <v-select
          v-model="schedule.minute"
          @input="$emit('input', schedule)"
          :items="minItems"
          dense
          outlined
          background-color="white"
          class="select-common minute-select pt-5"
          append-icon="mdi-chevron-down"
        />
      </span>
      <span>
        <v-select
          v-model="schedule.period"
          @input="$emit('input', schedule)"
          :items="periodItems"
          dense
          outlined
          background-color="white"
          class="select-common period-select pt-5"
          append-icon="mdi-chevron-down"
        />
      </span>
    </div>

    <div v-if="schedule.periodicity === 'Weekly'" class="mt-6">
      <div class="text-caption black--text mb-1">On</div>
      <v-btn
        v-for="day in schedule.days"
        :key="day.value"
        min-width="30"
        width="30"
        height="30"
        min-height="30"
        class="day-button"
        :ripple="false"
        @click="day.selected = !day.selected"
        :color="day.selected ? 'background' : 'aliceBlue'"
      >
        <span
          class="text-h6"
          :class="day.selected ? 'secondary--text' : 'gray--text'"
        >
          {{ day.day }}
        </span>
      </v-btn>
    </div>

    <div v-if="schedule.periodicity === 'Monthly'" class="mt-6">
      <div class="text-caption black--text mb-1">On</div>
      <div class="d-flex">
        <v-select
          v-model="schedule.monthlyPeriod"
          @input="$emit('input', schedule)"
          :items="monthlyPeriodItems"
          dense
          outlined
          background-color="white"
          class="select-common monthly-period-select mr-2"
          append-icon="mdi-chevron-down"
        />
        <v-select
          v-if="schedule.monthlyPeriod !== 'Day'"
          v-model="schedule.monthlyDay"
          @input="$emit('input', schedule)"
          :items="monthlyDayItems"
          dense
          outlined
          background-color="white"
          class="select-common monthly-day-select"
          append-icon="mdi-chevron-down"
        />
        <v-select
          v-else
          v-model="schedule.monthlyDayDate"
          @input="$emit('input', schedule)"
          :items="monthlyDayDateItems"
          dense
          outlined
          background-color="white"
          class="select-common monthly-day-select"
          append-icon="mdi-chevron-down"
        />
      </div>
    </div>

    <div class="gray--text pt-4">
      Delivery takes place
      <span class="neroBlack--text">
        [every
        {{ schedule.every !== 1 ? schedule.every : "" }}
        {{ timeFrame }}{{ schedule.every !== 1 ? "s" : "" }}]
      </span>
      <span v-if="schedule.periodicity !== 'Daily'">on </span>
      <span class="neroBlack--text" v-if="schedule.periodicity === 'Weekly'">
        <span v-if="selectedDaysString !== '[]'">
          {{ selectedDaysString }}
        </span>
      </span>
      <span class="neroBlack--text" v-if="schedule.periodicity === 'Monthly'">
        <span v-if="schedule.monthlyPeriod === 'Day'">
          [Day {{ schedule.monthlyDayDate }}]
        </span>
        <span v-else>
          [the {{ schedule.monthlyPeriod }} {{ schedule.monthlyDay }}]
        </span>
      </span>
      starting at
      <span class="neroBlack--text">
        [{{ schedule.hour }}:{{ schedule.minute }}{{ schedule.period }}]
      </span>
    </div>
  </div>
</template>
<script>
export default {
  name: "HuxSchedulePicker",

  props: {
    value: {
      type: Object,
      required: false,
    },
  },

  data() {
    return {
      repeatItems: ["Daily", "Weekly", "Monthly"],
      hourItems: Array.from({ length: 12 }, (_, i) => i + 1),
      minItems: ["00", 15, 30, 45],
      periodItems: ["AM", "PM"],
      monthlyPeriodItems: ["Day", "First", "Second", "Third", "Fourth", "Last"],
      monthlyDayItems: [
        "Day",
        "Weekend",
        "Weekend day",
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
      ],
      monthlyDayDateItems: Array.from({ length: 31 }, (_, i) => i + 1),
      schedule: {
        periodicity: "Daily",
        every: 1,
        hour: 12,
        minute: 15,
        period: "AM",
        monthlyPeriod: "Day",
        monthlyDay: "Day",
        monthlyDayDate: 1,
        days: [
          {
            day: "S",
            value: "Sunday",
            selected: false,
          },
          {
            day: "M",
            value: "Monday",
            selected: true,
          },
          {
            day: "T",
            value: "Tuesday",
            selected: false,
          },
          {
            day: "W",
            value: "Wednesday",
            selected: false,
          },
          {
            day: "T",
            value: "Thursday",
            selected: false,
          },
          {
            day: "F",
            value: "Friday",
            selected: false,
          },
          {
            day: "S",
            value: "Saturday",
            selected: false,
          },
        ],
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

    selectedDays() {
      return this.schedule.days.filter((each) => each.selected)
    },

    selectedDaysString() {
      let string = "["
      this.selectedDays.map((day, index) => {
        string += day.value
        if (this.selectedDays.length - 1 !== index) {
          string += " and "
        }
      })
      string += "]"
      return string
    },
  },
}
</script>
<style lang="scss" scoped>
.edit-schedule-wrapper {
  display: flex;
  align-items: center;

  ::v-deep .periodicity-select {
    width: 130px;
  }

  ::v-deep .every-select {
    width: 74px;
  }

  ::v-deep .hour-select {
    width: 74px;
  }

  ::v-deep .minute-select {
    width: 74px;
  }

  ::v-deep .period-select {
    width: 78px;
  }
}

::v-deep .monthly-period-select {
  max-width: 154px;
}

::v-deep .monthly-day-select {
  max-width: 154px;
}

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
.day-button {
  border-radius: 2px;
  margin-right: 2px;
  @extend .no-shadow;
}
</style>
