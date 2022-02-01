<template>
  <page max-width="100%" class="idr-wrapper">
    <template #header>
      <page-header class="page-header py-5" :header-height="120">
        <template #left>
          <div>
            <breadcrumb
              :items="[
                {
                  text: 'Email Deliverability',
                  disabled: true,
                  href: '/email-deliverability',
                  icon: 'email_deliverability',
                  iconSize: 26,
                  iconColor: 'success',
                  iconColorVariant: 'lighten3',
                },
              ]"
            />
          </div>
          <div class="text-subtitle-1 font-weight-regular col-md-9 pt-0 pl-0">
            In-depth review of key delivery metrics, reputation, and inbox
            indicators that mailbox providers pay attention to when evaluating
            an email sender’s digital reputation.
          </div>
        </template>
      </page-header>
      <v-progress-linear :active="loading" :indeterminate="loading" />
    </template>
    <!-- Header Overview section -->
    <overview :entity="entity" />
    <!-- Delivered count -->
    <delivered-chart />
    <!-- Sending domains overview -->
    <overview-1 :list="entity.overviewList" />
  </page>
</template>

<script>
import Breadcrumb from "../../../components/common/Breadcrumb.vue"
import Page from "../../../components/Page.vue"
import PageHeader from "../../../components/PageHeader.vue"
import DeliveredChart from "./DeliveredChart.vue"
import Overview1 from "./Domain/Overview.vue"
import Overview from "./Overview.vue"
export default {
  name: "EmailDeliverability",
  components: {
    Page,
    PageHeader,
    Breadcrumb,
    Overview,
    DeliveredChart,
    Overview1,
  },
  data() {
    return {
      loading: false,
      entity: {
        description:
          "Email engagement is key for successful email deliverability. The displayed charts highlight performance for the last 90 days.",
        overAllRate: 0.95,
        overviewList: [
          {
            domain: "Domain name",
            sent: 554,
            bounce_rate: 0.14,
            open_rate: 0.91,
            click_rate: 0.85,
          },
          {
            domain: "Domain name",
            sent: 554,
            bounce_rate: 0.14,
            open_rate: 0.91,
            click_rate: 0.85,
          },
          {
            domain: "Domain name",
            sent: 554,
            bounce_rate: 0.14,
            open_rate: 0.91,
            click_rate: 0.85,
          },
        ],
      },
    }
  },
}
</script>

<style lang="scss" scoped>
.overview-card {
  border-radius: 12px !important;
}
.overview-table {
  ::v-deep .v-data-table {
    .v-data-table-header {
      tr {
        height: 32px !important;
      }
      th {
        background: var(--v-primary-lighten2);
      }
    }
  }
  ::v-deep .v-data-table .v-data-table-header th:first-child {
    border-top-left-radius: 12px !important;
  }
  ::v-deep .v-data-table .v-data-table-header th:last-child {
    border-top-right-radius: 12px !important;
  }
}
</style>
