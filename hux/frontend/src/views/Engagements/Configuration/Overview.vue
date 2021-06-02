<template>
  <div>
    <h5 class="text-h5 mb-4">Engagement overview</h5>

    <v-row no-gutters>
      <MetricCard
        v-for="(item, index) in overview"
        :key="index"
        :title="item.title"
        :subtitle="item.subtitle"
        :icon="item.icon"
        :interactable="false"
        :height="80"
        :min-width="174"
        class="mr-4"
      />
    </v-row>
  </div>
</template>

<script>
import MetricCard from "@/components/common/MetricCard.vue"

export default {
  name: "EngagementOverview",

  components: {
    MetricCard,
  },

  data() {
    return {
      overview: [
        { title: "Destinations", subtitle: "0" },
        { title: "Target size", subtitle: "0" },
        { title: "Delivery schedule", subtitle: "Manual" },
      ],
    }
  },
}
</script>
