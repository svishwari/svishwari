<template>
  <div class="list-wrapper">
    <v-row v-if="hasAddedDatasources">
      <template>
        <descriptive-card
          v-for="dataSource in addedDataSources"
          :key="dataSource.id"
          :icon="dataSource.type"
          :title="dataSource.name"
          :description="dataSource.category"
          :disabled="dataSource.status !== 'Active'"
          :action-menu="dataSource.status !== 'Active'"
          :interactable="dataSource.status == 'Active' ? true : false"
          :coming-soon="false"
          :icon-color="true"
          :logo-option="true"
          :dot-option="'Remove'"
          class="mr-10 model-desc-card"
          height="225"
          width="255"
          data-e2e="dataSourcesList"
          :to="
            dataSource.status === 'Active'
              ? {
                  name: 'DataSourceListing',
                  params: { id: dataSource.id },
                }
              : undefined
          "
        >
          <template slot="top">
            <status
              :icon-size="18"
              :status="
                dataSource.status === 'Pending'
                  ? 'Requested'
                  : dataSource.status || ''
              "
              collapsed
              class="d-flex float-left"
              :data-e2e="`model-status-${dataSource.status}`"
            />
          </template>
          <template slot="action-menu-options">
            <div
              class="px-4 py-2 white d-flex flex-column text-h5"
              :data-e2e="`data-source-list-${dataSource.status}-remove`"
              @click="openModal(dataSource)"
            >
              <span class="d-flex align-center"> Remove </span>
            </div>
          </template>

          <template slot="default">
            <div class="text-h4 black--text">
              {{ dataSource.feed_count ? dataSource.feed_count : "-" }}
            </div>
            <p
              class="text-body-2 black--text text--lighten-4"
              data-e2e="model-owner"
            >
              No. of feeds
            </p>
          </template>
        </descriptive-card>
      </template>
    </v-row>

    <empty-state-data v-else>
      <template #icon> mdi-alert-circle-outline </template>
      <template #title> Oops! There’s nothing here yet </template>
      <template #subtitle>
        To create a connection, a data source must be imported!
        <br />
        Begin by selecting the plus button above.
      </template>
    </empty-state-data>

    <confirm-modal
      v-model="confirmModal"
      icon="sad-face"
      type="error"
      title="You are about to remove"
      :sub-title="`${selectedDataSource.name}`"
      body="Are you sure you want to remove this pending data source?"
      right-btn-text="Yes, remove it"
      data-e2e="remove-data-source-confirmation"
      @onCancel="confirmModal = !confirmModal"
      @onConfirm="confirmRemoval()"
    />
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"

import ConfirmModal from "@/components/common/ConfirmModal"
import Status from "@/components/common/Status"
import EmptyStateData from "@/components/common/EmptyStateData"
import DescriptiveCard from "@/components/common/Cards/DescriptiveCard"
import sortBy from "lodash/sortBy"

export default {
  name: "DataSourcesList",

  components: {
    EmptyStateData,
    Status,
    ConfirmModal,
    DescriptiveCard,
  },

  data() {
    return {
      drawer: false,
      selectedDataSource: {},
      confirmModal: false,
    }
  },

  computed: {
    ...mapGetters({
      dataSources: "dataSources/list",
    }),

    addedDataSources() {
      return sortBy(
        this.dataSources.filter((dataSource) => dataSource.is_added),
        ["status", "name"]
      )
    },

    hasAddedDatasources() {
      return Boolean(this.addedDataSources && this.addedDataSources.length)
    },
  },

  methods: {
    ...mapActions({
      batchUpdateDataSources: "dataSources/batchUpdate",
    }),
    openModal(dataSource) {
      this.selectedDataSource = dataSource
      this.confirmModal = true
    },

    async confirmRemoval() {
      await this.batchUpdateDataSources({
        body: {
          is_added: false,
        },
        data_source_ids: [this.selectedDataSource.id],
      })
      this.confirmModal = false
    },
  },
}
</script>
<style lang="scss" scoped>
.list-wrapper {
  .add-icon {
    display: block;
    margin-left: 7px;
    position: relative;
    top: 3px;
  }
  .v-card {
    .status {
      min-width: 80px;
      ::v-deep i {
        font-size: 17px;
      }
    }
  }
}
</style>
