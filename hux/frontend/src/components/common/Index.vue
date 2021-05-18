<template>
  <v-container>
    <v-subheader> Info Card </v-subheader>
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
      class="ma-2"
    ></huxButton>
    <huxButton
      ButtonText="Add"
      v-bind:isOutlined="true"
      size="x-small"
      variant="darkGrey"
      class="ma-2"
    ></huxButton>
    <huxButton
      ButtonText="Leave configuration"
      variant="primary"
      size="large"
      v-bind:isTile="true"
      class="ma-2"
    ></huxButton>
    <huxButton
      ButtonText="Success!"
      icon="mdi-check"
      iconPosition="left"
      variant="success"
      size="x-large"
      v-bind:isTile="true"
      class="ma-2"
    ></huxButton>
    <huxButton
      ButtonText="Cancel &amp; Return"
      variant="tertiary"
      v-bind:isTile="true"
      class="ma-2"
    ></huxButton>
    <huxButton
      ButtonText="Disabled"
      variant="tertiary"
      v-bind:isTile="true"
      v-bind:isDisabled="true"
      class="ma-2"
    ></huxButton>
    <huxButton
      ButtonText="Loader"
      variant="tertiary"
      v-bind:isTile="true"
      v-bind:enableLoading="true"
      class="ma-2"
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

    <v-subheader> Multilevel Select Dropdown </v-subheader>
    <hux-dropdown
      :label="selectedMenuItem"
      :selected="selectedMenuItem"
      :items="menuItems"
      @on-select="onSelectMenuItem"
    />

    <v-divider class="mt-10" />

    <v-subheader> Page Header </v-subheader>
    <PageHeader>
      <template slot="left">
        <Breadcrumb :items="items" />
      </template>
    </PageHeader>

    <v-divider class="mt-10" />

    <v-subheader> Hux Slider</v-subheader>
    <huxSlider :min="0" :max="1" :step="0.05" v-model="sliderRange" />

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

    <v-subheader> Headings </v-subheader>
    <p v-for="i in 6" :class="`text-h${i}`" :key="i">Heading {{ i }}</p>

    <v-divider class="mt-10" />

    <v-subheader> Descriptive Card </v-subheader>
    <DescriptiveCard
      icon="model-unsubscribe"
      title="Propensity to Unsubscribe"
      description="Propensity of a customer making a purchase after receiving an email."
    >
      <template slot="top">
        <Status status="pending" collapsed class="d-flex" />
      </template>

      <template slot="default">
        <p class="text-caption gray--text">Sarah Miller</p>

        <div class="d-flex justify-center mb-6">
          <CardStat label="Version" value="0.02" stat-class="border-0">
            <div class="mb-3">
              Trained date<br />
              12/22/2021 at 12:45pm
            </div>
            <div class="mb-3">
              Fulcrum date<br />
              12/20/2021
            </div>
            <div class="mb-3">
              Lookback period (days)<br />
              365
            </div>
            <div>
              Lookback period (days)<br />
              60
            </div>
          </CardStat>
          <CardStat label="Last trained" value="2 hrs ago">12:45pm</CardStat>
        </div>
      </template>
    </DescriptiveCard>

    <v-divider class="mt-10" />

    <v-subheader>Icons</v-subheader>
    <Icon type="model-unsubscribe" />
    <Icon type="model-unsubscribe" :size="48" color="secondary" />

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
import Status from "@/components/common/Status"
import Icon from "@/components/common/Icon"
import HuxSlider from "@/components/common/HuxSlider"
import HuxDropdown from "@/components/common/HuxDropdown"
import DescriptiveCard from "@/components/common/Cards/DescriptiveCard"
import CardStat from "@/components/common/Cards/Stat"

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
    DescriptiveCard,
    CardStat,
    HuxSlider,
    HuxDropdown,
    Status,
    Logo,
    Icon,
  },
  methods: {
    onupdatelabelText(newValue) {
      this.labelText = newValue
    },
    onSelectMenuItem(item) {
      console.log(item.name)
      if (this.selectedMenuItem == item.name) {
        this.selectedMenuItem = "Select a value..."
      } else {
        this.selectedMenuItem = item.name
      }
      if (item.action) {
        item.action()
      }
    },
  },
  data() {
    return {
      selectedMenuItem: "Select a value...",
      TextFieldValue: null,
      DropdownValue: null,
      labelText: "Select",
      sliderRange: [0.25, 0.65],
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

      menuItems: [
        {
          icon: "mdi-home-outline",
          name: "Menu Item 1",
          action: () => {
            console.log("menu-item-1")
          },
        },
        { isDivider: true },
        { icon: "mdi-bullhorn-outline", name: "Menu Item 2" },
        {
          name: "Sub 1",
          menu: [
            { icon: "mdi-home-outline", name: "1.1" },
            { icon: "mdi-bullhorn-outline", name: "1.2" },
            {
              name: "Sub-menu 2",
              menu: [
                { name: "2.1" },
                { name: "2.2" },
                {
                  name: "Sub-menu 3",
                  menu: [{ name: "3.1" }, { name: "3.2" }],
                },
              ],
            },
          ],
        },

        { icon: "mdi-flip-h mdi-account-plus-outline", name: "Menu Item 3" },
        { isDivider: true },
        {
          icon: "mdi-tune-vertical-variant",
          name: "Menu Item 4",
          action: () => {
            console.log("menu-item-4")
          },
        },
        {
          icon: "mdi-account-details-outline",
          name: "Menu Item 5",
          action: () => {
            console.log("menu-item-5")
          },
        },
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
