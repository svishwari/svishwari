<template>
  <div class="list-wrapper">
    <div class="d-flex align-end mb-4">
      <icon type="data-sources-list" :size="20" color="black-darken4" />
      <h5 class="text-h4 ml-2 mt-1">Data Sources</h5>
      <span @click="$emit('onAddDatasource')">
        <icon class="add-icon cursor-pointer" type="add" :size="27" />
      </span>
    </div>

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
        class="mb-3 pr-10 list"
        :to="
          dataSource.status === 'Active'
            ? {
                name: 'DataSourceListing',
                params: { id: dataSource.id },
              }
            : {}
        "
      >
        <status :status="dataSource.status" :icon-size="17" class="status" />
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
  </div>
</template>

<script>
import { mapGetters } from "vuex"

import CardHorizontal from "@/components/common/CardHorizontal"
import Icon from "@/components/common/Icon"
import Status from "@/components/common/Status"
import EmptyStateData from "@/components/common/EmptyStateData"

export default {
  name: "DataSourcesList",

  components: { EmptyStateData, CardHorizontal, Status, Icon },

  data() {
    return {
      drawer: false,
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
}
</script>
<style lang="scss" scoped>
.list-wrapper {
  .add-icon {
    display: block;
    margin-left: 7px;
    position: relative;
    top: 2px;
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
      color: var(--v-primary-base);
    }
  }
  .data-source-list-pending {
    @extend .cursor-default;
  }
}
</style>
