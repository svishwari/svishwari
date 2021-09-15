<template>
  <div class="add-data-source--wrap">
    <drawer v-model="localDrawer" @onClose="closeAddDataSource">
      <template #header-left>
        <div class="d-flex align-baseline">
          <h3 class="text-h3 font-weight-light pr-2">Select a data source</h3>
        </div>
      </template>
      <template #footer-left>
        <div class="d-flex align-baseline">
          <div
            class="font-weight-regular black--text text--darken-1 text-caption"
          >
            {{ dataSources.length }} results
          </div>
        </div>
      </template>
      <template #footer-right>
        <div v-if="isDataSourcesSelected" class="d-flex align-baseline">
          <huxButton
            variant="white"
            size="large"
            :is-tile="true"
            class="mr-2"
            @click="closeAddDataSource"
          >
            <span class="primary--text">Cancel</span>
          </huxButton>
          <huxButton
            variant="primary"
            size="large"
            :is-tile="true"
            :is-disabled="!isDataSourcesSelected"
            @click="addDataSources"
          >
            {{ dataSourcesBtnText }}
          </huxButton>
        </div>
      </template>
      <template #default>
        <div class="ma-3">
          <div class="font-weight-light">Data sources</div>
          <card-horizontal
            v-for="dataSource in enabledDataSources"
            :key="dataSource.id"
            :title="dataSource.name"
            :icon="dataSource.type"
            :is-added="
              dataSource.is_added ||
              selectedDataSourceIds.includes(dataSource.id)
            "
            :is-available="dataSource.is_enabled"
            :is-already-added="dataSource.is_added"
            class="my-3"
            data-e2e="dataSourcesAddList"
            @click="onDataSourceClick(dataSource.id)"
          />

          <v-divider style="border-color: var(--v-zircon-base)" />

          <card-horizontal
            v-for="dataSource in disabledDataSources"
            :key="dataSource.id"
            :title="dataSource.name"
            :icon="dataSource.type"
            :is-added="
              dataSource.is_added ||
              selectedDataSourceIds.includes(dataSource.id)
            "
            :is-available="dataSource.is_enabled"
            :is-already-added="dataSource.is_added"
            class="my-3"
            hide-button
          >
            <span class="font-weight-light letter-spacing-sm"
              ><i>Coming soon</i></span
            >
          </card-horizontal>
        </div>
      </template>
    </drawer>
  </div>
</template>

<script>
import Drawer from "@/components/common/Drawer"
import huxButton from "@/components/common/huxButton"
import CardHorizontal from "@/components/common/CardHorizontal"
import { mapGetters, mapActions } from "vuex"
export default {
  name: "DataSourceConfiguration",

  components: {
    Drawer,
    CardHorizontal,
    huxButton,
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
      selectedDataSourceIds: [],
    }
  },

  computed: {
    ...mapGetters({
      dataSources: "dataSources/list",
    }),

    isDataSourcesSelected() {
      return this.selectedDataSourceIds.length > 0
    },
    dataSourcesBtnText() {
      let count = this.selectedDataSourceIds.length
      return `Add ${count} data source${count > 1 ? "s" : ""}`
    },

    enabledDataSources() {
      return this.dataSources.filter((each) => each.is_enabled)
    },

    disabledDataSources() {
      return this.dataSources.filter((each) => !each.is_enabled)
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
      batchAddDataSources: "dataSources/batchAdd",
    }),
    onDataSourceClick: function (id) {
      if (this.selectedDataSourceIds.includes(id)) {
        const deselectedId = this.selectedDataSourceIds.indexOf(id)
        this.selectedDataSourceIds.splice(deselectedId, 1)
      } else {
        this.selectedDataSourceIds.push(id)
      }
    },
    addDataSources: function () {
      this.batchAddDataSources({
        body: {
          is_added: true,
          status: "Pending",
        },
        data_source_ids: this.selectedDataSourceIds,
      })
      this.closeAddDataSource()
    },
    closeAddDataSource: function () {
      this.localDrawer = false
      this.selectedDataSourceIds = []
    },
  },
}
</script>
