<template>
  <div>
    <Drawer v-model="toggleDrawer">
      <template #header-left>
        <h3 class="text-h3">Add audiences to this engagement</h3>
      </template>

      <template #default>
        <v-progress-linear :active="loading" :indeterminate="loading" />

        <div class="pa-8">
          <!-- TODO: HUS-229, HUS-445 -->
          <v-btn disabled tile color="primary" class="mb-4">
            <v-icon>mdi-plus</v-icon>
            New audience
          </v-btn>

          <DataCards
            :items="audiences"
            :fields="[
              {
                key: 'name',
                label: 'Name',
                sortable: true,
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
              <v-menu offset-y open-on-hover>
                <template #activator="{ on }">
                  <span v-on="on">
                    {{ row.value | Numeric(true, true) }}
                  </span>
                </template>
                <div class="px-4 py-3 text-caption white">
                  {{ row.value | Numeric }}
                </div>
              </v-menu>
            </template>

            <template #field:manage="row">
              <div class="d-flex align-center justify-end">
                <v-btn
                  v-if="isAdded(row.item)"
                  color="secondary"
                  width="100"
                  @click="remove(row.item)"
                >
                  <v-icon small class="mr-1">mdi-check</v-icon>
                  Added
                </v-btn>
                <v-btn
                  v-else
                  outlined
                  color="lightGrey"
                  width="100"
                  @click="add(row.item)"
                >
                  <span class="darkGrey--text">Add</span>
                </v-btn>
              </div>
            </template>
          </DataCards>
        </div>
      </template>

      <template #footer-left> {{ audiences.length }} results </template>
    </Drawer>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import DataCards from "@/components/common/DataCards.vue"
import Drawer from "@/components/common/Drawer.vue"

export default {
  name: "AudiencesDrawer",

  components: {
    DataCards,
    Drawer,
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
      toggleDrawer: false,
      loading: false,
    }
  },

  watch: {
    toggle(value) {
      this.toggleDrawer = value
    },
  },

  computed: {
    ...mapGetters({
      audiences: "audiences/list",
    }),
  },

  methods: {
    ...mapActions({
      getAudiences: "audiences/getAll",
    }),

    isAdded(audience) {
      return Boolean(this.value[audience.id])
    },

    add(audience) {
      this.$set(this.value, audience.id, {
        id: audience.id,
        name: audience.name,
        size: audience.size,
      })
    },

    remove(audience) {
      this.$delete(this.value, audience.id)
    },
  },

  async mounted() {
    this.loading = true
    await this.getAudiences()
    this.loading = false
  },
}
</script>
