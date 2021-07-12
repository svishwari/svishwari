<template>
  <div class="audiences-wrap">
    <PageHeader :headerHeightChanges="'py-3'">
      <template slot="left">
        <Breadcrumb :items="breadcrumbItems" />
      </template>
    </PageHeader>
    <PageHeader class="top-bar mb-3" :headerHeight="71">
      <template #left>
        <v-icon medium color="lightGrey">mdi-filter-variant</v-icon>
        <v-icon medium color="lightGrey" class="pl-4">mdi-magnify</v-icon>
      </template>

      <template #right>
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
      </template>
    </PageHeader>
    <v-progress-linear :active="loading" :indeterminate="loading" />
    <v-row class="pt-3 pb-7 pl-6 white" v-if="!loading">
      <hux-data-table
        :headers="columnDefs"
        :dataItems="getNotificationData"
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
            <div v-if="header.value == 'created'">
              <time-stamp :value="item['created']" />
            </div>
            <div v-if="header.value == 'notification_type'">
              <status
                :status="item['notification_type']"
                :showLabel="true"
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
import { mapActions, mapGetters } from "vuex"
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import huxButton from "@/components/common/huxButton"
import HuxDataTable from "../../components/common/dataTable/HuxDataTable.vue"
import TimeStamp from "../../components/common/huxTable/TimeStamp.vue"
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
          value: "created",
          width: "auto",
        },
        {
          text: "Type",
          value: "notification_type",
          width: "auto",
        },
        {
          text: "Description",
          value: "description",
          width: "600px",
        },
      ],
      loading: false,
    }
  },
  computed: {
    ...mapGetters({
      notification: "notification/list",
    }),
    getNotificationData() {
      return this.notification
    },
  },
  methods: {
    ...mapActions({
      getNotification: "notification/getAll",
    }),
    goBack() {
      this.$router.go(-1)
    },
  },
  async mounted() {
    this.loading = true
    await this.getNotification()
    this.loading = false
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

.backGround-header-dropdown {
  background-color: var(--v-aliceBlue-base) !important;
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
