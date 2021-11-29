<template>
  <drawer
    v-model="localDrawer"
    :content-padding="'pa-0'"
    :content-header-padding="'px-3'"
    :expanded-width="300"
    :width="300"
  >
    <template #header-left>
      <span class="text-h2 black--text"> Filter ({{ filterLength }}) </span>
    </template>
    <template #header-right>
      <v-btn
        plain
        :color="filterLength > 0 ? 'primary base' : 'black lighten3'"
        :disabled="!filterLength > 0"
        class="text-button float-right clear-btn"
        @click="clear()"
      >
        Clear
      </v-btn>
    </template>

    <template #default>
      <hux-filter-panels :expanded="selectedAttributes.length > 0 ? [0] : []">
        <v-checkbox
          v-model="selectedFavourite"
          color="#00a3e0"
          class="text--base-1 px-5 withoutExpansion"
          label="My favorites only"
          :style="{ 'border-bottom': '1px solid #E2EAEC' }"
        ></v-checkbox>
        <v-checkbox
          v-model="selectedAudienceWorkedWith"
          color="#00a3e0"
          class="text--base-1 px-5 withoutExpansion"
          label="Audiences I’ve worked on"
        ></v-checkbox>
        <hux-filter-panel title="Attributes" :count="selectedAttributes.length">
          <div class="text-body-1 black--text text--lighten-4 pb-2">MODELS</div>
          <div v-for="data in attributes" :key="data.id">
            <v-checkbox
              v-if="data.category == 'models'"
              v-model="selectedAttributes"
              multiple
              color="#00a3e0"
              class="text--base-1"
              :label="formatText(data.title)"
              :value="data.title"
            ></v-checkbox>
          </div>
          <br />
          <div class="text-body-1 black--text text--lighten-4 pb-2">
            GENERAL
          </div>
          <div v-for="data in attributes" :key="data.id">
            <v-checkbox
              v-if="data.category == 'general'"
              v-model="selectedAttributes"
              multiple
              color="#00a3e0"
              class="text--base-1"
              :label="formatText(data.title)"
              :value="data.title"
            ></v-checkbox>
          </div>
        </hux-filter-panel>
      </hux-filter-panels>
    </template>
    <template #footer-left>
      <v-btn
        tile
        color="white"
        class="text-button ml-1 primary-text"
        @click="cancel()"
      >
        Cancel
      </v-btn>
    </template>
    <template #footer-right>
      <v-btn
        tile
        color="primary"
        class="text-button ml-4"
        width="110"
        :disabled="!filterLength > 0"
        @click="apply()"
      >
        Apply filter
      </v-btn>
    </template>
  </drawer>
</template>

<script>
import Drawer from "@/components/common/Drawer"
import HuxFilterPanels from "@/components/common/FilterPanels"
import HuxFilterPanel from "@/components/common/FilterPanel"
import { formatText } from "@/utils.js"

export default {
  name: "AudienceFilterDrawer",
  components: {
    Drawer,
    HuxFilterPanels,
    HuxFilterPanel,
  },
  props: {
    value: {
      type: Boolean,
      required: true,
      default: false,
    },
  },
  data() {
    return {
      localDrawer: this.value,
      attributes: [
        {
          id: 1,
          title: "propensity_unsubscribe",
          category: "models",
        },
        {
          id: 2,
          title: "predicted_lifetime_value",
          category: "models",
        },
        {
          id: 3,
          title: "propensity_to_purchase",
          category: "models",
        },
        {
          id: 4,
          title: "age",
          category: "general",
        },
        {
          id: 5,
          title: "email",
          category: "general",
        },
        {
          id: 6,
          title: "gender",
          category: "general",
        },
        {
          id: 7,
          title: "country",
          category: "general",
        },
        {
          id: 8,
          title: "state",
          category: "general",
        },
        {
          id: 9,
          title: "city",
          category: "general",
        },
        {
          id: 10,
          title: "zipcode",
          category: "general",
        },
      ],
      selectedAttributes: [],
      selectedFavourite: false,
      selectedAudienceWorkedWith: false,
    }
  },

  computed: {
    filterLength() {
      let count = 0
      count = this.selectedAttributes.length
      if (this.selectedFavourite) count++
      if (this.selectedAudienceWorkedWith) count++

      return count
    },
  },
  watch: {
    value: function () {
      this.localDrawer = this.value
    },
    localDrawer: function () {
      this.$emit("input", this.localDrawer)
    },
  },
  methods: {
    getTime(value) {
      let today_date = new Date()
      return new Date(
        today_date.getFullYear(),
        today_date.getMonth(),
        today_date.getDate() - value
      )
    },
    clearFilter() {
      this.selectedAttributes = []
      this.selectedFavourite = false
      this.selectedAudienceWorkedWith = false
    },
    clear() {
      this.clearFilter()
      this.apply()
    },
    apply() {
      this.$emit("onSectionAction", {
        selectedAttributes: this.selectedAttributes,
        selectedFavourite: this.selectedFavourite,
        selectedAudienceWorkedWith: this.selectedAudienceWorkedWith,
      })
    },
    cancel() {
      this.clearFilter()
      this.localDrawer = false
    },
    formatText: formatText,
  },
}
</script>
<style scoped>
::v-deep.v-input--selection-controls {
  margin-top: 0px !important;
  padding-top: 0px !important;
}
::v-deep.v-input--selection-controls.v-input {
  flex: 1 1 auto !important;
}
::v-deep.input__slot {
  margin: 0px !important;
}
::v-deep .v-input--selection-controls .v-input__slot {
  margin-bottom: 0px !important;
}
::v-deep.theme--light .v-messages {
  min-height: 6px !important;
  color: var(--v-black-base);
}
.clear-btn {
  padding-left: 7.9rem !important;
  padding-top: 10px;
  padding-right: 0px !important;
}
.withoutExpansion {
  height: 34px;
  align-items: center;
  margin-top: 6px !important;
}
::v-deep.theme--light .v-label {
  font-size: 16px;
  font-weight: 400;
  line-height: 22px;
  letter-spacing: 0;
  color: var(--v-black-base);
}
</style>
