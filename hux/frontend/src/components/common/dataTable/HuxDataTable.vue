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
          </td>
        </tr>
      </template>
      <template v-slot:expanded-item="{ item }">
        <tr v-for="(field, index) in item.child" :key="index">
          <td></td>
          <slot name="expanded-row" v-bind:field="field"></slot>
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
