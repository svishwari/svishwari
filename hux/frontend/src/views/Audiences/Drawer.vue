<template>
  <div>
    <Drawer v-model="toggleDrawer">
      <template v-slot:header-left>
        <h3 class="text-h3">Add audiences to this engagement</h3>
      </template>

      <template v-slot:default>
        <v-progress-linear :active="loading" :indeterminate="loading" />

        <div class="pa-8">
          <!-- TODO: HUS-229, HUS-445 -->
          <v-btn disabled tile color="primary" class="mb-4">
            <v-icon>mdi-plus</v-icon>
            New audience
          </v-btn>

          <v-data-iterator
            :items="audiences"
            :items-per-page="100"
            hide-default-footer
          >
            <template v-slot:default="props">
              <v-card
                v-for="item in props.items"
                :key="item.id"
                elevation="2"
                class="mb-4"
              >
                <v-card-title>
                  <v-row align="center">
                    <v-menu
                      bottom
                      offset-y
                      nudge-left="-100%"
                      nudge-top="10px"
                      open-on-hover
                    >
                      <template v-slot:activator="{ on }">
                        <v-col class="grow" v-on="on">
                          {{ item.name }}
                        </v-col>
                      </template>
                      <div class="px-4 py-3 text-caption white">
                        <p class="mb-0">{{ item.name }}</p>
                        <p class="text-caption gray--text mb-0">
                          {{ item.size | Numeric }}
                        </p>
                      </div>
                    </v-menu>
                    <v-col class="grow">
                      {{ item.size | Numeric(true, true) }}
                    </v-col>
                    <v-col class="shrink">
                      <v-btn
                        v-if="isAdded(item.id)"
                        color="secondary"
                        width="100"
                        @click="remove(item.id)"
                      >
                        <v-icon small class="mr-1">mdi-check</v-icon>
                        Added
                      </v-btn>
                      <v-btn
                        v-else
                        outlined
                        color="lightGrey"
                        width="100"
                        @click="add(item.id)"
                      >
                        <span class="darkGrey--text">Add</span>
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-card-title>
              </v-card>
            </template>
          </v-data-iterator>
        </div>
      </template>

      <template v-slot:footer-left> {{ audiences.length }} results </template>
    </Drawer>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import Drawer from "@/components/common/Drawer.vue"

export default {
  name: "AudiencesDrawer",

  components: {
    Drawer,
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

    isAdded(id) {
      return this.value.find((el) => el === id)
    },

    add(id) {
      this.value.push(id)
    },

    remove(id) {
      const index = this.value.indexOf(id)
      this.value.splice(index, 1)
    },
  },

  async mounted() {
    this.loading = true
    await this.getAudiences()
    this.loading = false
  },
}
</script>
