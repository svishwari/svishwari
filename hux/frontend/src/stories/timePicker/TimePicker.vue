<template>
  <div class="d-flex justify-start">
    <v-menu v-model="menu" :close-on-content-click="false" offset-y>
      <template v-slot:activator="{ on, attrs }">
        <div
          class="d-flex align-items-center py-1 px-2 time-picker-button"
          :class="{ 'menu-active': menu }"
          v-bind="attrs"
          v-on="on"
        >
          <span class="new-b1 mr-2">
            {{ selectedTime }}
          </span>
          <icon type="Time" size="24" color="black-base" />
        </div>
      </template>
      <v-card
        class="time-picker-content d-flex flex-column new-b4 box-shadow-15-8"
      >
        <v-row class="justify-center">Hours</v-row>
        <v-row>
          <button
            v-for="(h, index) in Hours"
            :key="index"
            class="col-2"
            :class="{ 'selected-time-option': h == Hour }"
            @click="selectTimeType('hour', h)"
          >
            {{ h }}
          </button>
        </v-row>
        <v-row class="justify-center">Minutes</v-row>
        <v-row>
          <button
            v-for="(min, index) in Minutes"
            :key="index"
            class="col-2"
            :class="{ 'selected-time-option': min == Minute }"
            @click="selectTimeType('minute', min)"
          >
            {{ min }}
          </button>
        </v-row>
      </v-card>
    </v-menu>
    <v-menu v-model="menu2" :close-on-content-click="true" offset-y>
      <template v-slot:activator="{ on, attrs }">
        <div
          class="d-flex align-items-center py-1 px-2 time-picker-button-2 ml-2"
          :class="{ 'menu-active': menu2 }"
          v-bind="attrs"
          v-on="on"
        >
          <span class="new-b1 mr-2"> {{ selectedZone }} </span>
          <icon type="Dropdown - down" size="24" color="black-base" />
        </div>
      </template>
      <v-card
        class="time-picker-content-2 d-flex flex-column new-b1 box-shadow-15-8"
      >
        <v-row v-for="(selection, index) in Zones" :key="index">
          <button
            class="d-flex align-items-center"
            @click="selectTimeType('zone', selection)"
          >
            <icon
              v-if="showCheckMark && selection == selectedZone"
              type="Checkmark"
              size="24"
              color="primary-base"
              class="mr-2"
            />
            <icon
              v-if="icon"
              :type="icon"
              size="24"
              color="black-base"
              class="mr-2"
            />
            <span :class="{ 'selected-time-2': selection == selectedZone }">
              {{ selection }}
            </span>
          </button>
        </v-row>
      </v-card>
    </v-menu>
  </div>
</template>
<script>
import Icon from "../icons/Icon2.vue"
export default {
  name: "TimePicker",
  components: {
    Icon,
  },
  props: {
    hour: {
      type: String,
      required: false,
      default: "01",
    },
    minute: {
      type: String,
      required: false,
      default: "00",
    },
    zone: {
      type: String,
      required: false,
      default: "AM",
    },
    icon: {
      type: String,
      required: false,
      default: "",
    },
    showCheckMark: {
      type: Boolean,
      required: false,
      default: true,
    },
  },
  data: () => ({
    menu: false,
    Hours: [
      "01",
      "02",
      "03",
      "04",
      "05",
      "06",
      "07",
      "08",
      "09",
      "10",
      "11",
      "12",
    ],
    Minutes: [
      "00",
      "05",
      "10",
      "15",
      "20",
      "25",
      "30",
      "35",
      "40",
      "45",
      "50",
      "55",
    ],
    Zones: ["AM", "PM"],
    Hour: "01",
    Minute: "00",
    selectedZone: "AM",
  }),
  computed: {
    selectedTime() {
      return `${this.Hour}:${this.Minute}`
    },
  },
  watch: {
    hour() {
      this.Hour = this.hour
    },
    minute() {
      this.Minute = this.minute
    },
    zone() {
      this.selectedZone = this.zone
    },
  },
  methods: {
    selectTimeType(type, value) {
      switch (type) {
        case "hour":
          this.hour = value
          break

        case "minute":
          this.minute = value
          break

        default:
          // am or pm
          this.selectedZone = value
      }
    },
  },
}
</script>
<style lang="scss" scoped>
.time-picker-button {
  width: 92px;
  height: 32px;
  background-color: var(--v-white-base);
  border-radius: 5px;
  border: 1px solid var(--v-black-lighten1);
  color: var(--v-black-lighten6) !important;
  &.menu-active {
    border: 1px solid var(--v-black-base);
    color: var(--v-black-base) !important;
  }
}
.time-picker-button-2 {
  @extend .time-picker-button;
  width: 74px;
}
.time-picker-content {
  width: 248px !important;
  ::v-deep .row {
    margin: 8px 0px 0px 0px !important;
    color: var(--v-black-lighten6) !important;
    .col-2 {
      @extend .new-b4;
      height: 24px !important;
      width: 24px !important;
      max-width: 24px !important;
      margin: 8px !important;
      padding: 0px !important;
      &.selected-time-option {
        border-radius: 50% !important;
        background-color: var(--v-primary-base) !important;
        color: var(--v-white-base) !important;
      }
    }
    &:nth-child(1) {
      margin: 8px 0px 0px 0px !important;
    }
    &:nth-child(2) {
      margin: 0px 4px !important;
      color: var(--v-black-base) !important;
    }
    &:nth-child(3) {
      margin: 0px !important;
      padding: 8px 0px 0px 0px !important;
      box-shadow: inset 0px 1px 0px #e2eaec;
    }
    &:nth-child(4) {
      margin: 0px 4px !important;
      color: var(--v-black-base) !important;
    }
  }
}
.time-picker-content-2 {
  ::v-deep .row {
    height: 40px !important;
    margin: 0px !important;
    padding: 8px 16px !important;
    button {
      width: 100% !important;
      .selected-time-2 {
        color: var(--v-primary-base) !important;
      }
    }
  }
}
</style>
