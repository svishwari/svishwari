<template>
  <Drawer v-model="localToggle" :width="640">
    <template #header-left>
      <h3 class="text-h3">Select destinations to add to this audience</h3>
    </template>

    <template #default>
      <v-progress-linear :active="loading" :indeterminate="loading" />

      <div class="pa-8">
        <DataCards
          :items="enabledDestinations"
          :fields="[
            {
              key: 'name',
              label: 'Name',
              sortable: true,
            },
            {
              key: 'manage',
              sortable: false,
            },
          ]"
        >
          <template #field:manage="row">
            <div class="d-flex align-center justify-end">
              <HuxButton
                v-if="isAdded(row.item.id)"
                variant="secondary"
                width="100"
                height="40"
                icon="mdi-check"
                iconPosition="left"
                @click="remove(row.item)"
              >
                Added
              </HuxButton>
              <HuxButton
                v-else
                isOutlined
                variant="primary"
                width="100"
                height="40"
                @click="add(row.item)"
              >
                Add
              </HuxButton>
            </div>
          </template>
        </DataCards>
      </div>
    </template>

    <template #footer-left> {{ enabledDestinations.length }} results </template>
  </Drawer>
</template>

<script>
import { mapGetters } from "vuex"
import DataCards from "@/components/common/DataCards.vue"
import Drawer from "@/components/common/Drawer.vue"
import HuxButton from "@/components/common/huxButton.vue"

export default {
  name: "DestinationsDrawer",

  components: {
    DataCards,
    Drawer,
    HuxButton,
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

    enabledDestinations() {
      return this.destinations.filter((destination) => destination.is_enabled)
    },

    selectedDestinations() {
      if (this.selectedAudienceId) {
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

    add(destination) {},

    remove(destination) {},
  },
}
</script>
