<template>
  <drawer v-model="localToggle" :loading="loading">
    <template #header-left>
      <div class="d-flex align-baseline">
        <h3 class="text-h3 font-weight-light pr-2">
          Select a destination to add
        </h3>
      </div>
    </template>

    <template #default>
      <div class="ma-3 font-weight-light">
        <card-horizontal
          v-for="destination in destinationsList"
          :key="destination.id"
          :title="destination.name"
          :icon="destination.type"
          :is-added="isAdded(destination)"
          class="my-3"
          @click="add(destination)"
        />
      </div>
    </template>

    <template #footer-left>
      <div class="d-flex align-baseline gray--text text-caption">
        {{ destinationsList.length }} results
      </div>
    </template>
  </drawer>
</template>

<script>
import { mapGetters, mapActions } from "vuex"

import Drawer from "@/components/common/Drawer"
import CardHorizontal from "@/components/common/CardHorizontal"

export default {
  name: "SelectDestinationsDrawer",

  components: {
    Drawer,
    CardHorizontal,
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
            this.localToggle = false
          }
        }
      }
    },

    undoAdd(destination) {
      const index = this.value.indexOf(destination)
      this.value.splice(index, 1)
    },
  },
}
</script>
