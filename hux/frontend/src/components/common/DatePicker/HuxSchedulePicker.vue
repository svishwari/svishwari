<template>
  <div>
    <div
      class="edit-schedule-wrapper"
      :class="short ? '' : 'd-flex align-center'"
    >
      <div class="d-flex align-center">
        <span class="pr-2">
          <span class="black--text text--darken-4 text-body-2">Repeat</span>
          <v-select
            v-model="value.periodicity"
            :items="repeatItems"
            :menu-props="menuProps"
            dense
            outlined
            background-color="white"
            class="select-common periodicity-select"
            append-icon="mdi-chevron-down"
          />
        </span>
        <span class="pr-2">
          <span class="black--text text--darken-4 text-body-2">Every</span>
          <v-select
            v-model="value.every"
            :items="everyItems"
            :menu-props="menuProps"
            dense
            outlined
            background-color="white"
            class="select-common every-select"
            append-icon="mdi-chevron-down"
          />
        </span>
        <span class="black--text text--darken-4 body-1 pt-3 pr-3">
          {{ timeFrame }}(s) at
        </span>
      </div>
      <div class="d-flex align-center">
        <span class="pr-2">
          <v-select
            v-model="value.hour"
            :items="hourItems"
            :menu-props="menuProps"
            dense
            outlined
            background-color="white"
            :class="dropdownPadding('hour-select')"
            append-icon="mdi-chevron-down"
          />
        </span>
        <span
          v-if="colonSign"
          class="black--text text--darken-4 body-1 ml-1 mr-2"
          >:</span
        >
        <span class="pr-2">
          <v-select
            v-model="minute"
            :items="minItems"
            :menu-props="menuProps"
            dense
            outlined
            background-color="white"
            :class="dropdownPadding('minute-select')"
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
            :class="dropdownPadding('period-select')"
            append-icon="mdi-chevron-down"
          />
        </span>
      </div>
    </div>

    <div v-if="value.periodicity === 'Weekly'" class="weekly-buttons mt-3">
      <div class="text-body-2 black--text mb-1">On</div>
      <v-btn
        v-for="day in day_of_week"
        :key="day.value"
        min-width="30"
        width="30"
        height="30"
        min-height="30"
        class="day-button"
        :class="
          isDaySelected(day) ? 'day-button-selected primary lighten-1' : 'white'
        "
        :ripple="false"
        @click="toggleWeekDay(day)"
      >
        <span
          class="body-1"
          :class="
            isDaySelected(day)
              ? 'primary--text text--lighten-6'
              : 'black--text text--lighten-4'
          "
        >
          {{ day.day }}
        </span>
      </v-btn>
    </div>

    <div v-if="value.periodicity === 'Monthly'" class="mt-3">
      <div class="text-body-2 black--text mb-1">On</div>
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
        <hux-drop-down-search
          v-if="value.monthlyPeriod !== 'Day'"
          v-model="value.monthlyDay"
          :toggle-drop-down="toggleDropDown"
          :min-selection="1"
          :items="monthlyDayItems"
          :is-search-enabled="false"
          items-as-array
          :name="monthlyDayLabel"
        >
          <template #activator>
            <div class="mr-2">
              <v-select
                dense
                readonly
                :placeholder="monthlyDayLabel"
                class="dropdown-select-placeholder"
                outlined
                background-color="white"
                append-icon="mdi-chevron-down"
              />
            </div>
          </template>
        </hux-drop-down-search>
        <hux-drop-down-search
          v-else
          v-model="value.monthlyDayDate"
          :toggle-drop-down="toggleDropDown"
          :min-selection="1"
          :items="monthlyDayDateItems"
          :is-search-enabled="false"
          items-as-array
          :name="monthlyDayDateLabel"
        >
          <template #activator>
            <div class="mr-2">
              <v-select
                dense
                readonly
                :placeholder="monthlyDayDateLabel"
                class="dropdown-select-placeholder"
                outlined
                background-color="white"
                append-icon="mdi-chevron-down"
              />
            </div>
          </template>
        </hux-drop-down-search>
      </div>
    </div>

    <hux-delivery-text
      :schedule="value"
      :start-date="startDate"
      :end-date="endDate"
      class="pt-3 text-body-1"
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
import HuxDropDownSearch from "@/components/common/HuxDropDownSearch"

export default {
  name: "HuxSchedulePicker",

  components: {
    HuxDeliveryText,
    HuxDropDownSearch,
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
    short: {
      type: Boolean,
      default: false,
    },
    colonSign: {
      type: Boolean,
      default: false,
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
      toggleDropDown: false,
    }
  },
  computed: {
    monthlyDayLabel() {
      return `Day (${this.value.monthlyDay.length})`
    },
    monthlyDayDateLabel() {
      return `Day (${this.value.monthlyDayDate.length})`
    },
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
          this.value && this.value.monthlyDayDate.length
            ? this.value.monthlyDayDate
            : [1]
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
    dropdownPadding(widthClass) {
      return this.short
        ? `select-common mt-1 ${widthClass}`
        : `pt-5 select-common mt-1 ${widthClass}`
    },
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
    padding: 0px !important;
    ::v-deep .v-list-item {
      min-height: 32px !important;
      .v-list-item__content {
        padding: 5px 0px !important ;
        .v-list-item__title {
          font-style: normal !important;
          font-weight: 400 !important;
          font-size: 16px !important;
          line-height: 22px !important;
        }
      }
    }
  }
}

::v-deep .monthly-period-select {
  max-width: 115px;
}

::v-deep .monthly-day-select {
  max-width: 66px;
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
.weekly-buttons {
  .day-button {
    padding: 0;
    border-radius: 2px;
    margin-right: 2px;
    @extend .no-shadow;
  }
  .day-button-selected {
    border: 1px solid var(--v-primary-lighten6) !important;
  }
}

::v-deep .dropdown-select-placeholder {
  max-width: 110px !important;
  .v-input__control {
    .v-input__slot {
      fieldset {
        border-color: var(--v-black-lighten3);
      }
      input::placeholder {
        color: var(--v-black-base);
      }
    }
    .v-text-field__details {
      display: none;
    }
  }
}
</style>
