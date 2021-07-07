<template>
  <div class="audiences-wrap">
    <PageHeader :headerHeightChanges="'py-3'">
      <template slot="left">
        <Breadcrumb :items="breadcrumbItems" />
      </template>
    </PageHeader>
    <PageHeader class="top-bar backGround-header mb-3" :headerHeight="71">
      <template #left>
        <v-icon medium color="lightGrey">mdi-filter-variant</v-icon>
        <v-icon medium color="lightGrey" class="pl-4">mdi-magnify</v-icon>
      </template>

      <template #right>
        <router-link
          :to="{ name: 'alerts-notification' }"
          class="text-decoration-none"
          append
        >
          <huxButton
            ButtonText="Return to previous page"
            icon="mdi-keyboard-return"
            iconPosition="left"
            variant="primary"
            size="large"
            isTile
            class="ma-2 font-weight-regular no-shadow mr-0"
            @click="goBack()"
          >
            Return to previous page
          </huxButton>
        </router-link>
      </template>
    </PageHeader>
    <!-- <PageHeader class="top-bar backGround-header-dropdown" :headerHeight="71">
      <template #left>
        <span class="d-flex flex-row">
          <div>
        <HuxDropdown
            label="Alert type"
            :items="alertTypeItems"
        />
          </div>
          <div>
        <HuxDropdown
            label="Category"
            :items="categoryItems"
        />
          </div>
        </span>
      </template>
    </PageHeader> -->
    <v-progress-linear :active="loading" :indeterminate="loading" />
    <v-row class="pt-3 pb-7 pl-6 white" v-if="!loading">
      <hux-data-table
        :headers="columnDefs"
        :dataItems="rowData"
        :disableSort="true"
      >
        <template #row-item="{ item }">
          <td
            v-for="header in columnDefs"
            :key="header.value"
            :class="{
              'fixed-column': header.fixed,
              'v-data-table__divider': header.fixed,
              'primary--text': header.fixed,
            }"
            class="col-overflow"
            :style="{ width: header.width, left: 0 }"
          >
            <div v-if="header.value == 'time'">
              <time-stamp :value="item['time']" />
            </div>
            <div v-if="header.value == 'type'">
              <status
                :status="item['type']"
                :showLabel="true"
                class="status-icon"
                :iconSize="17"
              />
            </div>
            <tooltip v-if="header.value == 'description'" positionTop>
              <template #label-content>
                <span>{{ item[header.value] }}</span>
              </template>
              <template #hover-content>
                {{ item[header.value] }}
              </template>
            </tooltip>
          </td>
        </template>
      </hux-data-table>
    </v-row>
  </div>
</template>

<script>
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import huxButton from "@/components/common/huxButton"
import HuxDataTable from "../../components/common/dataTable/HuxDataTable.vue"
import TimeStamp from "../../components/common/huxTable/TimeStamp.vue"
// import HuxDropdown from "../../components/common/HuxDropdown.vue"
import Status from "../../components/common/Status.vue"
import Tooltip from "@/components/common/Tooltip.vue"
export default {
  name: "AlertsAndNotifications",
  components: {
    PageHeader,
    Breadcrumb,
    huxButton,
    HuxDataTable,
    TimeStamp,
    // HuxDropdown,
    Status,
    Tooltip,
  },
  data() {
    return {
      breadcrumbItems: [
        {
          text: "Alerts & Notifications",
          disabled: true,
          icon: "notifications",
        },
      ],
      categoryItems: [
        { name: "Orchestration" },
        { name: "Decisioning" },
        { name: "Data management" },
      ],
      alertTypeItems: [
        { name: "Success", modelIcon: "Success" },
        { name: "Critical", modelIcon: "Critical" },
        { name: "Feedback", modelIcon: "Feedback" },
        { name: "Informational", modelIcon: "Informational" },
      ],
      columnDefs: [
        {
          text: "Time",
          value: "time",
          width: "auto",
        },
        {
          text: "Type",
          value: "type",
          width: "auto",
        },
        {
          text: "Description",
          value: "description",
          width: "600px",
        },
        // {
        //   text: "Category",
        //   value: "category",
        //   width: "auto",
        // }
      ],
      rowData: [
        {
          time: "2021-07-04T09:41:22.237Z",
          type: "Success",
          description: "Data Source CS005 lost connection.",
          category: "Orchestration",
        },
        {
          time: "2021-07-04T09:41:22.237Z",
          type: "Feedback",
          description: "Facebook delivery stopped.",
          category: "Decisioning",
        },
        {
          time: "2021-07-04T09:41:22.237Z",
          type: "Critical",
          description:
            "Data Source CS004 lost connectivity. This is an example of a longer description that needs to be cut off.",
          category: "Data management",
        },
      ],
      loading: false,
    }
  },
  methods: {
    goBack() {
      window.history.back()
    },
  },
}
</script>
<style lang="scss" scoped>
.audiences-wrap {
  ::v-deep .menu-cell-wrapper .action-icon {
    display: none;
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
    table {
      tr {
        td {
          font-size: 14px;
          height: 63px;
        }
      }
    }
  }
  ::v-deep .menu-cell-wrapper :hover .action-icon {
    display: initial;
  }
  .icon-border {
    cursor: default !important;
  }
}
.radio-div {
  margin-top: -11px !important;
}
.backGround-header {
  background-color: var(--v-backgroundBlue-base) !important;
}
.backGround-header-dropdown {
  background-color: var(--v-aliceBlue-base) !important;
}
.status-icon {
  ::v-deep i {
    font-size: 17px !important;
  }
}
::v-deep .hux-dropdown {
  .v-btn__content {
    color: var(--v-darkBlue-base) !important;
  }
}
.col-overflow {
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}
</style>
