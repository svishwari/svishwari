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
    <div class="row px-15 my-1">
      <MetricCard
        v-for="(item, i) in infoListItems"
        class="ma-4"
        :width="165"
        :height="80"
        :key="i"
        :title="item.title"
        :subtitle="item.subtitle"
        :icon="item.icon"
        :interactable="false"
      >
        <template slot="short-name">
          <v-menu bottom offset-y open-on-hover>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                color="blue-grey"
                small
                outlined
                fab
                v-bind="attrs"
                v-on="on"
              >
                {{ item.shortName }}
              </v-btn>
            </template>
            <v-list>
              <v-list-item>
                <v-list-item-title>{{ item.fullName }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </template>
      </MetricCard>

      <MetricCard
        class="ma-4"
        width="59%"
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
      </MetricCard>
    </div>
    <div class="px-15 my-1">
      <v-card
        height="150"
        width="fit-content"
        elevation="1"
        class="rounded px-5 pt-5"
      >
        <div class="overview">Audience overview</div>
        <div
          class="row overview-list mb-0 ml-0 mt-1"
          v-if="isOverviewAvailable"
        >
          <MetricCard
            v-for="(item, i) in overviewListItems"
            class="list-item mr-3"
            :width="135"
            :height="80"
            :key="i"
            :title="item.title"
            :subtitle="item.subtitle"
            :icon="item.icon"
            :interactable="false"
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
import { mapGetters, mapActions } from "vuex"

import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
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
          icon: "mdi-flip-h mdi-account-plus-outline",
        },
        {
          text: this.$route.params.audienceName,
          disabled: true,
          href: this.$route.path,
        },
      ],
    }
  },
  computed: {
    ...mapGetters({
      overviewListItems: "AllOverviews",
      infoListItems: "AllInsightInfo",
    }),
    isOverviewAvailable() {
      return this.overviewListItems.length > 0
    },
  },
  methods: {
    ...mapActions(["getAllOverview", "getAllInsightInfo"]),
    refresh() {},
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
}
</style>
