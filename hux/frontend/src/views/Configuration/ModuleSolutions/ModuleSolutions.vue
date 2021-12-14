<template>
  <div class="module-solutions-wrapper mt-n4">
    <template v-if="getConfigurations.length > 0">
      <v-checkbox
        key="model-checkbox"
        v-model="selctedActive"
        color="primary lighten-6"
        class="text-body-2 c-black"
        label="Only show active items"
      ></v-checkbox>
      <div
        v-if="
          !selctedActive ||
          (selctedActive &&
            moduleCards.filter((x) => x.status == 'active').length > 0)
        "
        class="pb-2"
      >
        <span class="text-body-1 black--text"> Modules </span>
        <span class="text-body-2 black--text text--lighten4 pl-4">
          Our core capabilities built intentionally with modularity to enable a
          wide set of use cases and business solutions.
        </span>
      </div>
      <div class="d-flex justify-start align-start flex-wrap">
        <descriptive-card
          v-for="config in selctedActive
            ? moduleCards.filter((x) => x.status == 'active')
            : moduleCards"
          :key="config.name"
          :icon="config.icon"
          :icon-color="'white'"
          :title="config.name"
          :description="config.description"
          :disabled="['pending', 'requested'].includes(config.status)"
          :action-menu="false"
          :coming-soon="false"
          :logo-option="true"
          :interactable="false"
          description-height="90px"
          height="225"
          width="255"
          class="mr-12 model-desc-card"
          data-e2e="config-list"
        >
          <template slot="top">
            <status
              :icon-size="18"
              :status="config.status"
              collapsed
              class="d-flex float-left"
              data-e2e="model-status"
            />
          </template>
        </descriptive-card>
      </div>
      <div
        v-if="
          !selctedActive ||
          (selctedActive &&
            businessCards.filter((x) => x.status == 'active').length > 0)
        "
        class="pb-2 pt-4"
      >
        <span class="text-body-1 black--text"> Business Solutions </span>
        <span class="text-body-2 black--text text--lighten4 pl-4">
          Our end-to-end solutions that combine modules to target specific
          business objectives and meet the needs of our clients.
        </span>
      </div>
      <div class="d-flex justify-start align-start flex-wrap">
        <descriptive-card
          v-for="config in selctedActive
            ? businessCards.filter((x) => x.status == 'active')
            : businessCards"
          :key="config.name"
          :icon="config.icon"
          :icon-color="'white'"
          :title="config.name"
          :description="config.description"
          :disabled="['pending', 'requested'].includes(config.status)"
          :action-menu="false"
          :coming-soon="false"
          :logo-option="true"
          :interactable="false"
          description-height="90px"
          height="225"
          width="255"
          class="mr-12 model-desc-card"
          data-e2e="config-list"
        >
          <template slot="top">
            <status
              :icon-size="18"
              :status="config.status"
              collapsed
              class="d-flex float-left"
              data-e2e="model-status"
            />
          </template>
        </descriptive-card>
      </div>
    </template>
    <v-row v-else class="pa-4">
      <hux-empty
        class="empty-module-solutions"
        icon-type="settings"
        :icon-size="50"
        title="No modules to show"
        subtitle="Modules &amp; solutions are being activated. Please check back in 2 hours. Thank you!"
      >
      </hux-empty>
    </v-row>
  </div>
</template>

<script>
import HuxEmpty from "@/components/common/screens/Empty"
import DescriptiveCard from "@/components/common/Cards/DescriptiveCard"
import Status from "@/components/common/Status"
import { mapGetters } from "vuex"

export default {
  name: "ModuleSolutions",
  components: { HuxEmpty, DescriptiveCard, Status },
  data() {
    return {
      selctedActive: false,
    }
  },
  computed: {
    ...mapGetters({
      getConfigurations: "configurations/configurationModels",
    }),

    moduleCards() {
      return this.getConfigurations.filter((x) => x.type == "module")
    },

    businessCards() {
      return this.getConfigurations.filter((x) => x.type == "business_solution")
    },
  },
}
</script>

<style lang="scss" scoped>
.module-solutions-wrapper {
  .empty-module-solutions {
    ::v-deep .text-center {
      width: 470px !important;
      .text-body-2 {
        line-height: 22px !important;
      }
    }
  }
}
.c-black {
  color: black !important;
}
</style>
