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
    <page-header v-if="hasModels" header-height="71">
      <template #left>
        <v-btn disabled icon color="black">
          <icon type="search" :size="20" color="black" variant="lighten3" />
        </v-btn>
      </template>
      <template #right>
        <huxButton
          variant="primary"
          size="large"
          is-tile
          height="40"
          class="ma-2 font-weight-regular no-shadow mr-0 caption"
          data-e2e="addDataSource"
          @click="toggleDrawer()"
        >
          Request a model
        </huxButton>
      </template>
    </page-header>
    <v-progress-linear :active="loading" :indeterminate="loading" />

    <v-row v-if="!loading" class="pa-14" data-e2e="models-list">
      <template v-if="hasModels">
        <descriptive-card
          v-for="model in addedModels"
          :key="model.id"
          :action-menu="model.status !== 'Active'"
          :coming-soon="false"
          width="280"
          height="255"
          :icon="`model-${model.type || 'unsubscribe'}`"
          :title="model.name"
          :logo-option="true"
          :description="model.description"
          data-e2e="model-item"
          :disabled="model.status !== 'Active'"
          :interactable="model.status == 'Active' ? true : false"
          @click.native="goToDashboard(model)"
        >
          <template slot="top">
            <status
              :icon-size="18"
              :status="model.status || ''"
              collapsed
              class="d-flex float-left"
              :data-e2e="`model-status-${model.status}`"
            />
          </template>

          <template v-if="model.status == 'Active'" slot="default">
            <v-row no-gutters class="mt-4">
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
          <template slot="action-menu-options">
            <v-list class="list-wrapper">
              <v-list-item-group>
                <v-list-item @click="removeModel(model)">
                  <v-list-item-title> Remove </v-list-item-title>
                </v-list-item>
              </v-list-item-group>
            </v-list>
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

    <confirm-modal
      v-model="confirmModal"
      icon="sad-face"
      type="error"
      title="You are about to remove"
      :sub-title="`${selectedModal && selectedModal.name}`"
      right-btn-text="Yes, remove it"
      left-btn-text="Nevermind!"
      data-e2e="remove-modal-confirmation"
      @onCancel="confirmModal = !confirmModal"
      @onConfirm="confirmRemoval()"
    >
      <template #body>
        <div
          class="
            black--text
            text--darken-4 text-subtitle-1
            pt-6
            font-weight-regular
          "
        >
          Are you sure you want to remove this requested model&#63;
        </div>
      </template>
    </confirm-modal>

    <model-configuration v-model="drawer" />
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
import huxButton from "@/components/common/huxButton"
import Icon from "../../components/common/Icon.vue"
import ConfirmModal from "@/components/common/ConfirmModal"
import ModelConfiguration from "@/views/Models/Drawers/Configuration"

export default {
  name: "Models",

  components: {
    Breadcrumb,
    CardStat,
    DescriptiveCard,
    EmptyPage,
    PageHeader,
    Status,
    huxButton,
    Icon,
    ConfirmModal,
    ModelConfiguration,
  },

  data() {
    return {
      loading: false,
      drawer: false,
      confirmModal: false,
      selectedModal: null,
    }
  },

  computed: {
    ...mapGetters({
      models: "models/list",
    }),

    hasModels() {
      return this.models.length ? Object.entries(this.models[0]).length : false
    },
    addedModels() {
      return this.models.filter((model) =>
        ["Active", "Requested"].includes(model.status)
      )
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
      deleteModal: "models/remove",
    }),

    goToDashboard(model) {
      if (model.status === "Active") {
        this.$router.push({
          name: "ModelDashboard",
          params: { id: model.id },
        })
      }
    },
    toggleDrawer() {
      this.drawer = !this.drawer
    },
    removeModel(modal) {
      this.selectedModal = modal
      this.confirmModal = true
    },
    confirmRemoval() {
      this.deleteModal(this.selectedModal)
      this.confirmModal = false
    },
  },
}
</script>

<style lang="scss" scoped></style>
