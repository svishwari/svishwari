<template>
  <drawer v-model="localToggle" :width="640" :loading="loading">
    <template #header-left>
      <h3 class="text-h2">Add audiences to this engagement</h3>
    </template>

    <template #default>
      <div class="pa-6">
        <v-btn
          v-if="getAccess('audience', 'create')"
          tile
          color="primary"
          class="mb-4"
          @click="$emit('onAdd')"
        >
          <span class="text-button">Create a new audience</span>
        </v-btn>

        <data-cards
          :items="audiences"
          sort="asc"
          empty="No audiences have been created."
          card-class="select-aud-card"
          :fields="[
            {
              key: 'name',
              label: 'Audiences',
              sortable: true,
              col: '6',
            },
            {
              key: 'size',
              label: 'Size',
              sortable: true,
            },
            {
              key: 'manage',
              sortable: false,
            },
          ]"
        >
          <template #field:size="row">
            <tooltip>
              <template #label-content>
                <span class="text-body-1">
                  {{ row.value | Numeric(true, true) | Empty }}
                </span>
              </template>
              <template #hover-content>
                {{
                  row.value | Numeric | Empty("Size unavailable at this time")
                }}
              </template>
            </tooltip>
          </template>

          <template #field:name="row">
            <span class="text-body-1">
              {{ row.value }}
            </span>
          </template>

          <template #field:manage="row">
            <div class="d-flex align-center justify-end">
              <hux-button
                v-if="isAdded(row.item)"
                variant="primary darken-2"
                width="100"
                height="40"
                icon="mdi-check"
                icon-position="left"
                :box-shadow="false"
                @click="remove(row.item)"
              >
                Added
              </hux-button>
              <hux-button
                v-else
                is-outlined
                variant="black lighten-3"
                width="79"
                height="40"
                box-shadow
                data-e2e="audience-select-button"
                @click="add(row.item)"
              >
                <span class="black--text text--lighten-4">Add</span>
              </hux-button>
            </div>
          </template>
        </data-cards>
      </div>
    </template>

    <template #footer-left>
      <span class="black--text text--lighten-4 text-body-2">
        {{ audiences.length }} results
      </span>
    </template>
    <template #footer-right>
      <div
        v-if="isAudienceSelected && enableMultiple"
        class="d-flex align-baseline"
      >
        <hux-button
          variant="white"
          size="large"
          :is-tile="true"
          class="mr-2 btn-border box-shadow-none"
          @click="closeDrawer"
        >
          <span class="primary--text">Cancel</span>
        </hux-button>
        <hux-button
          variant="primary"
          size="large"
          :is-tile="true"
          :is-disabled="!isAudienceSelected"
          @click="addSelectedAudiences"
        >
          {{ `Add ${audiencesCount} audience${audiencesCount > 1 ? "s" : ""}` }}
        </hux-button>
      </div>
    </template>
  </drawer>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import DataCards from "@/components/common/DataCards.vue"
import Drawer from "@/components/common/Drawer.vue"
import HuxButton from "@/components/common/huxButton.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import { getAccess } from "@/utils"

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
    enableMultiple: {
      type: Boolean,
      required: false,
      default: false,
    },
    destinationId: {
      type: String,
      required: false,
      default: "",
    },
  },

  data() {
    return {
      localToggle: false,
      loading: false,
      selectedAudiences: {},
    }
  },

  computed: {
    ...mapGetters({
      audiences: "audiences/list",
    }),
    localSelectedAudiences: {
      get() {
        return this.selectedAudiences
      },
      set(value) {
        this.selectedAudiences = value
      },
    },

    isAudienceSelected() {
      if (Object.keys(this.newAudiences).length > 0) {
        return true
      } else if (Object.keys(this.removedAudiences).length > 0) {
        return true
      }
      return Object.keys(this.localSelectedAudiences).length
    },

    audiencesCount() {
      const countSummary = {
        added:
          Object.keys(this.newAudiences).length +
          Object.keys(this.value).length,
        removed: Object.keys(this.removedAudiences).length,
      }
      return countSummary.added - countSummary.removed
    },
    newAudiences() {
      const added = {}
      Object.keys(this.localSelectedAudiences).forEach((item) => {
        if (!Object.keys(this.value).includes(item)) {
          added[item] = this.localSelectedAudiences[item]
        }
      })
      return added
    },
    removedAudiences() {
      const removed = {}
      if (
        Object.keys(this.localSelectedAudiences) !== Object.keys(this.value)
      ) {
        Object.keys(this.value).forEach((item) => {
          if (!Object.keys(this.localSelectedAudiences).includes(item)) {
            removed[item] = this.value[item]
          }
        })
      }
      return removed
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
      getAudiences: "audiences/getAll",
    }),
    isAdded(audience) {
      return Boolean(
        this.enableMultiple
          ? this.localSelectedAudiences[audience.id]
          : this.value[audience.id]
      )
    },
    closeDrawer() {
      this.localToggle = false
      this.localSelectedAudiences = this.value
    },
    addSelectedAudiences() {
      this.$emit("triggerAddAudiences", {
        added: this.newAudiences,
        removed: this.removedAudiences,
      })
      this.closeDrawer()
    },
    add(audience) {
      if (!this.enableMultiple) this.$emit("onAddAudience", audience)
      this.$set(
        this.enableMultiple ? this.localSelectedAudiences : this.value,
        audience.id,
        {
          id: audience.id,
          name: audience.name,
          size: audience.size,
          destinations:
            this.destinationId != "" ? [{ id: this.destinationId }] : [],
        }
      )
    },

    remove(audience) {
      if (!this.enableMultiple) this.$emit("onRemoveAudience", audience)
      this.$delete(
        this.enableMultiple ? this.localSelectedAudiences : this.value,
        audience.id
      )
    },

    async fetchAudiences() {
      try {
        this.loading = true
        await this.getAudiences()
        this.loading = false
      } finally {
        this.loading = false
      }
    },
    getAccess: getAccess,
  },
}
</script>

<style lang="scss" scoped>
::v-deep .select-aud-card {
  padding: 10px 16px;
}
</style>
