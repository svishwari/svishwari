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
      <v-row class="table-card mb-3">
        <v-col cols="6" class="pb-0">
          <profile-identifiable-insights
            :insights="customerProfile['insights']"
            :piiaccess="customerProfile['pii_access']"
            :show-pii="showPIIData"
            @togglePII="getCustomerTogglePII"
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
            <v-card-title class="py-5 pl-6 d-flex justify-space-between">
              <h3 class="text-h3 black--text text--darken-4 mt-n2">
                Customer events
                <span class="text-body-1 black--text text--lighten-4">
                  (All time)
                </span>
              </h3>
              <v-btn
                text
                min-width="80"
                class="
                  d-flex
                  align-right
                  primary--text
                  text-decoration-none
                  pl-0
                  pr-0
                  idr-link
                  text-body-1
                  mt-n2
                "
                data-e2e="eventsDrawerButton"
                @click="toggleCustomerEventsDrawer()"
              >
                <icon
                  type="events-drawer"
                  color="primary"
                  :size="18"
                  class="mr-1"
                />
                Event details
              </v-btn>
            </v-card-title>
            <v-progress-linear
              v-if="loadingCustomerEvents"
              :active="loadingCustomerEvents"
              :indeterminate="loadingCustomerEvents"
            />
            <customer-event-chart
              v-if="!loadingCustomerEvents"
              :customers-data="events"
            />
          </v-card>
        </v-col>
      </v-row>
      <customer-events-drawer
        v-model="customerEventsDrawer"
        :events="eventsForTable"
      />
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
import CustomerEventsDrawer from "./Drawers/CustomerEventsDrawer"
import Icon from "@/components/common/Icon"
import { sortBy } from "lodash"

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
    CustomerEventsDrawer,
    Icon,
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
      customerEventsDrawer: false,
      showPIIData: false,
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

    eventsForTable() {
      return this.events.reduce((eventObject, event) => {
        let index = 0
        let temp = []
        const event_type_count = event["event_type_counts"]
        Object.keys(event_type_count).forEach((key) => {
          for (index = 0; index < event_type_count[key]; index++) {
            temp.push({ event_type: key, date: event["date"] })
          }
        })
        eventObject = eventObject.concat(sortBy(temp, [(o) => o.event_type]))
        return eventObject
      }, [])
    },
  },

  async mounted() {
    this.loading = true
    try {
      await this.getCustomer(this.id)
      this.getCustomerEvent()
    } finally {
      this.loading = false
    }
  },

  methods: {
    ...mapActions({
      getCustomer: "customers/get",
      getCustomerRedact: "customers/getRedact",
      getEvents: "customers/getCustomerEvents",
    }),
    async getCustomerEvent() {
      this.loadingCustomerEvents = true
      try {
        await this.getEvents(this.id)
      } finally {
        this.loadingCustomerEvents = false
      }
    },
    async getCustomerTogglePII(redactFlag) {
      let params = {
        id: this.id,
        redactFlag: redactFlag,
      }
      await this.getCustomerRedact(params)
      this.showPIIData = !this.showPIIData
    },
    toggleCustomerEventsDrawer() {
      this.customerEventsDrawer = !this.customerEventsDrawer
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
