<template>
  <v-card
    class="rounded-lg card-style standalone-delivery mt-4"
    flat
    height="156"
  >
    <v-card-title class="d-flex justify-space-between pb-2 pl-6 pt-3">
      <div class="d-flex align-center">
        <span class="text-h3">Standalone deliveries</span>
      </div>
      <v-spacer> </v-spacer>
      <div class="d-flex mr-4 deliver-all disabled" @click="deliverAll()">
        <icon
          class="deliver-icon mr-2"
          type="deliver"
          color="black"
          variant="lighten3"
          :size="24"
        />
        Deliver all
      </div>
    </v-card-title>
    <v-card-text class="pl-6 pr-6 pb-4 pt-0">
      <div
        v-if="deliveries.length == 0"
        class="empty-state py-4 black--text text--lighten-4 text-body-1"
      >
        This audience has no standalone deliveries. Add a destination below.
        <v-list dense class="add-list" :height="52">
          <v-list-item class="px-0" @click="$emit('onAddDestination', section)">
            <hux-icon type="plus" :size="16" color="primary" class="mr-4" />
            <hux-icon
              type="destination"
              :size="24"
              color="primary"
              class="mr-2"
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
      <hux-data-table
        v-else
        class="delivery-table"
        :columns="columnDefs"
        :sort-desc="true"
        :data-items="deliveries"
      >
        <template #row-item="{ item }">
          <td
            v-for="header in columnDefs"
            :key="header.value"
            class="text-body-2"
            :style="{ width: header.width }"
            data-e2e="map-state-list"
          >
            <div v-if="header.value == 'name'" class="text-body-1">
              <logo :type="item.type" :size="22" class="mb-n1"></logo>
              {{ item.name }}
              <v-menu class="menu-wrapper float-right" bottom offset-y>
                <template #activator="{ on, attrs }">
                  <v-icon v-bind="attrs" class="top-action" v-on="on">
                    mdi-dots-vertical
                  </v-icon>
                </template>
                <v-list class="menu-list-wrapper">
                  <v-list-item-group v-model="selection" active-class="">
                    <v-list-item>
                      <v-list-item-title> Deliver now </v-list-item-title>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-title> Open destination </v-list-item-title>
                    </v-list-item>
                    <v-list-item>
                      <v-list-item-title>
                        Remove destination
                      </v-list-item-title>
                    </v-list-item>
                  </v-list-item-group>
                </v-list>
              </v-menu>
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
            <div v-if="header.value == 'next_delivery'" class="text-body-1">
              <time-stamp :value="item['next_delivery']" />
            </div>
          </td>
        </template>
      </hux-data-table>
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

export default {
  name: "StandaloneDelivery",
  components: { HuxDataTable, TimeStamp, Size, Status, Icon, Logo, HuxIcon },
  props: {},
  data() {
    return {
      selection: null,
      columnDefs: [
        {
          text: "Destination",
          value: "name",
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
          value: "next_delivery",
          width: "25%",
        },
      ],
      deliveries: [],
    }
  },
  computed: {},
}
</script>

<style lang="scss" scoped>
.standalone-delivery {
  .deliver-all {
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
</style>
