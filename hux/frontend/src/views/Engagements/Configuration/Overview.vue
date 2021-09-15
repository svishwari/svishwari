<template>
  <div>
    <h5 class="text-h5 mb-4">Engagement overview</h5>

    <v-row no-gutters>
      <metric-card
        v-for="(item, index) in overview"
        :key="index"
        :title="item.title"
        :icon="item.icon"
        :max-width="172"
        class="mr-4 py-3"
      >
        <template #subtitle-extended>
          <span
            v-if="item.title === 'Target size'"
            class="font-weight-semi-bold"
          >
            <tooltip>
              <template #label-content>
                <span class="font-weight-semi-bold">
                  {{ item.subtitle | Numeric(false, false, true) }}
                </span>
              </template>
              <template #hover-content>
                {{ item.subtitle | Empty }}
              </template>
            </tooltip>
          </span>

          <span
            v-if="item.title === 'Delivery schedule'"
            class="font-weight-semi-bold"
          >
            {{ item.subtitle }}
          </span>

          <div v-if="item.destinations" class="d-flex align-center">
            <tooltip
              v-for="destination in item.destinations"
              :key="destination.type"
            >
              <template #label-content>
                <logo class="mr-2" :type="destination.type" :size="20" />
              </template>
              <template #hover-content>
                <span>{{ destination.name }}</span>
              </template>
            </tooltip>
            <span
              v-if="!item.destinations.length"
              class="font-weight-semi-bold"
            >
              0
            </span>
          </div>
        </template>
      </metric-card>
    </v-row>
  </div>
</template>

<script>
import { mapGetters } from "vuex"
import Logo from "@/components/common/Logo.vue"
import MetricCard from "@/components/common/MetricCard.vue"
import Tooltip from "@/components/common/Tooltip"

export default {
  name: "EngagementOverview",

  components: {
    Logo,
    MetricCard,
    Tooltip,
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
      if (!schedule) {
        return "Manual"
      } else {
        if (this.value && this.value.recurring) {
          return (
            this.value.recurring.start +
            (this.value.recurring.end ? " - " : "") +
            (this.value.recurring.end ? this.value.recurring.end : "")
          )
        } else {
          return "Now"
        }
      }
    },

    overview() {
      return [
        {
          title: "Destinations",
          destinations: this.selectedDestinationTypes,
        },
        {
          title: "Target size",
          subtitle: this.sumAudienceSizes,
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
