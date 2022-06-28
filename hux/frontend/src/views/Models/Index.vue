<template>
  <div class="models-wrap">
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
      <template #right>
        <v-btn
          icon
          data-e2e="audienceFilterToggle"
          @click.native="filterToggle()"
        >
          <icon
            type="filter"
            :size="27"
            :color="isFilterToggled ? 'primary' : 'black'"
            :variant="
              showError
                ? 'lighten3'
                : isFilterToggled
                ? 'lighten6'
                : 'darken4'
            "
          />
          <v-badge
            v-if="finalFilterApplied > 0"
            :content="finalFilterApplied"
            color="white"
            offset-x="6"
            offset-y="4"
            light
            bottom
            overlap
            bordered
          />
        </v-btn>
      </template>
    </page-header>


    <div
      class="d-flex flex-nowrap align-stretch flex-grow-1 flex-shrink-0 mw-100"
    >
      <div class="flex-grow-1 flex-shrink-1 overflow-hidden mw-100">
        <page-header   class="top-bar" v-if="addedModels.length > 0" :header-height="69">
      <template #left>
        <v-btn disabled icon color="black">
          <icon type="search" :size="20" color="black" variant="lighten3" />
        </v-btn>
      </template>
      <template #right>
        <huxButton
          v-if="getAccess('models', 'request_one')"
          variant="primary"
          size="large"
          is-tile
          height="40"
          class="ma-2 font-weight-regular no-shadow mr-0 caption"
          data-e2e="addModel"
          @click="toggleDrawer()"
        >
          Request a model
        </huxButton>
      </template>
    </page-header>
    <v-progress-linear :active="loading" :indeterminate="loading" />
        <v-row
          v-if="addedModels.length > 0 && !loading"
          class="padding-30 ma-0 content-section"
        >
        <descriptive-card
          v-for="model in addedModels"
          :key="model.id"
          :action-menu="model.status !== 'Active'"
          :coming-soon="false"
          width="280"
          height="255"
          :icon="`model-${getModelType(model)}`"
          :title="model.name"
          :logo-option="true"
          :description="model.description"
          :top-right-adjustment="
            model.status != 'active' ? 'ml-8 mt-6 mr-8' : 'mt-3 mr-8'
          "
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
          <template
            v-if="model.tags.industry.length > 0 && model.status == 'Active'"
            slot="top"
          >
            <div class="float-right">
              <tooltip v-for="tags in model.tags.industry" :key="tags">
                <template #label-content>
                  <logo
                    :key="tags"
                    :size="16"
                    class="mr-1"
                    :type="`${tags}_logo`"
                  />
                </template>
                <template #hover-content>
                  <span>{{ formatText(tags) }}</span>
                </template>
              </tooltip>
            </div>
          </template>
          <template v-if="model.status == 'Active'" slot="default">
            <v-row no-gutters class="mt-4">
              <v-col cols="5">
                <card-stat
                  label="Version"
                  :value="
                    model.latest_version.length == 10
                      ? model.latest_version.substring(2)
                      : model.latest_version | Empty
                  "
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
            <div
              class="px-4 py-2 white d-flex flex-column text-h5"
              data-e2e="remove-model"
              @click="removeModel(model)"
            >
              <span class="d-flex align-center"> Remove </span>
            </div>
          </template>
        </descriptive-card>
        </v-row>
        <v-row
          v-else-if="addedModels.length == 0 && !showError"
          class="background-empty"
        >
        <hux-empty
        icon-type="models-empty"
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
            @click="toggleDrawer()"
          >
            Request a model
          </hux-button>
        </template>
      </hux-empty>
        </v-row>
        <v-row
         v-else
          class="d-flex justify-center align-center"
        >
      <error
        icon-type="error-on-screens"
        :icon-size="50"
        title="Models are currently unavailable"
        subtitle="Our team is working hard to fix it. Please be patient and try again soon!"
        class="models-error-height"
      >
      </error>
        </v-row>
        <alert-drawer v-model="alertDrawer" :notification-id="notificationId" />
      </div>
      <div class="ml-auto">
        <model-filter
          ref="filters"
          v-model="isFilterToggled"
          :filter-options="filterOptions()"
          @onSectionAction="applyFilter"
          view-height="calc(100vh - 145px)"
        />
        <model-configuration v-model="drawer" @refresh="reloadWithCloseDrawer()" />
      </div>
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
    </div>
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
import Icon from "../../components/common/Icon.vue"
import ConfirmModal from "@/components/common/ConfirmModal"
import ModelConfiguration from "@/views/Models/Drawers/Configuration"
import Logo from "@/components/common/Logo.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import ModelFilter from "@/views/Models/Drawers/ModelFilter"
import { getAccess, formatText, getIndustryTags } from "@/utils.js"

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
    Icon,
    ConfirmModal,
    ModelConfiguration,
    Logo,
    Tooltip,
    ModelFilter,
  },
  data() {
    return {
      loading: false,
      showError: false,
      drawer: false,
      confirmModal: false,
      selectedModal: null,
      isFilterToggled: false,
      finalFilterApplied: 0,
      industryTags: getIndustryTags(),
      modelTypes: [
        "purchase",
        "prediction",
        "ltv",
        "churn",
        "propensity",
        "unsubscribe",
        "regression",
        "classification",
      ],
    }
  },
  computed: {
    ...mapGetters({
      models: "models/list",
    }),
    addedModels() {
      const actives = this.models
        .filter((model) => ["Active"].includes(model.status))
        .sort((a, b) => {
          return a.name < b.name
        })
      const others = this.models
        .filter((model) => ["Requested"].includes(model.status))
        .sort((a, b) => {
          return a.name < b.name
        })
      return [...actives, ...others]
    },
  },
  async mounted() {
    this.loading = true
    try {
      await this.getModels()
    } catch (error) {
      this.showError = true
    }
    this.loading = false
  },
  methods: {
    ...mapActions({
      getModels: "models/getAll",
      getModelsByFilter: "models/getFilteredModels",
      deleteModal: "models/remove",
    }),
    goToDashboard(model) {
      if (model.status === "Active") {
        this.$router.push({
          name: "ModelDashboard",
          params: {
            id: model.id,
            name: model.name,
            type: model.type,
          },
        })
      }
    },
    getModelType(model) {
      return this.modelTypes.includes(
        model.type ? model.type.toLowerCase() : ""
      )
        ? model.type.toLowerCase()
        : "unknown"
    },
    toggleDrawer() {
      this.drawer = !this.drawer
    },
    clearFilters() {
      this.$refs.filters.clear()
    },
    async reloadWithCloseDrawer() {
      this.toggleDrawer()
      this.refreshScreen()
    },
    async refreshScreen() {
      this.loading = true
      try {
        await this.getModels()
      } catch (error) {
        this.showError = true
      }
      this.loading = false
    },
    removeModel(modal) {
      this.selectedModal = modal
      this.confirmModal = true
    },
    async confirmRemoval() {
      this.confirmModal = false
      await this.deleteModal(this.selectedModal)
      this.refreshScreen()
    },
    async applyFilter(params) {
      this.loading = true
      this.finalFilterApplied = params.filterApplied
      let queryParams = {
        tags: params.selectedTags
      }
      await this.getModelsByFilter(queryParams)
      this.loading = false
    },
    filterToggle() {
        this.isFilterToggled = !this.isFilterToggled
    },
    filterOptions() {
      let options = []
      for (let tags of this.industryTags) {
      options.push({
                key: tags,
                name: formatText(tags),
                category: "industry",
                optionName: "Tags",
              })
      }
      return options
    },
    getAccess: getAccess,
    formatText: formatText,
  },
}
</script>

<style lang="scss" scoped>
.models-wrap {
  background: var(--v-white-base);
  ::v-deep .menu-cell-wrapper .action-icon {
    display: none;
  }
  .top-bar {
    margin-top: 1px;
    .v-icon--disabled {
      color: var(--v-black-lighten3) !important;
      font-size: 24px;
    }
    .text--refresh {
      margin-right: 10px;
    }
  }
  ::v-deep .menu-cell-wrapper :hover .action-icon {
    display: initial;
  }
  .icon-border {
    cursor: default !important;
  }
}
.padding-30 {
  padding: 30px !important;
}
::-webkit-scrollbar {
  width: 5px;
}
::-webkit-scrollbar-track {
  box-shadow: inset 0 0 5px var(--v-white-base);
  border-radius: 10px;
}
::-webkit-scrollbar-thumb {
  background: var(--v-black-lighten3);
  border-radius: 5px;
}
::-webkit-scrollbar-thumb:hover {
  background: var(--v-black-lighten3);
}
.content-section {
  height: calc(100vh - 250px);
  overflow-y: auto !important;
  overflow-x: hidden !important;
}
.models-error-height {
  height: 280px !important;
}
::v-deep .title-up {
  position: relative;
  top: -4px;
}
::v-deep .descriptive-card .description {
  padding-left: 24px !important;
  padding-right: 24px !important;
  height: 35px !important;
}
</style>
