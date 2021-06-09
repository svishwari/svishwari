<template>
  <div class="audience-insight-wrap">
    <PageHeader class="background-border">
      <template slot="left">
        <Breadcrumb :items="items" />
      </template>
      <template slot="right">
        <v-icon large :disabled="true"> mdi-refresh </v-icon>
        <v-icon size="22" class="icon-border pa-2 ma-1">
          mdi-plus-circle-multiple-outline
        </v-icon>
        <v-icon size="22" class="icon-border pa-2 ma-1"> mdi-pencil </v-icon>
        <v-icon size="22" class="icon-border pa-2 ma-1"> mdi-download </v-icon>
      </template>
    </PageHeader>
    <v-progress-linear :active="loading" :indeterminate="loading" />
    <div class="row px-15 my-1" v-if="audience && audience.audienceHistory">
      <MetricCard
        v-for="(item, i) in audience.audienceHistory"
        class="ma-4"
        :key="i"
        :grow="0"
        :title="item.title"
        :icon="item.icon"
      >
        <template #subtitle-extended>
          <span class="mr-2">
            <Tooltip>
              <template #label-content>
                {{ getFormattedTime(item.subtitle) }}
              </template>
              <template #hover-content>
                {{ item.subtitle | Date | Empty }}
              </template>
            </Tooltip>
          </span>
          <Avatar :name="getFullName(item.fullName)" />
        </template>
      </MetricCard>

      <MetricCard class="ma-4" :title="'Attributes'">
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
      </MetricCard>
    </div>
    <div class="px-15 my-1" v-if="audience && audience.insightInfo">
      <v-card elevation="1" class="rounded px-5 pt-5">
        <div class="overview">Audience overview</div>
        <div class="row overview-list mb-0 ml-0 mt-1">
          <MetricCard
            v-for="(item, i) in audience.insightInfo"
            class="mr-3"
            :key="i"
            :grow="i === 0 ? 2 : 1"
            :title="item.title"
            :subtitle="item.subtitle"
            :icon="item.icon"
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
import Avatar from "@/components/common/Avatar"
import Tooltip from "../../components/common/Tooltip.vue"
import MetricCard from "@/components/common/MetricCard"
import EmptyStateChart from "@/components/common/EmptyStateChart"
import lifetimeValue from "@/assets/images/lifetimeValue.svg"
import churn from "@/assets/images/churn.svg"
import plus from "@/assets/images/plus.svg"
export default {
  name: "AudienceInsight",
  components: {
    MetricCard,
    EmptyStateChart,
    PageHeader,
    Breadcrumb,
    Avatar,
    Tooltip,
    lifetimeValue,
    churn,
    plus,
  },
  data() {
    return {
      items: [
        {
          text: "Audiences",
          disabled: false,
          href: "/audiences",
          icon: "audiences",
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
    getFullName(fullname) {
      return fullname.first_name + " " + fullname.last_name
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
