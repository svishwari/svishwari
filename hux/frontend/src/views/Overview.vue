<template>
  <div class="overview-wrap">
    <PageHeader :title="`Welcome back, ${fullName}!`" class="py-7">
      <template slot="description">
        Hux is here to help you make better, faster decisions to improve your
        Customer Experiences.
        <a
          class="text-decoration-none"
          href="https://consulting.deloitteresources.com/offerings/customer-marketing/advertising-marketing-commerce/Pages/hux_marketing.aspx"
          target="_blank"
        >
          Learn More &gt;
        </a>
      </template>
      <template slot="right" class="paheHeadRightPanel">
        <v-menu offset-y :close-on-content-click="false">
          <template #activator="{ on, attrs }">
            <v-btn
              min-width="40"
              height="40"
              width="40"
              color="primary"
              v-bind="attrs"
              v-on="on"
              :disabled="true"
            >
              <v-icon size="23" color="white">mdi-cog</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item class="drop-wrap">
              <div class="title-wrap">
                <span class="heading">Configure Dashboard</span>
                <span class="description">Show or hide element panels.</span>
              </div>
              <v-checkbox
                v-for="(item, ix) in Object.keys(configureOptions)"
                :key="ix"
                :label="item | TitleCase"
                v-model="configureOptions[item]"
                hide-details
              >
              </v-checkbox>
            </v-list-item>
          </v-list>
        </v-menu>
      </template>
    </PageHeader>
    <div class="quickAccessMenu" v-if="this.configureOptions['configureHux']">
      <h5 class="mb-3 text-h5">Configure Hux</h5>
      <div class="card-wrap d-flex">
        <CardInfo
          v-for="(item, i) in configureHuxOptions"
          :key="i"
          :title="item.title"
          :description="item.description"
          :active="item.active"
          :to="item.route"
        ></CardInfo>
      </div>
    </div>
    <EmptyStateChart>
      <template #chart-image>
        <img src="@/assets/images/empty-state-chart-1.png" alt="Empty state" />
      </template>
    </EmptyStateChart>
  </div>
</template>

<script>
import PageHeader from "@/components/PageHeader"
import CardInfo from "@/components/common/CardInfo"
import EmptyStateChart from "@/components/common/EmptyStateChart"

export default {
  name: "overview",
  components: {
    PageHeader,
    CardInfo,
    EmptyStateChart,
  },
  data() {
    return {
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
            "Choose your data source from various customer touchpoint systems.",
          route: {
            name: "DataSourceConfiguration",
            query: { select: true },
          },
          active: true,
        },
        {
          title: "Add a destination",
          description:
            "Choose a destination where your actionable intelligence will be consumed.",
          route: {
            name: "DestinationConfiguration",
            query: { select: true },
          },
          active: true,
        },
        {
          title: "Build your models",
          description:
            "Build predictive models that intelligently characterize customer opportunities.",
          route: { name: "Models" },
          active: false,
        },
        {
          title: "Create an audience",
          description:
            "Create an audience based on customized orchestrated choices.",
          route: { name: "AudienceConfiguration" },
          active: true,
        },
        {
          title: "Create an engagement",
          description:
            "Put all this great data and information to good use by creating an engagement.",
          route: { name: "EngagementConfiguration" },
          active: true,
        },
      ],
    }
  },
  computed: {
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
}
</script>

<style lang="scss" scoped>
.overview-wrap {
  .quickAccessMenu {
    background: var(--v-aliceBlue-base);
    min-height: 265px;
    padding: 16px 30px 40px 30px;
    overflow-x: auto;
    h5 {
      line-height: 19px;
      letter-spacing: 0.5px;
      color: var(--v-neroBlack-base);
    }
    .card-wrap {
      .v-card {
        margin-right: 15px;
        &.v-card--disabled {
          background: var(--v-background-base);
        }
        &:hover {
          @extend .box-shadow-3;
        }
      }
    }
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
