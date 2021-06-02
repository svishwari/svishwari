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
          :class="{
            'list-item': true,
            'mr-3': true,
          }"
          :width="summaryCards[0].width"
          :min-width="summaryCards[0].minWidth"
          :height="75"
          :title="summaryCards[0].title"
          :subtitle="summaryCards[0].value"
          :interactable="false"
        >
        </MetricCard>
        <MetricCard
          :class="{
            'list-item': true,
            'mr-3': true,
          }"
          :width="summaryCards[1].width"
          :min-width="summaryCards[1].minWidth"
          :height="75"
          :title="summaryCards[1].title"
          :interactable="false"
        >
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
        <MetricCard
          :class="{
            'list-item': true,
            'mr-3': true,
          }"
          :width="summaryCards[2].width"
          :min-width="summaryCards[2].minWidth"
          :height="75"
          :title="summaryCards[2].title"
          :interactable="false"
        >
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
        <MetricCard
          :class="{
            'list-item': true,
            'mr-3': true,
            description: true,
          }"
          :width="summaryCards[3].width"
          :min-width="summaryCards[3].minWidth"
          :height="75"
          :title="summaryCards[3].title"
          :interactable="false"
        >
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

          <v-tab key="displayAds" class="pa-2" color>
            <Icon type="display_ads" :size="10" class="mr-2" />Display ads
          </v-tab>
          <v-tab key="email">@ Email</v-tab>
        </v-tabs>
        <v-tabs-items v-model="tabOption" class="mt-2">
          <v-tab-item key="displayAds">
            <v-card flat class="card-style">
              <v-card-text class="d-flex summary-tab-wrap">
                <MetricCard
                  class="list-item mr-2"
                  :width="item.width"
                  :height="70"
                  v-for="item in displayAdsSummary"
                  :key="item.id"
                  :title="item.title"
                  :titleTooltip="getTooltip(item)"
                  :subtitle="item.value"
                  :interactable="false"
                ></MetricCard>
              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item key="email">
            <v-card flat class="card-style">
              <v-card-text class="d-flex summary-tab-wrap">
                <MetricCard
                  class="list-item mr-1 rounded-lg"
                  :min-width="item.width"
                  :height="70"
                  v-for="item in emailSummary"
                  :key="item.id"
                  :title="item.title"
                  :subtitle="item.value"
                  :interactable="false"
                ></MetricCard>
              </v-card-text>
            </v-card>
          </v-tab-item>
        </v-tabs-items>
        <v-card minHeight="145px" flat class="mt-6 card-style">
          <v-card-title class="d-flex justify-space-between pb-6">
            <div class="d-flex align-center">
              <Icon
                type="audiences"
                :size="24"
                color="neroBlack"
                class="mr-2"
              /><span class="text-h5">Audience performance</span>
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
import Tooltip from "../../components/common/Tooltip.vue"

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
      tabOption: 0,
      Tooltips: [
        { acronym: "CPM", description: "Cost per Thousand Impressions"},
        { acronym: "CTR", description: "Click Through Rate"},
        { acronym: "CPA", description: "Cost per Action"},
        { acronym: "CPC", description: "Cost per Click"},
      ]
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
          hoverValue: this.fetchKey("update_time"),
          subLabel: this.fetchKey("updated_by"),
          width: "19%",
          minWidth: "164px",
        },
        {
          id: 3,
          title: "Created",
          value: this.getDateStamp(this.fetchKey("created_time")),
          hoverValue: this.fetchKey("created_time"),
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
        {
          id: 2,
          title: "Hard bounces / Rate",
          value: "125 • 0.1%",
          width: "139px",
        },
        {
          id: 3,
          title: "Delivered / Rate",
          value: "125 • 0.1%",
          width: "113px",
        },
        {
          id: 4,
          title: "Open / Rate",
          value: "365.2k • 72.8%",
          width: "122px",
        },
        {
          id: 5,
          title: "Click / CTR",
          value: "365.2k • 72.8%",
          width: "122px",
        },
        {
          id: 6,
          title: "Click to open rate  ",
          value: "72.8%",
          width: "121px",
        },
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
    getTooltip(summaryCard) {
      const acronymObject = this.Tooltips.filter(item => item.acronym === summaryCard.title)
      if(acronymObject.length === 0)
        return null
      return acronymObject[0].description
    }
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
  ::v-deep .mdi-checkbox-blank-circle {
    font-size: 18px;
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
            margin-bottom: 15px !important;
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
            .v-list-item__subtitle {
              display: none;
            }
          }
        }
      }
    }
    .summary-tab-wrap {
      .metric-card-wrapper {
        border: 1px solid var(--v-zircon-base);
        box-sizing: border-box;
        border-radius: 12px;
        ::v-deep .v-list-item__content {
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
      background: var(--v-white-base);
      box-shadow: 0px 0px 10px 2px rgba(0, 0, 0, 0.05);
      border-radius: 12px;
    }
  }
}
</style>
