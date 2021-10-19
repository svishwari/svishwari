<template>
  <v-container>
    <v-subheader> Data Table </v-subheader>
    <hux-data-table :columns="headers" :data-items="dataItems">
      <template #un-expanded-row="{ field, item, expand, isExpanded }">
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
            <template #activator="{ on, attrs }">
              <span
                class="avatar-border d-flex align-center justify-center"
                v-bind="attrs"
                :style="{ 'border-color': getColorCode(item[field]) }"
                v-on="on"
              >
                {{ item[field] }}
              </span>
            </template>
          </v-menu>
        </span>
        <span v-else-if="field == 'createdBy'">
          <v-menu bottom offset-y>
            <template #activator="{ on, attrs }">
              <span
                class="avatar-border d-flex align-center justify-center"
                v-bind="attrs"
                :style="{ 'border-color': getColorCode(item[field]) }"
                v-on="on"
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
      <template #expanded-row="{ field }">
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
            <template #activator="{ on, attrs }">
              <span
                class="avatar-border d-flex align-center justify-center"
                v-bind="attrs"
                :style="{
                  'border-color': getColorCode(field.lastUpdatedBy),
                }"
                v-on="on"
              >
                {{ field.lastUpdatedBy }}
              </span>
            </template>
          </v-menu>
        </td>
        <td>{{ field.created }}</td>
        <td>
          <v-menu bottom offset-y>
            <template #activator="{ on, attrs }">
              <span
                class="avatar-border d-flex align-center justify-center"
                v-bind="attrs"
                :style="{ 'border-color': getColorCode(field.createdBy) }"
                v-on="on"
              >
                {{ field.createdBy }}
              </span>
            </template>
          </v-menu>
        </td>
      </template>
    </hux-data-table>
    <v-divider class="mt-10" />
    <v-subheader> Info Card </v-subheader>
    <card-info></card-info>

    <v-divider class="mt-10" />

    <v-subheader> Text Field </v-subheader>
    <text-field
      v-model="TextFieldValue"
      label-text="Add Account ID"
      icon="mdi-alert-circle-outline"
      placeholder-text="Account name"
      required
    ></text-field>
    {{ TextFieldValue }}

    <v-divider class="mt-10" />

    <v-subheader> Modal </v-subheader>
    <confirm-modal
      v-model="errorModal"
      icon="sad-face"
      type="error"
      title="Action Word"
      sub-title="(i.e. Remove) ___________?"
      body="Are you sure you want to stop the configuration and go to another page? You will not be able to recover it but will need to start the process again."
      @onCancel="errorModal = !errorModal"
      @onConfirm="errorModal = !errorModal"
    >
      <template #activator>
        <huxButton size="large" class="ma-2" @click="errorModal = !errorModal">
          Error modal
        </huxButton>
      </template>
    </confirm-modal>

    <confirm-modal
      v-model="infoModal"
      icon="edit"
      type="primary"
      title="Edit"
      sub-title="<Audience>"
      body="Are you sure you want to remove the <Audience>?"
      @onCancel="infoModal = !infoModal"
      @onConfirm="infoModal = !infoModal"
    >
      <template #activator>
        <huxButton size="large" class="ma-2" @click="infoModal = !infoModal">
          Info modal
        </huxButton>
      </template>
    </confirm-modal>

    <v-divider class="mt-10" />

    <v-subheader> Button </v-subheader>
    <huxButton
      is-outlined
      size="large"
      icon="mdi-check"
      icon-position="left"
      class="ma-2"
    >
      Added
    </huxButton>
    <huxButton is-outlined size="x-small" variant="black darken-3" class="ma-2">
      Add
    </huxButton>
    <huxButton variant="primary" size="large" is-tile class="ma-2">
      Leave configuration
    </huxButton>
    <huxButton
      icon="mdi-check"
      icon-position="left"
      variant="success"
      size="x-large"
      is-tile
      class="ma-2"
    >
      Success!
    </huxButton>
    <huxButton variant="white" is-tile class="ma-2">
      Cancel &amp; Return
    </huxButton>
    <huxButton variant="white" is-tile is-disabled class="ma-2">
      Disabled
    </huxButton>
    <huxButton variant="white" is-tile enable-loading class="ma-2">
      Loader
    </huxButton>

    <v-divider class="mt-10" />

    <v-subheader> Select Dropdown </v-subheader>
    <dropdown-menu
      v-model="DropdownValue"
      :label-text="labelText"
      :menu-item="DropdownData"
      @updatelabelText="onupdatelabelText"
    ></dropdown-menu>
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
    <v-subheader> Start Date Picker </v-subheader>
    <hux-start-date
      :label="selectedStartDate"
      :selected="selectedStartDate"
      @on-date-select="onStartDateSelect"
    />
    <v-divider class="mt-10" />
    <v-subheader> End Date Picker </v-subheader>
    <hux-end-date
      :label="selectedEndDate"
      :selected="selectedEndDate"
      :is-sub-menu="true"
      @on-date-select="onEndDateSelect"
    />
    <v-divider class="mt-10" />

    <v-subheader> Page Header </v-subheader>
    <page-header>
      <template slot="left">
        <breadcrumb :items="items" />
      </template>
    </page-header>

    <v-divider class="mt-10" />

    <v-subheader> Hux Range Slider</v-subheader>
    <hux-slider
      v-model="sliderRange"
      :is-range-slider="true"
      :min="0"
      :max="1"
      :step="0.05"
    />

    <v-divider class="mt-10" />

    <v-subheader> Hux Table</v-subheader>
    <hux-table
      :column-def="columnDefs"
      :table-data="rowData"
      height="250px"
      has-check-box
    ></hux-table>

    <v-divider class="mt-10" />

    <v-subheader> Drawer</v-subheader>
    <v-btn @click="drawer = !drawer">Toggle Drawer</v-btn>
    <drawer v-model="drawer">
      <template #header-left>
        <h2>Heading</h2>
      </template>
      <template #header-right>
        <v-icon color="black"> mdi-dots-vertical </v-icon>
      </template>
      <template #default>
        <Button />
      </template>
      <template #footer-left>
        <h2>Heading</h2>
      </template>
      <template #footer-right>
        <v-icon color="black"> mdi-dots-vertical </v-icon>
      </template>
    </drawer>

    <v-divider class="mt-10" />

    <v-subheader>Metric Card</v-subheader>

    <metric-card
      class="ma-4"
      title="Metric Title"
      :max-width="202"
      :height="75"
      :interactable="false"
    >
      <template #subtitle-extended>
        <div class="text-body-1 black--text text--darken-4 mb-2">
          <icon class="mr-1" type="stock-up" :size="8" color="success" />
          <icon class="ml-1 mr-1" type="stock-down" :size="8" color="error" />
          3/1/2021 • 9:42AM
        </div>
      </template>
    </metric-card>

    <metric-card
      class="ma-4"
      title="Metric Title"
      :max-width="180"
      :height="75"
      :interactable="false"
    >
      <template #subtitle-extended>
        <div class="text-body-1 black--text text--darken-4 mb-2">
          3/1/2021 • 9:42AM
        </div>
      </template>
    </metric-card>

    <metric-card
      class="ma-4"
      title="Metric Title"
      :max-width="180"
      :height="75"
      :interactable="true"
    >
      <template #subtitle-extended>
        <div class="text-body-1 black--text text--darken-4 mb-2">
          3/1/2021 • 9:42AM
        </div>
      </template>
    </metric-card>

    <metric-card class="ma-4" title="Created on" :max-width="186" :height="75">
      <template #subtitle-extended>
        <span class="mr-2">
          <tooltip>
            <template #label-content>
              <span class="text-body-1 black--text text--darken-4">
                4 hours ago by
              </span>
            </template>
            <template #hover-content> 10/18/2021 at 8:37 AM </template>
          </tooltip>
        </span>
        <span class="mt-n2">
          <avatar name="Sarah Huxley" />
        </span>
      </template>
    </metric-card>

    <metric-card
      class="ma-4"
      title="Description"
      :max-width="400"
      :height="75"
      :interactable="false"
    >
      <template #subtitle-extended>
        <div class="text-body-1 black--text text--darken-4 mb-2">
          this is where the description text...
        </div>
      </template>
    </metric-card>

    <metric-card
      class="ma-4"
      :max-width="128"
      :height="75"
      title="0.01"
      subtitle="AUC"
      :high-level="true"
      :interactable="false"
    >
    </metric-card>

    <v-divider class="mt-10" />

    <v-subheader> Headings </v-subheader>
    <p v-for="i in 6" :key="i" :class="`text-h${i}`">Heading {{ i }}</p>

    <v-divider class="mt-10" />

    <v-subheader> Form Steps </v-subheader>
    <form-steps class="white pa-10">
      <form-step :step="1" label="General information" optional>
        Contents for step 1
      </form-step>

      <form-step :step="2" label="Select attribute(s)" border="inactive">
        Contents for step 2
      </form-step>

      <form-step :step="3" :disabled="true">
        Contents for disabled step 3
      </form-step>
    </form-steps>

    <v-divider class="mt-10" />

    <v-subheader> Data Cards </v-subheader>
    <data-cards
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
    </data-cards>

    <v-btn class="mr-4" @click="DataCards.bordered = !DataCards.bordered">
      Toggle bordered
    </v-btn>
    <v-btn class="mr-4" @click="DataCards.items.push(DataCards.newItem)">
      Add item
    </v-btn>
    <v-text-field
      v-model="DataCards.empty"
      label="Empty text"
      class="d-inline-flex"
    />

    <v-divider class="mt-10" />

    <v-subheader> Descriptive Card </v-subheader>
    <descriptive-card
      icon="model-unsubscribe"
      title="Propensity to Unsubscribe"
      description="Propensity of a customer making a purchase after receiving an email."
    >
      <template slot="top">
        <status status="Pending" collapsed class="d-flex" />
      </template>

      <template slot="default">
        <p class="text-caption black--text text--darken-1">Sarah Miller</p>

        <div class="d-flex justify-center mb-6">
          <card-stat label="Version" value="0.02" stat-class="border-0">
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
          </card-stat>
          <card-stat label="Last trained" value="2 hrs ago">12:45pm</card-stat>
        </div>
      </template>
    </descriptive-card>

    <v-divider class="mt-10" />

    <v-subheader>Icons</v-subheader>
    <icon type="model-unsubscribe" />
    <icon type="model-unsubscribe" :size="48" color="primary-lighten8" />

    <v-divider class="mt-10" />

    <v-subheader>Score Slider</v-subheader>
    <hux-slider :is-range-slider="false" :value="0.45"></hux-slider>

    <v-divider class="mt-10" />

    <v-subheader>Hux Identity Chart</v-subheader>
    <chord-chart
      v-model="chartData"
      :color-codes="colorCodes"
      :chart-legends-data="chartLegendsData"
    />

    <v-divider class="mt-10" />
    <v-subheader>Donut Chart</v-subheader>
    <div class="gender-chart">
      <doughnut-chart
        :chart-dimensions="genderChartDimensions"
        :data="genderChartData"
        label="Gender"
        data-e2e="gender-chart"
      ></doughnut-chart>
    </div>

    <v-divider class="mt-10" />

    <v-container class="my-4">
      <v-row align="baseline">
        <v-col></v-col>
        <v-col v-for="(legend, index) in chartLegendsData" :key="legend">
          <label :style="`color:${colorCodes[index]}`">
            <strong>{{ legend.prop }}</strong>
          </label>
        </v-col>
      </v-row>
      <v-row v-for="(row, index) in chartData" :key="row" align="center">
        <v-col class="text-right">
          <label :style="`color:${colorCodes[index]}`">
            <strong>{{ chartLegendsData[index].prop }}</strong>
          </label>
        </v-col>
        <v-col v-for="(value, subindex) in row" :key="value">
          <input
            v-if="index !== subindex"
            v-model.lazy="chartData[index][subindex]"
            solo
            dense
            type="number"
            class="white pa-2 shadow"
          />
        </v-col>
      </v-row>
    </v-container>

    <v-divider class="mt-10" />

    <v-subheader>Hux Map Chart with Tooltip</v-subheader>
    <map-chart></map-chart>

    <v-divider class="mt-10" />

    <v-subheader>Logos</v-subheader>
    <logo type="bluecore"></logo>
    <logo type="bluecore" :size="48"></logo>

    <logo type="facebook"></logo>
    <logo type="facebook" :size="48"></logo>

    <logo type="tableau"></logo>
    <logo type="tableau" :size="48"></logo>

    <logo type="google-ads"></logo>
    <logo type="google-ads" :size="48"></logo>

    <logo type="google-analytics"></logo>
    <logo type="google-analytics" :size="48"></logo>

    <logo type="aqfer"></logo>
    <logo type="aqfer" :size="48"></logo>

    <logo type="netsuite"></logo>
    <logo type="netsuite" :size="48"></logo>

    <logo type="sfmc"></logo>
    <logo type="sfmc" :size="48"></logo>

    <logo type="sendgrid"></logo>
    <logo type="sendgrid" :size="48"></logo>

    <logo type="qualtrics"></logo>
    <logo type="qualtrics" :size="48"></logo>
    <v-divider class="mt-10" />

    <v-subheader>Nested Data Table</v-subheader>
    <hux-data-table :columns="headerNest" :data-items="dataItemsNest" nested>
      <template #item-row="{ item, expand, isExpanded }">
        <tr :class="{ 'expanded-row': isExpanded }">
          <td
            v-for="header in headerNest"
            :key="header.value"
            :class="{
              'expanded-row': isExpanded,
            }"
            :style="{ width: header.width, left: 0 }"
          >
            <div v-if="header.value == 'name'" class="w-80">
              <v-icon
                :class="{ 'normal-icon': isExpanded }"
                @click="expand(!isExpanded)"
              >
                mdi-chevron-right
              </v-icon>
              {{ item[header.value] }}
            </div>
            <div v-if="header.value == 'audiences'">
              {{ item[header.value] }}
            </div>
            <div v-if="header.value == 'status'">
              <status
                :status="item[header.value]"
                :show-label="true"
                collapsed
                class="d-flex"
                :icon-size="17"
              />
            </div>
            <div v-if="header.value == 'size'">
              <size :value="item[header.value]" />
            </div>
          </td>
        </tr>
      </template>
      <template #expanded-row="{ expandedHeaders, item }">
        <td :colspan="expandedHeaders.length" class="pa-0 child">
          <hux-data-table
            :columns="expandedHeaders"
            :data-items="item.child"
            :show-header="false"
            class="expanded-table"
            nested
          >
            <template #item-row="{ rowItem, expand, isExpanded }">
              <tr :class="{ 'expanded-row': isExpanded }">
                <td
                  v-for="header in headerNest"
                  :key="header.value"
                  :colspan="header.value == 'name' ? 0 : 0"
                  :class="{
                    'expanded-row': isExpanded,
                  }"
                >
                  <div v-if="header.value == 'name'">
                    <v-icon
                      :class="{ 'normal-icon': isExpanded }"
                      @click="expand(!isExpanded)"
                    >
                      mdi-chevron-right
                    </v-icon>
                    {{ rowItem[header.value] }}
                  </div>
                  <div v-if="header.value == 'audiences'">
                    <div>
                      <size :value="rowItem[header.value]" />
                    </div>
                  </div>
                  <div v-if="header.value == 'status'">
                    <status
                      :status="rowItem[header.value]"
                      :show-label="true"
                      collapsed
                      class="d-flex"
                      :icon-size="17"
                    />
                  </div>
                  <div v-if="header.value == 'size'">
                    <size :value="rowItem[header.value]" />
                  </div>
                </td>
              </tr>
            </template>
            <template #expanded-row="{ subExpandedHeaders, expandedItem }">
              <td :colspan="subExpandedHeaders.length" class="pa-0 child">
                <hux-data-table
                  :columns="subExpandedHeaders"
                  :data-items="expandedItem.childNest"
                  :show-header="false"
                  class="expanded-table"
                  nested
                >
                  <template #item-row="{ rowItem }">
                    <tr>
                      <td
                        v-for="subHeader in headerNest"
                        :key="subHeader.value"
                        :style="{ width: subHeader.width, left: 0 }"
                      >
                        <div v-if="subHeader.value == 'name'">
                          {{ rowItem[subHeader.value] }}
                        </div>
                        <div v-if="subHeader.value == 'audiences'">
                          <div>
                            <size :value="rowItem[subHeader.value]" />
                          </div>
                        </div>
                        <div v-if="subHeader.value == 'status'">
                          <status
                            :status="rowItem[subHeader.value]"
                            :show-label="true"
                            collapsed
                            class="d-flex"
                            :icon-size="17"
                          />
                        </div>
                        <div v-if="subHeader.value == 'size'">
                          <size :value="rowItem[subHeader.value]" />
                        </div>
                      </td>
                    </tr>
                  </template>
                </hux-data-table>
              </td>
            </template>
          </hux-data-table>
        </td>
      </template>
    </hux-data-table>
  </v-container>
</template>

<script>
import CardInfo from "@/components/common/CardInfo"
import ConfirmModal from "@/components/common/ConfirmModal"
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
import ChordChart from "@/components/common/identityChart/ChordChart"
import MapChart from "@/components/common/MapChart/MapChart"
import { generateColor } from "@/utils"
import Size from "@/components/common/huxTable/Size.vue"
import HuxStartDate from "@/components/common/DatePicker/HuxStartDate"
import HuxEndDate from "@/components/common/DatePicker/HuxEndDate"
import DoughnutChart from "@/components/common/DoughnutChart/DoughnutChart"
import demographicsData from "@/api/mock/fixtures/demographicData.js"
import Tooltip from "@/components/common/Tooltip.vue"
import Avatar from "@/components/common/Avatar"

export default {
  name: "Components",
  components: {
    CardInfo,
    ConfirmModal,
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
    ChordChart,
    MapChart,
    Size,
    HuxStartDate,
    HuxEndDate,
    DoughnutChart,
    Tooltip,
    Avatar,
  },
  data() {
    return {
      genderChartDimensions: {
        width: 269,
        height: 200,
      },
      genderChartData: [
        {
          label: "Men",
          population_percentage:
            demographicsData.gender.gender_men.population_percentage,
          size: demographicsData.gender.gender_men.size,
        },
        {
          label: "Women",
          population_percentage:
            demographicsData.gender.gender_women.population_percentage,
          size: demographicsData.gender.gender_women.size,
        },
        {
          label: "Other",
          population_percentage:
            demographicsData.gender.gender_other.population_percentage,
          size: demographicsData.gender.gender_other.size,
        },
      ],
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
      selectedStartDate: "Select date",
      selectedEndDate: "Select date",
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
      errorModal: false,
      infoModal: false,

      overviewListItems: [
        { title: "Cities", subtitle: "19,495", icon: "mdi-map-marker-radius" },
      ],

      menuItems: [
        {
          icon: "mdi-home-outline",
          name: "Menu Item 1",
          action: () => {},
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
          action: () => {},
        },
        {
          icon: "mdi-account-details-outline",
          name: "Menu Item 5",
          action: () => {},
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
      headerNest: [
        { text: "Engagement name", value: "name", width: "auto" },
        { text: "Audiences", value: "audiences", width: "auto" },
        { text: "Status", value: "status", width: "auto" },
        { text: "Size", value: "size", width: "auto" },
      ],

      dataItemsNest: [
        {
          name: "Winter",
          audiences: 159,
          status: "Active",
          size: 1000,
          deliverySchedule: "Manual",
          lastUpdated: "1 week ago",
          lastUpdatedBy: "AZ",
          created: "1 month ago",
          createdBy: "JS",
          child: [
            {
              name: "Frozen goods",
              audiences: 209,
              status: "Delivering",
              size: 2000,
              deliverySchedule: "-",
              lastUpdated: "1 week ago",
              lastUpdatedBy: "SA",
              created: "1 month ago",
              createdBy: "JS",
              childNest: [
                {
                  name: "Goods Frozen",
                  audiences: 259,
                  status: "Delivered",
                  size: "565k",
                  deliverySchedule: "-",
                  lastUpdated: "1 week ago",
                  lastUpdatedBy: "SA",
                  created: "1 month ago",
                  createdBy: "JS",
                },
                {
                  name: "Goods Frozen 1",
                  audiences: 259,
                  status: "Delivering",
                  size: "565k",
                  deliverySchedule: "-",
                  lastUpdated: "1 week ago",
                  lastUpdatedBy: "SA",
                  created: "1 month ago",
                  createdBy: "JS",
                },
              ],
            },
            {
              name: "Texas",
              audiences: 109,
              status: "Delivering",
              size: 3000,
              deliverySchedule: "-",
              lastUpdated: "1 week ago",
              lastUpdatedBy: "PR",
              created: "1 month ago",
              createdBy: "JS",
              childNest: [
                {
                  name: "Texas goods",
                  audiences: 459,
                  status: "Delivered",
                  size: 0,
                  deliverySchedule: "-",
                  lastUpdated: "1 week ago",
                  lastUpdatedBy: "SA",
                  created: "1 month ago",
                  createdBy: "JS",
                },
                {
                  name: "Texas goods 1",
                  audiences: 459,
                  status: "Delivering",
                  size: 0,
                  deliverySchedule: "-",
                  lastUpdated: "1 week ago",
                  lastUpdatedBy: "SA",
                  created: "1 month ago",
                  createdBy: "JS",
                },
              ],
            },
          ],
        },
        {
          name: "Summer",
          audiences: 100,
          status: "Active",
          size: 1000,
          deliverySchedule: "Manual",
          lastUpdated: "1 week ago",
          lastUpdatedBy: "JS",
          created: "1 month ago",
          createdBy: "JS",
          child: [
            {
              name: "Goods",
              audiences: 209,
              status: "Delivering",
              size: 2000,
              deliverySchedule: "-",
              lastUpdated: "1 week ago",
              lastUpdatedBy: "SA",
              created: "1 month ago",
              createdBy: "JS",
              childNest: [
                {
                  name: "Summer goods",
                  audiences: 159,
                  status: "Delivered",
                  size: 0,
                  deliverySchedule: "-",
                  lastUpdated: "1 week ago",
                  lastUpdatedBy: "SA",
                  created: "1 month ago",
                  createdBy: "JS",
                },
                {
                  name: "Summer goods 1",
                  audiences: 159,
                  status: "Delivering",
                  size: 0,
                  deliverySchedule: "-",
                  lastUpdated: "1 week ago",
                  lastUpdatedBy: "SA",
                  created: "1 month ago",
                  createdBy: "JS",
                },
              ],
            },
            {
              name: "Texas Summer",
              audiences: 109,
              status: "Active",
              size: 3000,
              deliverySchedule: "-",
              lastUpdated: "1 week ago",
              lastUpdatedBy: "PR",
              created: "1 month ago",
              createdBy: "JS",
              childNest: [
                {
                  name: "Goods Texas Summer",
                  audiences: 359,
                  status: "Delivered",
                  size: 56,
                  deliverySchedule: "-",
                  lastUpdated: "1 week ago",
                  lastUpdatedBy: "SA",
                  created: "1 month ago",
                  createdBy: "JS",
                },
                {
                  name: "Goods Texas Summer 1",
                  audiences: 139,
                  status: "Delivering",
                  size: 565,
                  deliverySchedule: "-",
                  lastUpdated: "1 week ago",
                  lastUpdatedBy: "SA",
                  created: "1 month ago",
                  createdBy: "JS",
                },
              ],
            },
          ],
        },
      ],
      chartData: [
        [0, 30, 40, 10, 20],
        [30, 0, 15, 45, 10],
        [40, 15, 0, 25, 10],
        [10, 45, 25, 0, 20],
        [20, 10, 10, 20, 0],
      ],
      colorCodes: ["#005587", "#da291c", "#00a3e0", "#43b02a", "#efa34c"],
      chartLegendsData: [
        { prop: "Name", icon: "name", color: "#005587" },
        { prop: "Address", icon: "address", color: "#da291c" },
        { prop: "Email", icon: "email", color: "#00a3e0" },
        { prop: "Phone", icon: "phone", color: "#43b02a" },
        { prop: "Cookie", icon: "cookie", color: "#efa34c" },
      ],
    }
  },
  mounted() {},
  methods: {
    onupdatelabelText(newValue) {
      this.labelText = newValue
    },
    onSelectMenuItem(item) {
      if (this.selectedMenuItem == item.name) {
        this.selectedMenuItem = "Select a value..."
      } else {
        this.selectedMenuItem = item.name
      }
      if (item.action) {
        item.action()
      }
    },
    onStartDateSelect(val) {
      this.selectedStartDate = val
    },
    onEndDateSelect(val) {
      this.selectedEndDate = val
    },
    getColorCode(name) {
      return generateColor(name, 30, 60) + " !important"
    },
  },
}
</script>
<style lang="scss" scoped>
.main {
  margin: 10px;
}
::v-deep .hux-data-table.expanded-table {
  .v-data-table__wrapper {
    box-shadow: inset 0px 10px 10px -4px var(--v-black-lighten3) !important;
    .child-row {
      padding-left: 317px;
      border-right: none;
    }
  }
  td:nth-child(1) {
    background: none;
  }
}
.mdi-chevron-right {
  margin-top: -4px;
  transition: 0.3s cubic-bezier(0.25, 0.8, 0.5, 1), visibility 0s;
  &.normal-icon {
    transform: rotate(90deg);
  }
}
.gender-chart {
  width: 255px;
}
</style>
