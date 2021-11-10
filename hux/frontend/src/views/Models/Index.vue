<template>
  <div>
    <page-header data-e2e="models-header" :header-height="110">
      <template #left>
        <div>
          <breadcrumb
            :items="[
              {
                text: $options.name,
                icon: 'models',
              },
            ]"
          />
        </div>
        <div class="text-subtitle-1 font-weight-regular">
          Begin to interpret, explore, and understand your data by digging into
          your active models for an effective delivery experience.
        </div>
      </template>
    </page-header>
    <v-progress-linear :active="loading" :indeterminate="loading" />

    <v-row v-if="!loading" class="pa-14" data-e2e="models-list">
      <template v-if="hasModels">
        <descriptive-card
          v-for="model in models"
          :key="model.id"
          :action-menu="false"
          :coming-soon="false"
          width="280"
          height="255"
          :icon="`model-${model.type || 'unsubscribe'}`"
          :title="model.name"
          :description="model.description"
          data-e2e="model-item"
          :disabled="model.status !== 'Active'"
          @click.native="goToDashboard(model)"
        >
          <template slot="top">
            <status
              :icon-size="18"
              :status="model.status || ''"
              collapsed
              class="d-flex float-left"
              data-e2e="model-status"
            />
          </template>

          <template slot="default">
            <p
              class="text-body-2 black--text text--lighten-4"
              data-e2e="model-owner"
            >
              {{ model.owner }}
            </p>

            <v-row no-gutters>
              <v-col cols="5">
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
              </v-col>
              <v-col cols="7">
                <card-stat
                  label="Last trained"
                  :value="model.last_trained | Date('relative') | Empty"
                  data-e2e="model-last-trained-date"
                >
                  {{ model.last_trained | Date | Empty }}
                </card-stat>
              </v-col>
            </v-row>
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
