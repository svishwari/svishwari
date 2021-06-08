<template>
  <div class="audiences-wrap grey lighten-5">
    <PageHeader>
      <template slot="left">
        <Breadcrumb :items="breadcrumbItems" />
      </template>
      <template slot="right">
        <v-btn
          min-width="40"
          height="40"
          width="40"
          color="primary"
          :disabled="true"
        >
          <v-icon size="23" color="white">mdi-download</v-icon>
        </v-btn>
      </template>
    </PageHeader>
    <PageHeader class="top-bar" :headerHeight="71">
      <template slot="left">
        <v-icon medium :disabled="true">mdi-filter-variant</v-icon>
        <v-icon medium :disabled="true" class="pl-6">mdi-magnify</v-icon>
      </template>

      <template slot="right">
        <v-icon medium :disabled="true" color="primary refresh"
          >mdi-refresh</v-icon
        >
        <router-link
          :to="{ name: 'AudienceConfiguration' }"
          class="text-decoration-none"
          append
        >
          <huxButton
            icon="mdi-plus"
            iconPosition="left"
            variant="primary"
            size="large"
            v-bind:isTile="true"
            class="ma-2 font-weight-regular no-shadow mr-0"
          >
            <template #text>
              <span>Audience</span>
            </template>
          </huxButton>
        </router-link>
      </template>
    </PageHeader>
    <v-progress-linear :active="loading" :indeterminate="loading" />
    <v-row class="pt-3 pb-7" v-if="!loading">
      <hux-table
        v-if="isDataExists"
        :columnDef="columnDefs"
        :tableData="rowData"
        :rowHeight="60"
        height="calc(100vh - 220px)"
        class="pl-3"
      ></hux-table>

      <EmptyPage v-if="!isDataExists">
        <template v-slot:icon>mdi-alert-circle-outline</template>
        <template v-slot:title>Oops! There’s nothing here yet</template>
        <template v-slot:subtitle>
          You currently have no audiences created! You can create the
          <br />framework first then complete the details later. <br />Begin by
          selecting the button below.
        </template>
        <template v-slot:button>
          <router-link
            :to="{ name: 'AudienceConfiguration' }"
            class="route-link text-decoration-none"
            append
          >
            <huxButton
              icon="mdi-plus"
              iconPosition="left"
              variant="primary"
              size="large"
              v-bind:isTile="true"
              class="ma-2 font-weight-regular"
            >
              <template #text>
                <span>Audience</span>
              </template>
            </huxButton>
          </router-link>
        </template>
      </EmptyPage>
    </v-row>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"

import PageHeader from "@/components/PageHeader"
import EmptyPage from "@/components/common/EmptyPage"
import Breadcrumb from "@/components/common/Breadcrumb"
import huxButton from "@/components/common/huxButton"
import HuxTable from "@/components/common/huxTable.vue"
import UserAvatarCell from "@/components/common/huxTable/UserAvatarCell"
import MenuCell from "@/components/common/huxTable/MenuCell"
import DateTimeCell from "@/components/common/huxTable/DateTimeCell"
import sizeCell from "@/components/common/huxTable/sizeCell"

export default {
  name: "audiences",
  components: {
    PageHeader,
    Breadcrumb,
    huxButton,
    HuxTable,
    EmptyPage,
  },
  data() {
    return {
      breadcrumbItems: [
        {
          text: "Audiences",
          disabled: true,
          icon: "audiences",
        },
      ],

      columnDefs: [
        {
          headerName: "Audience name",
          field: "name",
          sortable: true,
          sort: "desc",
          pinned: "left",
          width: "300",
          cellRendererFramework: MenuCell,
          cellClass: "menu-cells",
          sortingOrder: ["desc", "asc"],
        },
        {
          headerName: "Size",
          field: "size",
          sortable: true,
          width: "100",
          cellRendererFramework: sizeCell,
          sortingOrder: ["desc", "asc"],
        },
        {
          headerName: "Last delivered",
          field: "last_delivered",
          width: "170",
          sortable: true,
          cellRendererFramework: DateTimeCell,
          sortingOrder: ["desc", "asc"],
        },
        {
          headerName: "Last updated",
          field: "update_time",
          sortable: true,
          width: "170",
          cellRendererFramework: DateTimeCell,
          sortingOrder: ["desc", "asc"],
        },
        {
          headerName: "Last updated by",
          field: "updated_by",
          sortable: true,
          width: "140",
          cellRendererFramework: UserAvatarCell,
          sortingOrder: ["desc", "asc"],
        },
        {
          headerName: "Created",
          field: "create_time",
          sortable: true,
          width: "160",
          cellRendererFramework: DateTimeCell,
          sortingOrder: ["desc", "asc"],
        },
        {
          headerName: "Created by",
          field: "created_by",
          sortable: true,
          cellRendererFramework: UserAvatarCell,
          sortingOrder: ["desc", "asc"],
        },
      ],
      loading: false,
    }
  },
  computed: {
    ...mapGetters({
      rowData: "audiences/list",
    }),
    isDataExists() {
      if (this.rowData) return this.rowData.length > 0
      return false
    },
  },
  methods: {
    ...mapActions({
      getAllAudiences: "audiences/getAll",
    }),
  },
  async mounted() {
    this.loading = true
    await this.getAllAudiences()
    this.loading = false
  },
}
</script>
<style lang="scss" scoped>
.audiences-wrap {
  ::v-deep .menu-cell-wrapper .action-icon {
    display: none;
  }
  .page-header--wrap {
    box-shadow: 0px 1px 1px -1px var(--v-lightGrey-base),
      0px 1px 1px 0px var(--v-lightGrey-base),
      0px 1px 2px 0px var(--v-lightGrey-base) !important;
  }
  .top-bar {
    margin-top: 1px;
    .v-icon--disabled {
      color: var(--v-lightGrey-base) !important;
      font-size: 24px;
    }
    .text--refresh {
      margin-right: 10px;
    }
  }
  ::v-deep .ag-row-hover .menu-cell-wrapper .action-icon {
    display: initial;
  }
}
</style>
