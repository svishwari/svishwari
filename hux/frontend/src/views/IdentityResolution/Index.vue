<template>
  <div>
    <page-header>
      <template #left>
        <breadcrumb
          :items="[
            {
              text: 'Identity Resolution',
              disabled: true,
              href: '/identity-resolution',
              icon: 'identity-resolution',
            },
          ]"
        />
      </template>
    </page-header>

    <v-progress-linear :active="loading" :indeterminate="loading" />

    <page v-if="!loading" max-width="100%">
      <v-row no-gutters>
        <metric-card
          v-for="(metric, index) in overview"
          :key="index"
          :title="metric.title"
          :min-width="170"
          class="mx-2 my-2"
        >
          <template #extra-item>
            <tooltip position-top>
              <template #label-content>
                <icon type="info" :size="12" />
              </template>
              <template #hover-content>
                <v-sheet max-width="240px">
                  {{ metric.description }}
                </v-sheet>
              </template>
            </tooltip>
          </template>

          <template #subtitle-extended>
            <tooltip>
              <template #label-content>
                <span class="font-weight-semi-bold">
                  <template v-if="metric.format === 'numeric'">
                    {{ metric.value | Numeric(true, true) }}
                  </template>
                  <template v-if="metric.format === 'percentage'">
                    {{ metric.value | Numeric(true, false, false, true) }}
                  </template>
                </span>
              </template>
              <template #hover-content>
                <template v-if="metric.format === 'numeric'">
                  {{ metric.value | Numeric(true, false) }}
                </template>
                <template v-if="metric.format === 'percentage'">
                  {{ metric.value | Numeric(false, false, false, true) }}
                </template>
              </template>
            </tooltip>
          </template>
        </metric-card>
      </v-row>

      <v-divider class="my-8"></v-divider>

      <empty-state-chart>
        <template #chart-image>
          <img
            src="@/assets/images/empty-state-chart-3.png"
            alt="Exciting visuals are in the works!"
          />
        </template>
      </empty-state-chart>
    </page>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex"

import Page from "@/components/Page"
import Breadcrumb from "@/components/common/Breadcrumb"
import EmptyStateChart from "@/components/common/EmptyStateChart"
import Icon from "@/components/common/Icon"
import MetricCard from "@/components/common/MetricCard"
import PageHeader from "@/components/PageHeader"
import Tooltip from "@/components/common/Tooltip.vue"

export default {
  name: "IdentityResolution",

  components: {
    Page,
    Breadcrumb,
    EmptyStateChart,
    Icon,
    MetricCard,
    PageHeader,
    Tooltip,
  },

  data() {
    return {
      loading: false,
    }
  },

  computed: {
    ...mapGetters({
      overview: "identity/overview",
    }),
  },

  async mounted() {
    this.loading = true
    await this.getOverview()
    this.loading = false
  },

  methods: {
    ...mapActions({
      getOverview: "identity/getOverview",
    }),
  },
}
</script>

<style lang="scss" scoped></style>
