<template>
  <div class="hux-date-picker">
    <v-menu
      ref="menu"
      v-model="menu"
      :close-on-content-click="false"
      :return-value.sync="start"
      :offset-x="isOffsetX"
      :offset-y="isOffsetY"
      :open-on-hover="isOpenOnHover"
      :transition="transition"
    >
      <template #activator="{ on }">
        <huxButton
          :v-on="on"
          text
          width="200"
          icon=" mdi-chevron-down"
          icon-position="right"
          tile
          class="ma-2 main-button pr-1"
          @click="menu = true"
        >
          {{ optionSelected["name"] || label }}
        </huxButton>
      </template>
      <v-list v-if="endDate">
        <v-list-item>
          <v-list-item-title> No end date </v-list-item-title>
        </v-list-item>
        <v-list-item @click="showCalendar = true">
          <v-list-item-title> Select date </v-list-item-title>
          <div class="flex-grow-1"></div>
          <v-icon color="primary">mdi-chevron-right</v-icon>
        </v-list-item>
      </v-list>
      <v-list v-if="!endDate">
        <v-date-picker
          v-model="start"
          class="start-date-picker"
          :min="todaysDate"
          no-title
          scrollable
        >
          <div class="date-picker-header" style="">
            <span class="header-label"> Date </span>
            <span class="header-value">
              {{ start || label }}
            </span>
          </div>
          <v-spacer></v-spacer>
          <huxButton
            size="large"
            variant="white"
            is-tile
            class="btn-cancel ml-4 btn-border box-shadow-none"
            @click="menu = false"
          >
            Cancel
          </huxButton>
          <huxButton
            variant="white"
            is-tile
            class="btn-select mr-4"
            @click="
              $refs.menu.save(start)
              selectDate(start)
            "
          >
            <span class="primary--text"> Select </span>
          </huxButton>
        </v-date-picker>
      </v-list>
    </v-menu>
  </div>
</template>
<script>
import huxButton from "@/components/common/huxButton"
export default {
  name: "HuxStartDate",
  components: {
    huxButton,
  },
  props: {
    selected: {
      type: [Object, String],
    },
    label: {
      type: String,
      required: false,
      default: "Select Option",
    },
    isOffsetX: { type: Boolean, default: false },
    isOffsetY: { type: Boolean, default: true },
    isOpenOnHover: { type: Boolean, default: false },
    transition: { type: String, default: "scale-transition" },
  },
  data: function () {
    return {
      endDate: false,
      menu: false,
      showCalendar: false,
      start: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
        .toISOString()
        .substr(0, 10),
      end: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
        .toISOString()
        .substr(0, 10),
      todaysDate: new Date(
        new Date().getTime() - new Date().getTimezoneOffset() * 60000
      ).toISOString(),
    }
  },
  computed: {
    optionSelected() {
      return this.selected || this.label
    },
  },
  methods: {
    selectDate(data) {
      this.$emit("on-date-select", data)
    },
  },
}
</script>

<style lang="scss" scoped>
.hux-date-picker {
  .main-button {
    min-width: 64px;
    padding: 0 16px;
    border-style: solid !important;
    border-width: 1px;
    border-color: var(--v-black-lighten3) !important;
    box-shadow: none !important;
    background-color: var(--v-white-base) !important;
    background: var(--v-white-base) !important;
    font-size: 14px;
    line-height: 22px;
    min-width: 215px;
    color: var(--v-black-darken4);
    width: 215px !important;
    height: 42px;
    border: 1px solid var(--v-black-lighten3) !important;
    border-radius: 4px;
    ::v-deep .v-btn__content {
      .spacer {
        &:nth-child(2) {
          display: none;
        }
      }
      .v-icon {
        color: var(--v-primary-base);
      }
    }
  }
}
.start-date-picker {
  ::v-deep .v-picker__body {
    margin-top: 20px;
    border-bottom: 1px solid var(--v-black-lighten3);
    .v-date-picker-table {
      table {
        border-collapse: collapse;
        thead {
          border-bottom: 1px solid var(--v-black-lighten3);
        }
      }
      .v-btn--active {
        background-color: rgba(0, 124, 176, 0.2) !important;
        .v-btn__content {
          color: var(--v-black-darken4) !important;
        }
      }
    }
  }
  ::v-deep .v-card__actions {
    display: flow-root !important;
    height: 40px;
    .btn-select {
      float: right;
    }
    .v-btn {
      height: 24px;
      margin-top: 3px;
    }
  }
  ::v-deep .date-picker-header {
    position: absolute;
    margin-top: -315px;
    padding: 4px 20px;
    width: 94%;
    background-color: var(--v-primary-lighten2) !important;
    .header-value {
      margin-left: 48px;
      color: var(--v-primary-base) !important;
    }
  }
}
</style>
