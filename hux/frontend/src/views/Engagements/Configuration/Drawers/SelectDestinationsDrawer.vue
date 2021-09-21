<template>
  <drawer v-model="localToggle" :width="640">
    <template #header-left>
      <h3 class="text-h3">Add destinations to this audience</h3>
    </template>

    <template #default>
      <v-progress-linear :active="loading" :indeterminate="loading" />

      <div class="pa-8">
        <data-cards
          :items="connectedDestinations"
          :fields="[
            {
              key: 'name',
              label: 'Destination',
            },
            {
              key: 'manage',
              sortable: false,
            },
          ]"
          :selected-items="selectedDestinations"
          empty="No destinations have been connected and added yet."
        >
          <template #field:name="{ item }">
            <div class="d-flex align-center">
              <logo
                :key="item.type"
                class="mr-2"
                :type="item.type"
                :size="26"
              />
              {{ item.name }}
            </div>
          </template>

          <template #field:manage="{ item }">
            <div class="d-flex align-center justify-end">
              <hux-button
                v-if="isAdded(item.id)"
                variant="primary lighten-8"
                width="100"
                height="40"
                icon="mdi-check"
                icon-position="left"
                :box-shadow="false"
                @click="undoAdd(item)"
              >
                Added
              </hux-button>
              <hux-button
                v-else
                is-outlined
                variant="primary"
                width="100"
                height="40"
                :box-shadow="false"
                @click="add(item)"
              >
                Add
              </hux-button>
            </div>
          </template>
        </data-cards>
      </div>
    </template>

    <template #footer-left>
      <span class="black--text text--darken-1 text-caption">
        {{ connectedDestinations.length }} results
      </span>
    </template>
  </drawer>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import DataCards from "@/components/common/DataCards.vue"
import Drawer from "@/components/common/Drawer.vue"
import HuxButton from "@/components/common/huxButton.vue"
import Logo from "@/components/common/Logo.vue"

export default {
  name: "DestinationsDrawer",

  components: {
    DataCards,
    Drawer,
    HuxButton,
    Logo,
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
      return Boolean(
        this.selectedDestinations.filter((destination) => destination.id === id)
          .length
      )
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
    },

    async fetchDependencies() {
      this.loading = true
      await this.getDestinations()
      this.loading = false
    },
  },
}
</script>
