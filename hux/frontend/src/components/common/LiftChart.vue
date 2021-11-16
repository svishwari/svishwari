<template>
  <hux-data-table :columns="headers" :data-items="data" disable-sort>
    <template #row-item="{ item }">
      <td
        v-for="header in headers"
        :key="header.value"
        :class="{ 'liftchart-bucket': header.value === 'bucket' }"
      >
        <div class="black--text text--darken-4 text-h6">
          {{ item[header.value].toLocaleString() }}
        </div>
      </td>
    </template>
  </hux-data-table>
</template>

<script>
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"

export default {
  name: "LiftChart",

  components: {
    HuxDataTable,
  },

  props: {
    data: {
      type: Array,
      required: false,
    },
    rmse: {
      type: Number,
      required: true,
    },
  },
  computed: {
    suffix() {
      return this.rmse !== -1 ? "$" : ""
    },
    headers() {
      return [
        { text: "Bucket", value: "bucket", width: "94px" },
        {
          text: `Predicted ${this.suffix}`,
          value: "predicted_value",
          width: "117px",
        },
        {
          text: `Actual ${this.suffix}`,
          value: "actual_value",
          width: "117px",
        },
        { text: "Profiles", value: "profile_count", width: "117px" },
        {
          text: `Rate ${this.suffix}<span class='pt-2'>(predicted)</span>`,
          value: "predicted_rate",
          width: "117px",
        },
        {
          text: `Rate ${this.suffix}<span class='pt-2'>(actual)</span>`,
          value: "actual_rate",
          width: "117px",
        },
        {
          text: "Lift <span class='pt-2'>(predicted)</span>",
          value: "predicted_lift",
          width: "117px",
        },
        {
          text: "Lift <span class='pt-2'>(actual)</span>",
          value: "actual_lift",
          width: "117px",
        },
        {
          text: "Size % <span class='pt-2'>(profiles)</span>",
          value: "profile_size_percent",
          width: "117px",
        },
      ]
    },
  },
}
</script>
<style lang="scss" scoped>
.hux-data-table {
  @extend .box-shadow-5;
  ::v-deep table {
    .v-data-table-header {
      tr {
        th {
          background: var(--v-primary-lighten2);
          height: 40px !important;
        }
      }
    }
    .liftchart-bucket {
      background: var(--v-primary-lighten2);
    }
    tbody {
      tr {
        td {
          height: 40px !important;
        }
      }
    }
  }
}
</style>
