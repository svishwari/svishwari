<template>
  <div class="audiences-wrap white">
    <page-header :header-height-changes="'py-3'">
      <template slot="left">
        <breadcrumb :items="breadcrumbItems" />
      </template>
      <template slot="right">
        <v-icon size="22" color="black lighten-3" class="icon-border pa-2 ma-1"
          >mdi-download</v-icon
        >
      </template>
    </page-header>
    <page-header class="top-bar" :header-height="71">
      <template slot="left">
        <v-icon medium color="black lighten-3">mdi-filter-variant</v-icon>
        <v-icon medium color="black lighten-3" class="pl-6">mdi-magnify</v-icon>
      </template>

      <template slot="right">
        <v-icon medium color="black lighten-3 refresh">mdi-refresh</v-icon>
        <router-link
          :to="{ name: 'AudienceConfiguration' }"
          class="text-decoration-none"
          append
        >
          <huxButton
            icon="mdi-plus"
            icon-position="left"
            variant="primary"
            size="large"
            is-tile
            class="ma-2 font-weight-regular no-shadow mr-0"
          >
            Audience
          </huxButton>
        </router-link>
      </template>
    </page-header>
    <v-progress-linear :active="loading" :indeterminate="loading" />
    <v-row v-if="!loading" class="pt-3 pb-7 pl-3 white">
      <hux-data-table
        v-if="isDataExists"
        :columns="columnDefs"
        :data-items="audienceList"
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
            <div v-if="header.value == 'name'" class="w-100 d-flex">
              <span v-if="item.is_lookalike == true" class="mr-3">
                <tooltip>
                  <template #label-content>
                    <icon
                      type="lookalike"
                      :size="20"
                      color="neroBlack"
                      class="mr-2"
                    />
                  </template>
                  <template #hover-content>Lookalike audience</template>
                </tooltip>
              </span>
              <menu-cell
                :value="item[header.value]"
                :menu-options="getActionItems(item)"
                route-name="AudienceInsight"
                :route-param="item['id']"
              />
            </div>
            <div v-if="header.value == 'status'" class="text-caption">
              <status
                :status="item[header.value]"
                :show-label="true"
                class="d-flex"
                :icon-size="17"
              />
            </div>
            <div v-if="header.value == 'size'">
              <size :value="item[header.value]" />
            </div>
            <div v-if="header.value == 'destinations'">
              <div
                v-if="item[header.value] && item[header.value].length > 0"
                class="d-flex align-center"
              >
                <div class="d-flex align-center">
                  <tooltip
                    v-for="destination in item[header.value]"
                    :key="`${item.id}-${destination.type}`"
                  >
                    <template #label-content>
                      <logo
                        :key="destination.id"
                        class="mr-1"
                        :type="destination.type"
                        :size="18"
                      />
                    </template>
                    <template #hover-content>
                      <span>{{ destination.name }}</span>
                    </template>
                  </tooltip>
                </div>
                <span
                  v-if="item[header.value] && item[header.value].length > 3"
                  class="ml-1"
                >
                  + {{ item[header.value].length - 2 }}
                </span>
              </div>
              <span v-else>—</span>
            </div>
            <div v-if="header.value == 'last_delivered'">
              <time-stamp :value="item[header.value]" />
            </div>
            <div
              v-if="
                header.value == 'update_time' || header.value == 'create_time'
              "
            >
              <time-stamp :value="item[header.value]" />
            </div>
            <div
              v-if="
                header.value == 'updated_by' || header.value == 'created_by'
              "
            >
              <avatar :name="item[header.value]" />
            </div>
          </td>
        </template>
      </hux-data-table>

      <empty-page v-if="!isDataExists">
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
              icon-position="left"
              variant="primary"
              size="large"
              is-tile
              class="ma-2 font-weight-regular"
            >
              Audience
            </huxButton>
          </router-link>
        </template>
      </empty-page>
    </v-row>

    <look-alike-audience
      :toggle="showLookAlikeDrawer"
      :selected-audience="selectedAudience"
      @onToggle="(val) => (showLookAlikeDrawer = val)"
      @onError="onError($event)"
    />

    <hux-alert
      v-model="flashAlert"
      :type="alert.type"
      :message="alert.message"
    />
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"

import PageHeader from "@/components/PageHeader"
import EmptyPage from "@/components/common/EmptyPage"
import Breadcrumb from "@/components/common/Breadcrumb"
import huxButton from "@/components/common/huxButton"
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import Avatar from "@/components/common/Avatar.vue"
import Size from "@/components/common/huxTable/Size.vue"
import TimeStamp from "@/components/common/huxTable/TimeStamp.vue"
import MenuCell from "@/components/common/huxTable/MenuCell.vue"
import LookAlikeAudience from "./Configuration/Drawers/LookAlikeAudience"
import Icon from "@/components/common/Icon.vue"
import Status from "../../components/common/Status.vue"
import Tooltip from "../../components/common/Tooltip.vue"
import Logo from "../../components/common/Logo.vue"
import HuxAlert from "@/components/common/HuxAlert.vue"

export default {
  name: "Audiences",
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
    LookAlikeAudience,
    Icon,
    Status,
    Tooltip,
    Logo,
    HuxAlert,
  },
  data() {
    return {
      flashAlert: false,
      alert: {
        type: "success",
        message: "",
      },
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
          text: "Status",
          value: "status",
          width: "160px",
        },
        {
          text: "Size",
          value: "size",
          width: "112px",
        },
        {
          text: "Destinations",
          value: "destinations",
          width: "150px",
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
      selectedAudience: null,
      showLookAlikeDrawer: false,
    }
  },
  computed: {
    ...mapGetters({
      rowData: "audiences/list",
    }),
    audienceList() {
      let audienceValue = this.rowData
      return audienceValue.sort((a, b) =>
        a.name.toLowerCase() === b.name.toLowerCase()
          ? 0
          : a.name.toLowerCase() < b.name.toLowerCase()
          ? -1
          : 1
      )
    },
    isDataExists() {
      if (this.rowData) return this.rowData.length > 0
      return false
    },
  },
  async mounted() {
    this.loading = true
    await this.getAllAudiences()
    this.loading = false
  },
  methods: {
    ...mapActions({
      getAllAudiences: "audiences/getAll",
    }),

    getActionItems(audience) {
      // This assumes we cannot create a lookalike audience from a lookalike audience
      let isLookalikeableActive =
        audience.lookalikeable === "Active" && !audience.is_lookalike

      let actionItems = [
        { title: "Favorite", isDisabled: true },
        { title: "Export", isDisabled: true },
        { title: "Edit", isDisabled: true },
        { title: "Duplicate", isDisabled: true },
        {
          title: "Create a lookalike",
          isDisabled: !isLookalikeableActive,
          menu: {
            title: "Facebook",
            onClick: () => {
              this.openLookAlikeDrawer(audience)
            },
            icon: "facebook",
          },
        },
        { title: "Delete", isDisabled: true },
      ]

      return actionItems
    },

    openLookAlikeDrawer(audience) {
      this.selectedAudience = audience
      this.showLookAlikeDrawer = true
    },
    onError(message) {
      this.alert.type = "error"
      this.alert.message = message
      this.flashAlert = true
    },
  },
}
</script>
<style lang="scss" scoped>
.audiences-wrap {
  ::v-deep .menu-cell-wrapper .action-icon {
    display: none;
  }
  .page-header--wrap {
    box-shadow: 0px 1px 1px -1px var(--v-black-lighten3),
      0px 1px 1px 0px var(--v-black-lighten3),
      0px 1px 2px 0px var(--v-black-lighten3) !important;
  }
  .top-bar {
    margin-top: 1px;
    .v-icon--disabled {
      color: var(--v-black-lighten3) !important;
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
      tbody {
        tr:last-child {
          td {
            border-bottom: 1px solid var(--v-black-lighten3) !important;
          }
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
