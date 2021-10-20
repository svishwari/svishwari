<template>
  <div class="list-wrapper">
    <!-- <div class="d-flex align-end mb-4">
      <icon type="data-sources-list" :size="20" color="black-darken4" />
      <h5 class="text-h4 ml-2 mt-1">Data Sources</h5>
      <span data-e2e="addDataSource" @click="$emit('onAddDatasource')">
        <icon class="add-icon cursor-pointer" type="add" :size="27" />
      </span>
    </div> -->
    <v-row >
    <template v-if="hasAddedDatasources">

       <descriptive-card
          v-for="dataSource in addedDataSources"
          :key="dataSource.id"
           :icon="dataSource.type"
          :title="dataSource.name"
          :description="''"
          :disabled="dataSource.status !== 'Active'"
           :action-menu="true"
            :coming-soon="false"
          class="mr-10 model-desc-card"
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
              :status="dataSource.status || ''"
              collapsed
              class="d-flex"
              data-e2e="model-status"
            />
          </template>
       </descriptive-card>
    </template>
    </v-row>

    <template v-if="hasAddedDatasources">
      <card-horizontal
        v-for="dataSource in addedDataSources"
        :key="dataSource.id"
        :title="dataSource.name"
        :icon="dataSource.type"
        :class="
          dataSource.status === 'Active'
            ? 'data-source-list-active'
            : 'data-source-list-pending'
        "
        hide-button
        data-e2e="dataSourcesList"
        class="mb-3 pr-7 list"
        :to="
          dataSource.status === 'Active'
            ? {
                name: 'DataSourceListing',
                params: { id: dataSource.id },
              }
            : undefined
        "
      >
        <div class="d-flex align-center">
          <status
            :status="dataSource.status"
            :icon-size="17"
            class="status"
            :class="dataSource.status === 'Pending' ? 'mr-10' : 'mr-16'"
          />
          <v-menu left offset-y close-on-click>
            <template #activator="{ on }">
              <v-icon
                v-if="dataSource.status === 'Pending'"
                color="black darken-4"
                data-e2e="data-source-list-pending-button"
                v-on="on"
              >
                mdi-dots-vertical
              </v-icon>
            </template>
            <div
              class="black--text text-darken-4 cursor-pointer px-4 py-2 white"
              data-e2e="data-source-list-pending-remove"
              @click="openModal(dataSource)"
            >
              Remove
            </div>
          </v-menu>
        </div>
      </card-horizontal>
    </template>

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

import CardHorizontal from "@/components/common/CardHorizontal"
import ConfirmModal from "@/components/common/ConfirmModal"
import Icon from "@/components/common/Icon"
import Status from "@/components/common/Status"
import EmptyStateData from "@/components/common/EmptyStateData"
import DescriptiveCard from "@/components/common/Cards/DescriptiveCard"

export default {
  name: "DataSourcesList",

  components: { EmptyStateData, CardHorizontal, Status, Icon, ConfirmModal, DescriptiveCard },

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
      return this.dataSources.filter((dataSource) => dataSource.is_added)
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
  .data-source-list-active {
    @extend .cursor-pointer;
    ::v-deep .card-horizontal-title {
      color: var(--v-primary-base) !important;
    }
  }
  .data-source-list-pending {
    @extend .cursor-default;
  }
}
</style>
