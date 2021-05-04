<template>
  <v-container>
    <v-subheader> Card </v-subheader>
    <CardInfo></CardInfo>

    <v-divider class="mt-10" />

    <v-subheader> Text Field </v-subheader>
    <TextField
      v-model="TextFieldValue"
      labelText="Add Account ID"
      icon="mdi-alert-circle-outline"
      placeholderText="Account name"
      v-bind:required="true"
    ></TextField>
    {{ TextFieldValue }}

    <v-divider class="mt-10" />

    <v-subheader> Alert </v-subheader>
    <v-btn @click="alert = !alert">Toogle alert</v-btn>
    <HuxAlert
      v-model="alert"
      type="success"
      title="YAY!"
      message="This is a success message! It will disappear in 5 seconds on its own."
    />

    <v-divider class="mt-10" />

    <v-subheader> Button </v-subheader>
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

    <v-divider class="mt-10" />

    <v-subheader> Select Dropdown </v-subheader>
    <DropdownMenu
      v-model="DropdownValue"
      v-bind:labelText="labelText"
      v-bind:menuItem="DropdownData"
      @updatelabelText="onupdatelabelText"
    ></DropdownMenu>
    {{ DropdownValue }}

    <v-divider class="mt-10" />

    <v-subheader> Page Header </v-subheader>
    <PageHeader>
      <template slot="left">
        <Breadcrumb :items="items" />
      </template>
    </PageHeader>

    <v-divider class="mt-10" />

    <v-subheader> Hux Table</v-subheader>
    <hux-table
      :columnDef="columnDefs"
      :tableData="rowData"
      height="250px"
      hasCheckBox
    ></hux-table>

    <v-divider class="mt-10" />

    <v-subheader> Drawer</v-subheader>
    <v-btn @click="drawer = !drawer">Toggle Drawer</v-btn>
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

    <v-divider class="mt-10" />

    <v-subheader>Metric Card</v-subheader>
    <MetricCard
      class="ma-4"
      :width="135"
      :height="80"
      v-for="(item, i) in overviewListItems"
      :key="i"
      :title="item.title"
      :subtitle="item.subtitle"
      :icon="item.icon"
      :active="true"
    ></MetricCard>

    <v-divider class="mt-10" />

    <v-subheader>Logos</v-subheader>
    <Logo type="facebook"></Logo>
    <Logo type="facebook" :size="48"></Logo>

    <Logo type="tableau"></Logo>
    <Logo type="tableau" :size="48"></Logo>

    <Logo type="google-ads"></Logo>
    <Logo type="google-ads" :size="48"></Logo>

    <Logo type="google-analytics"></Logo>
    <Logo type="google-analytics" :size="48"></Logo>

    <Logo type="aqfer"></Logo>
    <Logo type="aqfer" :size="48"></Logo>

    <Logo type="netsuite"></Logo>
    <Logo type="netsuite" :size="48"></Logo>

    <Logo type="salesforce"></Logo>
    <Logo type="salesforce" :size="48"></Logo>

    <Logo type="twilio"></Logo>
    <Logo type="twilio" :size="48"></Logo>
  </v-container>
</template>

<script>
import CardInfo from "@/components/common/CardInfo"
import HuxAlert from "@/components/common/HuxAlert"
import Breadcrumb from "@/components/common/Breadcrumb"
import TextField from "@/components/common/TextField"
import HuxTable from "@/components/common/huxTable.vue"
import huxButton from "@/components/common/huxButton"
import DropdownMenu from "@/components/common/DropdownMenu"
import PageHeader from "@/components/PageHeader"
import Drawer from "@/components/common/Drawer"
import MetricCard from "@/components/common/MetricCard"
import Logo from "@/components/common/Logo"

export default {
  name: "Components",
  components: {
    CardInfo,
    HuxAlert,
    Breadcrumb,
    TextField,
    huxButton,
    DropdownMenu,
    PageHeader,
    HuxTable,
    Drawer,
    MetricCard,
    Logo,
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
      alert: false,

      overviewListItems: [
        { title: "Cities", subtitle: "19,495", icon: "mdi-map-marker-radius" },
      ],
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
