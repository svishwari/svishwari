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
        <router-link
          :to="{ path: '/audiences/createAudience' }"
          class="route-link"
          append
        >
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
import DateTimeCell from "@/components/common/huxTable/DateTimeCell"
import sizeCell from "@/components/common/huxTable/sizeCell"
import attributeCell from "@/components/common/huxTable/attributeCell"

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
        {
          headerName: "Size",
          field: "size",
          sortable: true,
          cellRendererFramework: sizeCell,
        },
        {
          headerName: "Destinations",
          field: "destinations",
          sortable: true,
          cellRendererFramework: DestinationCell,
        },
        {
          headerName: "Attributes",
          field: "attributes",
          sortable: true,
          cellRendererFramework: attributeCell,
        },
        {
          headerName: "Last Delivered",
          field: "lastDelivered",
          sortable: true,
        },
        {
          headerName: "Last Updated",
          field: "lastUpdated",
          sortable: true,
          cellRendererFramework: DateTimeCell,
        },
        {
          headerName: "Last Updated By",
          field: "lastUpdatedBy",
          sortable: true,
          cellRendererFramework: UserAvatarCell,
        },
        {
          headerName: "Created",
          field: "created",
          sortable: true,
          cellRendererFramework: DateTimeCell,
        },
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
          size: {
            approxSize: "654K",
            actualSize: "2,345",
          },
          destinations: {
            details: [
              { logo: "../../../assets/images/facebook.png", name: "facebook" },
              {
                logo: "../../../assets/images/mailchimp.png",
                name: "MailChimp",
              },
              {
                logo: "../../../assets/images/facebook.png",
                name: "Salesforce",
              },
            ],
          },
          attributes: {
            attribute: "Churn +2",
            attributeList: [
              { attribute: "LTV" },
              { attribute: "Propensity" },
              { attribute: "Demgraphics" },
            ],
          },
          lastDelivered: "Today, 12:00 PM",
          lastUpdated: {
            shortDate: "Today, 12:00 PM",
            FullDate: "03/22/2021 12:45 PM",
          },
          lastUpdatedBy: {
            shortName: "HR",
            fullName: "John Smith",
          },
          created: {
            shortDate: "Today, 12:00 PM",
            FullDate: "03/22/2021 12:45 PM",
          },
          createdBy: {
            shortName: "RG",
            fullName: "John Smith",
          },
        },
        {
          audienceName: "Audience Name 1",
          status: "Delivering",
          size: {
            approxSize: "654K",
            actualSize: "2,345",
          },
          destinations: {
            details: [
              { logo: "../../../assets/images/facebook.png", name: "facebook" },
              {
                logo: "../../../assets/images/mailchimp.png",
                name: "MailChimp",
              },
              {
                logo: "../../../assets/images/facebook.png",
                name: "Salesforce",
              },
            ],
          },
          attributes: {
            attribute: "Churn +2",
            attributeList: [
              { attribute: "LTV" },
              { attribute: "Propensity" },
              { attribute: "Demgraphics" },
            ],
          },
          lastDelivered: "Today, 12:00 PM",
          lastUpdated: {
            shortDate: "Today, 12:00 PM",
            FullDate: "03/22/2021 12:45 PM",
          },
          lastUpdatedBy: {
            shortName: "HR",
            fullName: "John Smith",
          },
          created: {
            shortDate: "Today, 12:00 PM",
            FullDate: "03/22/2021 12:45 PM",
          },
          createdBy: {
            shortName: "RG",
            fullName: "John Smith",
          },
        },
        {
          audienceName: "Audience Name 1",
          status: "Active",
          size: {
            approxSize: "654K",
            actualSize: "2,345",
          },
          destinations: {
            details: [
              { logo: "../../../assets/images/facebook.png", name: "facebook" },
              {
                logo: "../../../assets/images/mailchimp.png",
                name: "MailChimp",
              },
              {
                logo: "../../../assets/images/facebook.png",
                name: "Salesforce",
              },
            ],
          },
          attributes: {
            attribute: "Churn +2",
            attributeList: [
              { attribute: "LTV" },
              { attribute: "Propensity" },
              { attribute: "Demgraphics" },
            ],
          },
          lastDelivered: "Today, 12:00 PM",
          lastUpdated: {
            shortDate: "Today, 12:00 PM",
            FullDate: "03/22/2021 12:45 PM",
          },
          lastUpdatedBy: {
            shortName: "HR",
            fullName: "John Smith",
          },
          created: {
            shortDate: "Today, 12:00 PM",
            FullDate: "03/22/2021 12:45 PM",
          },
          createdBy: {
            shortName: "RG",
            fullName: "John Smith",
          },
        },
        {
          audienceName: "Audience Name 1",
          status: "Delivering",
          size: {
            approxSize: "654K",
            actualSize: "2,345",
          },
          destinations: {
            details: [
              { logo: "../../../assets/images/facebook.png", name: "facebook" },
              {
                logo: "../../../assets/images/mailchimp.png",
                name: "MailChimp",
              },
              {
                logo: "../../../assets/images/facebook.png",
                name: "Salesforce",
              },
            ],
          },
          attributes: {
            attribute: "Churn +2",
            attributeList: [
              { attribute: "LTV" },
              { attribute: "Propensity" },
              { attribute: "Demgraphics" },
            ],
          },
          lastDelivered: "Today, 12:00 PM",
          lastUpdated: {
            shortDate: "Today, 12:00 PM",
            FullDate: "03/22/2021 12:45 PM",
          },
          lastUpdatedBy: {
            shortName: "HR",
            fullName: "John Smith",
          },
          created: {
            shortDate: "Today, 12:00 PM",
            FullDate: "03/22/2021 12:45 PM",
          },
          createdBy: {
            shortName: "RG",
            fullName: "John Smith",
          },
        },
        {
          audienceName: "Audience Name 1",
          status: "Error",
          size: {
            approxSize: "1000K",
            actualSize: "2,345",
          },
          destinations: {
            details: [
              { logo: "../../../assets/images/facebook.png", name: "facebook" },
              {
                logo: "../../../assets/images/mailchimp.png",
                name: "MailChimp",
              },
              {
                logo: "../../../assets/images/facebook.png",
                name: "Salesforce",
              },
            ],
          },
          attributes: {
            attribute: "Churn +2",
            attributeList: [
              { attribute: "LTV" },
              { attribute: "Propensity" },
              { attribute: "Demgraphics" },
            ],
          },
          lastDelivered: "Today, 12:00 PM",
          lastUpdated: {
            shortDate: "Today, 12:00 PM",
            FullDate: "03/22/2021 12:45 PM",
          },
          lastUpdatedBy: {
            shortName: "HR",
            fullName: "John Smith",
          },
          created: {
            shortDate: "Today, 12:00 PM",
            FullDate: "03/22/2021 12:45 PM",
          },
          createdBy: {
            shortName: "RG",
            fullName: "John Smith",
          },
        },
        {
          audienceName: "Audience Name 1",
          status: "Active",
          size: {
            approxSize: "2K",
            actualSize: "2,345",
          },
          destinations: {
            details: [
              { logo: "../../../assets/images/facebook.png", name: "facebook" },
              {
                logo: "../../../assets/images/mailchimp.png",
                name: "MailChimp",
              },
              {
                logo: "../../../assets/images/facebook.png",
                name: "Salesforce",
              },
            ],
          },
          attributes: {
            attribute: "Churn +2",
            attributeList: [
              { attribute: "LTV" },
              { attribute: "Propensity" },
              { attribute: "Demgraphics" },
            ],
          },
          lastDelivered: "Today, 12:00 PM",
          lastUpdated: {
            shortDate: "Today, 12:00 PM",
            FullDate: "03/22/2021 12:45 PM",
          },
          lastUpdatedBy: {
            shortName: "HR",
            fullName: "John Smith",
          },
          created: {
            shortDate: "Today, 12:00 PM",
            FullDate: "03/22/2021 12:45 PM",
          },
          createdBy: {
            shortName: "RG",
            fullName: "John Smith",
          },
        },
        {
          audienceName: "Audience Name 1",
          status: "Delivering",
          size: {
            approxSize: "2K",
            actualSize: "2,345",
          },
          destinations: {
            details: [
              { logo: "../../../assets/images/facebook.png", name: "facebook" },
              {
                logo: "../../../assets/images/mailchimp.png",
                name: "MailChimp",
              },
              {
                logo: "../../../assets/images/facebook.png",
                name: "Salesforce",
              },
            ],
          },
          attributes: {
            attribute: "Churn +2",
            attributeList: [
              { attribute: "LTV" },
              { attribute: "Propensity" },
              { attribute: "Demgraphics" },
            ],
          },
          lastDelivered: "Today, 12:00 PM",
          lastUpdated: {
            shortDate: "Today, 12:00 PM",
            FullDate: "03/22/2021 12:45 PM",
          },
          lastUpdatedBy: {
            shortName: "HR",
            fullName: "John Smith",
          },
          created: {
            shortDate: "Today, 12:00 PM",
            FullDate: "03/22/2021 12:45 PM",
          },
          createdBy: {
            shortName: "RG",
            fullName: "John Smith",
          },
        },
      ],
    }
  },
  computed: {},
  methods: {
    refresh() {},
  },
  beforeMount() {},
}
</script>
<style lang="scss" scoped>
.audiences-wrap {
  .route-link {
    text-decoration: none;
  }
}
</style>
