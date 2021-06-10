<template>
  <v-container>
    <v-subheader> Data Table </v-subheader>
    <HuxDataTable v-bind:headers="headers" v-bind:dataItems="dataItems">
      <template v-slot:un-expanded-row="{ field, item, expand, isExpanded }">
        <span v-if="field == 'engagementName'" class="primary--text">
          <v-icon
            v-if="'child' in item"
            color="primary"
            :class="{ 'rotate-icon': isExpanded }"
            @click="expand(!isExpanded)"
          >
            mdi-chevron-right
          </v-icon>
          {{ item[field] }}
        </span>
        <span v-else-if="field == 'status'">
          <v-icon
            v-if="item[field] == 'Active'"
            class="material-icons delivered"
          >
            mdi-checkbox-blank-circle
          </v-icon>
          <v-icon
            v-if="item[field] == 'Delivering'"
            class="material-icons alert"
          >
            mdi-alert-circle
          </v-icon>
        </span>
        <span v-else-if="field == 'lastUpdatedBy'">
          <v-menu bottom offset-y>
            <template v-slot:activator="{ on, attrs }">
              <span
                class="avatar-border d-flex align-center justify-center"
                v-bind="attrs"
                v-on="on"
                v-bind:style="{ 'border-color': getColorCode(item[field]) }"
              >
                {{ item[field] }}
              </span>
            </template>
          </v-menu>
        </span>
        <span v-else-if="field == 'createdBy'">
          <v-menu bottom offset-y>
            <template v-slot:activator="{ on, attrs }">
              <span
                class="avatar-border d-flex align-center justify-center"
                v-bind="attrs"
                v-on="on"
                v-bind:style="{ 'border-color': getColorCode(item[field]) }"
              >
                {{ item[field] }}
              </span>
            </template>
          </v-menu>
        </span>
        <span v-else>
          <span v-if="field != 'child'">
            {{ item[field] }}
          </span>
        </span>
      </template>
      <template v-slot:expanded-row="{ field }">
        <td class="primary--text">{{ field.engagementName }}</td>
        <td>{{ field.audiences }}</td>
        <td>
          <v-icon
            v-if="field.status == 'Active'"
            class="material-icons delivered"
          >
            mdi-checkbox-blank-circle
          </v-icon>
          <v-icon
            v-if="field.status == 'Delivering'"
            class="material-icons alert"
          >
            mdi-alert-circle
          </v-icon>
        </td>
        <td>{{ field.size }}</td>
        <td>{{ field.deliverySchedule }}</td>
        <td>{{ field.lastUpdated }}</td>
        <td>
          <v-menu bottom offset-y>
            <template v-slot:activator="{ on, attrs }">
              <span
                class="avatar-border d-flex align-center justify-center"
                v-bind="attrs"
                v-on="on"
                v-bind:style="{
                  'border-color': getColorCode(field.lastUpdatedBy),
                }"
              >
                {{ field.lastUpdatedBy }}
              </span>
            </template>
          </v-menu>
        </td>
        <td>{{ field.created }}</td>
        <td>
          <v-menu bottom offset-y>
            <template v-slot:activator="{ on, attrs }">
              <span
                class="avatar-border d-flex align-center justify-center"
                v-bind="attrs"
                v-on="on"
                v-bind:style="{ 'border-color': getColorCode(field.createdBy) }"
              >
                {{ field.createdBy }}
              </span>
            </template>
          </v-menu>
        </td>
      </template>
    </HuxDataTable>
    <v-divider class="mt-10" />
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

    <v-subheader> Modal </v-subheader>
    <ConfirmModal
      v-model="modal"
      type="primary"
      title="Action Word (i.e. Remove) ___________?"
      body="Are you sure you want to stop the configuration and go to another page? You will not be able to recover it but will need to start the process again."
      @onCancel="toggleModal()"
      @onConfirm="toggleModal()"
    >
      <template v-slot:activator>
        <huxButton size="large" class="ma-2" @click="modal = !modal">
          Open modal
        </huxButton>
      </template>
    </ConfirmModal>

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
      v-bind:isOutlined="true"
      size="large"
      icon="mdi-check"
      iconPosition="left"
      class="ma-2"
    >
      Added
    </huxButton>
    <huxButton
      v-bind:isOutlined="true"
      size="x-small"
      variant="darkGrey"
      class="ma-2"
    >
      Add
    </huxButton>
    <huxButton variant="primary" size="large" v-bind:isTile="true" class="ma-2">
      Leave configuration
    </huxButton>
    <huxButton
      icon="mdi-check"
      iconPosition="left"
      variant="success"
      size="x-large"
      v-bind:isTile="true"
      class="ma-2"
    >
      Success!
    </huxButton>
    <huxButton variant="tertiary" v-bind:isTile="true" class="ma-2">
      Cancel &amp; Return
    </huxButton>
    <huxButton
      variant="tertiary"
      v-bind:isTile="true"
      v-bind:isDisabled="true"
      class="ma-2"
    >
      Disabled
    </huxButton>
    <huxButton
      variant="tertiary"
      v-bind:isTile="true"
      v-bind:enableLoading="true"
      class="ma-2"
    >
      Loader
    </huxButton>

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

    <v-subheader> Hux Range Slider</v-subheader>
    <hux-slider
      :isRangeSlider="true"
      :min="0"
      :max="1"
      :step="0.05"
      v-model="sliderRange"
    />

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

    <v-subheader> Form Steps </v-subheader>
    <FormSteps class="white pa-10">
      <FormStep :step="1" label="General information" optional>
        Contents for step 1
      </FormStep>

      <FormStep :step="2" label="Select attribute(s)" border="inactive">
        Contents for step 2
      </FormStep>

      <FormStep :step="3" :disabled="true">
        Contents for disabled step 3
      </FormStep>
    </FormSteps>

    <v-divider class="mt-10" />

    <v-subheader> Data Cards </v-subheader>
    <DataCards
      :items="DataCards.items"
      :fields="DataCards.fields"
      :bordered="DataCards.bordered"
      :empty="DataCards.empty"
    >
      <template #field:size="row">
        {{ row.value | Numeric(true, true) }}
      </template>

      <template #field:manage="row">
        <div class="d-flex justify-end">
          <v-btn
            icon
            color="primary"
            @click="
              DataCards.items.splice(
                DataCards.items.findIndex((item) => item.id === row.item.id),
                1
              )
            "
          >
            <v-icon>mdi-delete-outline</v-icon>
          </v-btn>
        </div>
      </template>
    </DataCards>

    <v-btn @click="DataCards.bordered = !DataCards.bordered" class="mr-4">
      Toggle bordered
    </v-btn>
    <v-btn @click="DataCards.items.push(DataCards.newItem)" class="mr-4">
      Add item
    </v-btn>
    <v-text-field
      v-model="DataCards.empty"
      label="Empty text"
      class="d-inline-flex"
    />

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

    <v-subheader>Score Slider</v-subheader>
    <hux-slider :isRangeSlider="false" :value="45"></hux-slider>

    <v-divider class="mt-10" />

    <v-subheader>Logos</v-subheader>
    <Logo type="bluecore"></Logo>
    <Logo type="bluecore" :size="48"></Logo>

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
import ConfirmModal from "@/components/common/ConfirmModal"
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
import HuxDropdown from "@/components/common/HuxDropdown"
import DescriptiveCard from "@/components/common/Cards/DescriptiveCard"
import CardStat from "@/components/common/Cards/Stat"
import FormSteps from "@/components/common/FormSteps"
import FormStep from "@/components/common/FormStep"
import DataCards from "@/components/common/DataCards"
import HuxDataTable from "@/components/common/dataTable/HuxDataTable"
import HuxSlider from "@/components/common/HuxSlider"
import { generateColor } from "@/utils"

export default {
  name: "Components",
  components: {
    CardInfo,
    ConfirmModal,
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
    HuxDropdown,
    Status,
    Logo,
    Icon,
    HuxDataTable,
    DataCards,
    FormSteps,
    FormStep,
    HuxSlider,
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
    toggleModal() {
      this.modal = !this.modal
    },
    getColorCode(name) {
      return generateColor(name, 30, 60) + " !important"
    },
  },
  data() {
    return {
      DataCards: {
        items: [
          {
            id: 1,
            name: "Data field name",
            description: "Data field description",
            size: 123456789,
          },
          {
            id: 2,
            name: "Another data field name",
            description: "Another data field description",
            size: 812380123,
          },
        ],
        newItem: {
          id: 3,
          name: "Data field name 3",
          description: "Data field description 3",
          size: 1251024101,
        },
        fields: [
          {
            key: "name",
            label: "Name",
            sortable: true,
          },
          {
            key: "description",
            label: "Description",
            sortable: false,
          },
          {
            key: "size",
            label: "Target size",
            sortable: true,
          },
          {
            key: "manage",
            sortable: false,
          },
        ],
        bordered: false,
        empty: "No items available.",
      },

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
          icon: "home",
        },
        {
          text: "Connections",
          disabled: false,
          href: "connections",
          icon: "connections",
        },
        {
          text: "Destinations",
          disabled: true,
          href: "connections/destinations",
          icon: "destinations",
        },
      ],

      drawer: false,
      modal: false,
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

      dataItems: [
        {
          engagementName: "Winter",
          audiences: 159,
          status: "Active",
          size: "176M",
          deliverySchedule: "Manual",
          lastUpdated: "1 week ago",
          lastUpdatedBy: "AZ",
          created: "1 month ago",
          createdBy: "JS",
          child: [
            {
              engagementName: "Frozen goods",
              audiences: 159,
              status: "Delivering",
              size: "565k",
              deliverySchedule: "-",
              lastUpdated: "1 week ago",
              lastUpdatedBy: "SA",
              created: "1 month ago",
              createdBy: "JS",
            },
            {
              engagementName: "Texas",
              audiences: 159,
              status: "Active",
              size: "30M",
              deliverySchedule: "-",
              lastUpdated: "1 week ago",
              lastUpdatedBy: "PR",
              created: "1 month ago",
              createdBy: "JS",
            },
          ],
        },
        {
          engagementName: "Summer",
          audiences: 100,
          status: "Active",
          size: "476M",
          deliverySchedule: "Manual",
          lastUpdated: "1 week ago",
          lastUpdatedBy: "JS",
          created: "1 month ago",
          createdBy: "JS",
        },
      ],

      headers: [
        {
          text: "Engagement name",
          align: "left",
          value: "engagementName",
        },
        { text: "Audiences", value: "audiences" },
        { text: "Status", value: "status" },
        { text: "Size", value: "size" },
        { text: "Delivery schedule", value: "deliverySchedule" },
        { text: "Last updated", value: "lastUpdated" },
        { text: "Last updated By", value: "lastUpdatedBy" },
        { text: "Created", value: "created" },
        { text: "Created By", value: "createdBy" },
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
