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
    <div class="px-15 my-8">
      <v-card
        height="150"
        width="fit-content"
        elevation="2"
        class="rounded px-5 pt-5"
      >
        <div class="overview">Audience overview</div>
        <div class="row overview-list mb-0 ml-0 mt-1">
          <MetricCard
            class="list-item mr-3"
            :width="135"
            :height="80"
            v-for="(item, i) in overviewListItems"
            :key="i"
            :title="item.title"
            :subtitle="item.subtitle"
            :icon="item.icon"
            :active="false"
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
    }
  },
}
</script>
<style lang="scss" scoped></style>
