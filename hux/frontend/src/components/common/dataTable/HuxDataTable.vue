<template>
  <div class="hux-data-table">
    <v-data-table
      :headers="headers"
      :items="dataItems"
      :expanded.sync="expanded"
      show-expand
      item-key="name"
      :hide-default-footer="true"
    >
      <template v-slot:item="{ item, expand, isExpanded }">
        <tr>
          <td></td>
          <td v-for="field in Object.keys(item)" :key="field.name">
            <span v-if="field == 'engagementName'" class="primary--text">
              <v-icon
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
            <span v-else>
              <span v-if="field != 'child'">
                {{ item[field] }}
              </span>
            </span>
          </td>
        </tr>
      </template>
      <template v-slot:expanded-item="{ item }">
        <tr v-for="(field, index) in item.child" :key="index">
          <td></td>
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
          <td>{{ field.lastUpdatedBy }}</td>
          <td>{{ field.created }}</td>
          <td>{{ field.createdBy }}</td>
        </tr>
      </template>
    </v-data-table>
  </div>
</template>

<script>
export default {
  name: "HuxDataTable",
  components: {},
  props: {},
  data() {
    return {
      search: "",
      expanded: [],
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
      dataItems: [
        {
          engagementName: "Winter",
          audiences: 159,
          status: "Active",
          size: "476M",
          deliverySchedule: "Manual",
          lastUpdated: "1 week ago",
          lastUpdatedBy: "JS",
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
              lastUpdatedBy: "JS",
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
              lastUpdatedBy: "JS",
              created: "1 month ago",
              createdBy: "JS",
            },
          ],
        },
      ],
    }
  },
  computed: {},
  methods: {},
  beforeMount() {},
  mounted() {},
}
</script>

<style lang="scss" scoped>
.hux-data-table {
  .material-icons.delivered {
    color: var(--v-success-lighten1);
  }
  .material-icons.delivering {
    color: var(--v-success-lighten2);
  }
  .material-icons.alert {
    color: var(--v-error-base);
  }
  .rotate-icon {
    transition: 0.3s;
    -webkit-transition: 0.3s;
    -moz-transition: 0.3s;
    -ms-transition: 0.3s;
    -o-transition: 0.3s;
    -webkit-transform: rotate(90deg);
    -moz-transform: rotate(90deg);
    -o-transform: rotate(90deg);
    -ms-transform: rotate(90deg);
    transform: rotate(90deg);
  }
}
</style>
