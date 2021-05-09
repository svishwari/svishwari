<template>
  <div class="audience-insight-wrap">
    <PageHeader class="background-border">
      <template slot="left">
        <Breadcrumb :items="items" />
      </template>
      <template slot="right">
        <v-icon size="22" class="icon-border pa-2"> mdi-download </v-icon>
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
        :ripple="false"
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
        :ripple="false"
        :title="'Attributes'"
      >
        <template slot="extra-item">
          <div class="container pl-0">
            <ul>
              <li>
                <img src="../../assets/images/value.svg" />
                Lifetime Value
              </li>
              <li>
                <img src="../../assets/images/churn.svg" />
                Churn
              </li>
              <li>
                <v-icon size="20" color="primary"> mdi-plus </v-icon>
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
        <div class="row overview-list mb-0 ml-0 mt-1">
          <MetricCard
            v-for="(item, i) in overviewListItems"
            class="list-item mr-3"
            :width="135"
            :height="80"
            :key="i"
            :title="item.title"
            :subtitle="item.subtitle"
            :icon="item.icon"
            :ripple="false"
          ></MetricCard>
        </div>
      </v-card>
    </div>
    <v-divider class="my-8"></v-divider>
    <EmptyState>
      <template v-slot:chart-image>
        <img src="@/assets/images/empty-state-chart-3.png" alt="Empty state" />
      </template>
    </EmptyState>
  </div>
</template>

<script>
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import MetricCard from "@/components/common/MetricCard"
import EmptyState from "@/components/common/EmptyState"

export default {
  name: "AudienceInsight",
  components: {
    MetricCard,
    EmptyState,
    PageHeader,
    Breadcrumb,
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
          text: "Audience name",
          disabled: true,
          href: this.$route.path,
        },
      ],
      overviewListItems: [
        { title: "Target size", subtitle: "34,203,204" },
        { title: "Countries", subtitle: "2", icon: "mdi-earth" },
        { title: "US States", subtitle: "52", icon: "mdi-map" },
        { title: "Cities", subtitle: "19,495", icon: "mdi-map-marker-radius" },
        { title: "Age", subtitle: "-", icon: "mdi-cake-variant" },
        { title: "Women", subtitle: "52%", icon: "mdi-gender-female" },
        { title: "Men", subtitle: "46%", icon: "mdi-gender-male" },
        { title: "Other", subtitle: "2%", icon: "mdi-gender-male-female" },
      ],
      infoListItems: [
        {
          title: "Last updated",
          subtitle: "Yesterday by",
          shortName: "JS",
          fullName: "John Smith",
        },
        {
          title: "Created",
          subtitle: "Yesterday by",
          shortName: "JS",
          fullName: "John Smith",
        },
      ],
    }
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
