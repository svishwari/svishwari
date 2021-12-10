<template>
  <div class="add-data-source--wrap">
    <drawer v-model="localDrawer" @onClose="closeAddModel">
      <template #header-left>
        <breadcrumb :items="breadcrumbs" />
      </template>
      <template #footer-left>
        <div class="d-flex align-baseline">
          <div class="body-2">{{ models.length }} results</div>
        </div>
      </template>
      <template #footer-right>
        <div v-if="isModelsSelected" class="d-flex align-baseline">
          <hux-button
            variant="white"
            size="large"
            :is-tile="true"
            class="mr-2"
            @click="closeAddModel"
          >
            <span class="primary--text">Cancel</span>
          </hux-button>
          <hux-button
            variant="primary"
            size="large"
            :is-tile="true"
            :is-disabled="!isModelsSelected"
            @click="requestModels"
          >
            {{ modelsBtnText }}
          </hux-button>
        </div>
      </template>
      <template #default>
        <div class="ma-3">
          <div class="mb-7">
            <div
              v-for="(item, key) in enabledModels"
              :key="key"
              class="ma-3 mt-5"
            >
              <div class="body-2 text-body-2 black--text text--lighten-4">
                {{ key }}
              </div>
              <card-horizontal
                v-for="model in item"
                :key="model.id"
                :title="model.name"
                :icon="`model-${getModelType(model)}`"
                :is-added="['Active', 'Requested'].includes(model.status)"
                :is-available="model.is_enabled"
                :is-already-added="
                  ['Active', 'Requested'].includes(model.status)
                "
                class="my-3 body-1"
                data-e2e="modelAddList"
                :requested-button="model.status != 'Active'"
                :is-model-requested="model.status == 'Requested'"
              />
            </div>
          </div>

          <v-divider
            class="mb-2"
            style="border-color: var(--v-black-lighten2)"
          />
          <div
            v-for="(item, key) in modelsGroupedSorted"
            :key="key"
            class="ma-3 mt-5"
          >
            <div class="body-2 text-body-2 black--text text--lighten-4">
              {{ key }}
            </div>
            <card-horizontal
              v-for="model in item"
              :key="model.id"
              :title="model.name"
              :icon="`model-${getModelType(model)}`"
              :is-added="
                ['Active', 'Requested'].includes(model.status) ||
                selectedModelIds.includes(model.id)
              "
              :is-available="model.is_enabled"
              :is-already-added="['Active'].includes(model.status)"
              class="my-3 body-1"
              requested-button
              :is-model-requested="model.status == 'Requested'"
              data-e2e="dataSourcesRequestList"
              @click="onModelClick(model)"
            />
          </div>
        </div>
      </template>
    </drawer>
  </div>
</template>

<script>
import Drawer from "@/components/common/Drawer"
import CardHorizontal from "@/components/common/CardHorizontal"
import Breadcrumb from "@/components/common/Breadcrumb"
import { mapGetters, mapActions } from "vuex"
import { sortByName } from "../../../utils"
import HuxButton from "../../../components/common/huxButton.vue"

export default {
  name: "ModelConfiguration",

  components: {
    Drawer,
    CardHorizontal,
    Breadcrumb,
    HuxButton,
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
      selectedModelIds: [],
      selectedModelObjects: [],
      breadcrumbs: [
        {
          text: "Select a model to request",
          icon: "models-request",
          iconColor: "white",
        },
      ],
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

    isModelsSelected() {
      return this.selectedModelIds.length > 0
    },
    modelsBtnText() {
      let count = this.selectedModelIds.length
      return `Request ${count} model${count > 1 ? "s" : ""}`
    },

    enabledModels() {
      const oldresult = this.models.reduce(function (modelObject, model) {
        if (["Active", "Requested"].includes(model.status)) {
          modelObject[model.type] = modelObject[model.type] || []
          modelObject[model.type].push(model)
        }
        return modelObject
      }, Object.create(null))

      const result = Object.keys(oldresult)
        .sort()
        .reduce((obj, key) => {
          obj[key] = oldresult[key]
          return obj
        }, {})

      let orderedResult = Object.keys(result)
        .sort(function (a, b) {
          return a.toLowerCase().localeCompare(b.toLowerCase())
        })
        .reduce(function (Obj, key) {
          Obj[key] = result[key]
          return Obj
        }, {})

      sortByName(orderedResult, "name")
      return orderedResult
    },

    modelsGroupedSorted() {
      const oldresult = this.models.reduce(function (modelObject, model) {
        if (!["Active", "Requested"].includes(model.status)) {
          modelObject[model.type] = modelObject[model.type] || []
          modelObject[model.type].push(model)
        }
        return modelObject
      }, Object.create(null))

      const result = Object.keys(oldresult)
        .sort()
        .reduce((obj, key) => {
          obj[key] = oldresult[key]
          return obj
        }, {})

      let orderedResult = Object.keys(result)
        .sort(function (a, b) {
          return a.toLowerCase().localeCompare(b.toLowerCase())
        })
        .reduce(function (Obj, key) {
          Obj[key] = result[key]
          return Obj
        }, {})

      sortByName(orderedResult, "name")
      return orderedResult
    },
  },
  watch: {
    value: function () {
      this.localDrawer = this.value
    },
    localDrawer: function () {
      this.$emit("input", this.localDrawer)
      if (!this.localDrawer) {
        this.$emit("onClose")
      }
    },
  },
  methods: {
    ...mapActions({
      requestModel: "models/add",
    }),
    async onModelClick(model) {
      if (this.selectedModelIds.includes(model.id)) {
        const deselectedId = this.selectedModelIds.indexOf(model.id)
        this.selectedModelIds.splice(deselectedId, 1)
      } else {
        this.selectedModelIds.push(model.id)
      }
    },
    requestModels: function () {
      const selectedModels = JSON.parse(
        JSON.stringify(
          this.models.filter((mod) => this.selectedModelIds.includes(mod.id))
        )
      )
      selectedModels.forEach((mod) => {
        delete mod.description
        mod.status = "Requested"
      })
      this.requestModel(selectedModels)
      this.$emit("refresh")
    },
    closeAddModel: function () {
      this.localDrawer = false
      this.selectedModelIds = []
    },
    getModelType(model) {
      return this.modelTypes.includes(
        model.type ? model.type.toLowerCase() : ""
      )
        ? model.type.toLowerCase()
        : "unknown"
    },
  },
}
</script>

<style lang="scss">
// this is a temporary fix, this figma design need to be synced with other drawer design.
.add-data-source--wrap {
  .drawer-content.contentPadding {
    .card-horizontal-disabled {
      @extend .box-shadow-5;
      background: var(--v-white-base) !important;
      border: none !important;
    }
    svg {
      border: 1px solid var(--v-black-lighten2);
      border-radius: 50%;
      box-sizing: border-box;
      padding: 4px;
      width: 26px !important;
      height: 26px !important;
    }
  }
}
</style>
