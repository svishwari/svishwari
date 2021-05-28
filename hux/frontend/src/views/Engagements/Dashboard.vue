<template>
  <div class="engagement-dash">
    <!-- Page Header -->
    <PageHeader class="d-flex">
      <template slot="left">
        <div class="d-flex align-center bread-crumb">
          <Breadcrumb :items="breadcrumbItems" />
          <div class="ml-4">
            <Status :status="engagement.status"></Status>
          </div>
        </div>
      </template>
      <template slot="right">
        <v-icon size="22" :disabled="true" class="mr-2">mdi-refresh</v-icon>
        <v-icon size="22" :disabled="true" class="icon-border pa-2 ma-1">
          mdi-pencil
        </v-icon>
        <v-icon size="24" :disabled="true" class="icon-border pa-2 ma-1">
          mdi-download
        </v-icon>
      </template>
    </PageHeader>
    <v-progress-linear :active="loading" :indeterminate="loading" />
    <!-- Page Content Starts here -->
    <div class="inner-wrap px-15 py-8">
      <!-- Summary Cards Wrapper -->
      <div class="summary-wrap d-flex mb-8">
        <MetricCard
          :class="{
            'list-item': true,
            'mr-3': index != summaryCards.length - 1,
            description: index == summaryCards.length - 1,
          }"
          :width="summary.width"
          :min-width="summary.minWidth"
          :height="75"
          v-for="(summary, index) in summaryCards"
          :key="summary.id"
          :title="summary.title"
          :subtitle="summary.value"
          :interactable="false"
        >
          <template slot="short-name" v-if="summary.subLabel">
            <Avatar :name="summary.subLabel" />
          </template>
        </MetricCard>
      </div>

      <div class="audience-summary">
        <!-- Audience Destination Cards Wrapper -->
        <v-card class="rounded-lg" minHeight="145px" elevation="2">
          <v-card-title class="d-flex justify-space-between pb-6 pl-6 pt-5">
            <div class="d-flex align-center">
              <Icon
                type="audiences"
                :size="24"
                color="neroBlack"
                class="mr-2"
              />Audiences
            </div>
            <div class="mt-2">
              <a
                href="#"
                class="d-flex align-center primary--text text-decoration-none"
              >
                <Icon type="audiences" :size="16" class="mr-1" />Add an audience
              </a>
            </div>
          </v-card-title>
          <v-card-text class="pl-6 pr-6 pb-6">
            <div
              class="blank-section rounded-lg pa-5"
              v-if="engagement.audiences.length == 0"
            >
              Nothing to show here yet. Add an audience and then assign a
              destination.
            </div>
            <v-col class="d-flex flex-row pl-0 pt-0 pr-0 overflow-auto pb-3">
              <status-list
                v-for="(item) in engagement.audiences"
                :key="item.id"
                :title="item.name"
                :destinations="item.destinations"
              ></status-list>
            </v-col>
          </v-card-text>
        </v-card>
        <v-tabs v-model="tabOption" class="mt-8">
          <v-tabs-slider color="yellow"></v-tabs-slider>

          <v-tab key="displayAds" class="pa-2" color>
            <Icon type="display_ads" :size="10" class="mr-2" />Display ads
          </v-tab>
          <v-tab key="email">@ Email</v-tab>
        </v-tabs>
        <v-tabs-items v-model="tabOption" class="mt-2">
          <v-tab-item key="displayAds" class="rounded-lg">
            <v-card flat>
              <v-card-text class="d-flex mt-2 rounded-lg summary-wrap">
                <MetricCard
                  class="list-item mr-2"
                  :width="item.width"
                  :height="70"
                  v-for="(item) in displayAdsSummary"
                  :key="item.id"
                  :title="item.title"
                  :subtitle="item.value"
                  :interactable="false"
                ></MetricCard>
              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item key="email" class="rounded-lg">
            <v-card flat>
              <v-card-text class="mt-2 rounded-lg">
                <v-row class="summary-wrap pl-3 pr-3">
                  <MetricCard
                    class="list-item mr-1 rounded-lg"
                    :min-width="item.width"
                    :height="70"
                    v-for="(item) in emailSummary"
                    :key="item.id"
                    :title="item.title"
                    :subtitle="item.value"
                    :interactable="false"
                  ></MetricCard>
                </v-row>
              </v-card-text>
            </v-card>
          </v-tab-item>
        </v-tabs-items>
        <v-card minHeight="145px" elevation="2" class="mt-6">
          <v-card-title class="d-flex justify-space-between pb-6">
            <div class="d-flex align-center">
              <Icon
                type="audiences"
                :size="24"
                color="neroBlack"
                class="mr-2"
              />Audience performance
            </div>
          </v-card-title>
          <v-card-text class="pl-6 pr-6 pb-6 mt-6">
            <div
              class="blank-section rounded-sm pa-5"
              v-if="engagement.audiences.length == 0"
            >
              Nothing to show here yet. Add an audience and then assign a
              destination.
            </div>
          </v-card-text>
        </v-card>
      </div>
    </div>
  </div>
</template>

<script>
import moment from "moment"
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import Status from "@/components/common/Status"
import MetricCard from "@/components/common/MetricCard"
import Avatar from "@/components/common/Avatar"
import Icon from "@/components/common/Icon"
import StatusList from "../../components/common/StatusList.vue"

export default {
  name: "engagementDashboard",
  components: {
    PageHeader,
    Breadcrumb,
    Status,
    MetricCard,
    Avatar,
    Icon,
    StatusList,
  },
  data() {
    return {
      engagement: {
        name: "Engagement name",
        status: "active",
        schedule: "Manual",
        update_time: "2020-07-10T11:45:01.984Z",
        updated_by: "Mohit Bansal",
        created_time: "2020-07-10T11:45:01.984Z",
        created_by: "Mohit Bansal",
        description:
          "This is the filled out description for this particular engagement. If they didn’t add any then this box will not appear. ",
        audiences: [
          {
            name: "Audience - Main",
            destinations: [
              {
                id: 1,
                type: "mailchimp",
                status: "active",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },
              {
                id: 2,
                type: "facebook",
                status: "active",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },
              {
                id: 3,
                type: "insightIQ",
                status: "active",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },
              {
                id: 4,
                type: "adobe-experience",
                status: "pending",
                size: null,
                lastDeliveredOn: null,
              },
            ],
          },
          {
            name: "Audience 1",
            destinations: [
              {
                id: 1,
                type: "mailchimp",
                status: "active",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },

              {
                id: 2,
                type: "facebook",
                status: "active",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },
              {
                id: 3,
                type: "insightIQ",
                status: "pending",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },
            ],
          },
          {
            name: "Audience 2",
            destinations: [
              {
                id: 1,
                type: "mailchimp",
                status: "pending",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },
              {
                id: 2,
                type: "facebook",
                status: "active",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },
            ],
          },
          {
            name: "Audience 3",
            destinations: [
              {
                id: 1,
                type: "mailchimp",
                status: "pending",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },
              {
                id: 2,
                type: "facebook",
                status: "active",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },
            ],
          },
          {
            name: "Audience - test",
            destinations: [
              {
                id: 2,
                type: "facebook",
                status: "active",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },
            ],
          },
        ],
      },
      loading: false,
      tabOption: 0,
    }
  },
  computed: {
    breadcrumbItems() {
      const items = [
        {
          text: "Engagements",
          disabled: false,
          href: this.$router.resolve({ name: "Engagements" }).href,
          icon: "engagements",
        },
      ]
      if (this.engagement) {
        items.push({
          text: this.engagement.name,
          disabled: false,
        })
      }
      return items
    },
    summaryCards() {
      const summary = [
        {
          id: 1,
          title: "Delivery schedule",
          value: this.fetchKey("schedule"),
          subLabel: null,
          width: "12.6%",
          minWidth: "146px",
        },
        {
          id: 2,
          title: "Last updated",
          value: this.getDateStamp(this.fetchKey("update_time")),
          subLabel: this.fetchKey("updated_by"),
          width: "19%",
          minWidth: "164px",
        },
        {
          id: 3,
          title: "Created",
          value: this.getDateStamp(this.fetchKey("created_time")),
          subLabel: this.fetchKey("created_by"),
          width: "19%",
          minWidth: "164px",
        },
        {
          id: 4,
          title:
            "This is the filled out description for this particular engagement. If they didn’t add any then this box will not appear.",
          value: null,
          subLabel: null,
          width: "48%",
          minWidth: "518px",
        },
      ]
      return summary.filter((item) => item.title !== null)
    },
    displayAdsSummary() {
      return [
        { id: 1, title: "Spend", value: "$2.1M", width: "10%" },
        { id: 2, title: "Reach", value: "500k", width: "10%" },
        { id: 3, title: "Impressions", value: "456,850", width: "10%" },
        { id: 4, title: "Conversions", value: "521,006", width: "10%" },
        { id: 5, title: "Clicks", value: "498,587", width: "10%" },
        { id: 6, title: "Frequency", value: "500", width: "10%" },
        { id: 7, title: "CPM", value: "$850", width: "10%" },
        { id: 8, title: "CTR", value: "52%", width: "10%" },
        { id: 9, title: "CPA", value: "$652", width: "10%" },
        { id: 10, title: "CPC", value: "$485", width: "10%" },
        { id: 11, title: "Engagement rate", value: "56%", width: "10%" },
      ]
    },
    emailSummary() {
      return [
        { id: 1, title: "Sent", value: "Yesterday", width: "95px" },
        { id: 2, title: "Hard bounces / Rate", value: "125 • 0.1%", width: "139px" },
        { id: 3, title: "Delivered / Rate", value: "125 • 0.1%", width: "113px" },
        { id: 4, title: "Open / Rate", value: "365.2k • 72.8%", width: "122px" },
        { id: 5, title: "Click / CTR", value: "365.2k • 72.8%", width: "122px" },
        { id: 6, title: "Click to open rate  ", value: "72.8%", width: "121px" },
        {
          id: 7, 
          title: "Unique clicks / Unique opens",
          value: "365.2k • 72.8%",
          width: "185px",
        },
        {
          id: 8, 
          title: "Unsubscribe / Rate",
          value: "365.2k • 72.8%",
          width: "130px",
        },
      ]
    },
  },
  methods: {
    getDateStamp(value) {
      return value ? moment(new Date(value)).fromNow() + " by" : "-"
    },
    fetchKey(key) {
      return this.engagement ? this.engagement[key] : "-"
    },
    showCard(card) {
      if (card.cardType !== "description") return true
      else {
        return !!card.title
      }
    },
  },
  async mounted() {
    this.loading = true
    this.loading = false
  },
}
</script>

<style lang="scss" scoped>
.engagement-dash {
  .page-header--wrap {
    box-shadow: 0px 1px 0px var(--v-lightGrey-base) !important;
  }
  .inner-wrap {
    .summary-wrap {
      .metric-card-wrapper {
        border: 1px solid var(--v-zircon-base);
        box-sizing: border-box;
        border-radius: 12px;
        ::v-deep .v-list-item__content {
          padding-top: 15px;
          padding-bottom: 15px;
          .v-list-item__title {
            font-size: 12px;
            line-height: 16px;
            margin: 0 !important;
          }
          .v-list-item__subtitle {
            margin-bottom: 22px !important;
          }
        }
        &.description {
          ::v-deep .v-list-item__content {
            padding-top: 0px;

            .v-list-item__title {
              font-size: 14px;
              line-height: 22px;

              text-overflow: inherit;
              white-space: inherit;
              color: var(--v-neroBlack-base) !important;
            }
          }
        }
      }
    }
    .v-tabs {
      ::v-deep .v-tabs-bar {
        background: transparent;
        .v-tabs-bar__content {
          border-bottom: 2px solid var(--v-zircon-base);
          .v-tabs-slider-wrapper {
            width: 111px !important;
            .v-tabs-slider {
              background-color: var(--v-skyBlueDark-base) !important;
              border-color: var(--v-skyBlueDark-base) !important;
            }
          }
          .v-tab {
            text-transform: inherit;
            padding: 8px;
            color: var(--v-primary-base);
            svg {
              fill: transparent !important;
            }
            &.v-tab--active {
              color: var(--v-skyBlueDark-base);
            }
          }
        }
      }
    }
    .v-tabs-items {
      background: var(--v-white-base);
      box-shadow: 0px 0px 10px 2px rgba(0, 0, 0, 0.05);
      border-radius: 12px;
    }
  }
}
</style>
