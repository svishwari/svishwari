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
        :maxWidth="172"
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

  props: {
    value: {
      type: Object,
      required: true,
    },
  },

  computed: {
    numberOfDestinations() {
      let count = 0

      Object.values(this.value.audiences).forEach((audience) => {
        if (audience.destinations) {
          count += Object.keys(audience.destinations).length
        }
      })

      return count
    },

    sumAudienceSizes() {
      let size = 0

      Object.values(this.value.audiences).forEach((audience) => {
        if (audience.size) {
          size += Number(audience.size)
        }
      })

      return size
    },

    deliverySchedule() {
      const schedule = JSON.parse(this.value.delivery_schedule)
      return schedule ? schedule : "Manual"
    },

    overview() {
      return [
        {
          title: "Destinations",
          subtitle: this.$options.filters.Numeric(this.numberOfDestinations),
        },
        {
          title: "Target size",
          subtitle: this.$options.filters.Numeric(this.sumAudienceSizes),
        },
        {
          title: "Delivery schedule",
          subtitle: this.deliverySchedule,
        },
      ]
    },
  },
}
</script>
