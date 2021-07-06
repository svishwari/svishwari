<template>
  <div class="hux-date-picker">
    <v-menu
      ref="menu"
      :close-on-content-click="false"
      :return-value.sync="end"
      :offset-x="isOffsetX"
      :offset-y="isOffsetY"
      :open-on-hover="isOpenOnHover"
      :transition="transition"
      v-model="menu">
      <template #activator="{ on }">
        <huxButton
          :v-on="on"
          @click="menu = true"
          text
          width="200"
          icon=" mdi-chevron-down"
          iconPosition="right"
          tile
          class="ma-2 main-button pr-1">
          {{ optionSelected["name"] || label }}
        </huxButton>
      </template>
      <v-list>
        <v-list-item v-if="endDate">
          <v-list-item-title> No end date </v-list-item-title>
        </v-list-item>
        <v-list-item v-if="endDate" @click="showCalendar = true">
          <v-list-item-title> Select date </v-list-item-title>
        </v-list-item>
        <v-date-picker
          class="start-date-picker"
          v-model="start"
          no-title
          scrollable
          v-if="!endDate">
          <v-spacer></v-spacer>
          <huxButton variant="tertiary" isTile class="btn-cancel ml-4" @click="menu = false">
            Cancel
          </huxButton>
          <huxButton variant="tertiary" isTile class="btn-select mr-4"  @click="$refs.menu.save(start);selectDate(start)">
            <span class="primary--text">
              Select
            </span>
          </huxButton>
        </v-date-picker>
      </v-list>
    </v-menu>
    <v-date-picker
      class="end-date-picker"
      v-model="end"
      no-title
      scrollable
      v-if="showCalendar">
      <v-spacer></v-spacer>
      <huxButton variant="tertiary" isTile class="btn-cancel ml-4" @click="menu = false; showCalendar =false">
        Cancel
      </huxButton>
      <huxButton variant="tertiary" isTile class="btn-select mr-4"  @click="$refs.menu.save(end);selectDate(end)">
        <span class="primary--text">
          Select
        </span>
      </huxButton>
    </v-date-picker>
  </div>
</template>
<script>
import huxButton from "@/components/common/huxButton"
import Icon from "../Icon.vue"
export default {
  name: "hux-date-picker",
  components: {
    huxButton,
    Icon,
  },
  computed: {
    optionSelected() {
      return this.selected || this.label
    },
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
    items: Array,
    isOffsetX: { type: Boolean, default: false },
    isOffsetY: { type: Boolean, default: true },
    isOpenOnHover: { type: Boolean, default: false },
    endDate: { type: Boolean, default: false },
    transition: { type: String, default: "scale-transition" },
  },
  methods: {
    onSelect(item) {
      this.$emit("on-select", item)
      // this.menu = false
    },
    onMenuToggle(opened) {
      // if (!opened) {
      //   this.showCalendar = false
      // }
    },
    selectDate(data) {
      this.label = data
    },
  },
  data: function () {
    return {
      menu: this.value,
      menu: false,
      showCalendar: false,
      start: new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
        .toISOString()
        .substr(0, 10),
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
.start-date-picker, .end-date-picker {
  ::v-deep .v-picker__body {
    border-bottom: 1px solid var(--v-lightGrey-base);
    .v-date-picker-table{
      table {
        border-collapse: collapse;
        thead {
          border-bottom: 1px solid var(--v-lightGrey-base);
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
}
</style>
