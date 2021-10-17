<template>
  <div>
    <page-header data-e2e="models-header">
      <template slot="left">
        <breadcrumb
          :items="[
            {
              text: $options.name,
              icon: 'models',
            },
          ]"
        />
      </template>
    </page-header>
    <v-progress-linear :active="loading" :indeterminate="loading" />

    <v-row v-if="!loading" class="pa-14" data-e2e="models-list">
      <template v-if="hasModels">
        <descriptive-card
          v-for="model in models"
          :key="model.id"
          :icon="`model-${model.type || 'unsubscribe'}`"
          :title="model.name"
          :description="model.description"
          :disabled="model.status !== 'Active'"
          :action-menu="false"
          :coming-soon="false"
          height="255"
          width="280"
          data-e2e="model-item"
          class="mr-10"
          @click.native="goToDashboard(model)"
        >
          <template slot="top">
            <status
              :icon-size="17"
              :status="model.status || ''"
              collapsed
              class="d-flex float-left"
              data-e2e="model-status"
            />
          </template>

          <template slot="default">
            <div class="text-caption black--text text--darken-1 mb-2" data-e2e="model-owner">
              {{ model.owner }}
            </div>
            <div class="d-flex justify-center mb-6">
              <card-stat
                label="Version"
                :value="model.latest_version | Empty"
                stat-class="border-0"
                data-e2e="model-version"
              >
                <div class="mb-3">
                  Trained date<br />
                  {{ model.last_trained | Date | Empty }}
                </div>
                <div class="mb-3">
                  Fulcrum date<br />
                  {{ model.fulcrum_date | Date | Empty }}
                </div>
                <div class="mb-3">
                  Lookback period (days)<br />
                  {{ model.lookback_window }}
                </div>
                <div>
                  Prediction period (days)<br />
                  {{ model.prediction_window }}
                </div>
              </card-stat>
              <card-stat
                label="Last trained"
                :value="model.last_trained | Date('relative') | Empty"
                data-e2e="model-last-trained-date"
              >
                {{ model.last_trained | Date | Empty }}
              </card-stat>
            </div>
          </template>
        </descriptive-card>
      </template>

      <template v-else>
        <empty-page>
          <template #icon> mdi-alert-circle-outline </template>
          <template #title> Oops! There’s nothing here yet </template>
          <template #subtitle>
            Our team is still working hard activating your models. But they
            should be up and running soon! Please be patient in the meantime!
          </template>
        </empty-page>
      </template>
    </v-row>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import Breadcrumb from "@/components/common/Breadcrumb"
import CardStat from "@/components/common/Cards/Stat"
import DescriptiveCard from "@/components/common/Cards/DescriptiveCard"
import EmptyPage from "@/components/common/EmptyPage"
import PageHeader from "@/components/PageHeader"
import Status from "@/components/common/Status"

export default {
  name: "Models",

  components: {
    Breadcrumb,
    CardStat,
    DescriptiveCard,
    EmptyPage,
    PageHeader,
    Status,
  },

  data() {
    return {
      loading: false,
    }
  },

  computed: {
    ...mapGetters({
      models: "models/list",
    }),

    hasModels() {
      return this.models.length ? Object.entries(this.models[0]).length : false
    },
  },

  async mounted() {
    this.loading = true
    await this.getModels()
    this.loading = false
  },

  methods: {
    ...mapActions({
      getModels: "models/getAll",
    }),

    goToDashboard(model) {
      if (model.status === "Active") {
        this.$router.push({
          name: "ModelDashboard",
          params: { id: model.id },
        })
      }
    },
  },
}
</script>

<style lang="scss" scoped></style>
