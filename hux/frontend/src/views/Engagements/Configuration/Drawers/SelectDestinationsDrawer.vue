<template>
  <Drawer v-model="localToggle" :width="640">
    <template #header-left>
      <h3 class="text-h3">Add destinations to this audience</h3>
    </template>

    <template #default>
      <v-progress-linear :active="loading" :indeterminate="loading" />

      <div class="pa-8">
        <DataCards
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
          :selectedItems="selectedDestinations"
          empty="No destinations have been connected and added yet."
        >
          <template #field:name="{ item }">
            <div class="d-flex align-center">
              <Logo
                class="mr-2"
                :key="item.type"
                :type="item.type"
                :size="26"
              />
              {{ item.name }}
            </div>
          </template>

          <template #field:manage="{ item }">
            <div class="d-flex align-center justify-end">
              <HuxButton
                v-if="isAdded(item.id)"
                variant="secondary"
                width="100"
                height="40"
                icon="mdi-check"
                iconPosition="left"
                @click="undoAdd(item)"
              >
                Added
              </HuxButton>
              <HuxButton
                v-else
                isOutlined
                variant="primary"
                width="100"
                height="40"
                @click="add(item)"
              >
                Add
              </HuxButton>
            </div>
          </template>
        </DataCards>
      </div>
    </template>

    <template #footer-left>
      <span class="gray--text text-caption">
        {{ connectedDestinations.length }} results
      </span>
    </template>
  </Drawer>
</template>

<script>
import { mapGetters } from "vuex"
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

  watch: {
    toggle(value) {
      this.localToggle = value
    },

    localToggle(value) {
      this.$emit("onToggle", value)
    },
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

  methods: {
    isAdded(id) {
      return this.selectedDestinations.filter(
        (destination) => destination.id === id
      ).length
    },

    add(destination) {
      this.selectedDestinations.push({
        id: destination.id,
      })
    },

    undoAdd(destination) {
      const id = destination.id
      const index = this.selectedDestinations.findIndex(
        (destination) => destination.id === id
      )
      this.selectedDestinations.splice(index, 1)
    },
  },
}
</script>
