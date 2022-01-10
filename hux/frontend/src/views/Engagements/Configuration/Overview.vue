<template>
  <div class="eng-overview">
    <h5 class="text-h3 mb-2">Engagement overview</h5>

    <v-row no-gutters>
      <metric-card
        v-for="(item, index) in overview"
        :key="index"
        :title="item.title"
        :icon="item.icon"
        class="mr-4 py-3"
      >
        <template #subtitle-extended>
          <span v-if="item.title === 'Size'" class="text-subtitle-1">
            <tooltip>
              <template #label-content>
                <span v-if="item.subtitle !== '—'" class="text-subtitle-1">
                  {{ item.subtitle | Numeric(false, false, true) }}
                </span>
                <span v-else class="text-subtitle-1">
                  {{ item.subtitle }}
                </span>
              </template>
              <template #hover-content>
                {{ item.subtitle | Empty }}
              </template>
            </tooltip>
          </span>

          <span
            v-if="
              item.title === 'Delivery schedule' ||
              item.title === 'Engagement name' ||
              item.title === 'No. of audiences'
            "
          >
            <tooltip>
              <template #label-content>
                <span class="text-subtitle-1 text-ellipsis max-width-15ch">
                  {{ item.subtitle | Empty }}
                </span>
              </template>
              <template #hover-content>
                {{ item.subtitle | Empty }}
              </template>
            </tooltip>
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
            <span v-if="!item.destinations.length" class="text-subtitle-1">
              —
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
          title: "Engagement name",
          subtitle: this.value.name,
        },
        {
          title: "No. of audiences",
          subtitle:
            this.selectedAudiences.length > 0
              ? this.selectedAudiences.length
              : "—",
        },
        {
          title: "Size",
          subtitle: this.sumAudienceSizes ? this.sumAudienceSizes : "—",
        },
        {
          title: "Destinations",
          destinations: this.selectedDestinationTypes,
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
