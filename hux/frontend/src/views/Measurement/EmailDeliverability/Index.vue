<template>
  <page max-width="100%" class="idr-wrapper">
    <template #header>
      <span class="header-section">
        <page-header
          class="page-header py-5"
          header-min-height="110"
          header-max-height="120"
        >
          <template #left>
            <div>
              <breadcrumb
                :items="[
                  {
                    text: 'Email Deliverability',
                    disabled: true,
                    href: '/email-deliverability',
                    icon: 'email_deliverability',
                    iconSize: 25,
                    iconColor: 'black',
                    iconColorVariant: 'base',
                  },
                ]"
              />
            </div>
            <div class="text-subtitle-1 font-weight-regular pt-0 pl-0">
              In-depth review of key delivery metrics, reputation, and inbox
              indicators that mailbox providers pay attention to when evaluating
              an email sender’s digital reputation.
            </div>
          </template>
        </page-header>
        <v-progress-linear :active="loading" :indeterminate="loading" />
      </span>
    </template>
    <div
      v-if="overviewData && !loading"
      class="flex-grow-1 flex-shrink-1 content-section"
    >
      <!-- Header Overview section -->
      <overview data-e2e="deliverability-overview" :entity="entity" />
      <!-- Delivered count -->
      <delivered-chart
        v-if="deliveredCountData.length > 0"
        :email-data="deliveredCountData"
        data-e2e="delivered-count-open-rate-chart"
      />
      <v-card class="my-9 rounded-lg box-shadow-5">
        <v-row
          v-if="deliveredCountData.length == 0"
          class="total-customers-chart-frame py-14"
        >
          <empty-page
            v-if="!emailOverviewErrorState"
            type="model-features-empty"
            :size="50"
          >
            <template #title>
              <div>No data to show</div>
            </template>
            <template #subtitle>
              <div>
                Delivered count chart will appear here once email overview data
                is available.
              </div>
            </template>
          </empty-page>
          <empty-page v-else type="error-on-screens" :size="50">
            <template #title>
              <div>Delivered count chart is currently unavailable</div>
            </template>
            <template #subtitle>
              <div>
                Our team is working hard to fix it. Please be patient and try
                again soon!
              </div>
            </template>
          </empty-page>
        </v-row>
      </v-card>
      <!-- Sending domains overview -->
      <overview-1
        v-if="overviewData"
        :list="overviewData.sending_domains_overview"
      />
      <!-- Domains overview chart -->
      <v-row class="mt-0">
        <v-col md="6">
          <v-card class="mt-3 rounded-lg box-shadow-5" height="365">
            <v-card-title class="pb-2 pl-6 pt-5">
              <h3 class="text-h3">Sent</h3>
            </v-card-title>
            <domain-overview-chart
              v-if="
                !emailDomainErrorState &&
                domainChartData.sent &&
                domainChartData.sent.data.length > 0
              "
              :chart-data="domainChartData.sent.data"
              :chart-type="domainChartData.sent.type"
              data-e2e="sent-domain-chart"
            />
            <empty-page
              v-else-if="!emailDomainErrorState"
              type="model-features-empty"
              class="error-empty-spacing"
              :size="50"
            >
              <template #title>
                <div>No data to show</div>
              </template>
              <template #subtitle>
                <div>
                  Sent chart will appear here once Customer data is available.
                </div>
              </template>
            </empty-page>
            <empty-page
              v-else
              class="error-empty-spacing"
              type="error-on-screens"
              :size="50"
            >
              <template #title>
                <div>Sent chart is currently unavailable</div>
              </template>
              <template #subtitle>
                <div>
                  Our team is working hard to fix it. Please be patient and try
                  again soon!
                </div>
              </template>
            </empty-page>
          </v-card>
        </v-col>
        <v-col md="6">
          <v-card class="mt-3 rounded-lg box-shadow-5" height="365">
            <v-card-title class="pb-2 pl-6 pt-5">
              <h3 class="text-h3">Delivered rate</h3>
            </v-card-title>
            <domain-overview-chart
              v-if="
                !emailDomainErrorState &&
                domainChartData.deliveredRate &&
                domainChartData.deliveredRate.data.length > 0
              "
              :chart-data="domainChartData.deliveredRate.data"
              :chart-type="domainChartData.deliveredRate.type"
              data-e2e="delivered-rate-domain-chart"
            />
            <empty-page
              v-else-if="!emailDomainErrorState"
              type="model-features-empty"
              class="error-empty-spacing"
              :size="50"
            >
              <template #title>
                <div>No data to show</div>
              </template>
              <template #subtitle>
                <div>
                  Delivered rate chart will appear here once Customer data is
                  available.
                </div>
              </template>
            </empty-page>
            <empty-page
              v-else
              class="error-empty-spacing"
              type="error-on-screens"
              :size="50"
            >
              <template #title>
                <div>Delivered rate chart is currently unavailable</div>
              </template>
              <template #subtitle>
                <div>
                  Our team is working hard to fix it. Please be patient and try
                  again soon!
                </div>
              </template>
            </empty-page>
          </v-card>
        </v-col>
      </v-row>

      <v-row>
        <v-col md="6">
          <v-card class="rounded-lg box-shadow-5" height="365">
            <v-card-title class="pb-2 pl-6 pt-5">
              <h3 class="text-h3">Open rate</h3>
            </v-card-title>
            <domain-overview-chart
              v-if="
                !emailDomainErrorState &&
                domainChartData.openRate &&
                domainChartData.openRate.data.length > 0
              "
              :chart-data="domainChartData.openRate.data"
              :chart-type="domainChartData.openRate.type"
              data-e2e="open-rate-domain-chart"
            />
            <empty-page
              v-else-if="!emailDomainErrorState"
              type="model-features-empty"
              class="error-empty-spacing"
              :size="50"
            >
              <template #title>
                <div>No data to show</div>
              </template>
              <template #subtitle>
                <div>
                  Open rate chart will appear here once Customer data is
                  available.
                </div>
              </template>
            </empty-page>
            <empty-page
              v-else
              class="error-empty-spacing"
              type="error-on-screens"
              :size="50"
            >
              <template #title>
                <div>Open rate chart is currently unavailable</div>
              </template>
              <template #subtitle>
                <div>
                  Our team is working hard to fix it. Please be patient and try
                  again soon!
                </div>
              </template>
            </empty-page>
          </v-card>
        </v-col>
        <v-col md="6">
          <v-card class="rounded-lg box-shadow-5" height="365">
            <v-card-title class="pb-2 pl-6 pt-5">
              <h3 class="text-h3">Click rate</h3>
            </v-card-title>
            <domain-overview-chart
              v-if="
                !emailDomainErrorState &&
                domainChartData.clickRate &&
                domainChartData.clickRate.data.length > 0
              "
              :chart-data="domainChartData.clickRate.data"
              :chart-type="domainChartData.clickRate.type"
              data-e2e="click-rate-domain-chart"
            />
            <empty-page
              v-else-if="!emailDomainErrorState"
              type="model-features-empty"
              class="error-empty-spacing"
              :size="50"
            >
              <template #title>
                <div>No data to show</div>
              </template>
              <template #subtitle>
                <div>
                  Click rate chart will appear here once Customer data is
                  available.
                </div>
              </template>
            </empty-page>
            <empty-page
              v-else
              class="error-empty-spacing"
              type="error-on-screens"
              :size="50"
            >
              <template #title>
                <div>Click rate chart is currently unavailable</div>
              </template>
              <template #subtitle>
                <div>
                  Our team is working hard to fix it. Please be patient and try
                  again soon!
                </div>
              </template>
            </empty-page>
          </v-card>
        </v-col>
      </v-row>

      <v-row>
        <v-col md="6">
          <v-card class="rounded-lg box-shadow-5" height="365">
            <v-card-title class="pb-2 pl-6 pt-5">
              <h3 class="text-h3">Unsubscribe rate</h3>
            </v-card-title>
            <domain-overview-chart
              v-if="
                !emailDomainErrorState &&
                domainChartData.unsubscribeRate &&
                domainChartData.unsubscribeRate.data.length > 0
              "
              :chart-data="domainChartData.unsubscribeRate.data"
              :chart-type="domainChartData.unsubscribeRate.type"
              data-e2e="unsubscribe-rate-domain-chart"
            />
            <empty-page
              v-else-if="!emailDomainErrorState"
              type="model-features-empty"
              class="error-empty-spacing"
              :size="50"
            >
              <template #title>
                <div>No data to show</div>
              </template>
              <template #subtitle>
                <div>
                  Unsubscribe rate chart will appear here once Customer data is
                  available.
                </div>
              </template>
            </empty-page>
            <empty-page
              v-else
              class="error-empty-spacing"
              type="error-on-screens"
              :size="50"
            >
              <template #title>
                <div>Unsubscribe rate chart is currently unavailable</div>
              </template>
              <template #subtitle>
                <div>
                  Our team is working hard to fix it. Please be patient and try
                  again soon!
                </div>
              </template>
            </empty-page>
          </v-card>
        </v-col>
        <v-col md="6">
          <v-card class="rounded-lg box-shadow-5" height="365">
            <v-card-title class="pb-2 pl-6 pt-5">
              <h3 class="text-h3">Complaints rate</h3>
            </v-card-title>
            <domain-overview-chart
              v-if="
                !emailDomainErrorState &&
                domainChartData.complaintsRate &&
                domainChartData.complaintsRate.data.length > 0
              "
              :chart-data="domainChartData.complaintsRate.data"
              :chart-type="domainChartData.complaintsRate.type"
              data-e2e="complaints-rate-domain-chart"
            />
            <empty-page
              v-else-if="!emailDomainErrorState"
              class="error-empty-spacing"
              type="model-features-empty"
              :size="50"
            >
              <template #title>
                <div>No data to show</div>
              </template>
              <template #subtitle>
                <div>
                  Complaints rate chart will appear here once Customer data is
                  available.
                </div>
              </template>
            </empty-page>
            <empty-page
              v-else
              class="error-empty-spacing"
              type="error-on-screens"
              :size="50"
            >
              <template #title>
                <div>Complaints rate chart is currently unavailable</div>
              </template>
              <template #subtitle>
                <div>
                  Our team is working hard to fix it. Please be patient and try
                  again soon!
                </div>
              </template>
            </empty-page>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </page>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import Breadcrumb from "@/components/common/Breadcrumb.vue"
import Page from "@/components/Page.vue"
import PageHeader from "@/components/PageHeader.vue"
import DeliveredChart from "./DeliveredChart.vue"
import Overview1 from "./Domain/Overview.vue"
import Overview from "./Overview.vue"
import DomainOverviewChart from "@/components/common/DomainOverviewChart/DomainOverviewChart.vue"
import EmptyPage from "@/components/common/EmptyPage"

export default {
  name: "EmailDeliverability",
  components: {
    Page,
    PageHeader,
    Breadcrumb,
    Overview,
    DeliveredChart,
    Overview1,
    DomainOverviewChart,
    EmptyPage,
  },
  data() {
    return {
      loading: false,
      entity: {
        description:
          "Email engagement is key for successful email deliverability. The displayed charts highlight performance for the last 90 days.",
        overAllRate: null,
        overviewList: [],
      },
      domainChartData: {},
      deliveredCountData: [],
      emailOverviewErrorState: false,
      emailDomainErrorState: false,
    }
  },
  computed: {
    ...mapGetters({
      emailDomain: "emailDeliverability/domainlist",
      overviewData: "emailDeliverability/getOverview",
    }),
  },
  mounted() {
    this.fetchOverview()
    this.fetchDomainData()
  },
  methods: {
    ...mapActions({
      getEmailDomain: "emailDeliverability/getDomain",
      getOverviewData: "emailDeliverability/getEmailDeliverabilityOverview",
    }),
    async fetchOverview() {
      this.loading = true
      try {
        await this.getOverviewData()
        this.entity.overAllRate = this.overviewData?.overall_inbox_rate || null
        this.entity.overviewList =
          this.overviewData?.sending_domains_overview || []
        this.deliveredCountData =
          this.overviewData?.delivered_open_rate_overview || []
      } catch (error) {
        this.emailOverviewErrorState = true
      }
      this.loading = false
    },
    async fetchDomainData() {
      try {
        await this.getEmailDomain()
        if (this.emailDomain) {
          this.domainChartData = {
            sent: {
              data: this.emailDomain.sent,
              type: "sent",
            },
            openRate: {
              data: this.emailDomain.open_rate,
              type: "open rate",
            },
            deliveredRate: {
              data: this.emailDomain.delivered_rate,
              type: "Delivered rate",
            },
            clickRate: {
              data: this.emailDomain.click_rate,
              type: "Click rate",
            },
            unsubscribeRate: {
              data: this.emailDomain.unsubscribe_rate,
              type: "Unsubscribe rate",
            },
            complaintsRate: {
              data: this.emailDomain.complaints_rate,
              type: "Complaints rate",
            },
          }
        }
      } catch (error) {
        this.emailDomainErrorState = true
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.idr-wrapper {
  ::v-deep .v-breadcrumbs {
    li {
      font-family: Open Sans Light;
      font-size: 28px;
      font-style: normal;
      font-weight: 400 !important;
      line-height: 40px;
      letter-spacing: 0px;
      text-align: left;
    }
  }

  .overview-card {
    border-radius: 12px !important;
  }

  ::v-deep .container {
    height: calc(100vh - 70px) !important;
  }
}
::-webkit-scrollbar {
  width: 5px;
}
::-webkit-scrollbar-track {
  box-shadow: inset 0 0 5px var(--v-white-base);
  border-radius: 10px;
}
::-webkit-scrollbar-thumb {
  background: var(--v-black-lighten3);
  border-radius: 5px;
}
::-webkit-scrollbar-thumb:hover {
  background: var(--v-black-lighten3);
}
.header-section {
  position: fixed;
  width: 89%;
  z-index: 6 !important;
}
.content-section {
  margin-top: 110px;
  ::v-deep .error-empty-spacing {
    &.empty-page {
      .text-center {
        position: relative;
        bottom: 40px !important;
      }
    }
  }
}
</style>
