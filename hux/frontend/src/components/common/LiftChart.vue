<template>
  <hux-data-table :headers="headers" :dataItems="data" disableSort>
    <template #row-item="{ item }">
      <td
        v-for="header in headers"
        :key="header.value"
        :class="{ 'liftchart-bucket': header.value === 'bucket' }"
      >
        <div class="neroBlack--text text-h6">
          {{ item[header.value] }}
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

  data() {
    return {
      headers: [
        { text: "Bucket", value: "bucket", width: "94px" },
        { text: "Predicted $", value: "predicted_value", width: "117px" },
        { text: "Actual $", value: "actual_value", width: "117px" },
        { text: "Profiles", value: "profile_count", width: "117px" },
        {
          text: "Rate $<div class='pt-2'>(predicted)</div>",
          value: "predicted_rate",
          width: "117px",
        },
        {
          text: "Rate $<div class='pt-2'>(actual)</div>",
          value: "actual_rate",
          width: "117px",
        },
        {
          text: "Lift <div class='pt-2'>(predicted)</div>",
          value: "predicted_lift",
          width: "117px",
        },
        {
          text: "Lift <div class='pt-2'>(actual)</div>",
          value: "actual_lift",
          width: "117px",
        },
        {
          text: "Size %<div class='pt-2'>(profiles)</div>",
          value: "profile_size_percent",
          width: "117px",
        },
      ],
      //TODO: API Integration
      data: [
        {
          profile_size_percent: 97.16,
          bucket: 10,
          predicted_lift: 1.03,
          profile_count: 22,
          actual_rate: 0.29,
          actual_lift: 1.53,
          predicted_value: 693.69,
          actual_value: 797.81,
          predicted_rate: 0.31,
        },
        {
          profile_size_percent: 97.16,
          bucket: 20,
          predicted_lift: 1.03,
          profile_count: 22,
          actual_rate: 0.29,
          actual_lift: 1.53,
          predicted_value: 693.69,
          actual_value: 797.81,
          predicted_rate: 0.31,
        },
        {
          profile_size_percent: 97.16,
          bucket: 30,
          predicted_lift: 1.03,
          profile_count: 22,
          actual_rate: 0.29,
          actual_lift: 1.53,
          predicted_value: 693.69,
          actual_value: 797.81,
          predicted_rate: 0.31,
        },
        {
          profile_size_percent: 97.16,
          bucket: 40,
          predicted_lift: 1.03,
          profile_count: 22,
          actual_rate: 0.29,
          actual_lift: 1.53,
          predicted_value: 693.69,
          actual_value: 797.81,
          predicted_rate: 0.31,
        },
        {
          profile_size_percent: 97.16,
          bucket: 50,
          predicted_lift: 1.03,
          profile_count: 22,
          actual_rate: 0.29,
          actual_lift: 1.53,
          predicted_value: 693.69,
          actual_value: 797.81,
          predicted_rate: 0.31,
        },
        {
          profile_size_percent: 97.16,
          bucket: 60,
          predicted_lift: 1.03,
          profile_count: 22,
          actual_rate: 0.29,
          actual_lift: 1.53,
          predicted_value: 693.69,
          actual_value: 797.81,
          predicted_rate: 0.31,
        },
        {
          profile_size_percent: 97.16,
          bucket: 70,
          predicted_lift: 1.03,
          profile_count: 22,
          actual_rate: 0.29,
          actual_lift: 1.53,
          predicted_value: 693.69,
          actual_value: 797.81,
          predicted_rate: 0.31,
        },
        {
          profile_size_percent: 97.16,
          bucket: 80,
          predicted_lift: 1.03,
          profile_count: 22,
          actual_rate: 0.29,
          actual_lift: 1.53,
          predicted_value: 693.69,
          actual_value: 797.81,
          predicted_rate: 0.31,
        },
        {
          profile_size_percent: 97.16,
          bucket: 90,
          predicted_lift: 1.03,
          profile_count: 22,
          actual_rate: 0.29,
          actual_lift: 1.53,
          predicted_value: 693.69,
          actual_value: 797.81,
          predicted_rate: 0.31,
        },
        {
          profile_size_percent: 97.16,
          bucket: 100,
          predicted_lift: 1.03,
          profile_count: 22,
          actual_rate: 0.29,
          actual_lift: 1.53,
          predicted_value: 693.69,
          actual_value: 797.81,
          predicted_rate: 0.31,
        },
      ],
    }
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
          background: var(--v-aliceBlue-base);
          height: 40px !important;
        }
      }
    }
    .liftchart-bucket {
      background: var(--v-aliceBlue-base);
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
