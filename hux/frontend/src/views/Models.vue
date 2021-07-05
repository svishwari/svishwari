<template>
  <div>
    <page-header>
      <template slot="left">
        <Breadcrumb
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

    <v-row class="pa-14" v-if="!loading">
      <template v-if="hasModels">
        <DescriptiveCard
          v-for="model in models"
          :key="model.id"
          :icon="`model-${model.type || 'unsubscribe'}`"
          :title="model.name"
          :description="model.description"
          class="mr-10"
        >
          <template slot="top">
            <Status :iconSize="'17px'" :status="model.status || ''" collapsed class="d-flex" />
          </template>

          <template slot="default">
            <p class="text-caption gray--text">
              {{ model.owner }}
            </p>

            <div class="d-flex justify-center mb-6">
              <CardStat
                label="Version"
                :value="model.latest_version | Empty"
                stat-class="border-0"
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
              </CardStat>
              <CardStat
                label="Last trained"
                :value="model.last_trained | Date('relative') | Empty"
              >
                {{ model.last_trained | Date | Empty }}
              </CardStat>
            </div>
          </template>
        </DescriptiveCard>
      </template>

      <template v-else>
        <EmptyPage>
          <template #icon> mdi-alert-circle-outline </template>
          <template #title> Oops! There’s nothing here yet </template>
          <template #subtitle>
            Our team is still working hard activating your models. But they
            should be up and running soon! Please be patient in the meantime!
          </template>
        </EmptyPage>
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

  methods: {
    ...mapActions({
      getModels: "models/getAll",
    }),
  },

  async mounted() {
    this.loading = true
    await this.getModels()
    this.loading = false
  },
}
</script>
