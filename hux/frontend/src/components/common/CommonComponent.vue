<template>
  <div class="main">
    <v-subheader> Card </v-subheader>
    <v-divider></v-divider>
    <CardInfo></CardInfo>
    <br />

    <v-subheader> Text Feild </v-subheader>
    <v-divider></v-divider>
    <TextField
      v-model="TextFieldValue"
      labelText="Add Account ID"
      icon="mdi-alert-circle-outline"
      placeholderText="Account name"
      v-bind:required="true"
    ></TextField>
    {{ TextFieldValue }}
    <br />

    <v-subheader> Button </v-subheader>
    <v-divider></v-divider>
    <huxButton
      ButtonText="Added"
      v-bind:isOutlined="true"
      size="large"
      icon="mdi-check"
      iconPosition="left"
    ></huxButton>
    <huxButton
      ButtonText="Add"
      v-bind:isOutlined="true"
      size="x-small"
      variant="darkGrey"
    ></huxButton>
    <huxButton
      ButtonText="Leave configuration"
      variant="primary"
      size="large"
      v-bind:isTile="true"
    ></huxButton>
    <huxButton
      ButtonText="Success!"
      icon="mdi-check"
      iconPosition="left"
      variant="success"
      size="x-large"
      v-bind:isTile="true"
    ></huxButton>
    <huxButton
      ButtonText="Cancel &amp; Return"
      variant="tertiary"
      v-bind:isTile="true"
    ></huxButton>
    <huxButton
      ButtonText="Disabled"
      variant="tertiary"
      v-bind:isTile="true"
      v-bind:isDisabled="true"
    ></huxButton>
    <huxButton
      ButtonText="Loader"
      variant="tertiary"
      v-bind:isTile="true"
      v-bind:enableLoading="true"
    ></huxButton>
    <br />

    <v-subheader> Select Dropdown </v-subheader>
    <v-divider></v-divider>
    <DropdownMenu
      v-model="DropdownValue"
      v-bind:labelText="labelText"
      v-bind:menuItem="DropdownData"
      @updatelabelText="onupdatelabelText"
    ></DropdownMenu>
    {{ DropdownValue }}
    <br />

    <v-subheader> Page Header </v-subheader>
    <v-divider></v-divider>
    <PageHeader>
      <template slot="left">
        <Breadcrumb :items="items" />
      </template>
    </PageHeader>
    <br />

    <v-subheader> Hux Table</v-subheader>
    <v-divider></v-divider>
    <br />
    <hux-table
      :columnDef="columnDefs"
      :tableData="rowData"
      height="250px"
      hasCheckBox
    ></hux-table>

    <v-subheader> Drawer</v-subheader>
    <v-divider></v-divider>
    <br />
    <button @click="drawer = !drawer">Toggle</button>
    <drawer v-model="drawer">
      <template v-slot:header-left>
        <h2>Heading</h2>
      </template>
      <template v-slot:header-right>
        <v-icon color="black"> mdi-dots-vertical </v-icon>
      </template>
      <template v-slot:default>
        <Button />
      </template>
      <template v-slot:footer-left>
        <h2>Heading</h2>
      </template>
      <template v-slot:footer-right>
        <v-icon color="black"> mdi-dots-vertical </v-icon>
      </template>
    </drawer>
    <br />

     <v-subheader> Metric Card</v-subheader>
     <v-divider></v-divider>
     <MetricCard class="ma-4"></MetricCard>
  </div>
</template>

<script>
import CardInfo from "@/components/common/CardInfo"
import Breadcrumb from "@/components/common/Breadcrumb"
import TextField from "@/components/common/TextField"
import HuxTable from "@/components/common/huxTable.vue"
import huxButton from "@/components/common/huxButton"
import DropdownMenu from "@/components/common/DropdownMenu"
import PageHeader from "@/components/PageHeader"
import Drawer from "@/components/common/Drawer"
import MetricCard from "@/components/common/MetricCard"

export default {
  name: "CommonComponent",
  components: {
    CardInfo,
    Breadcrumb,
    TextField,
    huxButton,
    DropdownMenu,
    PageHeader,
    HuxTable,
    Drawer,
    MetricCard,
  },
  methods: {
    onupdatelabelText(newValue) {
      this.labelText = newValue
    },
  },
  data() {
    return {
      TextFieldValue: null,
      DropdownValue: null,
      labelText: "Select",
      DropdownData: [
        { value: "1 - 25" },
        { value: "26 - 50" },
        { value: "50+" },
      ],
      columnDefs: [
        {
          headerName: "Audience Name",
          field: "audienceName",
          sortable: true,
          sort: "desc",
        },
        { headerName: "Goals", field: "goals", sortable: true },
        { headerName: "Status", field: "status", sortable: true },
        { headerName: "Size", field: "size", sortable: true },
        { headerName: "Destinations", field: "destinations", sortable: true },
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
        },
        { headerName: "Created", field: "created", sortable: true },
        { headerName: "Created By", field: "createdBy", sortable: true },
      ],

      rowData: [
        {
          audienceName: "Audience Name 1",
          goals: "Goal",
          status: "Active",
          size: 1000,
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
          goals: "Goal",
          status: "Active",
          size: 1000,
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
          goals: "Goal",
          status: "Active",
          size: 1000,
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
          goals: "Goal",
          status: "Active",
          size: 1000,
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
          goals: "Goal",
          status: "Active",
          size: 1000,
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
          goals: "Goal",
          status: "Active",
          size: 1000,
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
          goals: "Goal",
          status: "Active",
          size: 1000,
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
          goals: "Goal",
          status: "Active",
          size: 1000,
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
          goals: "Goal",
          status: "Active",
          size: 1000,
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
          goals: "Goal",
          status: "Active",
          size: 1000,
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
          goals: "Goal",
          status: "Active",
          size: 1000,
          destinations: "SFMC",
          attributes: "Churn",
          lastDelivered: "Today, 12:00 PM",
          lastUpdated: "Today, 12:00 PM",
          lastUpdatedBy: "HR",
          created: "Today, 12:00 PM",
          createdBy: "RG",
        },
      ],
      items: [
        {
          text: "Home",
          disabled: false,
          href: "overview",
          icon: "mdi-home-outline",
        },
        {
          text: "Connections",
          disabled: false,
          href: "connections",
          icon: "mdi-bullhorn-outline",
        },
        {
          text: "Destinations",
          disabled: true,
          href: "connections/destinations",
          icon: "mdi-flip-h mdi-account-plus-outline",
        },
      ],

      drawer: false,
    }
  },
  mounted() {},
}
</script>
<style lang="scss" scoped>
.main {
  margin: 10px;
}
</style>
