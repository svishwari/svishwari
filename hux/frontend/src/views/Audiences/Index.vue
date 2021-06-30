<template>
  <div class="audiences-wrap">
    <PageHeader :headerHeightChanges="'py-3'">
      <template slot="left">
        <Breadcrumb :items="breadcrumbItems" />
      </template>
      <template slot="right">
        <v-icon size="22" color="lightGrey" class="icon-border pa-2 ma-1"
          >mdi-download</v-icon
        >
      </template>
    </PageHeader>
    <PageHeader class="top-bar" :headerHeight="71">
      <template slot="left">
        <v-icon medium color="lightGrey">mdi-filter-variant</v-icon>
        <v-icon medium color="lightGrey" class="pl-6">mdi-magnify</v-icon>
      </template>

      <template slot="right">
        <v-icon medium color="lightGrey refresh">mdi-refresh</v-icon>
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
            isTile
            class="ma-2 font-weight-regular no-shadow mr-0"
          >
            Audience
          </huxButton>
        </router-link>
      </template>
    </PageHeader>
    <v-progress-linear :active="loading" :indeterminate="loading" />
    <v-row class="pt-3 pb-7 pl-3" v-if="!loading">
      <hux-data-table
        :headers="columnDefs"
        :dataItems="audienceList"
        v-if="isDataExists"
      >
        <template #row-item="{ item }">
          <td
            v-for="header in columnDefs"
            :key="header.value"
            :class="{
              'fixed-column': header.fixed,
              'v-data-table__divider': header.fixed,
              'primary--text': header.fixed,
            }"
            :style="{ width: header.width, left: 0 }"
          >
            <div v-if="header.value == 'name'" class="w-100">
              <menu-cell
                :value="item[header.value]"
                :menuOptions="actionItems"
                routeName="AudienceInsight"
                :routeParam="item['id']"
              />
            </div>
            <div v-if="header.value == 'size'">
              <size :value="item[header.value]" />
            </div>
            <div v-if="header.value == 'last_delivered'">
              <time-stamp :value="item[header.value]" />
            </div>
            <div v-if="header.value == 'update_time'">
              <!-- TODO replace with header value -->
              <time-stamp :value="item['create_time']" />
            </div>
            <div v-if="header.value == 'updated_by'">
              <!-- TODO replace with header value -->
              <Avatar :name="item['created_by']" />
            </div>
            <div v-if="header.value == 'create_time'">
              <time-stamp :value="item[header.value]" />
            </div>
            <div v-if="header.value == 'created_by'">
              <Avatar :name="item[header.value]" />
            </div>
          </td>
        </template>
      </hux-data-table>

      <EmptyPage v-if="!isDataExists">
        <template #icon>mdi-alert-circle-outline</template>
        <template #title>Oops! There’s nothing here yet</template>
        <template #subtitle>
          You currently have no audiences created! You can create the
          <br />framework first then complete the details later. <br />Begin by
          selecting the button below.
        </template>
        <template #button>
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
              isTile
              class="ma-2 font-weight-regular"
            >
              Audience
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
import HuxDataTable from "../../components/common/dataTable/HuxDataTable.vue"
import Avatar from "../../components/common/Avatar.vue"
import Size from "../../components/common/huxTable/Size.vue"
import TimeStamp from "../../components/common/huxTable/TimeStamp.vue"
import MenuCell from "../../components/common/huxTable/MenuCell.vue"
export default {
  name: "audiences",
  components: {
    PageHeader,
    Breadcrumb,
    huxButton,
    EmptyPage,
    HuxDataTable,
    Avatar,
    Size,
    TimeStamp,
    MenuCell,
  },
  data() {
    return {
      actionItems: [
        { title: "Favorite" },
        { title: "Export" },
        { title: "Edit" },
        { title: "Duplicate" },
        { title: "Create a lookalike" },
        { title: "Delete" },
      ],
      breadcrumbItems: [
        {
          text: "Audiences",
          disabled: true,
          icon: "audiences",
        },
      ],
      columnDefs: [
        {
          text: "Audience name",
          value: "name",
          width: "331px",
          fixed: true,
          divider: true,
          class: "fixed-header",
        },
        {
          text: "Size",
          value: "size",
          width: "112px",
        },
        {
          text: "Last delivered",
          value: "last_delivered",
          width: "162",
        },
        {
          text: "Last updated",
          value: "update_time",
          width: "154",
        },
        {
          text: "Last updated by",
          value: "updated_by",
          width: "148",
        },
        {
          text: "Created",
          value: "create_time",
          width: "154",
        },
        {
          text: "Created by",
          value: "created_by",
          width: "100%",
        },
      ],
      loading: false,
    }
  },
  computed: {
    ...mapGetters({
      rowData: "audiences/list",
    }),
    audienceList() {
      let audienceValue = this.rowData
      return audienceValue.sort((a, b) =>
        a.name === b.name ? 0 : a.name < b.name ? -1 : 1
      )
    },
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
  .hux-data-table {
    margin-top: 1px;
    table {
      tr {
        td {
          font-size: 14px;
          height: 63px;
        }
      }
    }
  }
  ::v-deep .menu-cell-wrapper :hover .action-icon {
    display: initial;
  }
  .icon-border {
    cursor: default !important;
  }
}
.radio-div {
  margin-top: -11px !important;
}
</style>
