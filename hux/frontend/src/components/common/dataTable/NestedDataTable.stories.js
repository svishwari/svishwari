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
    
          columns: [
            { text: "Engagement name", value: "name", width: "auto" },
        { text: "Audiences", value: "audiences", width: "auto" },
        { text: "Status", value: "status", width: "auto" },
        { text: "Size", value: "size", width: "auto" },
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
computed: {
  headerNest() {
    return args.columns
  } 
},
template: `
<div>
<hux-data-table v-bind="$props" v-on="$props" nested>
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
</div>
`,
})

export const NestedDataTable = Template.bind({})
