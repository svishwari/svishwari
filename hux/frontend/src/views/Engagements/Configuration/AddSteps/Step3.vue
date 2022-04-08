<template>
  <div class="eng-step-3">
    <div class="black--text text-body-1">
      Set up a default delivery schedule
    </div>
    <div class="d-flex align-start">
      <v-col cols="6" class="pl-0">
        <div class="d-flex">
          <div
            class="cursor-pointer text-center rounded-lg manual py-5 px-5 mr-2"
            :class="[isActive ? 'active' : 'box-shadow-1']"
            @click="toggleClass($event)"
          >
            <icon
              type="manual"
              :color="isActive ? 'primary' : 'black'"
              :variant="isActive ? 'lighten6' : ''"
              :size="40"
            />
            <div
              class="mt-2 text-button"
              :class="isActive ? 'primary--text text--lighten-6' : ''"
            >
              Manual
            </div>
            <div class="pt-2 black--text text--lighten-4 text-body-2">
              Deliver this engagement when you are ready.
            </div>
          </div>
          <div
            class="
              cursor-pointer
              text-center
              rounded-lg
              recurring
              py-5
              px-5
              ml-2
            "
            :class="[!isActive ? 'active' : 'box-shadow-1']"
            @click="toggleClass($event)"
          >
            <icon
              type="recurring"
              :color="!isActive ? 'primary' : 'black'"
              :variant="!isActive ? 'lighten6' : ''"
              :size="40"
            />
            <div
              class="mt-2 text-button"
              :class="!isActive ? 'primary--text text--lighten-6' : ''"
            >
              Recurring
            </div>
            <div class="pt-2 black--text text--lighten-4 text-body-2">
              Deliver this engagement during a chosen timeframe.
            </div>
          </div>
        </div>
        <div v-if="!isActive" class="schedule-recurring mt-6 px-6 py-5">
          <div class="d-flex align-center">
            <div>
              <div class="text-body-2 pl-2 mb-n2">Start date</div>
              <hux-start-date
                :label="selectedStartDate"
                :selected="selectedStartDate"
                @on-date-select="onStartDateSelect"
              />
            </div>
            <div>
              <icon
                class="ml-2 mr-1 arrow-top-margin"
                type="arrow"
                :size="19"
                color="primary"
                variant="lighten6"
              />
            </div>
            <div>
              <div class="text-body-2 pl-2 mb-n2">End date</div>
              <hux-end-date
                :label="selectedEndDate"
                :selected="selectedEndDate"
                :is-sub-menu="true"
                :min-date="endMinDate"
                @on-date-select="onEndDateSelect"
              />
            </div>
          </div>
          <div class="mx-2 mt-2">
            <hux-schedule-picker
              v-model="value.delivery_schedule.schedule"
              short
              colon-sign
              :start-date="selectedStartDate"
              :end-date="selectedEndDate"
            />
          </div>
        </div>
      </v-col>
      <v-col cols="6" class="px-0">
        <audience-lists :value="value" />
      </v-col>
    </div>
  </div>
</template>

<script>
//Components
import Icon from "@/components/common/Icon"
import AudienceLists from "../AudienceLists"
import HuxStartDate from "@/components/common/DatePicker/HuxStartDate"
import HuxEndDate from "@/components/common/DatePicker/HuxEndDate"
import HuxSchedulePicker from "@/components/common/DatePicker/HuxSchedulePicker.vue"

export default {
  name: "Step3",

  components: {
    Icon,
    AudienceLists,
    HuxStartDate,
    HuxEndDate,
    HuxSchedulePicker,
  },

  props: {
    value: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      isActive: true,
      errorMessages: [],
      selectedStartDate: new Date(
        Date.now() - new Date().getTimezoneOffset() * 60000
      )
        .toISOString()
        .substr(0, 10),
      selectedEndDate: "No end date",
      endMinDate: new Date(
        new Date().getTime() - new Date().getTimezoneOffset() * 60000
      ).toISOString(),
    }
  },

  destroyed() {
    this.value.delivery_schedule.end_date = ""
    this.value.delivery_schedule.start_date = ""
  },

  methods: {
    toggleClass: function (event) {
      if (!event.currentTarget.classList.contains("active")) {
        this.isActive = !this.isActive
        this.$emit("isReccrActive", this.isActive)
      }
      if (this.isActive) {
        this.value.delivery_schedule.end_date = ""
        this.value.delivery_schedule.start_date = ""
      } else {
        this.value.delivery_schedule.start_date = new Date(
          Date.now() - new Date().getTimezoneOffset() * 60000
        )
          .toISOString()
          .substr(0, 10)
        this.selectedStartDate = this.value.delivery_schedule.start_date
        this.value.delivery_schedule.end_date = null
      }
    },

    onStartDateSelect(val) {
      this.selectedStartDate = val
      this.endMinDate = val
      this.value.delivery_schedule.start_date = val
    },

    onEndDateSelect(val) {
      if (!val) {
        this.selectedEndDate = "No end date"
        this.value.delivery_schedule.end_date = null
      } else {
        this.selectedEndDate = val
        this.value.delivery_schedule.end_date = val
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.eng-step-3 {
  margin-right: 16px;
  .d-flex {
    .manual,
    .recurring {
      height: 175px;
      width: 199px;
      border-radius: 12px;
    }
    .manual.active,
    .recurring.active {
      border: 1px solid var(--v-primary-lighten4);
    }
  }
  .schedule-recurring {
    background: var(--v-primary-lighten1);
    border: 1px solid var(--v-black-lighten2);
    border-radius: 5px;
    .arrow-top-margin {
      margin-top: 10px !important;
    }
    .hux-date-picker {
      ::v-deep .main-button {
        min-width: 153px !important;
        width: 153px !important;
      }
    }
    ::v-deep .edit-schedule-wrapper {
      .d-flex:nth-child(1) {
        @mixin dropdown-width($value) {
          .select-common {
            width: $value !important;
          }
        }
        .pr-2:nth-child(1) {
          @include dropdown-width(148px);
        }
        .pr-2:nth-child(2) {
          @include dropdown-width(106px);
        }
      }
    }
  }
}
</style>
