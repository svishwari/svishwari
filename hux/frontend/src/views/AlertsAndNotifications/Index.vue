<template>
  <div class="audiences-wrap">
    <PageHeader :headerHeightChanges="'py-3'">
      <template slot="left">
        <Breadcrumb :items="breadcrumbItems" />
      </template>
    </PageHeader>
    <PageHeader class="top-bar backGround-header" :headerHeight="71">
      <template #left>
        <v-icon medium color="blue">mdi-filter-variant</v-icon>
        <v-icon medium color="naroBlack" class="pl-4">mdi-magnify</v-icon>
      </template>

      <template #right>
        <router-link
          :to="{ name: 'alerts-notification' }"
          class="text-decoration-none"
          append
        >
          <huxButton
            ButtonText="Return to previous page"
            icon="mdi-plus"
            iconPosition="left"
            variant="primary"
            size="large"
            isTile
            class="ma-2 font-weight-regular no-shadow mr-0"
          >
            Return to previous page
          </huxButton>
        </router-link>
      </template>
    </PageHeader>
    <PageHeader class="top-bar backGround-header-dropdown" :headerHeight="71">
      <template #left>
        <HuxDropdown
            label="Alert type"
            :items="alertTypeItems"
        />
        
        <!-- <HuxDropdown
            label="Category"
            :items="alertTypeItems.title"
            />
        <HuxDropdown
            label="Date"
            :items="alertTypeItems.title"
        />           -->
      </template>
    </PageHeader>
    <v-progress-linear :active="loading" :indeterminate="loading" />
    <v-row class="pt-3 pb-7 pl-3 white" v-if="!loading">
      <hux-data-table
        :headers="columnDefs"
        :dataItems="rowData"
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
            :style="{ width: header.width, left: 0 }"
          >
            <div v-if="header.value == 'time'">
              <time-stamp :value="item['time']" />
            </div>
            <div v-if="header.value == 'type'">
               <status
                :status="item['type']"
                :showLabel="true"
                collapsed
                class="d-flex"
              /> {{ item['type']}}
              <!-- <time-stamp :value="item['type']" /> -->
            </div>
            <div v-if="header.value == 'description'">
              <!-- TODO replace with header value -->
              {{ item[header.value] }}
              <!-- <time-stamp :value="item['description']" /> -->
            </div>
            <div v-if="header.value == 'category'">
              <!-- TODO replace with header value -->
              {{ item[header.value] }}
              <!-- <Avatar :name="item['category']" /> -->
            </div>
            <!-- <div v-if="header.value == 'create_time'">
              <time-stamp :value="item[header.value]" />
            </div>
            <div v-if="header.value == 'created_by'">
              <Avatar :name="item[header.value]" />
            </div> -->
          </td>
        </template>
      </hux-data-table>
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
import MenuCell from "../../components/common/huxTable/MenuCell.vue"
import HuxDropdown from "../../components/common/HuxDropdown.vue"
import Status from "../../components/common/Status.vue"
export default {
  name: "AlertsAndNotifications",
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
    HuxDropdown,
    Status
  },
  data() {
    return {
        alertTypeItems: [
            {title: "Orchestration"},
             {title: "Decisioning"},
              {title: "Data management"}
            ],


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
          text: "Alerts & Notifications",
          disabled: true,
          icon: "audiences",
        },
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
          width: "auto",
        },
        {
          text: "Category",
          value: "category",
          width: "auto",
        }
      ],
      rowData: [
        {
          time: "2021-07-04T09:41:22.237Z",
          type: "Success",
          description: "Data Source CS005 lost connection.",
          category: "Orchestration"
        },
                {
          time: "2021-07-04T09:41:22.237Z",
          type: "Feedback",
          description: "Facebook delivery stopped.",
          category: "Decisioning"
        },
                {
          time: "2021-07-04T09:41:22.237Z",
          type: "Critical",
          description: "Data Source CS004 lost connectivity. This is an example of a longer description that needs to be cut off.",
          category: "Data management"
        }
      ],
      loading: false,
    }
  },
  computed: {
    ...mapGetters({
      rowData: "audiences/list",
    }),
    audienceList() {
      let audienceValue = this.rowData
      return audienceValue.sort((a, b) =>
        a.name.toLowerCase() === b.name.toLowerCase() ? 0 : a.name.toLowerCase() < b.name.toLowerCase() ? -1 : 1
      )
    },
    isDataExists() {
      if (this.rowData) return this.rowData.length > 0
      return false
    },
  },
  methods: {
    ...mapActions({
      getAllAudiences: "audiences/getAll",
    }),
  },
  async mounted() {
    this.loading = true
    await this.getAllAudiences()
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
.backGround-header {
    background-color: var(--v-backgroundBlue-base) !important;
}
.backGround-header-dropdown {
    background-color: var(--v-aliceBlue-base) !important;
}
</style>
