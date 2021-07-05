<template>
  <div>
    <h5 class="text-h5 mb-4">Engagement overview</h5>

    <v-row no-gutters>
      <MetricCard
        v-for="(item, index) in overview"
        :key="index"
        :title="item.title"
        :icon="item.icon"
        :maxWidth="172"
        class="mr-4"
      >
        <template #subtitle-extended>
          <span v-if="item.subtitle" class="font-weight-semi-bold">
            {{ item.subtitle }}
          </span>

          <div v-if="item.destinations" class="d-flex align-center">
            <Logo
              class="mr-2"
              v-for="destination in item.destinations"
              :key="destination.type"
              :type="destination.type"
              :size="20"
            />
            <span
              v-if="!item.destinations.length"
              class="font-weight-semi-bold"
            >
              0
            </span>
          </div>
        </template>
      </MetricCard>
    </v-row>
  </div>
</template>

<script>
import { mapGetters } from "vuex"
import Logo from "@/components/common/Logo.vue"
import MetricCard from "@/components/common/MetricCard.vue"

export default {
  name: "EngagementOverview",

  components: {
    Logo,
    MetricCard,
  },

  props: {
    value: {
      type: Object,
      required: true,
    },
  },

  computed: {
    ...mapGetters({
      destination: "destinations/single",
    }),

    selectedAudiences() {
      return Object.values(this.value.audiences)
    },

    selectedDestinationTypes() {
      const allDestinationIds = this.selectedAudiences.map((audience) => {
        return audience.destinations.map((destination) => {
          return destination.id
        })
      })
      const destinationIds = [...new Set(allDestinationIds.flat())]
      const destinationTypes = destinationIds.map((id) => {
        return this.destination(id)
      })
      return destinationTypes
    },

    sumAudienceSizes() {
      let size = 0

      this.selectedAudiences.forEach((audience) => {
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
          destinations: this.selectedDestinationTypes,
        },
        {
          title: "Target size",
          subtitle: this.$options.filters.Numeric(
            this.sumAudienceSizes,
            true,
            false,
            true
          ),
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
