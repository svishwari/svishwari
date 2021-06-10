<template>
  <div class="engagement-dash">
    <!-- Page Header -->
    <PageHeader class="d-flex">
      <template slot="left">
        <div class="d-flex align-center bread-crumb">
          <Breadcrumb :items="breadcrumbItems" />
          <div class="ml-3">
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
      <div class="summary-wrap d-flex mb-6">
        <MetricCard
          class="mr-3"
          :title="summaryCards[0].title"
          :subtitle="summaryCards[0].value"
        >
        </MetricCard>
        <MetricCard class="mr-3" :title="summaryCards[1].title">
          <template slot="subtitle-extended" v-if="summaryCards[1].subLabel">
            <span class="mr-2">
              <tooltip>
                <template slot="label-content">
                  {{ summaryCards[1].value }}
                </template>
                <template slot="hover-content">
                  {{ summaryCards[1].hoverValue | Date | Empty }}
                </template>
              </tooltip>
            </span>
            <Avatar :name="summaryCards[1].subLabel" />
          </template>
        </MetricCard>
        <MetricCard class="mr-3" :title="summaryCards[2].title">
          <template slot="subtitle-extended" v-if="summaryCards[1].subLabel">
            <span class="mr-2">
              <tooltip>
                <template slot="label-content">
                  {{ summaryCards[2].value }}
                </template>
                <template slot="hover-content">
                  {{ summaryCards[2].hoverValue | Date | Empty }}
                </template>
              </tooltip>
            </span>
            <Avatar :name="summaryCards[1].subLabel" />
          </template>
        </MetricCard>
        <MetricCard class="mr-3" :title="summaryCards[3].title" :maxWidth="540">
        </MetricCard>
      </div>

      <div class="audience-summary">
        <!-- Audience Destination Cards Wrapper -->
        <v-card class="rounded-lg card-style" minHeight="145px" flat>
          <v-card-title class="d-flex justify-space-between pb-6 pl-6 pt-5">
            <div class="d-flex align-center">
              <Icon
                type="audiences"
                :size="24"
                color="neroBlack"
                class="mr-2"
              /><span class="text-h5">Audiences</span>
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
                v-for="item in engagement.audiences"
                :key="item.id"
                :audience="item"
              ></status-list>
            </v-col>
          </v-card-text>
        </v-card>
        <v-tabs v-model="tabOption" class="mt-8">
          <v-tabs-slider color="primary"></v-tabs-slider>

          <v-tab
            key="displayAds"
            class="pa-2"
            color
            @click="fetchCampaignPerformanceDetails('ads')"
          >
            <Icon type="display_ads" :size="10" class="mr-2" />Display ads
          </v-tab>
          <v-tab key="email" @click="fetchCampaignPerformanceDetails('email')"
            >@ Email</v-tab
          >
        </v-tabs>
        <v-tabs-items v-model="tabOption" class="mt-2">
          <v-tab-item key="displayAds">
            <v-progress-linear
              :active="loadingTab"
              :indeterminate="loadingTab"
            />
            <campaign-summary
              :summary="displayAdsSummary"
              :campaignData="audiencePerformanceAdsData"
              type="ads"
            />
          </v-tab-item>
          <v-tab-item key="email">
            <v-progress-linear
              :active="loadingTab"
              :indeterminate="loadingTab"
            />
            <campaign-summary
              :summary="emailSummary"
              :campaignData="audiencePerformanceEmailData"
              type="email"
            />
          </v-tab-item>
        </v-tabs-items>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import moment from "moment"
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import Status from "@/components/common/Status"
import MetricCard from "@/components/common/MetricCard"
import Avatar from "@/components/common/Avatar"
import Icon from "@/components/common/Icon"
import StatusList from "../../components/common/StatusList.vue"
import Tooltip from "../../components/common/Tooltip.vue"
import CampaignSummary from "../../components/CampaignSummary.vue"

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
    Tooltip,
    CampaignSummary,
  },
  data() {
    return {
      engagement: {
        id: Math.floor(Math.random() * 10) + 1,
        name: "Engagement name",
        status: "active",
        schedule: "Manual",
        update_time: "2020-07-10T11:45:01.984Z",
        updated_by: "Rahul Goel",
        created_time: "2020-07-10T11:45:01.984Z",
        created_by: "Mohit Bansal",
        description:
          "This is the filled out description for this particular engagement. If they didn’t add any then this box will not appear. ",
        audiences: [
          {
            audienceId: 1,
            name: "Audience - Main",
            destinations: [
              {
                id: 1,
                type: "mailchimp",
                status: "delivered",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },
              {
                id: 2,
                type: "facebook",
                status: "delivered",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },
              {
                id: 3,
                type: "insightIQ",
                status: "delivered",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },
              {
                id: 4,
                type: "adobe-experience",
                status: "delivering",
                size: null,
                lastDeliveredOn: null,
              },
            ],
          },
          {
            audienceId: 1,
            name: "Audience 1",
            destinations: [
              {
                id: 1,
                type: "mailchimp",
                status: "delivered",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },

              {
                id: 2,
                type: "facebook",
                status: "delivered",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },
              {
                id: 3,
                type: "insightIQ",
                status: "delivering",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },
            ],
          },
          {
            audienceId: 1,
            name: "Audience 2",
            destinations: [
              {
                id: 1,
                type: "mailchimp",
                status: "delivering",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },
              {
                id: 2,
                type: "facebook",
                status: "delivered",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },
            ],
          },
          {
            audienceId: 1,
            name: "Audience 3",
            destinations: [
              {
                id: 1,
                type: "mailchimp",
                status: "delivering",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },
              {
                id: 2,
                type: "facebook",
                status: "delivered",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },
            ],
          },
          {
            audienceId: 1,
            name: "Audience - test",
            destinations: [
              {
                id: 2,
                type: "facebook",
                status: "delivered",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },
            ],
          },
        ],
      },
      loading: false,
      loadingTab: false,
      tabOption: 0,
      Tooltips: [
        { acronym: "CPM", description: "Cost per Thousand Impressions" },
        { acronym: "CTR", description: "Click Through Rate" },
        { acronym: "CPA", description: "Cost per Action" },
        { acronym: "CPC", description: "Cost per Click" },
      ],
      AdPerformaceData: {
        summary: {
          spend: 2000000,
          reach: 500000,
          impressions: 456850,
          conversions: 521006,
          clicks: 498587,
          frequency: 500,
          cost_per_thousand_impressions: 850,
          click_through_rate: 0.5201,
          cost_per_action: 652,
          cost_per_click: 485,
          engagement_rate: 0.5601,
        },
        audience_performance: [
          {
            name: "audience 1",
            spend: 2000000,
            reach: 500000,
            impressions: 456850,
            conversions: 521006,
            clicks: 498587,
            frequency: 500,
            cost_per_thousand_impressions: 850,
            click_through_rate: 0.5201,
            cost_per_action: 652,
            cost_per_click: 485,
            engagement_rate: 0.5601,
            campaigns: [
              {
                name: "Facebook",
                is_mapped: true,
                spend: 2000000,
                reach: 500000,
                impressions: 456850,
                conversions: 521006,
                clicks: 498587,
                frequency: 500,
                cost_per_thousand_impressions: 850,
                click_through_rate: 0.5201,
                cost_per_action: 652,
                cost_per_click: 485,
                engagement_rate: 0.5601,
              },
              {
                name: "Salesforce Marketing Cloud",
                is_mapped: true,
                spend: 2000000,
                reach: 500000,
                impressions: 456850,
                conversions: 521006,
                clicks: 498587,
                frequency: 500,
                cost_per_thousand_impressions: 850,
                click_through_rate: 0.5201,
                cost_per_action: 652,
                cost_per_click: 485,
                engagement_rate: 0.5601,
              },
              {
                name: "Google-Ads",
                is_mapped: true,
                spend: 2000000,
                reach: 500000,
                impressions: 456850,
                conversions: 521006,
                clicks: 498587,
                frequency: 500,
                cost_per_thousand_impressions: 850,
                click_through_rate: 0.5201,
                cost_per_action: 652,
                cost_per_click: 485,
                engagement_rate: 0.5601,
              },
            ],
          },
        ],
      },
    }
  },
  computed: {
    ...mapGetters({
      audiencePerformanceAds: "engagements/audiencePerformanceByAds",
      audiencePerformanceEmail: "engagements/audiencePerformanceByEmail",
    }),
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
    audiencePerformanceAdsData() {
      return this.audiencePerformanceAds
        ? this.audiencePerformanceAds.audience_performance
        : []
    },
    audiencePerformanceEmailData() {
      return this.audiencePerformanceEmail
        ? this.audiencePerformanceEmail.audience_performance
        : []
    },
    summaryCards() {
      const summary = [
        {
          id: 1,
          title: "Delivery schedule",
          value: this.fetchKey(this.engagement, "schedule"),
          subLabel: null,
        },
        {
          id: 2,
          title: "Last updated",
          value: this.getDateStamp(
            this.fetchKey(this.engagement, "update_time")
          ),
          hoverValue: this.fetchKey(this.engagement, "update_time"),
          subLabel: this.fetchKey(this.engagement, "updated_by"),
          width: "19%",
          minWidth: "164px",
        },
        {
          id: 3,
          title: "Created",
          value: this.getDateStamp(
            this.fetchKey(this.engagement, "created_time")
          ),
          hoverValue: this.fetchKey(this.engagement, "created_time"),
          subLabel: this.fetchKey(this.engagement, "created_by"),
          width: "19%",
          minWidth: "164px",
        },
        {
          id: 4,
          title:
            "This is the filled out description for this particular engagement. If they didn’t add any then this box will not appear.",
          value: null,
          subLabel: null,
        },
      ]
      return summary.filter((item) => item.title !== null)
    },
    displayAdsSummary() {
      return [
        {
          id: 1,
          title: "Spend",
          value: this.audiencePerformanceAds
            ? this.audiencePerformanceAds &&
              this.fetchKey(this.audiencePerformanceAds["summary"], "spend")
            : "-",
          width: "90px",
        },
        {
          id: 2,
          title: "Reach",
          value: this.audiencePerformanceAds
            ? this.audiencePerformanceAds &&
              this.fetchKey(this.audiencePerformanceAds["summary"], "reach")
            : "-",
          width: "90px",
        },
        {
          id: 3,
          title: "Impressions",
          value: this.audiencePerformanceAds
            ? this.audiencePerformanceAds &&
              this.fetchKey(
                this.audiencePerformanceAds["summary"],
                "impressions"
              )
            : "-",
          width: "90px",
        },
        {
          id: 4,
          title: "Conversions",
          value: this.audiencePerformanceAds
            ? this.audiencePerformanceAds &&
              this.fetchKey(
                this.audiencePerformanceAds["summary"],
                "conversions"
              )
            : "-",
          width: "90px",
        },
        {
          id: 5,
          title: "Clicks",
          value: this.audiencePerformanceAds
            ? this.audiencePerformanceAds &&
              this.fetchKey(this.audiencePerformanceAds["summary"], "clicks")
            : "-",
          width: "90px",
        },
        {
          id: 6,
          title: "Frequency",
          value: this.audiencePerformanceAds
            ? this.audiencePerformanceAds &&
              this.fetchKey(this.audiencePerformanceAds["summary"], "frequency")
            : "-",
          width: "90px",
        },
        {
          id: 7,
          title: "CPM",
          value: this.audiencePerformanceAds
            ? this.audiencePerformanceAds &&
              this.fetchKey(
                this.audiencePerformanceAds["summary"],
                "cost_per_thousand_impressions"
              )
            : "-",
          width: "90px",
        },
        {
          id: 8,
          title: "CTR",
          value: this.audiencePerformanceAds
            ? this.audiencePerformanceAds &&
              this.fetchKey(
                this.audiencePerformanceAds["summary"],
                "click_through_rate"
              )
            : "-",
          width: "90px",
        },
        {
          id: 9,
          title: "CPA",
          value: this.audiencePerformanceAds
            ? this.audiencePerformanceAds &&
              this.fetchKey(
                this.audiencePerformanceAds["summary"],
                "cost_per_action"
              )
            : "-",
          width: "90px",
        },
        {
          id: 10,
          title: "CPC",
          value:
            this.audiencePerformanceAds &&
            this.fetchKey(
              this.audiencePerformanceAds["summary"],
              "cost_per_click"
            ),
          width: "90px",
        },
        {
          id: 11,
          title: "Engagement rate",
          value:
            this.audiencePerformanceAds &&
            this.fetchKey(
              this.audiencePerformanceAds["summary"],
              "engagement_rate"
            ),
          width: "90px",
        },
      ]
    },
    emailSummary() {
      return [
        {
          id: 1,
          title: "Sent",
          value: this.audiencePerformanceEmail
            ? this.audiencePerformanceEmail &&
              this.fetchKey(this.audiencePerformanceEmail["summary"], "spend")
            : "-",
          width: "95px",
        },
        {
          id: 2,
          title: "Hard bounces / Rate",
          value: `${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "hard_bounces"
                )
              : "-"
          } * ${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "hard_bounces_rate"
                )
              : "-"
          }`,
          width: "139px",
        },
        {
          id: 3,
          title: "Delivered / Rate",
          value: `${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "delivered"
                )
              : "-"
          } * ${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "delivered_rate"
                )
              : "-"
          }`,
          width: "113px",
        },
        {
          id: 4,
          title: "Open / Rate",
          value: `${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(this.audiencePerformanceEmail["summary"], "open")
              : "-"
          } * ${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "open_rate"
                )
              : "-"
          }`,
          width: "122px",
        },
        {
          id: 5,
          title: "Click / CTR",
          value: `${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "clicks"
                )
              : "-"
          } * ${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "click_through_rate"
                )
              : "-"
          }`,
          width: "122px",
        },
        {
          id: 6,
          title: "Click to open rate  ",
          value: this.audiencePerformanceEmail
            ? this.audiencePerformanceEmail &&
              this.fetchKey(
                this.audiencePerformanceEmail["summary"],
                "click_to_open_rate"
              )
            : "-",
          width: "121px",
        },
        {
          id: 7,
          title: "Unique clicks / Unique opens",
          value: `${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "unique_clicks"
                )
              : "-"
          } * ${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "unique_opens"
                )
              : "-"
          }`,
          width: "185px",
        },
        {
          id: 8,
          title: "Unsubscribe / Rate",
          value: `${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "unsubscribe"
                )
              : "-"
          } * ${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "unsubscribe_rate"
                )
              : "-"
          }`,
          width: "130px",
        },
      ]
    },
  },
  methods: {
    ...mapActions({
      getAudiencePerformanceById: "engagements/getAudiencePerformance",
    }),

    getDateStamp(value) {
      return value ? moment(new Date(value)).fromNow() + " by" : "-"
    },
    fetchKey(obj, key) {
      return obj ? obj[key] : "-"
    },
    showCard(card) {
      if (card.cardType !== "description") return true
      else {
        return !!card.title
      }
    },
    async fetchCampaignPerformanceDetails(type) {
      this.loadingTab = true
      await this.getAudiencePerformanceById({
        type: type,
        id: this.engagement.id,
      })
      this.loadingTab = false
    },
    getTooltip(summaryCard) {
      const acronymObject = this.Tooltips.filter(
        (item) => item.acronym === summaryCard.title
      )
      if (acronymObject.length === 0) return null
      return acronymObject[0].description
    },
  },
  async mounted() {
    this.loading = true
    this.getAudiencePerformanceById({ type: "ads", id: this.engagement.id })
    this.loading = false
  },
}
</script>

<style lang="scss" scoped>
.engagement-dash {
  .page-header--wrap {
    box-shadow: 0px 1px 0px var(--v-lightGrey-base) !important;
  }
  ::v-deep .mdi-checkbox-blank-circle {
    font-size: 18px;
  }
  .inner-wrap {
    .summary-wrap {
      flex-wrap: wrap;
    }
    .summary-tab-wrap {
      .metric-card-wrapper {
        border: 1px solid var(--v-zircon-base);
        box-sizing: border-box;
        border-radius: 12px;
        ::v-deep .v-list-item {
          .v-list-item__content {
            padding-top: 15px;
            padding-bottom: 15px;
            margin-left: -5px !important;
            .v-list-item__title {
              font-size: 12px;
              line-height: 16px;
              margin: 0 !important;
            }
            .v-list-item__subtitle {
              margin-bottom: 15px !important;
            }
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
            .v-tabs-slider {
              background-color: var(--v-info-base) !important;
              border-color: var(--v-info-base) !important;
            }
          }
          .v-tab {
            text-transform: inherit;
            padding: 8px;
            color: var(--v-primary-base);
            cursor: default;
            font-size: 15px;
            line-height: 20px;
            svg {
              fill: transparent !important;
              path {
                stroke: var(--v-primary-base);
              }
            }
            &.v-tab--active {
              color: var(--v-info-base);
              svg {
                path {
                  stroke: var(--v-info-base);
                }
              }
            }
          }
        }
      }
    }
    .v-tabs-items {
      overflow: auto;
      background-color: transparent;
      .v-window-item--active {
        background: transparent;
      }
    }
  }
}
</style>
