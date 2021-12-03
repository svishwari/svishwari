<template>
  <div>
    <div class="edit-schedule-wrapper">
      <span class="pr-2">
        <span class="black--text text--darken-4 text-caption">Repeat</span>
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
        <span class="black--text text--darken-4 text-caption">Every</span>
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
      <span class="black--text text--darken-4 text-h6 pt-3 pr-3">
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
          v-model="minute"
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
        v-for="day in day_of_week"
        :key="day.value"
        min-width="30"
        width="30"
        height="30"
        min-height="30"
        class="day-button"
        :ripple="false"
        :color="isDaySelected(day) ? 'primary lighten-1' : 'primary lighten-2'"
        @click="toggleWeekDay(day)"
      >
        <span
          class="text-h6"
          :class="
            isDaySelected(day)
              ? 'primary--text text--lighten-8'
              : 'black--text text--darken-1'
          "
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
          v-model="monthlyDayDate"
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

    <hux-delivery-text
      :schedule="value"
      :start-date="startDate"
      :end-date="endDate"
      class="pt-4"
    />

    <div
      v-if="
        value.periodicity === 'Monthly' &&
        value.monthlyPeriod === 'Day' &&
        value.monthlyDayDate === 31
      "
      class="black--text text--darken-1 pt-1"
    >
      Some months are fewer than 31 days, for these months the delivery will
      take place on the last day of the month.
    </div>
  </div>
</template>
<script>
import { dayAbbreviation } from "@/utils"
import HuxDeliveryText from "@/components/common/DatePicker/HuxDeliveryText"

export default {
  name: "HuxSchedulePicker",

  components: {
    HuxDeliveryText,
  },

  props: {
    value: {
      type: Object,
      required: false,
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
      day_of_week: [
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
    monthlyDayDate: {
      get() {
        return parseInt(
          this.value && this.value.day_of_month ? this.value.day_of_month[0] : 1
        )
      },
      set(value) {
        this.value.monthlyDayDate = value
      },
    },
    minute: {
      get() {
        if (this.value && this.value.minute === 0) return "00"
        return this.value.minute
      },
      set(value) {
        this.value.minute = value
      },
    },

    timeFrame() {
      return this.value.periodicity === "Daily"
        ? "day"
        : this.value.periodicity === "Weekly"
        ? "week"
        : "month"
    },

    selectedDays() {
      return this.day_of_week.filter((each) => this.isDaySelected(each))
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
        if (this.value.day_of_week.length !== 1) {
          let index = this.value.day_of_week.indexOf(dayAbbreviation(day.value))
          this.value.day_of_week.splice(index, 1)
        }
      } else {
        this.value.day_of_week.push(dayAbbreviation(day.value))
      }
    },

    isDaySelected(day) {
      return this.value.day_of_week.includes(dayAbbreviation(day.value))
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
    width: 75px;
  }

  ::v-deep .hour-select {
    width: 75px;
  }

  ::v-deep .minute-select {
    width: 75px;
  }

  ::v-deep .period-select {
    width: 81px;
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
        color: var(--v-black-lighten3) !important;
        border-width: 1px !important;
      }
      input::placeholder {
        color: var(--v-black-lighten3) !important;
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
