<template>
  <div class="audiences-wrap grey lighten-5">
    <PageHeader>
      <template slot="left">
        <Breadcrumb :items="items" />
      </template>
    </PageHeader>
    <PageHeader class="mt-1" style="height: 71px">
      <template slot="left">
        <v-icon large @click="refresh"> mdi-filter-variant </v-icon>
      </template>

      <template slot="right">
        <v-icon color="primary" large @click="refresh"> mdi-refresh </v-icon>
        <!-- <router-link to="/createAudience" > -->
        <router-link :to="{ path: '/audiences/createAudience' }" append>
          <huxButton
            ButtonText="Audience"
            icon="mdi-plus"
            iconPosition="left"
            variant="primary"
            size="large"
            v-bind:isTile="true"
          ></huxButton>
        </router-link>
      </template>
    </PageHeader>
    <v-row class="pt-3 pb-7">
      <hux-table
        :columnDef="columnDefs"
        :tableData="rowData"
        :frameworkComponents="frameworkComponents"
        :rowHeight="60"
        height="350px"
        hasCheckBox
      ></hux-table>
    </v-row>
  </div>
</template>

<script>
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import huxButton from "@/components/common/huxButton"
import HuxTable from "@/components/common/huxTable.vue"
import StatusCell from "@/components/common/huxTable/StatusCell"
import UserAvatarCell from "@/components/common/huxTable/UserAvatarCell"
import MenuCell from "@/components/common/huxTable/MenuCell"
import DestinationCell from "@/components/common/huxTable/DestinationCell"

export default {
  name: "audiences",
  components: {
    PageHeader,
    Breadcrumb,
    huxButton,
    HuxTable,
  },
  data() {
    return {
      frameworkComponents: this.frameworkComponents,
      items: [
        {
          text: "Audiences",
          disabled: false,
          href: this.$route.path,
          icon: "mdi-flip-h mdi-account-plus-outline",
        },
      ],

      columnDefs: [
        {
          headerName: "Audience Name",
          field: "audienceName",
          sortable: true,
          sort: "desc",
          pinned: "left",
          width: "300",
          cellRendererFramework: MenuCell,
          cellClass: "menu-cells",
        },
        {
          headerName: "Status",
          field: "status",
          sortable: true,
          cellRendererFramework: StatusCell,
        },
        { headerName: "Size", field: "size", sortable: true },
        {
          headerName: "Destinations",
          field: "destinations",
          sortable: true,
          cellRendererFramework: DestinationCell,
        },
        { headerName: "Attributes", field: "attributes", sortable: true },
        {
          headerName: "Last Delivered",
          field: "lastDelivered",
          sortable: true,
        },
        { headerName: "Last Updated", field: "lastUpdated", sortable: true },
        {
          headerName: "Last Updated By",
          field: "lastUpdatedBy",
          sortable: true,
          cellRendererFramework: UserAvatarCell,
        },
        { headerName: "Created", field: "created", sortable: true },
        {
          headerName: "Created By",
          field: "createdBy",
          sortable: true,
          cellRendererFramework: UserAvatarCell,
        },
      ],

      rowData: [
        {
          audienceName: "Audience Name 1",
          status: "Active",
          size: "654K",
          destinations: "SFMC",
          attributes: "Churn",
          lastDelivered: "Today, 12:00 PM",
          lastUpdated: "Today, 12:00 PM",
          lastUpdatedBy: "HR",
          created: "Today, 12:00 PM",
          createdBy: "RG",
        },
        {
          audienceName: "Audience Name 1",
          status: "Delivering",
          size: "1000K",
          destinations: "SFMC",
          attributes: "Churn",
          lastDelivered: "Today, 12:00 PM",
          lastUpdated: "Today, 12:00 PM",
          lastUpdatedBy: "HR",
          created: "Today, 12:00 PM",
          createdBy: "RG",
        },
        {
          audienceName: "Audience Name 1",
          status: "Active",
          size: "2K",
          destinations: "SFMC",
          attributes: "Churn",
          lastDelivered: "Today, 12:00 PM",
          lastUpdated: "Today, 12:00 PM",
          lastUpdatedBy: "HR",
          created: "Today, 12:00 PM",
          createdBy: "RG",
        },
        {
          audienceName: "Audience Name 1",
          status: "Delivering",
          size: "654K",
          destinations: "SFMC",
          attributes: "Churn",
          lastDelivered: "Today, 12:00 PM",
          lastUpdated: "Today, 12:00 PM",
          lastUpdatedBy: "HR",
          created: "Today, 12:00 PM",
          createdBy: "RG",
        },
        {
          audienceName: "Audience Name 1",
          status: "Error",
          size: "1000K",
          destinations: "SFMC",
          attributes: "Churn",
          lastDelivered: "Today, 12:00 PM",
          lastUpdated: "Today, 12:00 PM",
          lastUpdatedBy: "HR",
          created: "Today, 12:00 PM",
          createdBy: "RG",
        },
        {
          audienceName: "Audience Name 1",
          status: "Active",
          size: "2K",
          destinations: "SFMC",
          attributes: "Churn",
          lastDelivered: "Today, 12:00 PM",
          lastUpdated: "Today, 12:00 PM",
          lastUpdatedBy: "HR",
          created: "Today, 12:00 PM",
          createdBy: "RG",
        },
        {
          audienceName: "Audience Name 1",
          status: "Delivering",
          size: "654K",
          destinations: "SFMC",
          attributes: "Churn",
          lastDelivered: "Today, 12:00 PM",
          lastUpdated: "Today, 12:00 PM",
          lastUpdatedBy: "HR",
          created: "Today, 12:00 PM",
          createdBy: "RG",
        },
      ],
    }
  },
  computed: {},
  methods: {
    refresh() {},
  },
  beforeMount() {
    this.frameworkComponents = {
      StatusCell: StatusCell,
    }
  },
}
</script>
<style lang="scss" scoped></style>
