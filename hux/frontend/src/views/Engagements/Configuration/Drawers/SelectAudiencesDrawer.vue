<template>
  <Drawer v-model="localToggle" :width="640" :loading="loading">
    <template #header-left>
      <h3 class="text-h3">Add audiences to this engagement</h3>
    </template>

    <template #default>
      <div class="pa-6">
        <v-btn tile color="primary" class="mb-4" @click="$emit('onAdd')">
          <v-icon>mdi-plus</v-icon>
          New audience
        </v-btn>

        <DataCards
          :items="audiences"
          initialSort="asc"
          :fields="[
            {
              key: 'name',
              label: 'Name',
              sortable: true,
              col: '6',
            },
            {
              key: 'size',
              label: 'Target size',
              sortable: true,
            },
            {
              key: 'manage',
              sortable: false,
            },
          ]"
        >
          <template #field:size="row">
            <Tooltip>
              <template #label-content>
                {{ row.value | Numeric(true, true) | Empty }}
              </template>
              <template #hover-content>
                {{
                  row.value | Numeric | Empty("Size unavailable at this time")
                }}
              </template>
            </Tooltip>
          </template>

          <template #field:manage="row">
            <div class="d-flex align-center justify-end">
              <HuxButton
                v-if="isAdded(row.item)"
                variant="secondary"
                width="100"
                height="40"
                icon="mdi-check"
                iconPosition="left"
                :boxShadow="false"
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
                :boxShadow="false"
                @click="add(row.item)"
              >
                Add
              </HuxButton>
            </div>
          </template>
        </DataCards>
      </div>
    </template>

    <template #footer-left> {{ audiences.length }} results </template>
  </Drawer>
</template>

<script>
import { mapGetters } from "vuex"
import DataCards from "@/components/common/DataCards.vue"
import Drawer from "@/components/common/Drawer.vue"
import HuxButton from "@/components/common/huxButton.vue"
import Tooltip from "@/components/common/Tooltip.vue"

export default {
  name: "AudiencesDrawer",

  components: {
    DataCards,
    Drawer,
    HuxButton,
    Tooltip,
  },

  props: {
    value: {
      type: Object,
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
      audiences: "audiences/list",
    }),
  },

  methods: {
    isAdded(audience) {
      return Boolean(this.value[audience.id])
    },

    add(audience) {
      this.$set(this.value, audience.id, {
        id: audience.id,
        name: audience.name,
        size: audience.size,
        destinations: audience.destinations.map((destination) => {
          return {
            id: destination.id,
          }
        }),
      })
    },

    remove(audience) {
      this.$delete(this.value, audience.id)
    },
  },
}
</script>
