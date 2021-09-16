<template>
  <div>
    <page-header class="background-border" :header-height-changes="'py-3'">
      <template #left>
        <breadcrumb :items="items" />
      </template>
      <template #right>
        <v-icon
          size="22"
          color="black lighten-3"
          class="icon-border icon-cursor pa-2 ma-1"
        >
          mdi-download
        </v-icon>
      </template>
    </page-header>
    <v-progress-linear :active="loading" :indeterminate="loading" />

    <div v-if="!loading && customerProfile" class="pl-15 py-6 pr-9">
      <v-row>
        <v-col cols="3">
          <v-card
            class="
              text-center
              rounded-lg
              card-info-wrapper
              box-shadow-5
              card-height
            "
          >
            <v-card-title class="title-font-size">
              <span class="d-inline-block text-truncate mr-1">
                {{ customerDetails["first_name"] }}
              </span>
              <span class="d-inline-block text-truncate">
                {{ customerDetails["last_name"] }}
              </span>
            </v-card-title>
            <v-card-text class="justify-center title-text py-3">
              <icon type="smile" :size="16" color="primary-lighten8" />
              <div>Hux ID</div>
              <span class="sample-card-text">
                {{ customerDetails["hux_id"] }}
              </span>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col
          v-for="data in customerOverview"
          :key="data.id"
          :cols="data.colValue"
          class="matix-card-space"
        >
          <v-card
            class="rounded-lg card-info-wrapper card-shadow no-background"
          >
            <v-card-text class="pl-3 pr-3 pb-3 pt-3 matrix-card">
              <div class="text-caption black--text text--darken-1 pb-1">
                {{ data.title }}
                <tooltip v-if="data.hoverTooltip" position-top>
                  <template #label-content>
                    <icon v-if="data.hoverTooltip" type="info" :size="12" />
                  </template>
                  <template #hover-content>
                    {{ data.hoverTooltip }}
                  </template>
                </tooltip>
              </div>
              <hux-slider
                v-if="data.format === 'slider'"
                :is-range-slider="false"
                :value="data.value"
              ></hux-slider>
              <span v-else class="sample-card-text">
                <template v-if="data.format === 'date-relative'">
                  {{ data.value | Date("relative", true) | Empty }}
                </template>
                <template v-if="data.format === 'currency'">
                  {{ data.value | Currency | Empty }}
                </template>
              </span>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-row class="details-card">
        <v-col cols="3"> </v-col>
        <v-col
          v-for="data in customerOverviewMore"
          :key="data.id"
          :cols="data.colValue"
          class="matix-card-space"
        >
          <v-card
            class="rounded-lg card-info-wrapper card-shadow no-background"
          >
            <v-card-text class="pl-3 pr-3 pb-3 pt-3 matrix-card">
              <div class="title-text pb-1">
                {{ data.title }}
                <tooltip v-if="data.hoverTooltip" position-top>
                  <template #label-content>
                    <icon v-if="data.hoverTooltip" type="info" :size="12" />
                  </template>
                  <template #hover-content>
                    {{ data.hoverTooltip }}
                  </template>
                </tooltip>
              </div>
              <div class="sample-card-text">{{ data.value }}</div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-row class="table-card">
        <v-col cols="5" class="pb-0">
          <v-card class="rounded-lg card-info-wrapper box-shadow-5">
            <v-card-title class="py-3 card-heading">
              {{ cardTitles[0].title }}
              <tooltip position-top>
                <icon
                  type="ds_lock_special"
                  :size="17"
                  color="black-darken4"
                  class="ml-2"
                />
                <template #tooltip>
                  You do not have access to see individual information.<br />
                  Contact your administrator for access.
                </template>
              </tooltip>
            </v-card-title>
            <v-card-text class="justify-center title-text">
              <v-simple-table>
                <template v-slot:default>
                  <tbody>
                    <tr>
                      <td class="title-text">Email</td>
                      <td class="table-text blur-text">
                        {{ customerInsights["email"] | Empty }}
                      </td>
                      <td class="title-text">Address</td>
                      <td class="table-text blur-text">
                        {{ customerInsights["address"] | Empty }}
                      </td>
                    </tr>
                    <tr>
                      <td class="title-text">Phone</td>
                      <td class="table-text blur-text">
                        {{ customerInsights["phone"] | Empty }}
                      </td>
                      <td class="title-text">City</td>
                      <td class="table-text blur-text">
                        {{ customerInsights["city"] | Empty }}
                      </td>
                    </tr>
                    <tr>
                      <td class="title-text">Age</td>
                      <td class="table-text blur-text">
                        {{ customerInsights["age"] | Empty }}
                      </td>
                      <td class="title-text">State</td>
                      <td class="table-text blur-text">
                        {{ customerInsights["state"] | Empty }}
                      </td>
                    </tr>
                    <tr>
                      <td class="title-text">Gender</td>
                      <td class="table-text">
                        <span class="blur-text">
                          {{ customerInsights["gender"] | Empty }}
                        </span>
                      </td>
                      <td class="title-text">Zip</td>
                      <td class="table-text">
                        <span class="blur-text">
                          {{ customerInsights["zip"] | Empty }}
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </template>
              </v-simple-table>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="3" class="pb-0">
          <v-card class="rounded-lg card-info-wrapper box-shadow-5">
            <v-card-title class="card-heading py-3">
              {{ cardTitles[1].title }}
            </v-card-title>
            <v-card-text class="title-text">
              <v-simple-table>
                <template v-slot:default>
                  <tbody>
                    <tr
                      v-for="pref in customerContactPreferences"
                      :key="pref.id"
                    >
                      <td class="title-text">{{ pref.title }}</td>
                      <td class="table-text cl">
                        <template v-if="pref.value === true">True</template>
                        <template v-if="pref.value === false">False</template>
                      </td>
                    </tr>
                  </tbody>
                </template>
              </v-simple-table>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="4" class="matix-card-space pb-0">
          <identity-chart :chart-data="customerIdentityResolution" />
        </v-col>
      </v-row>

      <v-row class="mt-0">
        <v-col md="12" class="pt-0 pr-1">
          <v-card class="mt-3 rounded-lg box-shadow-5" height="350">
            <v-card-title class="chart-style pb-2 pl-5 pt-5">
              <div class="mt-2">
                <span class="neroBlack--text text-h5"> Customer events </span>
              </div>
              <v-progress-linear
                v-if="loadingCustomerEvents"
                :active="loadingCustomerEvents"
                :indeterminate="loadingCustomerEvents"
              />
            </v-card-title>
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
import dayjs from "dayjs"
import { mapActions, mapGetters } from "vuex"
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import Tooltip from "@/components/common/Tooltip.vue"
import Icon from "@/components/common/Icon"
import HuxSlider from "@/components/common/HuxSlider"
import IdentityChart from "@/components/common/identityChart/IdentityChart"
import CustomerEventChart from "@/components/common/CustomerEventChart/CustomerEventChart"
import CustomerData from "@/api/mock/fixtures/totalCustomersData.js"
import CustomerEventData from "@/api/mock/fixtures/customerEventData.js"

export default {
  name: "CustomerProfileDetails",
  components: {
    PageHeader,
    Breadcrumb,
    Tooltip,
    Icon,
    HuxSlider,
    IdentityChart,
    CustomerEventChart,
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

    customerDetails() {
      return this.customerProfile["overview"]
    },

    customerInsights() {
      return this.customerProfile["insights"]
    },

    customerIdentityResolution() {
      return this.customerProfile["identity_resolution"]
    },

    customerContactPreferences() {
      const contactPreferences = this.customerProfile["contact_preferences"]
      return [
        {
          id: 1,
          title: "Email",
          value: contactPreferences["preference_email"],
          subLabel: null,
        },
        {
          id: 2,
          title: "Push",
          value: contactPreferences["preference_push"],
          width: "19%",
          minWidth: "164px",
        },
        {
          id: 3,
          title: "SMS",
          value: contactPreferences["preference_sms"],
          width: "19%",
          minWidth: "164px",
        },
        {
          id: 4,
          title: "In-App",
          value: contactPreferences["preference_in_app"],
          subLabel: null,
        },
      ]
    },

    customerOverview() {
      const overview = this.customerProfile["overview"]
      return [
        {
          id: 1,
          title: "Customer length",
          value: overview["since"],
          format: "date-relative",
          colValue: 2.5,
        },
        {
          id: 2,
          title: "Match confidence",
          value: overview["match_confidence"],
          format: "slider",
          colValue: 2.5,
          hoverTooltip:
            "A percentage that indicates the level of certainty that all incoming records were accurately matched to a given customer.",
        },
        {
          id: 3,
          title: "Lifetime value",
          value: overview["ltv_actual"],
          format: "currency",
          colValue: 2,
          hoverTooltip:
            "Assessment of the lifetime financial value of each customer.",
        },
        {
          // this value from the API is a number of months (float).
          // we first convert it to a date (eg. months ago)
          // then display this date as relative time (x days, months, years, etc)
          id: 4,
          title: "Conversion time",
          value: dayjs().subtract(overview["conversion_time"], "month"),
          format: "date-relative",
          colValue: 2.5,
          hoverTooltip:
            "The average time customer takes to convert to a purchase.",
        },
      ]
    },

    customerOverviewMore() {
      const overviewMore = this.customerProfile["overview"]
      return [
        {
          id: 5,
          title: "Churn score",
          value: this.$options.filters.Empty(overviewMore["churn_rate"]),
          colValue: 2,
          hoverTooltip:
            "The measure of a customer’s likelihood to stop using a product.",
        },
        {
          id: 6,
          title: "Last click",
          colValue: 2.5,
          value: this.formattedDate(overviewMore["last_click"])
            ? this.formattedDate(overviewMore["last_click"])
            : "n/a",
        },
        {
          id: 7,
          title: "Last purchase date",
          colValue: 2.5,
          value: this.formattedDate(overviewMore["last_purchase"]),
        },
        {
          id: 8,
          title: "Last open",
          colValue: 2.5,
          value: this.formattedDate(overviewMore["last_email_open"]),
        },
      ]
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
    formattedDate(value) {
      if (value) {
        return this.$options.filters.Date(value, "relative")
      }
      return "-"
    },
    async getCustomerEvent() {
      this.loadingCustomerEvents = true
      await this.getEvents(this.id)
      this.loadingCustomerEvents = false
    },
  },
}
</script>

<style lang="scss" scoped>
.customer-profile-wrap {
  ::v-deep .mdi-chevron-right::before {
    content: none;
  }
}
::v-deep .v-card__title {
  background: var(--v-primary-lighten2);
}
::v-deep .v-card__text {
  padding: 0px;
}
.hux-data-table {
  ::v-deep table {
    .v-data-table-header {
      tr {
        height: 40px !important;
      }
      th {
        background: var(--v-primary-lighten2);
      }
    }
  }
}
.v-data-table {
  .v-data-table__wrapper {
    tr:hover:not(.v-data-table__expanded__content):not(.v-data-table__empty-wrapper) {
      background: white !important;
    }
  }
}
.title-font-size {
  font-family: Open Sans;
  font-style: normal;
  font-weight: 300 !important;
  font-size: 21px;
  line-height: 25px;
  color: var(--v-black-darken4);
  justify-content: center;
}
.title-text {
  font-family: Open Sans;
  font-style: normal;
  font-weight: normal;
  color: var(--v-black-darken1) !important;
  font-size: 12px !important;
}
.table-text {
  color: var(--v-black-darken4);
  font-size: 12px !important;
}
.card-heading {
  font-size: 15px !important;
  color: var(--v-black-darken4);
  font-weight: 400;
  height: 54px !important;
}
.sample-card-text {
  font-size: 14px;
  font-family: Open Sans;
  font-style: normal;
  font-weight: 600;
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
.hux-score-slider {
  margin-bottom: -27px !important;
  margin-top: -8px;

  ::v-deep .slider-value-display {
    width: 36px;
  }
}
.blur-text {
  color: transparent;
  text-shadow: 0 0 8px #000;
  user-select: none;
}
.no-background {
  background: none !important;
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
