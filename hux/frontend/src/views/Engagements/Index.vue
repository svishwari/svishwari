<template>
  <div class="engagements-wrap">
    <PageHeader>
      <template #left>
        <Breadcrumb :items="breadcrumbItems" />
      </template>
      <template #right>
        <v-icon size="24" :disabled="true" class="icon-border pa-2 ma-1">
          mdi-download
        </v-icon>
      </template>
    </PageHeader>
    <PageHeader class="top-bar" :headerHeight="71">
      <template #left>
        <v-icon medium disabled>mdi-filter-variant</v-icon>
        <v-icon medium disabled class="pl-6">mdi-magnify</v-icon>
      </template>

      <template #right>
        <v-icon medium disabled color="primary refresh">mdi-refresh</v-icon>
        <router-link
          :to="{ name: 'EngagementConfiguration' }"
          class="text-decoration-none"
          append
        >
          <huxButton
            ButtonText="Engagement"
            icon="mdi-plus"
            iconPosition="left"
            variant="primary"
            size="large"
            isTile
            class="ma-2 font-weight-regular no-shadow mr-0"
          >
            Engagement
          </huxButton>
        </router-link>
      </template>
    </PageHeader>
    <v-progress-linear :active="loading" :indeterminate="loading" />
    <hux-data-table
      v-if="rowData.length > 0"
      :headers="columnDefs"
      :dataItems="rowData"
      nested
    >
      <template #item-row="{ item, expand, isExpanded }">
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
            :style="{ width: header.width, left: 0 }"
          >
            <div v-if="header.value == 'name'" class="w-80">
              <menu-cell
                :value="item[header.value]"
                :menuOptions="actionItems"
                routeName="EngagementDashboard"
                :routeParam="item['id']"
              >
                <template #expand-icon>
                  <v-icon
                    v-if="item.audiences.length > 0"
                    :class="{ 'normal-icon': isExpanded }"
                    @click="
                      expand(!isExpanded)
                      getAudiencesForEngagement(item)
                      markCurrentRow(item.id)
                    "
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
                :showLabel="true"
                collapsed
                class="d-flex"
              />
            </div>
            <div v-if="header.value == 'size'">
              <size :value="item[header.value]" />
            </div>
            <div v-if="header.value == 'delivery_schedule'">
              {{ manualDeliverySchedule }}
            </div>
            <div v-if="header.value == 'update_time'">
              <time-stamp :value="item[header.value]" />
            </div>
            <div v-if="header.value == 'updated_by'">
              <avatar :name="item[header.value]" />
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
      <template #expanded-row="{ headers, item }">
        <td
          :colspan="headers.length"
          class="pa-0 child"
          v-if="item.audiences.length > 0"
        >
          <v-progress-linear
            :active="item.isCurrentRow"
            :indeterminate="item.isCurrentRow"
          />
          <hux-data-table
            :headers="headers"
            :dataItems="item.audienceList"
            :showHeader="false"
            class="expanded-table"
            v-if="item.audiences.length > 0"
          >
            <template #row-item="{ item }">
              <td
                v-for="header in subHeaders"
                :key="header.value"
                :colspan="header.value == 'name' ? 3 : 0"
                :class="{
                  'child-row': header.value == 'name',
                }"
              >
                <div v-if="header.value == 'name'">
                  <tooltip>
                    <template #label-content>
                      <router-link
                        :to="{
                          name: 'AudienceInsight',
                          params: { id: item['id'] },
                        }"
                        class="text-decoration-none primary--text"
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
                  <div class="ml-16 pl-1">
                    <size :value="item[header.value]" />
                  </div>
                </div>
                <div v-if="header.value == 'delivery_schedule'">
                  {{ item[header.value] }}
                </div>
                <div v-if="header.value == 'update_time'">
                  <div class="ml-16 pl-4" style="width: max-content">
                    <time-stamp :value="item[header.value]" />
                  </div>
                </div>
                <div v-if="header.value == 'updated_by'">
                  <div class="ml-16 pl-7">
                    <Avatar :name="item[header.value]" />
                  </div>
                </div>
                <div v-if="header.value == 'create_time'">
                  <div class="ml-10">
                    <time-stamp :value="item[header.value]" />
                  </div>
                </div>
                <div v-if="header.value == 'created_by'">
                  <div class="ml-13">
                    <Avatar :name="item[header.value]" />
                  </div>
                </div>
              </td>
            </template>
          </hux-data-table>
        </td>
      </template>
    </hux-data-table>

    <v-row class="pt-3 pb-7 pl-3" v-if="rowData.length == 0">
      <EmptyPage>
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
              ButtonText="Engagement"
              icon="mdi-plus"
              iconPosition="left"
              variant="primary"
              size="large"
              isTile
              class="ma-2 font-weight-regular"
            >
              Engagement
            </huxButton>
          </router-link>
        </template>
      </EmptyPage>
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
  name: "engagements",
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
        { text: "Status", value: "status", width: "140px" },
        { text: "Size", value: "size", width: "200px" },
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
      _headers.splice(1, 2)
      return _headers
    },
  },
  methods: {
    ...mapActions({
      getAllEngagements: "engagements/getAll",
      getAudienceById: "audiences/getAudienceById",
      updateAudienceList: "engagements/updateAudienceList",
      markCurrentRow: "engagements/markCurrentRow",
    }),
    // TODO: replace with data from GET /engagements when available
    async getAudiencesForEngagement(item) {
      this.audienceList = []
      let audienceIds = item.audiences.map((key) => key.id)
      for (let id of audienceIds) {
        await this.getAudienceById(id)
        this.audienceList.push(this.audiencesData(id))
      }
      await this.updateAudienceList({ id: item.id, data: this.audienceList })
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
}
</script>

<style lang="scss" scoped>
.engagements-wrap {
  background: var(--v-white-base);
  ::v-deep .menu-cell-wrapper .action-icon {
    display: none;
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
        th {
          background: var(--v-aliceBlue-base);
          &:first-child {
            border-radius: 12px 0px 0px 0px;
          }
          &:last-child {
            border-radius: 0px 12px 0px 0px;
          }
        }
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
        padding-left: 317px;
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
</style>
