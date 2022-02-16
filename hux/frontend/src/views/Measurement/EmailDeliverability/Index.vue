<template>
  <page max-width="100%" class="idr-wrapper">
    <template #header>
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
                  iconSize: 36,
                  iconColor: 'success',
                  iconColorVariant: 'lighten3',
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
    </template>
    <div v-if="overviewData && !loading">
      <!-- Header Overview section -->
      <overview :entity="entity" />
      <!-- Delivered count -->
      <delivered-chart
        v-if="deliveredCountData.length > 0"
        :email-data="deliveredCountData"
      />
      <!-- Sending domains overview -->
      <overview-1 v-if="overviewData" :list="entity.overviewList" />
      <!-- Domains overview chart -->
      <v-row v-if="domainChartData.sent && domainChartData.deliveredRate">
        <v-col md="6">
          <v-card class="mt-3 rounded-lg box-shadow-5" height="365">
            <v-card-title class="pb-2 pl-6 pt-5">
              <h3 class="text-h3">Sent</h3>
            </v-card-title>
            <domain-overview-chart
              :chart-data="domainChartData.sent.data"
              :chart-type="domainChartData.sent.type"
            />
          </v-card>
        </v-col>
        <v-col md="6">
          <v-card class="mt-3 rounded-lg box-shadow-5" height="365">
            <v-card-title class="pb-2 pl-6 pt-5">
              <h3 class="text-h3">Delivered rate</h3>
            </v-card-title>
            <domain-overview-chart
              :chart-data="domainChartData.deliveredRate.data"
              :chart-type="domainChartData.deliveredRate.type"
            />
          </v-card>
        </v-col>
      </v-row>

      <v-row v-if="domainChartData.openRate && domainChartData.clickRate">
        <v-col md="6">
          <v-card class="mt-3 rounded-lg box-shadow-5" height="365">
            <v-card-title class="pb-2 pl-6 pt-5">
              <h3 class="text-h3">Open rate</h3>
            </v-card-title>
            <domain-overview-chart
              :chart-data="domainChartData.openRate.data"
              :chart-type="domainChartData.openRate.type"
            />
          </v-card>
        </v-col>
        <v-col md="6">
          <v-card class="mt-3 rounded-lg box-shadow-5" height="365">
            <v-card-title class="pb-2 pl-6 pt-5">
              <h3 class="text-h3">Click rate</h3>
            </v-card-title>
            <domain-overview-chart
              :chart-data="domainChartData.clickRate.data"
              :chart-type="domainChartData.clickRate.type"
            />
          </v-card>
        </v-col>
      </v-row>

      <v-row
        v-if="domainChartData.unsubscribeRate && domainChartData.complaintsRate"
      >
        <v-col md="6">
          <v-card class="mt-3 rounded-lg box-shadow-5" height="365">
            <v-card-title class="pb-2 pl-6 pt-5">
              <h3 class="text-h3">Unsubscribe Rate</h3>
            </v-card-title>
            <domain-overview-chart
              :chart-data="domainChartData.unsubscribeRate.data"
              :chart-type="domainChartData.unsubscribeRate.type"
            />
          </v-card>
        </v-col>
        <v-col md="6">
          <v-card class="mt-3 rounded-lg box-shadow-5" height="365">
            <v-card-title class="pb-2 pl-6 pt-5">
              <h3 class="text-h3">Complaints rate</h3>
            </v-card-title>
            <domain-overview-chart
              :chart-data="domainChartData.complaintsRate.data"
              :chart-type="domainChartData.complaintsRate.type"
            />
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
  },
  data() {
    return {
      loading: false,
      entity: {
        description:
          "Email engagement is key for successful email deliverability. The displayed charts highlight performance for the last 90 days.",
        overAllRate: 0.95,
        overviewList: [],
      },
      domainChartData: {},
      deliveredCountData: [],
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
      await this.getOverviewData()
      this.entity.overAllRate = this.overviewData.overall_inbox_rate,
      this.entity.overviewList = this.overviewData.sending_domains_overview,
      this.deliveredCountData = this.overviewData.delivered_open_rate_overview
      this.loading = false
    },
    async fetchDomainData() {
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
}
</style>
