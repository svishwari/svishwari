<template>
  <div class="customer-dashboard-wrap">
    <PageHeader class="background-border">
      <template slot="left">
        <Breadcrumb :items="items" />
      </template>
      <template slot="right">
        <hux-button
          variant="white"
          size="large"
          :isTile="true"
          :iconType="false"
          @click="viewAllCustomer()"
          >View all customers
          <template #custom-icon>
            <Icon type="customer-profiles" :size="24" color="neroBlack" />
          </template>
        </hux-button>
        <v-icon size="22" class="icon-border pa-2 ma-1"> mdi-download </v-icon>
      </template>
    </PageHeader>
    <v-progress-linear :active="loading" :indeterminate="loading" />
    <div class="row px-15 my-2" v-if="primaryItems">
      <MetricCard
        v-for="(item, i) in primaryItems"
        class="ma-5"
        :key="i"
        :grow="i !== 7 ? 1 : 0"
        :title="item.title"
        :subtitle="i !== 7 ? item.subtitle : ''"
        :icon="item.icon"
        :interactable="false"
      >
        <template v-if="i === 7" #subtitle-extended>
          <span class="font-weight-semi-bold"
            >{{ item.date }} <span class="day-time-divider"></span>
            {{ item.time }}
          </span>
        </template>
        <template v-if="i!==7" #extra-item>
          <Tooltip :positionTop="true">
            <template #label-content>
              <Icon type="info" :size="12" />
            </template>
            <template class="newp" #hover-content>
              {{ item.toolTipText }}
            </template>
          </Tooltip>
        </template>
      </MetricCard>
    </div>
    <div class="px-15 my-1" v-if="overviewListItems">
      <v-card class="rounded pa-5 box-shadow-5">
        <div class="overview">Customer overview</div>
        <div class="row overview-list mb-0 ml-0 mt-1">
          <MetricCard
            v-for="(item, i) in overviewListItems"
            class="mr-3"
            :key="i"
            :grow="i === 0 ? 2 : 1"
            :title="item.title"
            :subtitle="item.subtitle"
            :icon="item.icon"
            :interactable="i === 0 ? true : false"
          >
            <template v-if="i == 0" #extra-item>
              <Tooltip :positionTop="true">
                <template #label-content>
                  <Icon type="info" :size="12" />
                </template>
                <template class="newp" #hover-content>
                  {{ item.toolTipText }}
                </template>
              </Tooltip>
            </template>
          </MetricCard>
        </div>
      </v-card>
    </div>
    <v-divider class="my-8"></v-divider>
    <EmptyStateChart>
      <template #chart-image>
        <img src="@/assets/images/empty-state-chart-3.png" alt="Empty state" />
      </template>
    </EmptyStateChart>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import Tooltip from "../../components/common/Tooltip.vue"
import MetricCard from "@/components/common/MetricCard"
import EmptyStateChart from "@/components/common/EmptyStateChart"
import huxButton from "@/components/common/huxButton"
import Icon from "@/components/common/Icon"

export default {
  name: "CustomerProfiles",
  components: {
    MetricCard,
    EmptyStateChart,
    PageHeader,
    Breadcrumb,
    Tooltip,
    huxButton,
    Icon,
  },

  data() {
    return {
      overviewListItems: [
        {
          title: "No. of customers",
          subtitle: "12M",
          toolTipText:
            "Total no. of unique hux ids generated to represent a customer.",
        },
        { title: "Countries", subtitle: "2", icon: "mdi-earth" },
        { title: "US States", subtitle: "52", icon: "mdi-map" },
        { title: "Cities", subtitle: "19k", icon: "mdi-map-marker-radius" },
        { title: "Age", subtitle: "-", icon: "mdi-cake-variant" },
        { title: "Women", subtitle: "52%", icon: "mdi-gender-female" },
        { title: "Men", subtitle: "46%", icon: "mdi-gender-male" },
        { title: "Other", subtitle: "2%", icon: "mdi-gender-male-female" },
      ],
      primaryItems: [
        {
          title: "Total no. of records",
          subtitle: "12M",
          toolTipText: "Total no. of input records across all data feeds.",
        },
        { title: "Match rate", subtitle: "60%", toolTipText: "Percentage of input records that are consolidated into Hux Ids." },
        {
          title: "Unique Hux IDs",
          subtitle: "12M",
          toolTipText: "Total Hux Ids that represent an anonymous or known customer.",
        },
        {
          title: "Anonymous IDs",
          subtitle: "20M",
          toolTipText: "IDs related to online vistors that have not logged in, typically identified by a browser cookie or device id.",
        },
        { title: "Known IDs", subtitle: "20M", toolTipText: "Ids related to profiles that contain PII from online or offline enagagement: name, postal address, email address or phone number." },
        {
          title: "Individual IDs",
          subtitle: "20M",
          toolTipText: "Represents a First Name, Last Name and Address combination, used to identify a customer that lives at an address.",
        },
        {
          title: "Household IDs",
          subtitle: "20M",
          toolTipText: "Represents a Last Name and Address combination, used to identify family members that live at the same address.",
        },
        {
          title: "Updated",
          subtitle: "",
          toolTipText: "Updated",
          date: "Today",
          time: "12:30PM",
        },
      ],
      items: [
        {
          text: "Customer Profiles",
          disabled: true,
          href: "/audiences",
          icon: "customer-profiles",
        },
        {
          text: "",
          disabled: true,
          href: this.$route.path,
        },
      ],
      loading: false,
    }
  },

  computed: {
    ...mapGetters({
      customers: "customers/list",
      overview: "customers/overview",
    }),
  },

  methods: {
    ...mapActions({
      getCustomers: "customers/getAll",
      getOverview: "customers/getOverview",
    }),
    viewAllCustomer() {},
  },

  async mounted() {
    this.loading = true
    
    await this.getOverview()
    await this.getCustomers()
    this.loading = false
  },
}
</script>

<style lang="scss" scoped>
::v-deep.v-btn:not(.v-btn--round).v-size--large {
  height: 28px;
  min-width: 178px;
  padding: 12px;
}

::v-deep .v-btn {
  margin-right: 14px;
  .v-btn__content {
    color: rgba(0, 85, 135, 1);
  }
}

.my-2 {
  margin-top: 24px !important;
  margin-bottom: 24px !important;
  margin-left: -6px;
  margin-right: -6px;
}

.day-time-divider:before {
  content: " \25CF";
  font-size: 8px;
}

.ma-5 {
  margin: 6px !important;
}

.customer-dashboard-wrap {
  ::v-deep .mdi-chevron-right::before {
    content: none;
  }
}
</style>
