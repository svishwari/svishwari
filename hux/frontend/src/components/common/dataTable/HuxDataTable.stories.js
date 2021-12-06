import HuxDataTable from "@/components/common/dataTable/HuxDataTable"

export default {
    component: HuxDataTable,
  
    title: "Components",
  
    argTypes: {
      dataItems: { control: { type: "array" } },
      columns: { control: { type: "array" } },
    },
  
    args: {
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
    
          columns: [
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
    },
  
    parameters: {
      design: {
        type: "figma",
        url: "https://www.figma.com/file/4qNDv9mcu1ZWZkZxO3fVpP/6.0-Release?node-id=6852%3A108904",
      },
    },
  }

const Template = (args, { argTypes }) => ({
components: { HuxDataTable },
props: Object.keys(argTypes),
template: `
<div>
  <hux-data-table v-bind="$props" v-on="$props">
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
</div>
`,
})

export const DataTable = Template.bind({})
