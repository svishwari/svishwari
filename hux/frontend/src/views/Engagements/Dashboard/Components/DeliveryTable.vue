<template>
  <div>
    <v-list dense class="pa-0 delivery-table">
      <hux-data-table
        v-if="section[audienceKey].length > 0"
        :columns="headers"
        :sort-desc="true"
        :data-items="section[audienceKey]"
      >
        <template #row-item="{ item }">
          <td
            v-for="header in headers"
            :key="header.value"
            class="text-body-2 column"
            :style="{ width: header.width }"
            data-e2e="map-state-list"
          >
            <div v-if="header.value == 'name'" class="text-body-1 h-25">
              <hux-icon
                v-if="item.is_lookalike"
                type="lookalike"
                :size="24"
              ></hux-icon>
              <span class="ml-1 ellipsis primary--text">
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
                :status="
                  tableData != '' ? item[tableData]['status'] : item['status']
                "
                :show-label="true"
                class="d-flex"
                :icon-size="17"
              />
            </div>
            <div v-if="header.value == 'destinations'">
              <tooltip
                v-for="destination_logo in item[header.value]"
                :key="destination_logo.delivery_platform_type"
              >
                <template #label-content>
                  <logo
                    :type="destination_logo.delivery_platform_type"
                    size="24"
                    class="ml-n1"
                  />
                </template>
                <template #hover-content>
                  {{ destination_logo.name }}
                </template>
              </tooltip>
            </div>
            <div v-if="header.value == 'size'" class="text-body-1">
              <size
                :value="
                  tableData != '' ? item[tableData]['size'] : item['size']
                "
              />
            </div>
            <div v-if="header.value == 'filters'" class="filter_col">
              <span
                v-if="
                  item[header.value] == 'null' ||
                  !item[header.value] ||
                  item[header.value].length == 0
                "
              >
                —
              </span>
              <span v-else>
                <span
                  v-for="(filter, filterIndex) in filterTags[item.name]"
                  :key="filterIndex"
                >
                  <v-chip
                    v-if="filterIndex < 4"
                    small
                    class="mr-1 ml-0 mt-0 mb-1 text-subtitle-2"
                    text-color="primary"
                    color="var(--v-primary-lighten3)"
                  >
                    {{ formatText(filter) }}
                  </v-chip>
                </span>
                <tooltip>
                  <template #label-content>
                    <span
                      v-if="filterTags[item.name].size > 4"
                      class="text-subtitle-2 primary--text"
                    >
                      +{{ filterTags[item.name].size - 4 }}
                    </span>
                  </template>
                  <template #hover-content>
                    <span
                      v-for="(filter, filterIndex) in filterTags[item.name]"
                      :key="filterIndex"
                    >
                      <v-chip
                        v-if="filterIndex >= 4"
                        small
                        class="mr-1 ml-0 mt-0 mb-1 text-subtitle-2"
                        text-color="primary"
                        color="var(--v-primary-lighten3)"
                      >
                        {{ formatText(filter) }}
                      </v-chip>
                      <br v-if="filterIndex >= 4" />
                    </span>
                  </template>
                </tooltip>
              </span>
            </div>
            <div v-if="header.value == 'update_time'" class="text-body-1">
              <time-stamp
                :value="
                  tableData != ''
                    ? item[tableData]['update_time']
                    : item['update_time']
                "
              />
            </div>
            <div v-if="header.value == 'match_rate'" class="text-body-1">
              {{
                tableData != ""
                  ? item[tableData]["match_rate"]
                  : item["match_rate"] | Percentage
              }}
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
            class="primary--text text-body-1 mb-1"
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
import { formatText } from "@/utils.js"

export default {
  name: "DeliveryTable",
  components: {
    HuxDataTable,
    Tooltip,
    HuxIcon,
    Logo,
    Status,
    Size,
    TimeStamp,
  },
  props: {
    section: {
      type: Object,
      required: true,
    },
    menuItems: {
      type: Array,
      required: false,
    },
    audienceMenuOptions: {
      type: Array,
      required: false,
      default: () => [],
    },
    audienceKey: {
      type: String,
      required: true,
    },
    filterTags: {
      type: Object,
      required: false,
      default: () => {},
    },
    headers: {
      type: Array,
      required: true,
    },
    tableData: {
      type: String,
      required: false,
      default: "",
    },
  },
  data() {
    return {
      openMenu: {},
    }
  },
  computed: {
    sectionActions() {
      return this.sectionType === "engagement"
        ? this.engagementMenuOptions
        : this.audienceMenuOptions
    },
    buttonActions() {
      this.audienceMenuOptions.forEach((element) => {
        switch (element.title.toLowerCase()) {
          case "create lookalike":
            element["active"] = this.section.lookalikable === "Active"
            break

          default:
            break
        }
      })
      return this.audienceMenuOptions
    },
  },
  watch: {
    // To reset the value of the openMenu
    openMenu(newValue) {
      if (!newValue) this.openMenu = {}
    },
  },
  methods: {
    formatText: formatText,
  },
}
</script>

<style lang="scss" scoped>
.filter_col {
  height: 59px !important;
  overflow: auto;
  display: table-cell;
  vertical-align: middle;
}
.delivery-table {
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
}
.h-25 {
  height: 25px;
}
</style>
