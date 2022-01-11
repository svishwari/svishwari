<template>
  <drawer v-model="localToggle" :loading="loading">
    <template #header-left>
      <div class="d-flex align-baseline">
        <h3 class="text-h2 pr-2 d-flex align-center">
          <icon type="map" :size="32" class="mx-2" />
          <div class="pl-1">Add a destination</div>
        </h3>
      </div>
    </template>

    <template #default>
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
          :is-added="isAdded(destination)"
          :is-available="destination.is_enabled"
          class="my-3"
          :data-e2e="`destination-select-button-${destination.type}`"
          @click="add(destination)"
        />
      </div>
    </template>

    <template #footer-left>
      <div class="d-flex align-baseline body-2">
        {{ destinationsList.length }} results
      </div>
    </template>
  </drawer>
</template>

<script>
import { mapGetters, mapActions } from "vuex"

import Drawer from "@/components/common/Drawer"
import CardHorizontal from "@/components/common/CardHorizontal"
import Icon from "@/components/common/Icon"

import { groupBy } from "@/utils"
import sortBy from "lodash/sortBy"

export default {
  name: "SelectDestinationsDrawer",

  components: {
    Drawer,
    CardHorizontal,
    Icon,
  },

  props: {
    value: {
      type: Array,
      required: true,
    },

    toggle: {
      type: Boolean,
      required: false,
      default: false,
    },
    closeOnAction: {
      type: Boolean,
      required: false,
      default: false,
    },
  },

  data() {
    return {
      loading: false,
      localToggle: false,
    }
  },

  computed: {
    ...mapGetters({
      destinations: "destinations/list",
    }),

    destinationsList() {
      return this.destinations.filter(
        (each) => each.is_added && each.is_enabled
      )
    },

    groupByCategory() {
      return groupBy(
        sortBy(this.destinationsList, ["category", "name"]),
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
    async fetchDependencies() {
      this.loading = true
      await this.getDestinations()
      this.loading = false
    },

    isAdded(destination) {
      return this.value.findIndex((each) => destination.id === each.id) !== -1
        ? true
        : false
    },

    add(destination) {
      if (this.isAdded(destination)) {
        this.undoAdd(destination)
      } else {
        if (destination.type === "sfmc") {
          this.$emit("onSalesforceAdd", destination)
        } else {
          this.value.push(destination)
          if (this.closeOnAction) {
            this.$emit("onAddDestination", {
              destination: { id: destination.id },
            })
          }
        }
      }
    },

    undoAdd(destination) {
      const index = this.value.findIndex((each) => destination.id === each.id)
      this.value.splice(index, 1)
      this.$emit("onRemoveDestination", {
        destination: { id: destination.id },
      })
    },
  },
}
</script>
