<template>
  <v-card class="rounded-lg card-style standalone-delivery mt-4" flat>
    <v-card-title class="d-flex justify-space-between pb-2 pl-6 pt-6">
      <div class="d-flex align-center">
        <span class="text-h3">Standalone deliveries</span>
        <tooltip :max-width="396" position-top>
          <template #label-content>
            <icon
              type="info"
              :size="8"
              class="ml-1 mb-1"
              color="primary"
              variant="base"
            />
          </template>
          <template #hover-content>
            These are deliveries that are not part of an engagement.
          </template>
        </tooltip>
      </div>
      <v-spacer> </v-spacer>
      <div
        :class="{
          'black--text text--lighten-3 disabled':
            audience.standalone_deliveries &&
            audience.standalone_deliveries.length == 0,
          'primary--text':
            audience.standalone_deliveries &&
            audience.standalone_deliveries.length > 0,
        }"
        class="d-flex mr-4 cursor-pointer deliver-icon text-body-1"
        @click="deliverAll()"
      >
        <icon
          class="mr-2"
          :type="
            audience.standalone_deliveries.length == 0 ? 'deliver' : 'deliver_2'
          "
          :size="24"
          :color="
            audience.standalone_deliveries.length == 0 ? 'black' : 'primary'
          "
          :variant="
            audience.standalone_deliveries.length == 0 ? 'lighten3' : 'base'
          "
        />
        Deliver all
      </div>
    </v-card-title>
    <v-card-text class="pl-6 pr-6 pb-6 pt-3">
      <div
        v-if="
          audience &&
          audience.standalone_deliveries &&
          audience.standalone_deliveries.length > 0
        "
      >
        <hux-data-table
          class="delivery-table"
          :columns="columnDefs"
          :sort-desc="true"
          :data-items="audience.standalone_deliveries"
        >
          <template #row-item="{ item }">
            <td
              v-for="header in columnDefs"
              :key="header.value"
              class="text-body-2"
              :style="{ width: header.width }"
              data-e2e="map-state-list"
            >
              <div
                v-if="header.value == 'delivery_platform_name'"
                class="text-body-1"
              >
                <logo
                  :type="item.delivery_platform_type"
                  :size="22"
                  class="mb-n1"
                >
                </logo>
                <span class="ml-2 text-ellipsis mb-n1">
                  {{ item.delivery_platform_name }}
                </span>
                <span class="action-icon font-weight-light float-right d-none">
                  <v-menu class="menu-wrapper" bottom offset-y>
                    <template #activator="{ on, attrs }">
                      <v-icon
                        v-bind="attrs"
                        class="top-action"
                        color="primary"
                        v-on="on"
                      >
                        mdi-dots-vertical
                      </v-icon>
                    </template>
                    <v-list class="menu-list-wrapper">
                      <v-list-item-group>
                        <v-list-item
                          v-for="option in destinationMenuOptions"
                          :key="option.id"
                          :disabled="!option.active"
                          @click="standaloneOptions(option)"
                        >
                          <v-list-item-title v-if="!option.menu">
                            {{ option.title }}
                          </v-list-item-title>
                        </v-list-item>
                      </v-list-item-group>
                    </v-list>
                  </v-menu>
                </span>
              </div>
              <div v-if="header.value == 'status'" class="text-body-1">
                <status
                  :status="item['status']"
                  :show-label="true"
                  class="d-flex"
                  :icon-size="17"
                />
              </div>
              <div v-if="header.value == 'size'" class="text-body-1">
                <size :value="item['size']" />
              </div>
              <div v-if="header.value == 'last_delivered'" class="text-body-1">
                <time-stamp :value="item['last_delivered']" />
              </div>
            </td>
          </template>
        </hux-data-table>

        <v-list dense class="add-list list-border" :height="52">
          <v-list-item @click="$emit('onAddStandaloneDestination', audience)">
            <tooltip>
              <template #label-content>
                <hux-icon
                  type="plus"
                  :size="16"
                  color="primary"
                  class="mr-4 mb-1"
                />
                <hux-icon
                  type="destination"
                  :size="24"
                  color="primary"
                  class="mr-2"
                />
              </template>
              <template #hover-content>
                <div class="py-2 white d-flex flex-column">
                  <span> Add a destination to this engagement </span>
                </div>
              </template>
            </tooltip>
            <v-btn
              text
              min-width="7rem"
              height="2rem"
              class="primary--text text-body-1"
            >
              Destination
            </v-btn>
          </v-list-item>
        </v-list>
      </div>

      <div v-else class="empty-state black--text text--lighten-4 text-body-1">
        <div class="mb-1">
          This audience has no standalone deliveries. Add a destination below.
        </div>
        <v-list dense class="add-list" :height="52">
          <v-list-item
            class="px-0"
            @click="$emit('onAddStandaloneDestination', audience)"
          >
            <hux-icon type="plus" :size="16" color="primary" class="mr-3" />
            <hux-icon
              type="destination"
              :size="24"
              color="primary"
              class="mr-1"
            />
            <v-btn
              text
              min-width="7rem"
              height="2rem"
              class="primary--text text-body-1"
            >
              Destination
            </v-btn>
          </v-list-item>
        </v-list>
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import TimeStamp from "@/components/common/huxTable/TimeStamp.vue"
import Size from "@/components/common/huxTable/Size.vue"
import Status from "@/components/common/Status.vue"
import Icon from "@/components/common/Icon.vue"
import Logo from "@/components/common/Logo.vue"
import HuxIcon from "@/components/common/Icon.vue"
import Tooltip from "@/components/common/Tooltip"

export default {
  name: "StandaloneDelivery",
  components: {
    HuxDataTable,
    TimeStamp,
    Size,
    Status,
    Icon,
    Logo,
    HuxIcon,
    Tooltip,
  },
  props: {
    audience: {
      type: Object,
      required: false,
      default: () => {},
    },
  },
  data() {
    return {
      selection: null,
      columnDefs: [
        {
          text: "Destination",
          value: "delivery_platform_name",
          width: "35%",
        },
        {
          text: "Status",
          value: "status",
          width: "25%",
        },
        {
          text: "Target size",
          value: "size",
          width: "15%",
          hoverTooltip:
            "Average order value for all customers (known and anyonymous) for all time.",
        },
        {
          text: "Last delivery",
          value: "last_delivered",
          width: "25%",
        },
      ],
      destinationMenuOptions: [
        { id: 1, title: "Deliver now", active: false },
        { id: 3, title: "Open destination", active: false },
        { id: 4, title: "Remove destination", active: false },
      ],
    }
  },
  computed: {},
  methods: {
    standaloneOptions() {
      // TODO:APIs are not ready
    },
    deliverAll() {
      // TODO:APIs are not ready
    },
  },
}
</script>

<style lang="scss" scoped>
.standalone-delivery {
  .deliver-icon {
    &.disabled {
      color: var(--v-black-lighten3);
    }
  }
  .delivery-table {
    ::v-deep .v-data-table {
      .v-data-table-header {
        tr {
          height: 32px !important;
        }
        th {
          background: var(--v-primary-lighten2);
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
}
.list-border {
  border-bottom: thin solid rgba(0, 0, 0, 0.12) !important;
}
::v-deep .v-data-table__wrapper {
  tbody {
    tr {
      td:nth-child(1) {
        &:hover,
        &:focus {
          .action-icon {
            display: block !important;
          }
        }
      }
    }
  }
}
</style>
