<template>
  <drawer v-model="localToggle" :width="640">
    <template #header-left>
      <div class="d-flex align-baseline">
        <h3 class="text-h2 pr-2 d-flex align-center">
          <icon type="map" :size="32" class="mx-2" />
          <div class="pl-1">Add a destination</div>
        </h3>
      </div>
    </template>

    <template #default>
      <v-progress-linear :active="loading" :indeterminate="loading" />
      <div
        v-for="(values, category, index) in groupByCategory"
        :key="`destinations-${index}`"
        class="mx-6"
      >
        <label class="d-block body-2 mt-6 mb-2">{{ category }}</label>

        <card-horizontal
          v-for="destination in values"
          :key="destination.id"
          :title="destination.name"
          :icon="destination.type"
          :is-added="isAdded(destination.id)"
          :is-available="destination.is_enabled"
          class="my-3"
          :data-e2e="
            isAdded(destination.id)
              ? ''
              : `destination-select-button-${destination.type}`
          "
          @click="addToggle(destination)"
        />
      </div>
    </template>

    <template #footer-left>
      <div class="d-flex align-baseline body-2">
        {{ connectedDestinations.length }} results
      </div>
    </template>
  </drawer>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import Drawer from "@/components/common/Drawer.vue"
import Icon from "@/components/common/Icon"
import CardHorizontal from "@/components/common/CardHorizontal"

import { groupBy } from "@/utils"
import sortBy from "lodash/sortBy"

export default {
  name: "DestinationsDrawer",

  components: {
    Drawer,
    Icon,
    CardHorizontal,
  },

  props: {
    value: {
      type: Object,
      required: true,
    },

    selectedAudienceId: {
      required: true,
    },

    toggle: {
      type: Boolean,
      required: false,
      default: false,
    },
  },

  data() {
    return {
      localToggle: false,
      loading: false,
    }
  },

  computed: {
    ...mapGetters({
      destinations: "destinations/list",
    }),

    connectedDestinations() {
      return this.destinations.filter((destination) => {
        return destination.is_enabled && destination.is_added
      })
    },

    selectedDestinations() {
      if (this.selectedAudienceId && this.value[this.selectedAudienceId]) {
        return this.value[this.selectedAudienceId].destinations
      }
      return []
    },

    groupByCategory() {
      return groupBy(
        sortBy(this.connectedDestinations, ["category", "name"]),
        "category"
      )
    },
  },

  watch: {
    toggle(value) {
      this.localToggle = value
    },

    localToggle(value) {
      this.$emit("onToggle", value)
    },
  },

  methods: {
    ...mapActions({
      getDestinations: "destinations/getAll",
    }),

    isAdded(id) {
      return this.selectedDestinations.findIndex((each) => id === each.id) !==
        -1
        ? true
        : false
    },

    addToggle(destination) {
      if (this.isAdded(destination.id)) {
        this.undoAdd(destination)
      } else {
        this.add(destination)
      }
    },

    add(destination) {
      if (destination.type === "sfmc") {
        this.$emit("onSalesforce", destination)
      } else {
        this.selectedDestinations.push({
          id: destination.id,
        })
        this.$emit("addedDestination", {
          destination: { id: destination.id },
        })
      }
    },

    undoAdd(destination) {
      const id = destination.id
      const index = this.selectedDestinations.findIndex(
        (destination) => destination.id === id
      )
      this.selectedDestinations.splice(index, 1)
      this.$emit("removeDestination", {
        destination: { id: destination.id },
      })
    },

    async fetchDependencies() {
      this.loading = true
      try {
        await this.getDestinations()
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
