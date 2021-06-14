<template>
  <div class="engagements-wrap grey lighten-5">
    <PageHeader>
      <template slot="left">
        <Breadcrumb :items="breadcrumbItems" />
      </template>
    </PageHeader>
    <PageHeader class="top-bar" :headerHeight="71">
      <template slot="left">
        <v-icon medium :disabled="true">mdi-filter-variant</v-icon>
        <v-icon medium :disabled="true" class="pl-6">mdi-magnify</v-icon>
      </template>

      <template slot="right">
        <v-icon medium :disabled="true" color="primary refresh"
          >mdi-refresh</v-icon
        >
        <router-link
          :to="{ name: 'AudienceConfiguration' }"
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
    <v-progress-linear :active="!loading" :indeterminate="!loading" />
    <hux-data-table :headers="columnDefs" :dataItems="rowData" nested>
      <template #item-row="{ item, expand, isExpanded }">
        <tr>
          <td
            v-for="header in columnDefs"
            :key="header.value"
            :class="{
              'fixed-column': header.fixed,
              'v-data-table__divider': header.fixed,
              'primary--text': header.fixed,
            }"
            :style="{ width: header.width, left: 0 }"
          >
            <div v-if="header.value == 'name'" class="w-100">
              {{ item.isExpanded }}
              <v-icon
                :class="{ 'normal-icon': isExpanded }"
                @click="expand(!isExpanded)"
              >
                mdi-chevron-right
              </v-icon>
              <tooltip>
                <template slot="label-content">
                  <span class="primary--text"> {{ item[header.value] }} </span>
                </template>
                <template slot="hover-content">
                  {{ item[header.value] }}
                </template>
              </tooltip>
            </div>
            <div v-if="header.value == 'Audiences'">
              {{ item[header.value] }}
            </div>
            <div v-if="header.value == 'Status'">
              <status :status="item[header.value]" collapsed class="d-flex" />
            </div>
            <div v-if="header.value == 'Size'">
              <size :value="item[header.value]" />
            </div>
            <div v-if="header.value == 'Delivery_schedule'">
              {{ item[header.value] }}
            </div>
            <div v-if="header.value == 'Updated'">
              <time-stamp :value="item[header.value]" />
            </div>
            <div v-if="header.value == 'UpdatedBy'">
              <avatar :name="getName(item[header.value])" />
            </div>
            <div v-if="header.value == 'create'">
              <time-stamp :value="item[header.value]" />
            </div>
            <div v-if="header.value == 'createdBy'">
              <avatar :name="getName(item[header.value])" />
            </div>
          </td>
        </tr>
      </template>
      <template #expanded-row="{ headers, item }">
        <td
          :colspan="headers.length"
          class="pa-0 child"
          v-if="item.engagementList"
        >
          <hux-data-table
            :headers="headers"
            :dataItems="item.engagementList"
            :showHeader="false"
            class="expanded-table"
            v-if="item"
          >
            <template #row-item="{ item }">
              <td
                v-for="header in subHeaders"
                :key="header.value"
                :colspan="header.value == 'name' ? 3 : 0"
                :style="header.value == 'name' ? 'padding-left:295px' : null"
              >
                <div v-if="header.value == 'name'">
                  <tooltip>
                    <template slot="label-content">
                      <span class="primary--text"> {{ item[header.value] }} </span>
                    </template>
                    <template slot="hover-content">
                      {{ item[header.value] }}
                    </template>
                  </tooltip>
                </div>
                <div v-if="header.value == 'Size'">
                  <size :value="item[header.value]" />
                </div>
                <div v-if="header.value == 'Delivery_schedule'">
                  {{ item[header.value] }}
                </div>
                <div v-if="header.value == 'Updated'">
                  <time-stamp :value="item[header.value]" />
                </div>
                <div v-if="header.value == 'UpdatedBy'">
                  <avatar :name="getName(item[header.value])" />
                </div>
                <div v-if="header.value == 'create'">
                  <time-stamp :value="item[header.value]" />
                </div>
                <div v-if="header.value == 'createdBy'">
                  <avatar :name="getName(item[header.value])" />
                </div>
              </td>
            </template>
          </hux-data-table>
        </td>
      </template>
    </hux-data-table>

    <v-row class="pt-3 pb-7 pl-3" v-if="!loading">
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
            ></huxButton>
          </router-link>
        </template>
      </EmptyPage>
    </v-row>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"

import rowData from "./data.json"
import PageHeader from "@/components/PageHeader"
import EmptyPage from "@/components/common/EmptyPage"
import Breadcrumb from "@/components/common/Breadcrumb"
import huxButton from "@/components/common/huxButton"
import HuxDataTable from "../../components/common/dataTable/HuxDataTable.vue"
import Avatar from "../../components/common/Avatar.vue"
import Size from "../../components/common/huxTable/Size.vue"
import TimeStamp from "../../components/common/huxTable/TimeStamp.vue"
import MenuCell from "../../components/common/huxTable/MenuCell.vue"
import Status from "../../components/common/Status.vue"
import Tooltip from "../../components/common/Tooltip.vue"
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
    MenuCell,
    Status,
    Tooltip,
  },
  data() {
    return {
      breadcrumbItems: [
        {
          text: "Engagements",
          disabled: true,
          icon: "engagements",
        },
      ],
      loading: true,
      rowData: rowData.engagements,
      columnDefs: [
        { text: "Engagement name", value: "name", width: "278px" },
        { text: "Audiences", value: "Audiences", width: "278px" },
        { text: "Status", value: "Status", width: "278px" },
        { text: "Size", value: "Size", width: "278px" },
        {
          text: "Delivery schedule",
          value: "Delivery_schedule",
          width: "278px",
        },
        { text: "Last updated", value: "Updated", width: "278px" },
        { text: "Last updated by", value: "UpdatedBy", width: "278px" },
        { text: "Created", value: "create", width: "278px" },
        { text: "Created by", value: "createdBy", width: "278px" },
      ],
    }
  },
  computed: {
    subHeaders() {
      const _headers = JSON.parse(JSON.stringify(this.columnDefs))
      _headers.splice(1, 2)
      return _headers
    },
  },
  methods: {
    ...mapActions({}),
    getName(item) {
      return item.first_name + " " + item.last_name
    },
  },
}
</script>

<style lang="scss" scoped>
.engagements-wrap {
  ::v-deep .menu-cell-wrapper .action-icon {
    display: none;
  }
  .mdi-chevron-right {
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
    margin-top: 1px;
    ::v-deep table {
      tr {
        height: 64px;
        &:hover {
          background: var(--v-aliceBlue-base) !important;
        }
        td {
          font-size: 12px !important;
          color: var(--v-neroBlack-base);
        }
        td:nth-child(1) {
          font-size: 14px !important;
        }
      }
    }
  }
  ::v-deep .hux-data-table.expanded-table {
    .v-data-table__wrapper {
      box-shadow: inset 0px 10px 10px -4px #d0d0ce !important;
    }
  }
  ::v-deep .menu-cell-wrapper :hover .action-icon {
    display: initial;
  }
}
</style>
