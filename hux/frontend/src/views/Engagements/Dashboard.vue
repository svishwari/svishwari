<template>
  <div class="engagement-dash">
    <!-- Page Header -->
    <PageHeader class="d-flex">
      <template #left>
        <div class="d-flex align-center bread-crumb">
          <Breadcrumb :items="breadcrumbItems" />
          <div class="ml-3" v-if="engagementList && engagementList.status">
            <Status :status="engagementList.status"></Status>
          </div>
        </div>
      </template>
      <template #right>
        <v-icon size="22" :disabled="true" class="mr-2">mdi-refresh</v-icon>
        <v-icon size="22" :disabled="true" class="icon-border pa-2 ma-1">
          mdi-pencil
        </v-icon>
        <v-icon size="22" color="lightGrey" class="icon-border pa-2 ma-1">
          mdi-download
        </v-icon>
      </template>
    </PageHeader>
    <v-progress-linear :active="loading" :indeterminate="loading" />
    <!-- Page Content Starts here -->
    <div class="inner-wrap px-15 py-8">
      <!-- Summary Cards Wrapper -->
      <div class="summary-wrap d-flex mb-6">
        <MetricCard class="mr-3 shrink" :title="summaryCards[0].title">
          <template #subtitle-extended>
            <div class="font-weight-semi-bold neroBlack--text my-2">Manual</div>
          </template>
        </MetricCard>
        <MetricCard class="mr-3 shrink" :title="summaryCards[1].title">
          <template #subtitle-extended v-if="summaryCards[1].subLabel">
            <span class="mr-2">
              <tooltip>
                <template #label-content>
                  <span class="font-weight-semi-bold neroBlack--text">
                    {{ summaryCards[1].value }}
                  </span>
                </template>
                <template #hover-content>
                  {{ summaryCards[1].hoverValue | Date | Empty }}
                </template>
              </tooltip>
            </span>
            <Avatar :name="summaryCards[1].subLabel" />
          </template>
        </MetricCard>
        <MetricCard class="mr-3 shrink" :title="summaryCards[2].title">
          <template #subtitle-extended v-if="summaryCards[2].subLabel">
            <span class="mr-2">
              <tooltip>
                <template #label-content>
                  <span class="font-weight-semi-bold neroBlack--text">
                    {{ summaryCards[2].value }}
                  </span>
                </template>
                <template #hover-content>
                  {{ summaryCards[2].hoverValue | Date | Empty }}
                </template>
              </tooltip>
            </span>
            <Avatar :name="summaryCards[2].subLabel" />
          </template>
        </MetricCard>
        <MetricCard
          v-if="engagementList && engagementList.description"
          class="mr-3 grow"
          title=""
          :maxWidth="800"
        >
          <template #subtitle-extended>
            {{ summaryCards[3].title }}
          </template>
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
              class="empty-state pa-5 text--gray"
              v-if="engagement.audiences.length == 0"
            >
              Nothing to show here yet. Add an audience, assign and deliver that
              audience to a destination.
            </div>
            <v-col
              class="d-flex flex-row pl-0 pt-0 pr-0 overflow-auto pb-3"
              v-if="audienceMergedData.length >= 0"
            >
              <status-list
                v-for="item in audienceMergedData"
                :key="item.id"
                :audience="item"
              />
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
            <span style="width: 15px">
              <Icon type="display_ads" :size="10" class="mr-2" />
            </span>
            Display ads
          </v-tab>
          <v-tab key="email" @click="fetchCampaignPerformanceDetails('email')">
            @ Email
          </v-tab>
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
      // TODO Move all the mock data into Faker
      engagement: {
        id: Math.floor(Math.random() * 10) + 1,
        name: "Engagement name",
        status: "Active",
        schedule: "Manual",
        update_time: "2020-07-10T11:45:01.984Z",
        updated_by: "Rahul Goel",
        create_time: "2020-07-10T11:45:01.984Z",
        created_by: "Mohit Bansal",
        description:
          "This is the filled out description for this particular engagement. If they didn’t add any then this box will not appear. ",
        audiences: [
          {
            audienceId: 1,
            name: "Audience with no destination",
            destinations: [],
          },
          {
            audienceId: 1,
            name: "Audience - Main",
            destinations: [
              {
                id: 1,
                type: "mailchimp",
                status: "Delivered",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },
              {
                id: 2,
                type: "facebook",
                status: "Not Delivered",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },
              {
                id: 3,
                type: "insightIQ",
                status: "Delivered",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },
              {
                id: 4,
                type: "adobe-experience",
                status: "Delivering",
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
                status: "Delivered",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },

              {
                id: 2,
                type: "facebook",
                status: "Delivered",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },
              {
                id: 3,
                type: "insightIQ",
                status: "Delivering",
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
                status: "Delivering",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },
              {
                id: 2,
                type: "facebook",
                status: "Delivered",
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
                status: "Delivering",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },
              {
                id: 2,
                type: "facebook",
                status: "Delivered",
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
                status: "Delivered",
                size: 356046921,
                lastDeliveredOn: "2021-01-13T22:04:33.187Z",
              },
            ],
          },
        ],
      },
      destinationArr: [],
      audienceMergedData: [],
      loading: false,
      loadingTab: false,
      tabOption: 0,
      Tooltips: [
        { acronym: "CPM", description: "Cost per Thousand Impressions" },
        { acronym: "CTR", description: "Click Through Rate" },
        { acronym: "CPA", description: "Cost per Action" },
        { acronym: "CPC", description: "Cost per Click" },
      ],
    }
  },
  computed: {
    ...mapGetters({
      audiencePerformanceAds: "engagements/audiencePerformanceByAds",
      audiencePerformanceEmail: "engagements/audiencePerformanceByEmail",
      getEngagement: "engagements/engagement",
      getAudience: "audiences/audience",
      getDestinations: "destinations/single",
    }),

    engagementList() {
      return this.getEngagement(this.$route.params.id)
    },

    breadcrumbItems() {
      const items = [
        {
          text: "Engagements",
          disabled: false,
          href: this.$router.resolve({ name: "Engagements" }).href,
          icon: "engagements",
        },
      ]
      if (this.engagementList) {
        items.push({
          text: this.engagementList.name,
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
          value: this.fetchKey(this.engagementList, "delivery_schedule"),
          subLabel: null,
        },
        {
          id: 2,
          title: "Last updated",
          value: this.getDateStamp(
            this.fetchKey(this.engagementList, "update_time")
          ),
          hoverValue: this.fetchKey(this.engagementList, "update_time"),
          subLabel: this.fetchKey(this.engagementList, "updated_by"),
          width: "19%",
          minWidth: "164px",
        },
        {
          id: 3,
          title: "Created",
          value: this.getDateStamp(
            this.fetchKey(this.engagementList, "create_time")
          ),
          hoverValue: this.fetchKey(this.engagementList, "create_time"),
          subLabel: this.fetchKey(this.engagementList, "created_by"),
          width: "19%",
          minWidth: "164px",
        },
        {
          id: 4,
          title: this.fetchKey(this.engagementList, "description"),
          value: null,
          subLabel: null,
        },
      ]
      return summary.filter((item) => item.title !== null)
    },
    displayAdsSummary() {
      if (
        !this.audiencePerformanceAds ||
        (this.audiencePerformanceAds &&
          this.audiencePerformanceAds.length === 0)
      )
        return []
      return [
        {
          id: 1,
          title: "Spend",
          field: "spend",
          value: this.audiencePerformanceAds
            ? this.audiencePerformanceAds &&
              this.fetchKey(this.audiencePerformanceAds["summary"], "spend")
            : "-",
        },
        {
          id: 2,
          field: "reach",
          title: "Reach",
          value: this.audiencePerformanceAds
            ? this.audiencePerformanceAds &&
              this.fetchKey(this.audiencePerformanceAds["summary"], "reach")
            : "-",
        },
        {
          id: 3,
          title: "Impressions",
          field: "impressions",
          value: this.audiencePerformanceAds
            ? this.audiencePerformanceAds &&
              this.fetchKey(
                this.audiencePerformanceAds["summary"],
                "impressions"
              )
            : "-",
        },
        {
          id: 4,
          title: "Conversions",
          field: "conversions",
          value: this.audiencePerformanceAds
            ? this.audiencePerformanceAds &&
              this.fetchKey(
                this.audiencePerformanceAds["summary"],
                "conversions"
              )
            : "-",
        },
        {
          id: 5,
          title: "Clicks",
          field: "clicks",
          value: this.audiencePerformanceAds
            ? this.audiencePerformanceAds &&
              this.fetchKey(this.audiencePerformanceAds["summary"], "clicks")
            : "-",
        },
        {
          id: 6,
          title: "Frequency",
          field: "frequency",
          value: this.audiencePerformanceAds
            ? this.audiencePerformanceAds &&
              this.fetchKey(this.audiencePerformanceAds["summary"], "frequency")
            : "-",
        },
        {
          id: 7,
          title: "CPM",
          field: "cost_per_thousand_impressions",
          value: this.audiencePerformanceAds
            ? this.audiencePerformanceAds &&
              this.fetchKey(
                this.audiencePerformanceAds["summary"],
                "cost_per_thousand_impressions"
              )
            : "-",
        },
        {
          id: 8,
          title: "CTR",
          field: "click_through_rate",
          value: this.audiencePerformanceAds
            ? this.audiencePerformanceAds &&
              this.fetchKey(
                this.audiencePerformanceAds["summary"],
                "click_through_rate"
              )
            : "-",
        },
        {
          id: 9,
          title: "CPA",
          field: "cost_per_action",
          value: this.audiencePerformanceAds
            ? this.audiencePerformanceAds &&
              this.fetchKey(
                this.audiencePerformanceAds["summary"],
                "cost_per_action"
              )
            : "-",
        },
        {
          id: 10,
          title: "CPC",
          field: "cost_per_click",
          value:
            this.audiencePerformanceAds &&
            this.fetchKey(
              this.audiencePerformanceAds["summary"],
              "cost_per_click"
            ),
        },
        {
          id: 11,
          title: "Engagement rate",
          field: "engagement_rate",
          value:
            this.audiencePerformanceAds &&
            this.fetchKey(
              this.audiencePerformanceAds["summary"],
              "engagement_rate"
            ),
        },
      ]
    },
    emailSummary() {
      if (
        !this.audiencePerformanceEmail ||
        (this.audiencePerformanceEmail &&
          this.audiencePerformanceEmail.length === 0)
      )
        return []
      return [
        {
          id: 1,
          title: "Sent",
          field: "sent",
          value:
            this.audiencePerformanceEmail &&
            this.audiencePerformanceEmail["summary"]
              ? this.audiencePerformanceEmail &&
                this.fetchKey(this.audiencePerformanceEmail["summary"], "sent")
              : "-",
        },
        {
          id: 2,
          title: "Hard bounces / Rate",
          field: "hard_bounces|hard_bounces_rate",
          value: `${`${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "hard_bounces"
                )
              : "-"
          }|${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "hard_bounces_rate"
                )
              : "-"
          }`}`,
        },
        {
          id: 3,
          title: "Delivered / Rate",
          field: "delivered|delivered_rate",
          value: `${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "delivered"
                )
              : "-"
          }|${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "delivered_rate"
                )
              : "-"
          }`,
        },
        {
          id: 4,
          title: "Open / Rate",
          field: "open|open_rate",
          value: `${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(this.audiencePerformanceEmail["summary"], "open")
              : "-"
          }|${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "open_rate"
                )
              : "-"
          }`,
        },
        {
          id: 5,
          title: "Click / CTR",
          field: "clicks|click_through_rate",
          value: `${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "clicks"
                )
              : "-"
          }|${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "click_through_rate"
                )
              : "-"
          }`,
        },
        {
          id: 6,
          title: "Click to open rate  ",
          field: "click_to_open_rate",
          value: this.audiencePerformanceEmail
            ? this.audiencePerformanceEmail &&
              this.fetchKey(
                this.audiencePerformanceEmail["summary"],
                "click_to_open_rate"
              )
            : "-",
        },
        {
          id: 7,
          title: "Unique clicks / Unique opens",
          field: "unique_clicks|unique_opens",
          value: `${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "unique_clicks"
                )
              : "-"
          }|${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "unique_opens"
                )
              : "-"
          }`,
        },
        {
          id: 8,
          title: "Unsubscribe / Rate",
          field: "unsubscribe|unsubscribe_rate",
          value: `${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "unsubscribe"
                )
              : "-"
          }|${
            this.audiencePerformanceEmail
              ? this.audiencePerformanceEmail &&
                this.fetchKey(
                  this.audiencePerformanceEmail["summary"],
                  "unsubscribe_rate"
                )
              : "-"
          }`,
        },
      ]
    },
  },
  methods: {
    ...mapActions({
      getAudiencePerformanceById: "engagements/getAudiencePerformance",
      getEngagementById: "engagements/get",
      getAudienceById: "audiences/getAudienceById",
      destinationById: "destinations/get",
    }),

    async audienceList() {
      let engData = this.getEngagement(this.$route.params.id)
      let audienceIds = []
      let audiencesDetailsData = []
      let audienceDetails = []
      //audience id pushing in one array
      engData.audiences.forEach((data) => audienceIds.push(data.id))
      // getting audience by id
      for (let id of audienceIds) {
        await this.getAudienceById(id)
        audienceDetails.push(this.getAudience(id))
      }
      // extracting the audience data and merging into object
      audienceDetails.forEach((element) => {
        let filteredAudience = engData.audiences.filter(
          (d) => d.id == element.id
        )
        let audEngobj = Object.assign(filteredAudience[0])
        audEngobj.name = element.name
        audEngobj.size = element.size
        audEngobj.last_delivered = element.last_delivered
        audiencesDetailsData.push(audEngobj)
      })
      //Extracting the destination data
      for (let i = 0; i < audiencesDetailsData.length; i++) {
        for (let j = 0; j < audiencesDetailsData[i].destinations.length; j++) {
          await this.destinationById(audiencesDetailsData[i].destinations[j].id)
          let response = this.getDestinations(
            audiencesDetailsData[i].destinations[j].id
          )
          audiencesDetailsData[i].destinations[j] = response
        }
      }
      // pushing merged data into variable
      this.audienceMergedData = audiencesDetailsData
    },

    getDateStamp(value) {
      return value ? moment(new Date(value)).fromNow() + " by" : "-"
    },
    fetchKey(obj, key) {
      return obj && obj[key] ? obj[key] : "-"
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
        id: this.engagementList.id,
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
    await this.getEngagementById(this.$route.params.id)
    await this.getAudiencePerformanceById({
      type: "ads",
      id: this.engagementList.id,
    })
    this.audienceList()
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
  .empty-state {
    background: var(--v-aliceBlue-base);
    width: 100%;
    font-size: 14px;
    line-height: 22px;
    color: var(--v-gray-base);
    border: 1px solid var(--v-lightGrey-base);
    box-sizing: border-box;
    border-radius: 5px;
  }
  .inner-wrap {
    .summary-wrap {
      flex-wrap: wrap;
      .metric-card-wrapper {
        padding: 10px 15px;
      }
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
            width: 128px;
            .v-tabs-slider {
              background-color: var(--v-info-base) !important;
              border-color: var(--v-info-base) !important;
            }
          }
          .v-tab {
            text-transform: inherit;
            padding: 8px;
            color: var(--v-primary-base);
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
      overflow: inherit;
      background-color: transparent !important;
      .v-window-item--active {
        background: transparent;
      }
    }
  }
}
.theme--light.v-btn.v-btn--disabled.v-btn--has-bg {
  background-color: white !important;
}
</style>
