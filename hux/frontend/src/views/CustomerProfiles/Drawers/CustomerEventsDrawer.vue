<template>
  <drawer v-model="localDrawer" content-padding="pa-0">
    <template #header-left>
      <h3 class="text-h2">Events</h3>
    </template>
    <template #footer-left>
      <div class="d-flex align-baseline">
        <div class="body-2 pl-4">{{ events.length }} results</div>
      </div>
    </template>

    <template #default>
      <div class="header-break"></div>
      <v-progress-linear :active="loading" :indeterminate="loading" />
      <hux-data-table
        :columns="tableColumns"
        :data-items="events"
        row-height="60px"
        class="notifications-table small-table"
        sort-column="date"
        sort-desc
      >
        <template #row-item="{ item }">
          <td
            v-for="header in tableColumns"
            :key="header.value"
            class="text-body-1 py-2 mw-100 text-truncate"
            data-e2e="customerEventRow"
          >
            <template
              v-if="header.value == 'event_type'"
              class="d-flex align-center"
            >
              <icon
                :type="item[header.value]"
                color="primary"
                :size="24"
                class="mr-1"
              />
              <span class="position-event-center">
                {{ event_underscore_remove(item[header.value]) }}
              </span>
            </template>
            <template v-if="header.value == 'date'">
              {{ item[header.value] | Date("MM/DD/YYYY") }}
            </template>
          </td>
        </template>
      </hux-data-table>
    </template>
  </drawer>
</template>

<script>
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import Drawer from "@/components/common/Drawer.vue"
import Icon from "@/components/common/Icon.vue"
import { capitalize, split, join } from "lodash"

export default {
  name: "CustomerEventsDrawer",

  components: {
    HuxDataTable,
    Drawer,
    Icon,
  },

  props: {
    events: {
      type: Object,
      required: true,
    },
    value: {
      type: Boolean,
      required: true,
      default: false,
    },
  },

  data() {
    return {
      localDrawer: this.value,
      loading: false,
      items: [],
      tableColumns: [
        {
          text: "Event",
          value: "event_type",
          width: "350px",
        },
        {
          text: "Event date",
          value: "date",
          width: "200px",
        },
      ],
    }
  },

  watch: {
    value: function () {
      this.localDrawer = this.value
    },
    localDrawer: function () {
      this.$emit("input", this.localDrawer)
    },
  },

  methods: {
    event_underscore_remove(str) {
      return join(split(capitalize(str), "_"), " ")
    },
  },
}
</script>
<style lang="scss" scoped>
.hux-data-table {
  ::v-deep .v-data-table__wrapper {
    .v-data-table-header {
      th {
        &:first-child {
          padding: 9px 10px 9px 25px !important;
        }
        padding: 9px 10px !important;
        &:last-child {
          padding: 9px 20px 9px 10px !important;
        }
      }
    }
    tbody {
      tr {
        td {
          &:first-child {
            padding: 3px 10px 0px 25px !important;
          }
          padding: 3px 10px !important;
          &:last-child {
            padding: 3px 20px 0px 10px !important;
          }
        }
      }
    }
  }
}
.header-break {
  border-bottom: 1px solid var(--v-black-lighten2) !important;
}
.position-event-center {
  position: relative;
  bottom: 5px;
}

::v-deep .v-toolbar__title {
  padding-left: 10px !important;
}
</style>
