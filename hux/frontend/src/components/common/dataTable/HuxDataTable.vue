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
            <slot
              name="un-expanded-row"
              v-bind:field="field"
              v-bind:item="item"
              v-bind:expand="expand"
              v-bind:isExpanded="isExpanded"
            >
            </slot>

            <!-- <span v-if="field == 'engagementName'" class="primary--text">
              <v-icon v-if="('child' in item)"
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
            </span> -->
          </td>
        </tr>
      </template>
      <template v-slot:expanded-item="{ item }">
        <tr v-for="(field, index) in item.child" :key="index">
          <td></td>
          <slot name="expanded-row" v-bind:field="field"></slot>
          <!-- <td class="primary--text">{{ field.engagementName }}</td>
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
          <td>{{ field.createdBy }}</td> -->
        </tr>
      </template>
    </v-data-table>
  </div>
</template>

<script>
export default {
  name: "HuxDataTable",
  components: {},
  props: {
    dataItems: {
      type: Array,
      default: () => [],
      required: true,
    },
    headers: {
      type: Array,
      default: () => [],
      required: true,
    },
  },
  data() {
    return {
      search: "",
      expanded: [],
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
  ::v-deep .material-icons.delivered {
    color: var(--v-success-lighten1);
  }
  ::v-deep .material-icons.delivering {
    color: var(--v-success-lighten2);
  }
  ::v-deep .material-icons.alert {
    color: var(--v-error-base);
  }
  ::v-deep .rotate-icon {
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
  ::v-deep .avatar-border {
    border-width: 2px;
    border-style: solid;
    border-radius: 50%;
    font-size: 14px;
    width: 35px;
    height: 35px;
    line-height: 22px;
    color: var(--v-neroBlack-base) !important;
    cursor: default !important;
    background: transparent !important;
  }
}
</style>
