<template>
  <div class="overview-wrap">
    <PageHeader
      :title="'Welcome back, ' + firstName + ' ' + lastName + '!'"
      icon="mdi-bullhorn-outline"
    >
      <template slot="description">
        <div>
          Hux is here to help you make better, faster decisions to improve your
          Customer Experiences.
          <a>Learn More ></a>
        </div>
      </template>
      <template slot="right">
        <v-btn>
          <v-icon large color="white darken-2">mdi-cogs</v-icon>
        </v-btn>
      </template>
    </PageHeader>
    <div class="quickAccessMenu">
      <h6>Configure Hux</h6>
      <div class="card-wrap">
        <CardInfo
          v-for="(item, i) in configureHuxOptions"
          :key="i"
          :title="item.title"
          :description="item.description"
          :active="item.active"
        ></CardInfo>
      </div>
    </div>
  </div>
</template>

<script>
import PageHeader from "@/components/PageHeader"
import CardInfo from "@/components/common/CardInfo"

export default {
  name: "overview",
  components: {
    PageHeader,
    CardInfo,
  },
  data() {
    return {
      configureOptions: {
        configureHux: true,
        activeCustomers: true,
        currentCampaigns: true,
        upcomingCampaigns: true,
        dataManagement: false,
      },
      configureHuxOptions: [
        {
          title: "Add a destination",
          description:
            "Choose a destination where your actionable intelligence will be consumed.",
          path: "/connections",
          active: true,
        },
        {
          title: "Create a campaign",
          description: "Descriptive text for the action item.",
          path: "/campaign",
          active: true,
        },
        {
          title: "Create an audience",
          description: "Descriptive text for the action item.",
          path: "/audiences",
          active: true,
        },
        {
          title: "Build your models",
          description: "Descriptive text for the action item.",
          path: "/audiences",
          active: false,
        },
        {
          title: "Connect data source",
          description: "Descriptive text for the action item.",
          path: "/audiences",
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
  },
}
</script>

<style lang="scss" scoped>
.overview-wrap {
  .quickAccessMenu {
    background: #ecf4f9;
    min-height: 265px;
    padding: 16px 30px 30px 30px;
    h6 {
      font-style: normal;
      font-weight: normal;
      font-size: 14px;
      line-height: 19px;
      /* identical to box height */

      letter-spacing: 0.5px;

      /* Text/Dark - D */

      color: #1e1e1e;
      margin-bottom: 20px;
    }
    .card-wrap {
      display: flex;
      .v-card {
        margin-right: 15px;
        &.v-card--disabled {
          background: #f9fafb;
        }
      }
    }
  }
}
</style>
