<template>
  <div>
    <v-progress-linear
      :active="loadingCustomersList"
      :indeterminate="loadingCustomersList"
    />
    <hux-data-table
      :columns="columnDefs"
      :sort-column="'hux_id'"
      :data-items="customers"
    >
      <template #row-item="{ item }">
        <td
          v-for="header in columnDefs"
          :key="header.value"
          :style="{ width: header.width }"
        >
          <router-link
            v-if="header.value == 'hux_id'"
            :to="{
              name: 'CustomerProfileDetails',
              params: { id: item[header.value] },
            }"
            data-e2e="customerID"
            class="cell text-h6"
            append
          >
            {{ item[header.value] }}
          </router-link>
          <div v-if="header.value == 'last_name'" class="cell text-h6">
            <span v-if="item.last_name">{{ item.last_name }} </span>
          </div>
          <div v-if="header.value == 'first_name'" class="cell text-h6">
            <span v-if="item.first_name"> {{ item.first_name }}</span>
          </div>
          <div v-if="header.value == 'match_confidence'">
            <hux-slider
              :is-range-slider="false"
              :value="item[header.value]"
              class="match-confidence"
            ></hux-slider>
          </div>
        </td>
      </template>
    </hux-data-table>
    <observer v-if="customers.length" @intersect="intersected"></observer>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import HuxSlider from "@/components/common/HuxSlider"
import Tooltip from "@/components/common/Tooltip"
import Observer from "@/components/common/Observer"

export default {
  name: "CustomerList",
  components: {
    Tooltip,
    HuxDataTable,
    HuxSlider,
    Observer,
  },

  data() {
    return {
      enableLazyLoad: false,
      loadingCustomersList: false,
      batchCount: 1,
      columnDefs: [
        {
          text: "Hux ID",
          value: "hux_id",
          width: "auto",
        },
        {
          text: "Last name",
          value: "last_name",
          width: "auto",
        },
        {
          text: "First name",
          value: "first_name",
          width: "auto",
        },
        {
          text: "Match confidence",
          value: "match_confidence",
          width: "250px",
        },
      ],
      lastBatch: 0,
      batchDetails: {
        batchSize: 100,
        batchNumber: 1,
        isLazyLoad: false,
      },
    }
  },

  computed: {
    ...mapGetters({
      customersList: "customers/list",
      customerOverview: "customers/overview",
    }),

    customers() {
      let sortedCustomerList = this.customersList
      return sortedCustomerList.sort((a, b) => a.id - b.id)
    },
  },

  async mounted() {
    this.loadingCustomersList = true
    await this.fetchCustomerByBatch()
    this.calculateLastBatch()
    this.loadingCustomersList = false
    this.enableLazyLoad = true
  },

  methods: {
    ...mapActions({
      getCustomers: "customers/getAll",
    }),

    async fetchCustomerByBatch() {
      await this.getCustomers(this.batchDetails)
      this.batchDetails.batchNumber++
    },

    intersected() {
      if (this.batchDetails.batchNumber <= this.lastBatch) {
        this.batchDetails.isLazyLoad = true
        this.fetchCustomerByBatch()
      } else {
        this.enableLazyLoad = false
      }
    },
    
    calculateLastBatch() {
      this.lastBatch = Math.ceil(
        this.customerOverview.total_customers / this.batchDetails.batchSize
      )
    },
  },
}
</script>

<style lang="scss" scoped>
.hux-data-table {
  margin-top: 1px;
}
::v-deep .v-sheet .theme--light .v-toolbar {
  background: var(--v-primary-lighten2);
}
::v-deep .hux-data-table {
  .v-data-table {
    .v-data-table-header {
      tr {
        height: 40px !important;
      }
      th {
        background: var(--v-primary-lighten2);
      }
    }
    > .v-data-table__wrapper {
      > table {
        > tbody > tr > td {
          padding-top: 0;
          padding-bottom: 0;
        }
      }
    }
    .match-confidence {
      .slider-value-display {
        margin-top: 16px;
        width: 33px;
      }
      .v-slider__track-container {
        margin-top: 12px !important;
      }
      .v-slider__thumb-container {
        margin-top: 12px !important;
      }
    }
  }
  .cell {
    display: inline-block;
    max-width: 100%;
    text-decoration: none;
  }
}
</style>
