<template>
  <div class="add-data-source--wrap">
    <drawer v-model="localDrawer" @onClose="closeAddDataSource">
      <template #header-left>
        <breadcrumb :items="breadcrumbs" />
      </template>
      <template #footer-left>
        <div class="d-flex align-baseline">
          <div class="body-2 pl-4">{{ dataSources.length }} results</div>
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
          <div class="ma-3 mb-7">
            <div class="body-2">Data sources</div>
            <card-horizontal
              v-for="dataSource in enabledDataSources"
              :key="dataSource.id"
              :title="dataSource.name"
              :icon="dataSource.type"
              :is-added="dataSource.is_added"
              :is-available="dataSource.is_enabled"
              :is-already-added="dataSource.is_added"
              class="my-3 body-1"
              data-e2e="dataSourcesAddList"
              :requested-button="dataSource.status !== 'Active'"
            />
          </div>

          <v-divider
            class="mb-2"
            style="border-color: var(--v-black-lighten2)"
          />
          <div
            v-for="(item, key) in dataSourcesGroupedSorted"
            :key="key"
            class="ma-3 mt-5"
          >
            <div class="body-2">{{ key }}</div>
            <card-horizontal
              v-for="dataSource in item"
              :key="dataSource.id"
              :title="dataSource.name"
              :icon="dataSource.type"
              :is-added="
                dataSource.is_added ||
                selectedDataSourceIds.includes(dataSource.id)
              "
              :is-available="dataSource.is_enabled"
              :is-already-added="dataSource.is_added"
              class="my-3 body-1"
              :requested-button="dataSource.status !== 'Active'"
              @click="onDataSourceClick(dataSource.id)"
            />
          </div>
        </div>
      </template>
    </drawer>
  </div>
</template>

<script>
import Drawer from "@/components/common/Drawer"
import huxButton from "@/components/common/huxButton"
import CardHorizontal from "@/components/common/CardHorizontal"
import Breadcrumb from "@/components/common/Breadcrumb"
import { mapGetters, mapActions } from "vuex"
export default {
  name: "DataSourceConfiguration",

  components: {
    Drawer,
    CardHorizontal,
    huxButton,
    Breadcrumb,
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
      breadcrumbs: [
        {
          text: "Select a data source to request",
          icon: "data-source-config",
        },
      ],
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
      return `Request ${count} data source${count > 1 ? "s" : ""}`
    },

    enabledDataSources() {
      const activeEnabled = this.dataSources
        .filter((each) => each.is_added && each.status === "Active")
        .sort(function (a, b) {
          var textA = a.name.toUpperCase()
          var textB = b.name.toUpperCase()
          return textA < textB ? -1 : textA > textB ? 1 : 0
        })

      const notActiveEnabled = this.dataSources
        .filter((each) => each.is_added && each.status !== "Active")
        .sort(function (a, b) {
          var textA = a.name.toUpperCase()
          var textB = b.name.toUpperCase()
          return textA < textB ? -1 : textA > textB ? 1 : 0
        })
      return [...activeEnabled, ...notActiveEnabled]
    },

    dataSourcesGroupedSorted() {
      const oldresult = this.dataSources.reduce(function (
        dataSourceObject,
        dataSource
      ) {
        if (!dataSource.is_added) {
          dataSourceObject[dataSource.category] =
            dataSourceObject[dataSource.category] || []
          dataSourceObject[dataSource.category].push(dataSource)
        }
        return dataSourceObject
      },
      Object.create(null))

      const result = Object.keys(oldresult)
        .sort()
        .reduce((obj, key) => {
          obj[key] = oldresult[key]
          return obj
        }, {})

      Object.values(result).forEach((val) => {
        val.sort(function (a, b) {
          var textA = a.name.toUpperCase()
          var textB = b.name.toUpperCase()
          return textA < textB ? -1 : textA > textB ? 1 : 0
        })
      })
      return result
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
      batchUpdateDataSources: "dataSources/batchUpdate",
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
      this.batchUpdateDataSources({
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

<style lang="scss"></style>
