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
      <template slot="right" class="paheHeadRightPanel">
        <v-menu offset-y :close-on-content-click="false">
          <template v-slot:activator="{ on, attrs }">
            <v-btn color="primary configBtn" v-bind="attrs" v-on="on">
              <v-icon large color="white darken-2">mdi-cog</v-icon>
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
  filters: {
    TitleCase(value) {
      return value
        .replace(/([A-Z])/g, (match) => ` ${match}`)
        .replace(/^./, (match) => match.toUpperCase())
        .trim()
    },
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
  .page-header--right {
    .configBtn {
      width: 40px;
      height: 40px;
      min-width: 40px;
      .v-icon {
        font-size: 23px !important;
        color: white !important;
      }
    }
  }

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
      color: #005587;
    }
    .description {
      color: inherit;
    }
  }
  .v-input {
    margin: 0;
    .v-input__control {
      background: red;
      .v-messages {
        display: none !important;
      }
    }
  }
}
</style>
