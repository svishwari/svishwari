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
          sort="asc"
          empty="No audiences have been created."
          :selectedItems="value"
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

    <template #footer-left>
      <span class="gray--text text-caption">
        {{ audiences.length }} results
      </span>
    </template>
    <template #footer-right>
      <div
        v-if="isAudienceSelected && enableMultiple"
        class="d-flex align-baseline"
      >
        <huxButton
          variant="tertiary"
          size="large"
          :isTile="true"
          class="mr-2"
          @click="closeDrawer"
        >
          <span class="primary--text">Cancel</span>
        </huxButton>
        <huxButton
          variant="primary"
          size="large"
          :isTile="true"
          :isDisabled="!isAudienceSelected"
          @click="addSelectedAudiences"
        >
          {{ `Add ${audiencesCount} audience${audiencesCount > 1 ? "s" : ""}` }}
        </huxButton>
      </div>
    </template>
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
    enableMultiple: {
      type: Boolean,
      required: false,
      default: false,
    },
  },

  data() {
    return {
      localToggle: false,
      loading: false,
      selectedAudiences: {},
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
      // return false
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

  methods: {
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
          destinations: audience.destinations.map((destination) => {
            return {
              id: destination.id,
            }
          }),
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
  },
}
</script>
