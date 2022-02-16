<template>
  <v-card class="overview-card mt-6 pt-5 pb-6 pl-6 pr-6 box-shadow-5">
    <v-card-title class="d-flex justify-space-between pa-0 pr-2">
      <h3 class="text-h3 mb-2">Sending domains overview</h3>
    </v-card-title>
    <hux-data-table
      class="overview-table mt-4"
      :columns="columnDefs"
      :sort-desc="true"
      :data-items="list"
    >
      <template #row-item="{ item }">
        <td
          v-for="header in columnDefs"
          :key="header.value"
          class="text-body-2"
          :style="{ width: header.width }"
          data-e2e="map-state-list"
        >
          <div v-if="header.value == 'domain_name'" class="text-body-1">
            <span class="text-ellipsis mb-n1">
              {{ item.domain_name }}
            </span>
          </div>
          <div v-if="header.value == 'sent'" class="text-body-1">
            <span class="text-ellipsis mb-n1">
              {{ item.sent | Numeric }}
            </span>
          </div>
          <div v-if="header.value == 'bounce_rate'" class="text-body-1">
            <span class="text-ellipsis mb-n1">
              {{ item.bounce_rate | Percentage }}
            </span>
          </div>
          <div v-if="header.value == 'open_rate'" class="text-body-1">
            <span class="text-ellipsis mb-n1">
              {{ item.open_rate | Percentage }}
            </span>
          </div>
          <div v-if="header.value == 'click_rate'" class="text-body-1">
            <span class="text-ellipsis mb-n1">
              {{ item.click_rate | Percentage }}
            </span>
          </div>
          <div v-if="header.value == 'size'" class="text-body-1"></div>
          <div
            v-if="header.value == 'last_delivered'"
            class="text-body-1"
          ></div>
        </td>
      </template>
    </hux-data-table>
  </v-card>
</template>

<script>
import HuxDataTable from "../../../../components/common/dataTable/HuxDataTable.vue"
export default {
  name: "DomainOverview",
  components: { HuxDataTable },
  props: {
    list: {
      type: Array,
      required: true,
      default: () => [],
    },
  },
  data() {
    return {
      columnDefs: [
        {
          text: "Domains",
          value: "domain_name",
          width: "30%",
        },
        {
          text: "Sent",
          value: "sent",
          width: "17.5%",
        },
        {
          text: "Bounce rate",
          value: "bounce_rate",
          width: "17.5%",
        },
        {
          text: "Open rate",
          value: "open_rate",
          width: "17.5%",
        },
        {
          text: "Click rate",
          value: "click_rate",
          width: "17.5%",
        },
      ],
    }
  },
}
</script>

<style lang="scss" scoped>
.overview-table {
  ::v-deep .v-data-table {
    .v-data-table-header {
      tr {
        height: 32px !important;
      }
      th {
        background: var(--v-primary-lighten2);
        box-shadow: none;
      }
    }
  }
  ::v-deep .v-data-table .v-data-table-header th:first-child {
    border-top-left-radius: 12px !important;
  }
  ::v-deep .v-data-table .v-data-table-header th:last-child {
    border-top-right-radius: 12px !important;
  }
}
</style>
