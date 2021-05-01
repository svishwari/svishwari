<template>
  <div class="audiences-wrap grey lighten-5">
    <PageHeader>
      <template slot="left">
        <Breadcrumb :items="breadcrumbItems" />
      </template>
    </PageHeader>
    <PageHeader class="mt-1" headerHeight="71">
      <template slot="left">
        <v-icon large :disabled="true" @click="refresh"> mdi-filter-variant </v-icon>
      </template>

      <template slot="right">
        <v-icon large :disabled="true" color="primary" @click="refresh"> mdi-refresh </v-icon>
        <router-link
          :to="{ path: '/audiences/create-audience' }"
          class="text-decoration-none"
          append
        >
          <huxButton
            ButtonText="Audience"
            icon="mdi-plus"
            iconPosition="left"
            variant="primary"
            size="large"
            v-bind:isTile="true"
            class="ma-2 font-weight-regular"
          ></huxButton>
        </router-link>
      </template>
    </PageHeader>
    <v-row class="pt-3 pb-7">

      <hux-table
        v-if="isDataExists"
        :columnDef="columnDefs"
        :tableData="rowData"
        :rowHeight="60"
        height="350px"
        hasCheckBox
      ></hux-table>

      <EmptyPage  v-if="!isDataExists">
        <template v-slot:icon> mdi-alert-circle-outline </template>
        <template v-slot:title> Oops! There’s nothing here yet </template>
        <template v-slot:subtitle>
          You currently have no audiences created! You can create the <br />
          framework first then complete the details later. <br />
          Begin by selecting the button below.
        </template>
        <template v-slot:button>
          <router-link
            :to="{ path: '/audiences/create-audience' }"
            class="route-link text-decoration-none"
            append
          >
            <huxButton
              ButtonText="Audience"
              icon="mdi-plus"
              iconPosition="left"
              variant="primary"
              size="large"
              v-bind:isTile="true"
              class="ma-2 font-weight-regular"
            ></huxButton>
          </router-link>
        </template>
      </EmptyPage>

    </v-row>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"

import PageHeader from "@/components/PageHeader"
import EmptyPage from "@/components/EmptyPage"
import Breadcrumb from "@/components/common/Breadcrumb"
import huxButton from "@/components/common/huxButton"
import HuxTable from "@/components/common/huxTable.vue"
import StatusCell from "@/components/common/huxTable/StatusCell"
import UserAvatarCell from "@/components/common/huxTable/UserAvatarCell"
import MenuCell from "@/components/common/huxTable/MenuCell"
import DestinationCell from "@/components/common/huxTable/DestinationCell"
import DateTimeCell from "@/components/common/huxTable/DateTimeCell"
import sizeCell from "@/components/common/huxTable/sizeCell"
import attributeCell from "@/components/common/huxTable/attributeCell"

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
          disabled: false,
          href: this.$route.path,
          icon: "mdi-flip-h mdi-account-plus-outline",
        },
      ],

      columnDefs: [
        {
          headerName: "Audience Name",
          field: "audienceName",
          sortable: true,
          sort: "desc",
          pinned: "left",
          width: "300",
          cellRendererFramework: MenuCell,
          cellClass: "menu-cells",
        },
        {
          headerName: "Status",
          field: "status",
          sortable: true,
          cellRendererFramework: StatusCell,
        },
        {
          headerName: "Size",
          field: "size",
          sortable: true,
          cellRendererFramework: sizeCell,
        },
        {
          headerName: "Destinations",
          field: "destinations",
          sortable: true,
          cellRendererFramework: DestinationCell,
        },
        {
          headerName: "Attributes",
          field: "attributes",
          sortable: true,
          cellRendererFramework: attributeCell,
        },
        {
          headerName: "Last Delivered",
          field: "lastDelivered",
          sortable: true,
        },
        {
          headerName: "Last Updated",
          field: "lastUpdated",
          sortable: true,
          cellRendererFramework: DateTimeCell,
        },
        {
          headerName: "Last Updated By",
          field: "lastUpdatedBy",
          sortable: true,
          cellRendererFramework: UserAvatarCell,
        },
        {
          headerName: "Created",
          field: "created",
          sortable: true,
          cellRendererFramework: DateTimeCell,
        },
        {
          headerName: "Created By",
          field: "createdBy",
          sortable: true,
          cellRendererFramework: UserAvatarCell,
        },
      ],
    }
  },
  computed: {
    ...mapGetters({
      rowData: "AllAudiences",
    }),
    isDataExists() {
      return ( this.rowData.length > 0 )
    }
  },
  methods: {
    ...mapActions(["getAllAudiences"]),
    refresh() {},
  },
  async mounted() {
    await this.getAllAudiences()
  },
}
</script>
<style lang="scss" scoped>
.audiences-wrap {
  ::v-deep .menu-cell-wrapper .action-icon {
    display: none;
  }
  ::v-deep .ag-row-hover .menu-cell-wrapper .action-icon {
    display: initial;
  }
}
</style>
