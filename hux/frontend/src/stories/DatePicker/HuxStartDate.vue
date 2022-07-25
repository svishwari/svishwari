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
          class="ma-2 main-button new-b1 pr-1"
          @click="menu = true"
        >
          {{ selected | Date("MM/DD/YYYY") | Empty(label) }}
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
          class="start-date-picker mb-4"
          :min="todaysDate"
          no-title
          scrollable
        >
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
  methods: {
    selectDate(data) {
      //this.$emit("on-date-select", data)
      this.selected = data
    },
  },
}
</script>

<style lang="scss" scoped>
.hux-date-picker {
  .main-button {
    min-width: 64px;
    padding: 0 16px;
    border-color: var(--v-black-lighten1) !important;
    box-shadow: none !important;
    background-color: var(--v-white-base) !important;
    min-width: 215px;
    color: var(--v-black-lighten6) !important;
    width: 215px !important;
    height: 42px;
    border: 1px solid var(--v-black-lighten1) !important;
    border-radius: 5px;
    &:hover {
      border-color: var(--v-black-lighten8) !important;
    }
    &:active {
      border-color: var(--v-black-base) !important;
      color: var(--v-black-base) !important;
    }
    ::v-deep .v-btn__content {
      .spacer {
        &:nth-child(2) {
          display: none;
        }
      }
      .v-icon {
        color: var(--v-black-base);
      }
    }
  }
}
.start-date-picker {
  ::v-deep .v-picker__body {
    border-bottom: 1px solid var(--v-black-lighten3);
    .v-date-picker-table {
      table {
        border-collapse: collapse;
        thead {
          tr {
            th {
              @extend .new-b4;
              color: var(--v-black-base);
            }
          }
        }
        tbody {
          tr {
            td {
              @extend .new-b4;
              color: var(--v-black-base);
              .v-btn.v-btn--disabled {
                color: var(--v-black-lighten5) !important;
              }
              .v-btn.v-btn--text.v-btn--rounded:hover {
                width: 24px;
                height: 24px;
                background-color: var(--v-black-lighten7) !important;
              }
              .v-btn.v-date-picker-table__current.v-btn--rounded.v-btn--outlined {
                width: 24px;
                height: 24px;
                border: 1px solid var(--v-primary-lighten6);
                color: var(--v-black-base) !important;
              }
            }
          }
        }
      }
      .v-btn--active {
        width: 24px;
        height: 24px;
        background-color: var(--v-primary-base) !important;
        .v-btn__content {
          color: var(--v-white-base) !important;
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
  ::v-deep .v-date-picker-header {
    @extend .new-b4;
    .v-btn.v-btn--icon {
      color: var(--v-black-base);
      &.v-btn--disabled {
        .v-btn__content {
          color: var(--v-black-lighten3) !important;
        }
      }
    }
    .v-date-picker-header__value {
      height: 40px;
      > div {
        height: 100%;
        > button {
          @extend .new-b4;
          padding: 10px 16px;
          &:hover {
            background: var(--v-black-lighten7) !important;
            color: var(--v-black-lighten6) !important;
          }
          &:active {
            color: var(--v-primary-base) !important;
          }
        }
      }
    }
  }
}
</style>
