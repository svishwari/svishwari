<template>
  <div>
    <v-progress-linear
      v-if="loadingCustomersList"
      :active="loadingCustomersList"
      :indeterminate="loadingCustomersList"
    />
    <span v-if="!loadingCustomersList && customers.length != 0">
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
              class="cell text-ellipsis text-body-1 mt-1"
              append
            >
              <span v-if="item[header.value]">{{ item[header.value] }} </span>
              <span v-else> - </span>
            </router-link>
            <div
              v-if="header.value == 'last_name'"
              class="cell text-ellipsis text-body-1 mt-1"
              :class="
                item.last_name && item.last_name.trim() == '++REDACTED++'
                  ? 'blur-text'
                  : ''
              "
            >
              <span v-if="item.last_name">{{ item.last_name }} </span>
              <span v-else> - </span>
            </div>
            <div
              v-if="header.value == 'first_name'"
              class="cell text-ellipsis text-body-1 mt-1"
              :class="
                item.first_name && item.first_name.trim() == '++REDACTED++'
                  ? 'blur-text'
                  : ''
              "
            >
              <span v-if="item.first_name"> {{ item.first_name }}</span>
              <span v-else> - </span>
            </div>
            <div v-if="header.value == 'match_confidence'">
              <hux-slider
                v-if="item[header.value]"
                :is-range-slider="false"
                :value="item[header.value]"
                :slider-text-color="true"
                class="match-confidence"
              ></hux-slider>
              <span v-else> - </span>
            </div>
          </td>
        </template>
      </hux-data-table>
      <v-progress-linear v-if="enableLazyLoad" active indeterminate />
      <observer v-if="customers.length" @intersect="intersected"></observer>
    </span>
    <div
      v-else-if="!loadingCustomersList && customers.length == 0"
      class="list-frame py-14"
    >
      <empty-page
        v-if="customers.length == 0 && !errorCustomerList"
        type="lift-table-empty"
        :size="50"
      >
        <template #title>
          <div class="title-no-notification">No customer data to show</div>
        </template>
        <template #subtitle>
          <div class="text-body-2 black--text text--base mt-2">
            Customer list will appear here once customer data is available.
          </div>
        </template>
      </empty-page>
      <empty-page
        v-else-if="errorCustomerList"
        class="title-no-notification"
        type="error-on-screens"
        :size="50"
      >
        <template #title>
          <div class="title-no-notification">
            Customers list is currently unavailable
          </div>
        </template>
        <template #subtitle>
          <div class="text-body-2 black--text text--base mt-2">
            Our team is working hard to fix it. Please be patient and try again
            soon!
          </div>
        </template>
      </empty-page>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import HuxSlider from "@/components/common/HuxSlider"
import Observer from "@/components/common/Observer"
import EmptyPage from "@/components/common/EmptyPage"
export default {
  name: "CustomerList",
  components: {
    HuxDataTable,
    HuxSlider,
    Observer,
    EmptyPage,
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
          width: "280px",
        },
      ],
      lastBatch: 0,
      batchDetails: {
        batchSize: 100,
        batchNumber: 1,
        isLazyLoad: false,
      },
      errorCustomerList: false,
    }
  },
  computed: {
    ...mapGetters({
      customersList: "customers/list",
      customerOverview: "customers/overview",
    }),
    customers() {
      let sortedCustomerList = this.customersList
      if (sortedCustomerList) {
        sortedCustomerList.forEach((data) => (data.id = data.hux_id))
      }
      return sortedCustomerList.sort((a, b) => a.id - b.id)
    },
  },
  async mounted() {
    this.loadingCustomersList = true
    let nolazyLoad = false
    try {
      await this.fetchCustomerByBatch()
      this.calculateLastBatch()
    } catch (error) {
      this.errorCustomerList = true
      nolazyLoad = true
    }
    this.loadingCustomersList = false
    this.enableLazyLoad = !nolazyLoad
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
        height: 32px !important;
      }
      th {
        background: var(--v-primary-lighten2);
        box-shadow: none;
      }
    }
    > .v-data-table__wrapper {
      > table {
        > tbody > tr > td {
          padding-top: 0;
          padding-bottom: 0;
          height: 60px !important;
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
    max-width: 100%;
    text-decoration: none;
  }
}
::v-deep .hux-data-table .table-overflow {
  overflow-x: inherit !important;
}
::v-deep .hux-data-table .v-data-table .match-confidence .slider-value-display {
  margin-top: 1px !important;
  width: 45px !important;
  margin-left: 10px !important;
}
::v-deep .hux-score-slider .v-slider--horizontal {
  min-height: 7px !important;
}
::v-deep .v-application--is-ltr .v-input__append-outer {
  margin-left: 16px !important;
}
::v-deep .hux-data-table .v-data-table .v-data-table-header th:first-child {
  border-top-left-radius: 12px !important;
}
::v-deep .hux-data-table .v-data-table .v-data-table-header th:last-child {
  border-top-right-radius: 12px !important;
}
.list-frame {
  background-image: url("../../assets/images/no-lift-chart-frame.png");
  background-position: center;
  background-size: 100% 100%;
}
.title-no-notification {
  font-size: 24px !important;
  line-height: 34px !important;
  font-weight: 300 !important;
  letter-spacing: 0 !important;
  color: var(--v-black-base);
}
</style>
