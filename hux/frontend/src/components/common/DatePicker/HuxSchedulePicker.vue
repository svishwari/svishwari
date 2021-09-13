<template>
  <div>
    <div class="edit-schedule-wrapper">
      <span class="pr-2">
        <div class="neroBlack--text text-caption">Repeat</div>
        <v-select
          v-model="value.periodicity"
          :items="repeatItems"
          :menu-props="menuProps"
          dense
          outlined
          background-color="white"
          class="select-common periodicity-select mt-1"
          append-icon="mdi-chevron-down"
        />
      </span>
      <span class="pr-2">
        <div class="neroBlack--text text-caption">Every</div>
        <v-select
          v-model="value.every"
          :items="everyItems"
          :menu-props="menuProps"
          dense
          outlined
          background-color="white"
          class="select-common every-select mt-1"
          append-icon="mdi-chevron-down"
        />
      </span>
      <span class="neroBlack--text text-h6 pt-3 pr-3">
        {{ timeFrame }}(s) at
      </span>
      <span class="pr-2">
        <v-select
          v-model="value.hour"
          :items="hourItems"
          :menu-props="menuProps"
          dense
          outlined
          background-color="white"
          class="select-common hour-select pt-5 mt-1"
          append-icon="mdi-chevron-down"
        />
      </span>
      <span class="pr-2">
        <v-select
          v-model="value.minute"
          :items="minItems"
          :menu-props="menuProps"
          dense
          outlined
          background-color="white"
          class="select-common minute-select pt-5 mt-1"
          append-icon="mdi-chevron-down"
        />
      </span>
      <span>
        <v-select
          v-model="value.period"
          :items="periodItems"
          :menu-props="menuProps"
          dense
          outlined
          background-color="white"
          class="select-common period-select pt-5 mt-1"
          append-icon="mdi-chevron-down"
        />
      </span>
    </div>

    <div v-if="value.periodicity === 'Weekly'" class="mt-6">
      <div class="text-caption black--text mb-1">On</div>
      <v-btn
        v-for="day in days"
        :key="day.value"
        min-width="30"
        width="30"
        height="30"
        min-height="30"
        class="day-button"
        :ripple="false"
        :color="isDaySelected(day) ? 'background' : 'aliceBlue'"
        @click="toggleWeekDay(day)"
      >
        <span
          class="text-h6"
          :class="isDaySelected(day) ? 'secondary--text' : 'gray--text'"
        >
          {{ day.day }}
        </span>
      </v-btn>
    </div>

    <div v-if="value.periodicity === 'Monthly'" class="mt-6">
      <div class="text-caption black--text mb-1">On</div>
      <div class="d-flex">
        <v-select
          v-model="value.monthlyPeriod"
          :items="monthlyPeriodItems"
          :menu-props="menuProps"
          dense
          outlined
          background-color="white"
          class="select-common monthly-period-select mr-2"
          append-icon="mdi-chevron-down"
        />
        <v-select
          v-if="value.monthlyPeriod !== 'Day'"
          v-model="value.monthlyDay"
          :items="monthlyDayItems"
          :menu-props="menuProps"
          dense
          outlined
          background-color="white"
          class="select-common monthly-day-select"
          append-icon="mdi-chevron-down"
        />
        <v-select
          v-else
          v-model="value.monthlyDayDate"
          :items="monthlyDayDateItems"
          :menu-props="menuProps"
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
        {{ value.every !== 1 ? value.every : "" }}
        {{ timeFrame }}{{ value.every !== 1 ? "s" : "" }}]
      </span>
      <span v-if="value.periodicity !== 'Daily'">on </span>
      <span v-if="value.periodicity === 'Weekly'" class="neroBlack--text">
        <span v-if="selectedDaysString !== '[]'">
          {{ selectedDaysString }}
        </span>
      </span>
      <span v-if="value.periodicity === 'Monthly'" class="neroBlack--text">
        <span v-if="value.monthlyPeriod === 'Day'">
          [Day {{ value.monthlyDayDate }}]
        </span>
        <span v-else>
          [the {{ value.monthlyPeriod }} {{ value.monthlyDay }}]
        </span>
      </span>
      starting at
      <span class="neroBlack--text">
        [{{ value.hour }}:{{ value.minute }}{{ value.period }}]
      </span>
    </div>

    <div
      v-if="
        value.periodicity === 'Monthly' &&
        value.monthlyPeriod === 'Day' &&
        value.monthlyDayDate === 31
      "
      class="gray--text pt-1"
    >
      Some months are fewer than 31 days, for these months the delivery will
      take place on the last day of the month.
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
      days: [
        {
          day: "S",
          value: "Sunday",
        },
        {
          day: "M",
          value: "Monday",
        },
        {
          day: "T",
          value: "Tuesday",
        },
        {
          day: "W",
          value: "Wednesday",
        },
        {
          day: "T",
          value: "Thursday",
        },
        {
          day: "F",
          value: "Friday",
        },
        {
          day: "S",
          value: "Saturday",
        },
      ],
      menuProps: {
        contentClass: "select-menu-class",
        offsetY: true,
        nudgeBottom: "4px",
      },
    }
  },
  computed: {
    everyItems() {
      return this.value.periodicity === "Daily"
        ? Array.from({ length: 7 }, (_, i) => i + 1)
        : this.value.periodicity === "Weekly"
        ? Array.from({ length: 4 }, (_, i) => i + 1)
        : Array.from({ length: 12 }, (_, i) => i + 1)
    },

    timeFrame() {
      return this.value.periodicity === "Daily"
        ? "day"
        : this.value.periodicity === "Weekly"
        ? "week"
        : "month"
    },

    selectedDays() {
      return this.days.filter((each) => this.isDaySelected(each))
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

  methods: {
    toggleWeekDay(day) {
      if (this.isDaySelected(day)) {
        if (this.value.days.length !== 1) {
          let index = this.value.days.indexOf(day.value)
          this.value.days.splice(index, 1)
        }
      } else {
        this.value.days.push(day.value)
      }
    },

    isDaySelected(day) {
      return this.value.days.includes(day.value)
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

.select-menu-class {
  .v-select-list {
    ::v-deep .v-list-item__title {
      font-size: 14px;
    }
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
