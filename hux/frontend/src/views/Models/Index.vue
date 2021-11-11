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
              :icon-size="17"
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
      <hux-empty
        v-else-if="!hasModels && !showError"
        icon-type="models"
        :icon-size="50"
        title="No models to show"
        subtitle="Models will appear here once they are added or requested."
      >
        <template #button>
          <hux-button
            variant="primary"
            is-tile
            width="224"
            height="40"
            class="text-button my-4"
          >
            Request a model
          </hux-button>
        </template>
      </hux-empty>
      <error
          v-else
          icon-type="error-on-screens"
          :icon-size="50"
          title="Models are currently unavailable"
          subtitle="Our team is working hard to fix it. Please be patient and try again soon!"
        >
      </error>
    </v-row>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import Breadcrumb from "@/components/common/Breadcrumb"
import CardStat from "@/components/common/Cards/Stat"
import DescriptiveCard from "@/components/common/Cards/DescriptiveCard"
import HuxEmpty from "@/components/common/screens/Empty"
import Error from "@/components/common/screens/Error"
import PageHeader from "@/components/PageHeader"
import Status from "@/components/common/Status"
import huxButton from "@/components/common/huxButton"

export default {
  name: "Models",

  components: {
    Breadcrumb,
    CardStat,
    DescriptiveCard,
    HuxEmpty,
    Error,
    PageHeader,
    Status,
    huxButton,
  },

  data() {
    return {
      loading: false,
      showError: false,
    }
  },

  computed: {
    ...mapGetters({
      models: "models/list",
    }),

    hasModels() {
      return this.models.length ? Object.entries(this.models[0]).length : false
      console.log(this.models)
    },
  },

  async mounted() {
    this.loading = true
    try{
    await this.getModels()
    } catch (error) {
      this.showError=true
    }
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
