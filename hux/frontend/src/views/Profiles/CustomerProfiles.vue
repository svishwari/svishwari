<template>
  <div class="audience-insight-wrap">
    <PageHeader class="background-border">
      <template slot="left">
        <Breadcrumb :items="items" />
      </template>
      <template slot="right">
          <hux-button
          button-text="View all customers"
          variant="white"
          size="large"
          :isTile="true"
          :iconType="false"
          icon="customer-profiles"
          iconPosition = "left"
        ></hux-button>
        <v-icon size="22" class="icon-border pa-2 ma-1"> mdi-download </v-icon>
      </template>
    </PageHeader>
    <v-progress-linear :active="loading" :indeterminate="loading" />
    <div class="row px-15 my-1" v-if="primaryItems">
      <MetricCard
        v-for="(item, i) in primaryItems"
        class="ma-5"
        :width="143"
        :height="80"
        :key="i"
        :title="item.title"
        :titleTooltip="i==0?'wow':''"
        :subtitle="item.subtitle"
        :icon="item.icon"
        :interactable="true"
      >
        <!-- <template slot="short-name">
          <v-menu bottom offset-y open-on-hover>
            <template v-slot:activator="{ on, attrs }">
              <span
                class="blue-grey d-flex align-center justify-center"
                v-bind="attrs"
                v-on="on"
                v-bind:style="{ 'border-color': getColorCode(item.shortName) }"
              >
                {{ getShortName(item.shortName) }}
              </span>
            </template>
            <v-list>
              <v-list-item>
                <v-list-item-title>{{ item.fullName }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </template> -->
      </MetricCard>

      <!-- <MetricCard
        class="ma-4"
        width="53%"
        :height="80"
        :interactable="false"
        :title="'Attributes'"
      >
        <template slot="extra-item">
          <div class="container pl-0">
            <ul>
              <li>
                <lifetimeValue />
                Lifetime Value
              </li>
              <li>
                <churn />
                Churn
              </li>
              <li>
                <plus />
                Age, Email, Zipcode
              </li>
            </ul>
          </div>
        </template>
      </MetricCard> -->
    </div>
    <div class="px-15 my-1" v-if="overviewListItems">
      <v-card
        height="150"
        width="fit-content"
        elevation="1"
        class="rounded px-5 pt-5"
      >
        <div class="overview">Customer overview</div>
        <div class="row overview-list mb-0 ml-0 mt-1">
          <MetricCard
            v-for="(item, i) in overviewListItems"
            class="list-item mr-3"
            :width="135"
            :height="80"
            :key="i"
            :title="item.title"
            titleTooltip="wow"
            :subtitle="item.subtitle"
            :icon="item.icon"
            :interactable="true"
          ></MetricCard>
        </div>
      </v-card>
    </div>
    <v-divider class="my-8"></v-divider>
    <EmptyStateChart>
      <template v-slot:chart-image>
        <img src="@/assets/images/empty-state-chart-3.png" alt="Empty state" />
      </template>
    </EmptyStateChart>
  </div>
</template>

<script>
import { generateColor } from "@/utils"
import { mapGetters, mapActions } from "vuex"
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import MetricCard from "@/components/common/MetricCard"
import EmptyStateChart from "@/components/common/EmptyStateChart"
import lifetimeValue from "@/assets/images/lifetimeValue.svg"
import churn from "@/assets/images/churn.svg"
import plus from "@/assets/images/plus.svg"
import huxButton from "@/components/common/huxButton"
export default {
  name: "CustomerProfiles",
  components: {
    MetricCard,
    EmptyStateChart,
    PageHeader,
    Breadcrumb,
    lifetimeValue,
    churn,
    plus,
    huxButton
  },
  data() {
    return {
      overviewListItems: [
        { title: "No. of customers", subtitle: "12M" },
        { title: "Countries", subtitle: "2", icon: "mdi-earth" },
        { title: "US States", subtitle: "52", icon: "mdi-map" },
        { title: "Cities", subtitle: "19k", icon: "mdi-map-marker-radius" },
        { title: "Age", subtitle: "-", icon: "mdi-cake-variant" },
        { title: "Women", subtitle: "52%", icon: "mdi-gender-female" },
        { title: "Men", subtitle: "46%", icon: "mdi-gender-male" },
        { title: "Other", subtitle: "2%", icon: "mdi-gender-male-female" },
      ],
      primaryItems: [
        { title: "Total no. of records", subtitle: "12M" },
        { title: "Match rate", subtitle: "60%" },
        { title: "Unique Hux IDs", subtitle: "12M" },
        { title: "Anonymous IDs", subtitle: "20M" },
        { title: "Known IDs", subtitle: "20M" },
        { title: "Individual IDs", subtitle: "20M" },
        { title: "Household IDs", subtitle: "20M" },
        { title: "Updated", subtitle: "Today 12:30PM" },
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
      getAudience: "audiences/audience",
    }),
    audience() {
      return this.getAudience(this.$route.params.id)
    },
  },
  methods: {
    ...mapActions({
      getAudienceById: "audiences/getAudienceById",
    }),
    refresh() {},
    getFormattedTime(time) {
      return this.$options.filters.Date(time, "relative") + " by"
    },
    getShortName(fullname) {
      return fullname
        .split(" ")
        .map((n) => n[0])
        .join("")
    },
    getColorCode(name) {
      return generateColor(name, 30, 60) + " !important"
    },
  },
  async mounted() {
    this.loading = true
    await this.getAudienceById(this.$route.params.id)
    this.items[1].text = this.audience.name
    this.loading = false
  },
}
</script>
<style lang="scss" scoped>
.audience-insight-wrap {
    ::v-deep .menu-cell-wrapper .action-icon {
    display: none;
  }

    ::v-deep .mdi-chevron-right::before {
    content: none;
}

::v-deep .v-application .ma-4 {
    margin: 5px !important;
    background-color: red;
}

.ma-5 {
     margin: 5px !important;
   // background-color: red; 
}
  .container {
    ul {
      padding: 0;
      margin: 0;
      list-style-type: none;
    }
  }
  .container {
    ul {
      li {
        width: fit-content;
        height: auto;
        float: left;
        margin-left: 2%;
      }
    }
  }
  .blue-grey {
    border-width: 2px;
    border-style: solid;
    border-radius: 50%;
    font-size: 14px;
    width: 35px;
    height: 35px;
    line-height: 22px;
    color: var(--v-neroBlack-base) !important;
    cursor: default !important;
    background: transparent !important;
  }
}
</style>
