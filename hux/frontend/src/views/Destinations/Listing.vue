<template>
  <div class="destinations-view-wrap">
    <page-header class="background-border">
      <template slot="left">
        <breadcrumb :items="items" />
      </template>
      <template slot="right">
        <v-icon color="black lighten-3" size="22" class="icon-border pa-2 ma-1">
          mdi-download
        </v-icon>
      </template>
    </page-header>
    <page-header
      bg-color="primary lighten-1"
      style="height: 70px; border: 1px solid var(--v-black-lighten3) !important"
    >
      <template slot="left">
        <v-icon color="primary" class="mr-3 cursor-pointer" large>
          mdi-filter-variant
        </v-icon>
        <v-icon class="mr-3 cursor-pointer" large> mdi-magnify </v-icon>
      </template>

      <template slot="right">
        <v-icon color="primary" large class="mr-3 cursor-pointer">
          mdi-refresh
        </v-icon>
        <v-icon color="primary" large class="mr-3 cursor-pointer">
          mdi-format-list-bulleted
        </v-icon>
        <v-icon color="black lighten-3" large class="mr-3 cursor-pointer">
          mdi-dots-grid
        </v-icon>
        <router-link
          :to="{ name: 'DestinationConfiguration' }"
          class="text-decoration-none"
        >
          <huxButton
            variant="primary base"
            icon-color="white"
            icon-variant="base"
            icon="plus"
            size="large"
            is-custom-icon
            is-tile
          >
            Destination
          </huxButton>
        </router-link>
      </template>
    </page-header>
    <page-header
      bg-color="primary lighten-2"
      style="height: 70px; border: 1px solid var(--v-black-lighten3) !important"
    >
      <template slot="left">
        <div class="d-flex filters-wrapper">
          <dropdown-menu
            v-for="(item, index) in filters"
            :key="item.name"
            v-model="item.selectedValue"
            :label-text="item.name"
            :menu-item="item.values"
            @updatelabelText="onFilterSelection(index)"
          />
        </div>
      </template>
    </page-header>
    <hux-table
      :column-def="columnDefs"
      :table-data="rowData"
      height="250px"
      has-check-box
    />
  </div>
</template>

<script>
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import DropdownMenu from "@/components/common/DropdownMenu"
import huxButton from "@/components/common/huxButton"
import HuxTable from "@/components/common/huxTable.vue"

export default {
  name: "Connections",
  components: { huxButton, PageHeader, Breadcrumb, DropdownMenu, HuxTable },
  data() {
    return {
      items: [
        {
          text: "Connections",
          disabled: false,
          href: "/connections",
          icon: "connections",
        },
        {
          text: "Destinations",
          disabled: true,
          href: this.$route.path,
          icon: "destinations",
        },
      ],
      // This is a temporary fix for table components
      // This is a TODO item
      filters: [
        {
          name: "No. of campaigns",
          values: [
            { value: "1-10" },
            { value: "11-25" },
            { value: "26-50" },
            { value: "50+" },
          ],
          selectedValue: null,
        },
        {
          name: "Updated by",
          values: [
            { value: "Susan Underwood" },
            { value: "James Smith" },
            { value: "Dan Thomas" },
            { value: "Eli Handlebar" },
          ],
          selectedValue: null,
        },
        {
          name: "Added by",
          values: [
            { value: "Susan Underwood" },
            { value: "James Smith" },
            { value: "Dan Thomas" },
            { value: "Eli Handlebar" },
          ],
          selectedValue: null,
        },
      ],
      columnDefs: [
        {
          headerName: "Destination",
          field: "destinationName",
          sortable: true,
          width: "500",
        },
        { headerName: "Engagement(s)", field: "engagements", sortable: true },
        {
          headerName: "Last processed",
          field: "lastProcessed",
          sortable: true,
        },
        { headerName: "Updated by", field: "updatedBy", sortable: true },
        { headerName: "Added date", field: "addedDate", sortable: true },
        { headerName: "Added by", field: "addedBy", sortable: true },
      ],
      rowData: [
        {
          destinationName: "Facebook",
          engagements: "5",
          lastProcessed: "1 week ago",
          updatedBy: "SU",
          addedDate: "Yesterday",
          addedBy: "RB",
        },
        {
          destinationName: "Facebook",
          engagements: "5",
          lastProcessed: "1 week ago",
          updatedBy: "SU",
          addedDate: "Yesterday",
          addedBy: "RB",
        },
        {
          destinationName: "Facebook",
          engagements: "5",
          lastProcessed: "1 week ago",
          updatedBy: "SU",
          addedDate: "Yesterday",
          addedBy: "RB",
        },
        {
          destinationName: "Facebook",
          engagements: "5",
          lastProcessed: "1 week ago",
          updatedBy: "SU",
          addedDate: "Yesterday",
          addedBy: "RB",
        },
      ],
    }
  },
  methods: {
    onFilterSelection: function (index) {
      this.filters[index].name = this.filters[index].selectedValue
    },
  },
}
</script>

<style lang="scss" scoped>
// Will be removed once table integrates filter
.destinations-view-wrap {
  .filters-wrapper {
    ::v-deep .avatar-menu {
      margin-right: 10px;
    }
  }
}
</style>
