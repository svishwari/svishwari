<template>
  <page max-width="100%">
    <template #header>
      <page-header
        :title="`Welcome back, ${fullName}!`"
        :header-height="110"
        data-e2e="welcome-banner"
      >
        <template #left>
          <p class="text-subtitle-1 font-weight-regular mb-0">
            Hux is here to help you make better, faster decisions to improve
            your customer experiences.
            <a
              class="text-decoration-none"
              href="https://consulting.deloitteresources.com/offerings/customer-marketing/advertising-marketing-commerce/Pages/hux_marketing.aspx"
              target="_blank"
            >
              Learn More &gt;
            </a>
          </p>
        </template>
      </page-header>
    </template>

    <v-row>
      <v-col>
        <v-card class="rounded-lg box-shadow-5" height="367">
          <v-card-title class="pa-6">
            <h3 class="text-h3 black--text text--darken-4">
              Total customers
              <span class="text-body-1 black--text text--lighten-4">
                (last 9 months)
              </span>
            </h3>
          </v-card-title>
          <v-progress-linear
            v-if="loadingCustomerChart"
            :active="loadingCustomerChart"
            :indeterminate="loadingCustomerChart"
          />
          <total-customer-chart
            v-if="!loadingCustomerChart"
            :customers-data="totalCustomers"
            data-e2e="total-customers-chart"
          />
        </v-card>
      </v-col>
    </v-row>
  </page>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import Page from "@/components/Page.vue"
import PageHeader from "@/components/PageHeader.vue"
import TotalCustomerChart from "@/components/common/TotalCustomerChart/TotalCustomerChart.vue"

export default {
  name: "Home",

  components: {
    Page,
    PageHeader,
    TotalCustomerChart,
  },

  data() {
    return {
      loadingCustomerChart: false,
    }
  },

  computed: {
    ...mapGetters({
      totalCustomers: "customers/totalCustomers",
      firstName: "users/getFirstname",
      lastName: "users/getLastName",
    }),

    fullName() {
      return `${this.firstName} ${this.lastName}`
    },
  },

  mounted() {
    this.fetchTotalCustomers()
  },

  methods: {
    ...mapActions({
      getTotalCustomers: "customers/getTotalCustomers",
    }),
    async fetchTotalCustomers() {
      this.loadingCustomerChart = true
      await this.getTotalCustomers()
      this.loadingCustomerChart = false
    },
  },
}
</script>

<style lang="scss" scoped></style>
