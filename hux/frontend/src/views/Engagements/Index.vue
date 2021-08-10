<template>
  <div class="engagements-wrap">
    <page-header :header-height-changes="'py-3'">
      <template #left>
        <breadcrumb :items="breadcrumbItems" />
      </template>
      <template #right>
        <v-icon size="22" color="lightGrey" class="icon-border pa-2 ma-1">
          mdi-download
        </v-icon>
      </template>
    </page-header>
    <page-header class="top-bar" :header-height="71">
      <template #left>
        <v-icon medium color="lightGrey">mdi-filter-variant</v-icon>
        <v-icon medium color="lightGrey" class="pl-6">mdi-magnify</v-icon>
      </template>

      <template #right>
        <v-icon medium disabled color="primary refresh">mdi-refresh</v-icon>
        <router-link
          :to="{ name: 'EngagementConfiguration' }"
          class="text-decoration-none"
          append
        >
          <huxButton
            button-text="Engagement"
            icon="mdi-plus"
            icon-position="left"
            variant="primary"
            size="large"
            is-tile
            class="ma-2 font-weight-regular no-shadow mr-0"
          >
            Engagement
          </huxButton>
        </router-link>
      </template>
    </page-header>
    <v-progress-linear :active="loading" :indeterminate="loading" />
    <hux-data-table
      v-if="rowData.length > 0"
      :columns="columnDefs"
      :data-items="rowData"
      nested
    >
      <template #item-row="{ item, expandFunc, isExpanded }">
        <tr :class="{ 'expanded-row': isExpanded }">
          <td
            v-for="header in columnDefs"
            :key="header.value"
            :class="{
              'fixed-column': header.fixed,
              'v-data-table__divider': header.fixed,
              'primary--text': header.fixed,
              'expanded-row': isExpanded,
            }"
            :style="{ width: header.width }"
          >
            <div v-if="header.value == 'name'" class="w-80">
              <menu-cell
                :value="item[header.value]"
                :menu-options="actionItems"
                route-name="EngagementDashboard"
                :route-param="item['id']"
              >
                <template #expand-icon>
                  <v-icon
                    v-if="item.audiences.length > 0"
                    :class="{ 'normal-icon': isExpanded }"
                    @click="expandFunc(!isExpanded)"
                  >
                    mdi-chevron-right
                  </v-icon>
                </template>
              </menu-cell>
            </div>
            <div v-if="header.value == 'audiences'">
              {{ item[header.value].length }}
            </div>
            <div v-if="header.value == 'status'">
              <status
                :status="item[header.value]"
                :show-label="true"
                class="d-flex"
                :icon-size="17"
              />
            </div>
            <div v-if="header.value == 'size'">
              <size :value="item[header.value]" />
            </div>
            <div v-if="header.value == 'delivery_schedule'">
              {{ manualDeliverySchedule | Empty("-") }}
            </div>
            <div v-if="header.value == 'update_time'">
              <!-- TODO replace with header value -->
              <time-stamp :value="item['create_time']" />
            </div>
            <div v-if="header.value == 'updated_by'">
              <!-- TODO replace with header value -->
              <avatar :name="item['created_by']" />
            </div>
            <div v-if="header.value == 'create_time'">
              <time-stamp :value="item[header.value]" />
            </div>
            <div v-if="header.value == 'created_by'">
              <avatar :name="item[header.value]" />
            </div>
          </td>
        </tr>
      </template>
      <template #expanded-row="{ expandedHeaders, parentItem }">
        <td
          v-if="parentItem.audiences.length > 0"
          :colspan="expandedHeaders.length"
          class="pa-0 child"
        >
          <hux-data-table
            v-if="parentItem.audiences.length > 0"
            :columns="expandedHeaders"
            :data-items="parentItem.audiences"
            :show-header="false"
            class="expanded-table"
          >
            <template #row-item="{ item }">
              <td :style="{ width: expandedHeaders[0].width }"></td>
              <td
                v-for="header in getAudienceHeaders(subHeaders)"
                :key="header.value"
                :class="{
                  'child-row': header.value == 'name',
                }"
                :style="{ width: header.width }"
              >
                <div v-if="header.value == 'name'">
                  <tooltip>
                    <template #label-content>
                      <router-link
                        :to="{
                          name: 'AudienceInsight',
                          params: { id: item['id'] },
                        }"
                        class="text-decoration-none primary--text ellipsis-21"
                        append
                        >{{ item[header.value] }}
                      </router-link>
                    </template>
                    <template #hover-content>
                      {{ item[header.value] }}
                    </template>
                  </tooltip>
                </div>
                <div v-if="header.value == 'size'">
                  <div>
                    <size :value="item[header.value]" />
                  </div>
                </div>
                <div v-if="header.value == 'delivery_schedule'">
                  {{ item[header.value] | Empty("-") }}
                </div>
                <div v-if="header.value == 'update_time'">
                  <div style="width: max-content">
                    <time-stamp :value="item['create_time']" />
                  </div>
                </div>
                <div v-if="header.value == 'updated_by'">
                  <div>
                    <avatar :name="item['created_by']" />
                  </div>
                </div>
                <div v-if="header.value == 'create_time'">
                  <div>
                    <time-stamp :value="item[header.value]" />
                  </div>
                </div>
                <div v-if="header.value == 'created_by'">
                  <div>
                    <avatar :name="item[header.value]" />
                  </div>
                </div>
              </td>
            </template>
          </hux-data-table>
        </td>
      </template>
    </hux-data-table>

    <v-row v-if="rowData.length == 0 && !loading" class="pt-3 pb-7 pl-3">
      <empty-page>
        <template #icon>mdi-alert-circle-outline</template>
        <template #title>Oops! There’s nothing here yet</template>
        <template #subtitle>
          Plan your engagement ahead of time. You can create the <br />
          framework first then add audiences later. <br />
          Begin by selecting the button below.
        </template>
        <template #button>
          <router-link
            :to="{ name: 'AudienceConfiguration' }"
            class="route-link text-decoration-none"
            append
          >
            <huxButton
              button-text="Engagement"
              icon="mdi-plus"
              icon-position="left"
              variant="primary"
              size="large"
              is-tile
              class="ma-2 font-weight-regular"
            >
              Engagement
            </huxButton>
          </router-link>
        </template>
      </empty-page>
    </v-row>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import PageHeader from "@/components/PageHeader"
import EmptyPage from "@/components/common/EmptyPage"
import Breadcrumb from "@/components/common/Breadcrumb"
import huxButton from "@/components/common/huxButton"
import HuxDataTable from "../../components/common/dataTable/HuxDataTable.vue"
import Avatar from "../../components/common/Avatar.vue"
import Size from "../../components/common/huxTable/Size.vue"
import TimeStamp from "../../components/common/huxTable/TimeStamp.vue"
import Status from "../../components/common/Status.vue"
import Tooltip from "../../components/common/Tooltip.vue"
import MenuCell from "../../components/common/huxTable/MenuCell.vue"
export default {
  name: "Engagements",
  components: {
    PageHeader,
    Breadcrumb,
    huxButton,
    EmptyPage,
    HuxDataTable,
    Avatar,
    Size,
    TimeStamp,
    Status,
    Tooltip,
    MenuCell,
  },
  data() {
    return {
      actionItems: [
        { title: "Favorite" },
        { title: "Export" },
        { title: "Edit" },
        { title: "Duplicate" },
        { title: "Create a lookalike" },
        { title: "Delete" },
      ],
      breadcrumbItems: [
        {
          text: "Engagements",
          disabled: true,
          icon: "engagements",
        },
      ],
      loading: true,
      rowData: [],
      manualDeliverySchedule: "Manual",
      audienceList: [],
      columnDefs: [
        { text: "Engagement name", value: "name", width: "300px" },
        { text: "Audiences", value: "audiences", width: "200px" },
        { text: "Status", value: "status", width: "200px" },
        {
          text: "Delivery schedule",
          value: "delivery_schedule",
          width: "200px",
        },
        { text: "Last updated", value: "update_time", width: "200px" },
        { text: "Last updated by", value: "updated_by", width: "141px" },
        { text: "Created", value: "create_time", width: "200px" },
        { text: "Created by", value: "created_by", width: "140px" },
      ],
    }
  },
  computed: {
    ...mapGetters({
      engagementData: "engagements/list",
      audiencesData: "audiences/audience",
    }),
    audience(id) {
      return this.audiencesData(id)
    },
    subHeaders() {
      const _headers = JSON.parse(JSON.stringify(this.columnDefs))
      _headers.splice(1, 1)
      return _headers
    },
  },

  async mounted() {
    this.loading = true
    await this.getAllEngagements()
    this.rowData = this.engagementData.sort((a, b) =>
      a.name > b.name ? 1 : -1
    )
    this.loading = false
  },

  methods: {
    ...mapActions({
      getAllEngagements: "engagements/getAll",
      updateAudienceList: "engagements/updateAudienceList",
    }),
    getAudienceHeaders(headers) {
      headers[0].width = "200px"
      return headers
    },
  },
}
</script>

<style lang="scss" scoped>
.engagements-wrap {
  background: var(--v-white-base);
  ::v-deep .menu-cell-wrapper .action-icon {
    display: none;
  }
  .ellipsis-21 {
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 21ch;
    display: inline-block;
    width: 21ch;
    white-space: nowrap;
  }
  .mdi-chevron-right {
    margin-top: -4px;
    transition: 0.3s cubic-bezier(0.25, 0.8, 0.5, 1), visibility 0s;
    &.normal-icon {
      transform: rotate(90deg);
    }
  }
  .page-header--wrap {
    box-shadow: 0px 1px 1px -1px var(--v-lightGrey-base),
      0px 1px 1px 0px var(--v-lightGrey-base),
      0px 1px 2px 0px var(--v-lightGrey-base) !important;
  }
  .top-bar {
    margin-top: 1px;
    .v-icon--disabled {
      color: var(--v-lightGrey-base) !important;
      font-size: 24px;
    }
    .text--refresh {
      margin-right: 10px;
    }
  }
  .hux-data-table {
    ::v-deep table {
      tr {
        height: 64px;
        &:hover {
          background: var(--v-aliceBlue-base) !important;
        }
        td {
          font-size: 14px !important;
          color: var(--v-neroBlack-base);
        }
        td:nth-child(1) {
          font-size: 14px !important;
        }
      }
      .expanded-row {
        background-color: var(--v-aliceBlue-base) !important;
      }
      .v-data-table-header {
        th:nth-child(1) {
          position: sticky;
          top: 0;
          left: 0;
          z-index: 4;
          border-right: thin solid rgba(0, 0, 0, 0.12);
        }
        border-radius: 12px 12px 0px 0px;
      }
      tr {
        th {
          border-top: thin solid rgba(0, 0, 0, 0.12);
        }
        &:hover {
          background: var(--v-aliceBlue-base) !important;
        }
        height: 64px;
        td {
          font-size: 14px !important;
          line-height: 22px;
          color: var(--v-neroBlack-base);
        }
        td:nth-child(1) {
          position: sticky;
          top: 0;
          left: 0;
          z-index: 4;
          background: var(--v-white-base);
          border-right: thin solid rgba(0, 0, 0, 0.12);
          &:hover {
            background: var(--v-aliceBlue-base) !important;
          }
          .menu-cell-wrapper > div {
            a.text-decoration-none {
              .ellipsis {
                width: auto !important;
              }
            }
          }
        }
      }
      tbody {
        tr:last-child {
          td {
            border-bottom: 1px solid var(--v-lightGrey-base) !important;
          }
        }
      }
    }
    .child {
      ::v-deep .theme--light {
        background: var(--v-background-base);
        .v-data-table__wrapper {
          box-shadow: inset 0px 10px 10px -4px var(--v-lightGrey-base);
          border-bottom: thin solid rgba(0, 0, 0, 0.12);
        }
      }
    }
  }
  ::v-deep .hux-data-table.expanded-table {
    .v-data-table__wrapper {
      box-shadow: inset 0px 10px 10px -4px #d0d0ce !important;
      .child-row {
        border-right: none;
      }
    }
    td:nth-child(1) {
      background: none;
    }
  }
  ::v-deep .menu-cell-wrapper :hover .action-icon {
    display: initial;
  }
}
.icon-border {
  cursor: default !important;
}
</style>
