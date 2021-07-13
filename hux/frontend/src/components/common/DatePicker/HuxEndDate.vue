<template>
  <div class="hux-date-picker">
    <v-menu
      ref="endmenu"
      :close-on-content-click="false"
      :offset-x="isOffsetX"
      :offset-y="isOffsetY"
      :open-on-hover="isOpenOnHover"
      :transition="transition"
      close-on-click
      v-model="endmenu"
    >
      <template #activator="{ on }">
        <v-list-item
          v-if="!isSubMenu"
          class="d-flex justify-space-between pr-1"
          v-on="on"
        >
          Select date
          <div class="flex-grow-1"></div>
          <v-icon color="primary">mdi-chevron-right</v-icon>
        </v-list-item>
        <huxButton
          v-else
          :v-on="on"
          @click="endmenu = true"
          text
          width="200"
          icon=" mdi-chevron-down"
          iconPosition="right"
          tile
          class="ma-2 main-button pr-1"
        >
          {{ selected }}
        </huxButton>
      </template>
      <v-list>
        <template>
          <div class="dropdown-menuitems">
            <v-list-item @click="onCancel()" v-if="isSubMenu">
              <v-list-item-title class="d-flex align-center">
                No end date
              </v-list-item-title>
            </v-list-item>
            <hux-end-date
              :is-offset-x="true"
              :is-offset-y="false"
              :isSubMenu="false"
              @on-date-select="(val) => $emit('on-date-select', val)"
              v-if="isSubMenu"
            />
            <v-list-item v-if="!isSubMenu">
              <v-list-item-title class="d-flex align-center">
                <v-date-picker
                  class="end-date-picker"
                  v-model="end"
                  no-title
                  scrollable
                >
                  <div class="date-picker-header" style="">
                    <span class="header-label"> Date </span>
                    <span class="header-value"> {{ end }} </span>
                  </div>
                  <v-spacer></v-spacer>
                  <huxButton
                    variant="tertiary"
                    isTile
                    class="btn-cancel ml-4"
                    @click="onCancel()"
                  >
                    Cancel
                  </huxButton>
                  <huxButton
                    variant="tertiary"
                    isTile
                    class="btn-select mr-4"
                    @click="
                      $refs.endmenu.save(end)
                      selectDate(end)
                    "
                  >
                    <span class="primary--text"> Select </span>
                  </huxButton>
                </v-date-picker>
              </v-list-item-title>
            </v-list-item>
          </div>
        </template>
      </v-list>
    </v-menu>
  </div>
</template>
<script>
import huxButton from "@/components/common/huxButton"
export default {
  name: "hux-end-date",
  components: {
    huxButton,
  },
  computed: {},
  props: {
    selected: {
      type: [Object, String],
    },
    label: {
      type: String,
      required: false,
      default: "Select date",
    },
    isOffsetX: { type: Boolean, default: false },
    isOffsetY: { type: Boolean, default: true },
    isOpenOnHover: { type: Boolean, default: false },
    isSubMenu: { type: Boolean, default: false },
    transition: { type: String, default: "scale-transition" },
  },
  methods: {
    onCancel() {
      this.endmenu = false
      this.showCalendar = false
      this.$refs.endmenu.$parent.$el.parentNode.children[0].click()
    },
    selectDate(data) {
      this.$emit("on-date-select", data)
      this.$refs.endmenu.$parent.$el.parentNode.children[0].click()
    },
  },
  data: function () {
    return {
      endmenu: this.value,
      end: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
        .toISOString()
        .substr(0, 10),
    }
  },
}
</script>

<style lang="scss" scoped>
.hux-date-picker {
  .main-button {
    height: 32px;
    min-width: 64px;
    padding: 0 16px;
    border-style: solid !important;
    border-width: 1px;
    border-color: var(--v-lightGrey-base) !important;
    border-radius: 0;
    box-shadow: none !important;
    background-color: var(--v-white-base) !important;
    background: var(--v-white-base) !important;
    font-size: 14px;
    line-height: 22px;
    width: auto !important;
    min-width: 200px;
    color: var(--v-neroBlack-base);
    width: 215px !important;
    height: 42px;
    border: 1px solid var(--v-lightGrey-base) !important;
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
.dropdown-menuitems {
  min-width: 230px;
  font-size: 14px;
  line-height: 22px !important;
  color: var(--v-neroBlack-base);
  .v-list-item {
    min-height: 32px;
    .v-list-item__title {
      line-height: 22px !important;
    }
  }
  .group_title {
    text-transform: uppercase;
    color: var(--v-gray-base);
  }
}
.end-date-picker {
  ::v-deep .v-picker__body {
    margin-top: 30px;
    border-bottom: 1px solid var(--v-lightGrey-base);
    .v-date-picker-table {
      table {
        border-collapse: collapse;
        thead {
          border-bottom: 1px solid var(--v-lightGrey-base);
        }
      }
      .v-btn--active {
        background-color: rgba(0, 124, 176, 0.2) !important;
        .v-btn__content {
          color: var(--v-neroBlack-base) !important;
        }
      }
    }
  }
  ::v-deep .v-card__actions {
    display: flow-root !important;
    .btn-select {
      float: right;
    }
  }
  ::v-deep .date-picker-header {
    position: absolute;
    margin-top: -315px;
    padding: 4px 20px;
    width: 94%;
    background-color: var(--v-aliceBlue-base) !important;
    .header-value {
      margin-left: 12px;
      color: var(--v-primary-base) !important;
    }
  }
}
</style>