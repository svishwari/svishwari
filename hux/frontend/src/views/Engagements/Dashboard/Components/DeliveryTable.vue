<template>
  <div>
    <v-list dense class="pa-0 delivery-table">
      <hux-data-table
        v-if="section.audiences.length > 0"
        :columns="columnDefs"
        :sort-desc="true"
        :data-items="section.audiences"
      >
        <template #row-item="{ item }">
          <td
            v-for="header in columnDefs"
            :key="header.value"
            class="text-body-2 column"
            :style="{ width: header.width }"
            data-e2e="map-state-list"
          >
            <div v-if="header.value == 'name'" class="text-body-1">
              <logo
                v-if="item.is_lookalike"
                :type="item.delivery_platform_type"
                :size="24"
              ></logo>
              <span class="ml-2 ellipsis primary--text">
                {{ item.name }}
              </span>
              <span class="action-icon font-weight-light float-right d-none">
                <v-menu
                  v-model="openMenu[item.id]"
                  class="menu-wrapper"
                  bottom
                  offset-y
                >
                  <template #activator="{ on, attrs }">
                    <v-icon
                      v-bind="attrs"
                      class="mr-2 more-action"
                      color="primary"
                      v-on="on"
                      @click.prevent
                    >
                      mdi-dots-vertical
                    </v-icon>
                  </template>
                  <v-list class="menu-list-wrapper">
                    <v-list-item-group>
                      <v-list-item
                        v-for="option in sectionActions"
                        :key="option.id"
                        :disabled="!option.active"
                        @click="
                          $emit('onSectionAction', {
                            target: option,
                            data: item,
                            parent: section,
                          })
                        "
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
            <div v-if="header.value == 'destinations'">
              <logo
                v-for="destination_logo in item[header.value]"
                :key="destination_logo.delivery_platform_type"
                :type="destination_logo.delivery_platform_type"
                size="24"
                class="ml-n1"
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

      <v-list dense class="add-list" :height="52">
        <v-list-item @click="$emit('triggerSelectAudience', $event)">
          <tooltip>
            <template #label-content>
              <hux-icon
                type="plus"
                :size="12"
                color="primary"
                class="mr-1 mb-2"
              />
              <hux-icon
                type="add_audience"
                :size="24"
                color="primary"
                class="mr-1"
              />
            </template>
            <template #hover-content>
              <div class="py-2 white d-flex flex-column">
                <span> Add a audience to this engagement </span>
              </div>
            </template>
          </tooltip>
          <span
            min-width="7rem"
            height="2rem"
            class="primary--text text-body-1 mb-2"
          >
            Audience
          </span>
        </v-list-item>
      </v-list>
    </v-list>
  </div>
</template>

<script>
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import HuxIcon from "@/components/common/Icon.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import Logo from "@/components/common/Logo.vue"
import Status from "@/components/common/Status.vue"
import Size from "@/components/common/huxTable/Size.vue"
import TimeStamp from "@/components/common/huxTable/TimeStamp.vue"

export default {
  name: "DeliveryTable",
  components: { HuxDataTable, Tooltip, HuxIcon, Logo, Status, Size, TimeStamp },
  props: {
    section: {
      type: Object,
      required: true,
    },
    menuItems: {
      type: Array,
      required: false,
    },
  },
  data() {
    return {
      openMenu: {},
      columnDefs: [
        {
          text: "Audiences",
          value: "name",
          width: "20%",
        },
        {
          text: "Status",
          value: "status",
          width: "15%",
        },
        {
          text: "Destination",
          value: "destinations",
          width: "15%",
        },
        {
          text: "Target size",
          value: "size",
          width: "15%",
          hoverTooltip:
            "Average order value for all customers (known and anyonymous) for all time.",
          tooltipWidth: "201px",
        },
        {
          text: "Attributes",
          value: "attributes",
          width: "25%",
        },
        {
          text: "Last delivery",
          value: "update_time",
          width: "10%",
        },
      ],

      audienceMenuOptions: [
        { id: 1, title: "Deliver now", active: true },
        { id: 2, title: "Create lookalike", active: true },
        { id: 3, title: "Add a destination", active: true },
        { id: 4, title: "Remove audience", active: true },
      ],
    }
  },
  computed: {
    sectionActions() {
      return this.sectionType === "engagement"
        ? this.engagementMenuOptions
        : this.audienceMenuOptions
    },
  },
  watch: {
    // To reset the value of the openMenu
    openMenu(newValue) {
      if (!newValue) this.openMenu = {}
    },
  },
}
</script>

<style lang="scss" scoped>
.hux-data-table {
  ::v-deep table {
    .v-data-table-header {
      tr {
        th {
          background: var(--v-primary-lighten2);
          height: 40px !important;
        }
      }
    }
    tbody {
      tr {
        td {
          height: 40px !important;
        }
      }
    }
    border-radius: 12px 12px 0px 0px;
    overflow: hidden;
  }
}
.delivery-table {
  border-radius: 12px;
  border: 1px solid var(--v-black-lighten2);
}
</style>
