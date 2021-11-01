<template>
  <div>
    <page-header class="background-border" :header-height-changes="'py-3'">
      <template #left>
        <breadcrumb :items="items" />
      </template>
    </page-header>
    <v-progress-linear :active="loading" :indeterminate="loading" />

    <div v-if="!loading && customerProfile" class="pa-7">
      <profile-overview :profile="customerProfile['overview']" />
      <v-row class="table-card">
        <v-col cols="6" class="pb-0">
          <profile-identifiable-insights
            :insights="customerProfile['insights']"
          />
        </v-col>
        <v-col class="pb-0 customCol">
          <contact-preferences
            :insights="customerProfile['contact_preferences']"
          />
        </v-col>
        <v-col class="matix-card-space pb-0">
          <individual-identity
            :insights="customerProfile['identity_resolution']"
          />
        </v-col>
      </v-row>

      <v-row class="mt-0">
        <v-col md="12" class="pt-0 pr-1">
          <v-card class="mt-3 rounded-lg box-shadow-5" height="370">
            <!-- <v-card-title class="chart-style pb-2 pl-5 pt-5">
              <div class="mt-2">
                <span class="neroBlack--text text-h5"> Customer events </span>
              </div>
              <v-progress-linear
                v-if="loadingCustomerEvents"
                :active="loadingCustomerEvents"
                :indeterminate="loadingCustomerEvents"
              />
            </v-card-title> -->
            <v-card-title class="pa-6">
            <h3 class="text-h3 black--text text--darken-4">
              Customer events
              <span class="text-body-1 black--text text--lighten-4">
                (All time)
              </span>
            </h3>
          </v-card-title>
          <v-progress-linear
              v-if="loadingCustomerChart"
              :active="loadingCustomerChart"
              :indeterminate="loadingCustomerChart"
            />
            <customer-event-chart
              v-if="!loadingCustomerEvents"
              :customers-data="events"
            />
          </v-card>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import CustomerEventChart from "@/components/common/CustomerEventChart/CustomerEventChart"
import CustomerData from "@/api/mock/fixtures/totalCustomersData.js"
import CustomerEventData from "@/api/mock/fixtures/customerEventData.js"
import ProfileOverview from "./ProfileOverview.vue"
import ProfileIdentifiableInsights from "./ProfileIdentifiableInsights.vue"
import ContactPreferences from "./ContactPreferences.vue"
import IndividualIdentity from "./IndividualIdentity.vue"

export default {
  name: "CustomerProfileDetails",
  components: {
    PageHeader,
    Breadcrumb,
    CustomerEventChart,
    ProfileOverview,
    ProfileIdentifiableInsights,
    ContactPreferences,
    IndividualIdentity,
  },
  data() {
    return {
      customerEvent: CustomerEventData,
      customerData: CustomerData,
      items: [
        {
          text: "Customer Profiles",
          disabled: false,
          href: this.$router.resolve({ name: "CustomerProfiles" }).href,
          icon: "customer-profiles",
        },
        {
          text: this.$route.params.id,
          disabled: true,
          href: "/customers" + this.$route.params.id,
        },
      ],
      cardTitles: [
        {
          id: 1,
          title: "Customer insights",
          icon: "customer-profiles",
        },
        {
          id: 2,
          title: "Contact preferences",
          icon: "customer-profiles",
        },
      ],
      loading: false,
      loadingCustomerEvents: true,
    }
  },
  computed: {
    ...mapGetters({
      customer: "customers/single",
      events: "customers/getEvents",
    }),

    id() {
      return this.$route.params.id
    },

    customerProfile() {
      return this.customer(this.$route.params.id)
    },
  },

  async mounted() {
    this.loading = true
    await this.getCustomer(this.id)
    this.getCustomerEvent()
    this.loading = false
  },

  methods: {
    ...mapActions({
      getCustomer: "customers/get",
      getEvents: "customers/getCustomerEvents",
    }),
    async getCustomerEvent() {
      this.loadingCustomerEvents = true
      await this.getEvents(this.id)
      this.loadingCustomerEvents = false
    },
  },
}
</script>

<style lang="scss" scoped>
.customCol {
  flex: 0 0 22%;
  width: 22%;
}
::v-deep .v-data-table {
  td {
    border-top: solid 1px var(--v-black-lighten2);
    border-bottom: none !important;
  }
}
.card-heading {
  color: var(--v-black-darken4);
  height: 54px !important;
}
.sample-card-text {
  color: var(--v-black-darken4) !important;
}
.icon-cursor {
  cursor: default !important;
}
.details-card {
  position: relative;
  margin-top: -93px;
}
.table-card {
  height: 284px;
}
.card-height {
  height: 155px !important;
}

.matrix-card {
  height: 70px !important;
}
.matix-card-space {
  padding-right: 5px !important;
}
::v-deep .v-input {
  @extend .sample-card-text;
}
.chart-style {
  background: var(--v-white-base) !important;
}
</style>
