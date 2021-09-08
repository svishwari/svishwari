<template>
  <div class="overview-wrap">
    <page-header
      :title="`Welcome back, ${fullName}!`"
      class="py-7"
      header-height="auto"
    >
      <template slot="description">
        Hux is here to help you make better, faster decisions to improve your
        customer experiences.
        <a
          class="text-decoration-none"
          href="https://consulting.deloitteresources.com/offerings/customer-marketing/advertising-marketing-commerce/Pages/hux_marketing.aspx"
          target="_blank"
        >
          Learn More &gt;
        </a>
      </template>
    </page-header>
    <div v-if="configureOptions['configureHux']" class="quickAccessMenu">
      <h5 class="mb-3 text-h5">Configure Hux</h5>
      <div class="card-wrap d-flex">
        <card-info
          v-for="(item, i) in configureHuxOptions"
          :key="i"
          :title="item.title"
          :description="item.description"
          :active="item.active"
          :to="item.route"
        ></card-info>
      </div>
    </div>
    <v-row class="px-8 mt-2">
      <v-col md="12">
        <v-card class="mt-3 rounded-lg box-shadow-5" height="350">
          <v-card-title class="chart-style pb-2 pl-5 pt-5">
            <div class="mt-2">
              <span class="neroBlack--text text-h5">
                Total customers
                <span class="text-body-2 time-frame">
                  ({{ timeFrameLabel }})
                </span>
              </span>
            </div>
          </v-card-title>
          <v-progress-linear
            v-if="loadingCustomerChart"
            :active="loadingCustomerChart"
            :indeterminate="loadingCustomerChart"
          />
          <total-customer-chart
            v-if="!loadingCustomerChart"
            :customers-data="totalCustomers"
          />
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import PageHeader from "@/components/PageHeader"
import CardInfo from "@/components/common/CardInfo"
import TotalCustomerChart from "@/components/common/TotalCustomerChart/TotalCustomerChart"

export default {
  name: "Overview",
  components: {
    PageHeader,
    CardInfo,
    TotalCustomerChart,
  },
  data() {
    return {
      loadingCustomerChart: false,
      timeFrameLabel: "last 9 months",
      configureOptions: {
        configureHux: true,
        activeCustomers: true,
        currentEngagements: true,
        upcomingEngagements: true,
        dataManagement: false,
      },
      configureHuxOptions: [
        {
          title: "Connect data source",
          description:
            "Connect your data sources to enable data unification in a single location.",
          route: {
            name: "DataSourceConfiguration",
            query: { select: true },
          },
          active: true,
        },
        {
          title: "Add a destination",
          description:
            "Select the destinations you wish to deliver your audiences and/or engagements to.",
          route: {
            name: "DestinationConfiguration",
            query: { select: true },
          },
          active: true,
        },
        {
          title: "Create an audience",
          description:
            "Create audiences by segmenting your customer list based on who you wish to target.",
          route: { name: "AudienceConfiguration" },
          active: true,
        },
        {
          title: "Create an engagement",
          description:
            "Select your audiences and destinations where you wish to run campaigns on.",
          route: { name: "EngagementConfiguration" },
          active: true,
        },
      ],
    }
  },
  computed: {
    ...mapGetters({
      totalCustomers: "customers/totalCustomers",
    }),
    firstName() {
      return this.$store.getters.getFirstname
    },
    lastName() {
      return this.$store.getters.getLastName
    },
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

<style lang="scss" scoped>
.overview-wrap {
  .page-header--wrap {
    @extend .box-shadow-plain;
  }
  .quickAccessMenu {
    background: var(--v-aliceBlue-base);
    min-height: 265px;
    padding: 16px 30px 40px 30px;
    overflow-x: auto;
    border: 1px solid var(--v-zircon-base);
    h5 {
      line-height: 19px;
      letter-spacing: 0.5px;
      color: var(--v-neroBlack-base);
    }
    .card-wrap {
      .v-card {
        margin-right: 15px;
        @extend .box-shadow-5;
        &.v-card--disabled {
          background: var(--v-background-base);
        }
        &:hover {
          @extend .box-shadow-3;
        }
      }
    }
  }
  .time-frame {
    color: var(--v-gray-base) !important;
  }
}
.drop-wrap {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 19px 18px 19px 25px;
  min-height: inherit;
  .title-wrap {
    display: flex;
    flex-direction: column;
    font-style: normal;
    font-weight: normal;
    font-size: 12px;
    line-height: 16px;
    min-height: 64px;
    .heading {
      text-transform: uppercase;
      margin-bottom: 5px;
      color: var(--v-primary-base);
    }
    .description {
      color: inherit;
    }
  }
  .v-input {
    margin: 0;
    .v-input__control {
      background: var(--v-error-base);
      .v-messages {
        display: none !important;
      }
    }
  }
}
</style>
