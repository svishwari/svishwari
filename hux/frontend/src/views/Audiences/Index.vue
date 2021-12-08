<template>
  <div class="audiences-wrap white">
    <page-header class="py-5" :header-height="110">
      <template #left>
        <div>
          <breadcrumb :items="breadcrumbItems" />
        </div>
        <div class="text-subtitle-1 font-weight-regular">
          Segment your customers into audiences based on your customer data and
          model scores.
        </div>
      </template>
      <template #right>
        <icon
          type="filter"
          :size="22"
          class="cursor-pointer"
          color="black-darken4"
          @click.native="isFilterToggled = !isFilterToggled"
        />
      </template>
    </page-header>
    <div
      class="d-flex flex-nowrap align-stretch flex-grow-1 flex-shrink-0 mw-100"
    >
      <div class="flex-grow-1 flex-shrink-1 overflow-hidden mw-100">
        <page-header class="top-bar" :header-height="71">
          <template slot="left">
            <v-btn disabled icon color="black">
              <icon type="search" :size="20" color="black" variant="lighten3" />
            </v-btn>
          </template>

          <template slot="right">
            <router-link
              :to="{ name: 'AudienceConfiguration' }"
              class="text-decoration-none"
              append
            >
              <huxButton
                variant="primary base"
                icon-color="white"
                icon-variant="base"
                icon="plus"
                size="large"
                is-custom-icon
                is-tile
                class="ma-2 font-weight-regular no-shadow mr-0"
              >
                Audience
              </huxButton>
            </router-link>
          </template>
        </page-header>
        <v-progress-linear
          :active="loading"
          :indeterminate="loading"
          class="tab-min-width"
        />
        <div v-if="!loading" class="white">
          <hux-data-table
            v-if="isDataExists"
            :columns="columnDefs"
            :data-items="audienceList"
            view-height="calc(100vh - 210px)"
            sort-column="update_time"
            sort-desc="false"
            data-e2e="audience-table"
            class="big-table"
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
                :style="{ minWidth: header.width, left: 0 }"
              >
                <div
                  v-if="header.value == 'name'"
                  class="w-100 d-flex"
                  data-e2e="audiencelist"
                >
                  <span v-if="item.is_lookalike == true" class="mr-3">
                    <tooltip>
                      <template #label-content>
                        <icon type="lookalike" :size="20" class="mr-2" />
                      </template>
                      <template #hover-content>Lookalike audience</template>
                    </tooltip>
                  </span>
                  <menu-cell
                    :value="item[header.value]"
                    :menu-options="getActionItems(item)"
                    route-name="AudienceInsight"
                    :route-param="item['id']"
                    data-e2e="audiencename"
                    has-favorite
                    :is-favorite="isUserFavorite(item, 'audiences')"
                    class="text-body-1"
                    @actionFavorite="handleActionFavorite(item, 'audiences')"
                  />
                </div>
                <div v-if="header.value == 'status'">
                  <status
                    :status="item[header.value]"
                    :show-label="true"
                    class="d-flex"
                    :icon-size="18"
                  />
                </div>
                <div v-if="header.value == 'size'">
                  <size :value="item[header.value]" />
                </div>
                <div
                  v-if="header.value == 'filters' && item[header.value]"
                  class="filter_col"
                >
                  <span v-if="item[header.value] === 'null'">—</span>
                  <span v-else>
                    <span
                      v-for="(filter, filterIndex) in filterTags[item.name]"
                      :key="filterIndex"
                    >
                      <v-chip
                        v-if="filterIndex < 4"
                        small
                        class="mr-1 ml-0 mt-0 mb-1 text-subtitle-2"
                        text-color="primary"
                        color="var(--v-primary-lighten3)"
                      >
                        {{ formatText(filter) }}
                      </v-chip>
                    </span>
                    <tooltip>
                      <template #label-content>
                        <span
                          v-if="filterTags[item.name].size > 4"
                          class="text-subtitle-2 primary--text"
                        >
                          +{{ filterTags[item.name].size - 4 }}
                        </span>
                      </template>
                      <template #hover-content>
                        <span
                          v-for="(filter, filterIndex) in filterTags[item.name]"
                          :key="filterIndex"
                        >
                          <v-chip
                            v-if="filterIndex >= 4"
                            small
                            class="mr-1 ml-0 mt-0 mb-1 text-subtitle-2"
                            text-color="primary"
                            color="var(--v-primary-lighten3)"
                          >
                            {{ formatText(filter) }}
                          </v-chip>
                          <br v-if="filterIndex >= 4" />
                        </span>
                      </template>
                    </tooltip>
                  </span>
                </div>
                <div v-if="header.value == 'destinations'">
                  <div
                    v-if="item[header.value] && item[header.value].length > 0"
                    class="d-flex align-center"
                  >
                    <div class="d-flex align-center destination-ico">
                      <tooltip
                        v-for="destination in getOverallDestinations(
                          item[header.value]
                        )"
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
                      class="ml-1 text-body-1 black--text"
                    >
                      <tooltip>
                        <template #label-content>
                          +{{ item[header.value].length - 3 }}
                        </template>
                        <template #hover-content>
                          <div class="d-flex flex-column">
                            <div
                              v-for="extraDestination in getExtraDestinations(
                                item[header.value]
                              )"
                              :key="extraDestination.id"
                              class="d-flex align-center py-2"
                            >
                              <logo
                                :key="extraDestination.id"
                                class="mr-4"
                                :type="extraDestination.type"
                                :size="18"
                              />
                              <span>{{ extraDestination.name }}</span>
                            </div>
                          </div>
                        </template>
                      </tooltip>
                    </span>
                  </div>
                  <span v-else>—</span>
                </div>
                <div v-if="header.value == 'last_delivered'">
                  <tooltip>
                    <template #label-content>
                      {{ item[header.value] | Date("relative") | Empty }}
                    </template>
                    <template #hover-content>
                      <div>
                        <div class="neroBlack--text text-body-2 mb-2">
                          Delivered to:
                        </div>
                        <div
                          v-for="deliveries in item['deliveries']"
                          :key="deliveries.last_delivered"
                          class="mb-2"
                        >
                          <div class="d-flex align-center mb-1">
                            <logo
                              :type="deliveries.delivery_platform_type"
                              :size="18"
                            />
                            <span class="ml-1 neroBlack--text text-body-2">
                              {{ deliveries.delivery_platform_name }}
                            </span>
                          </div>
                          <div class="neroBlack--text text-body-2">
                            {{ deliveries.last_delivered | Date | Empty }}
                          </div>
                        </div>
                      </div>
                    </template>
                  </tooltip>
                </div>
                <div
                  v-if="
                    header.value == 'update_time' ||
                    header.value == 'create_time'
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
          <empty-page v-if="!isDataExists" type="no-audience" size="50">
            <template #title>Oops! There’s nothing here yet</template>
            <template #subtitle>
              You currently have no audiences created! You can create the
              <br />framework first then complete the details later. <br />Begin
              by selecting the button below.
            </template>
            <template #button>
              <router-link
                :to="{ name: 'AudienceConfiguration' }"
                class="route-link text-decoration-none"
                append
              >
                <huxButton
                  variant="primary base"
                  icon-color="white"
                  icon-variant="base"
                  icon="plus"
                  size="large"
                  is-custom-icon
                  is-tile
                  class="ma-2 font-weight-regular caption"
                >
                  Audience
                </huxButton>
              </router-link>
            </template>
          </empty-page>
        </div>

        <look-alike-audience
          ref="lookalikeWorkflow"
          :toggle="showLookAlikeDrawer"
          :selected-audience="selectedAudience"
          @onToggle="(val) => (showLookAlikeDrawer = val)"
        />
      </div>
      <div class="ml-auto">
        <audience-filter
          v-model="isFilterToggled"
          @onSectionAction="applyFilter"
        />
      </div>
    </div>

    <confirm-modal
      v-model="confirmModal"
      icon="sad-face"
      type="error"
      title="You are about to delete"
      :sub-title="`${confirmSubtitle}`"
      right-btn-text="Yes, delete it"
      left-btn-text="Nevermind!"
      data-e2e="remove-audience-confirmation"
      @onCancel="confirmModal = !confirmModal"
      @onConfirm="confirmRemoval()"
    >
      <template #body>
        <div
          class="
            black--text
            text--darken-4 text-subtitle-1
            pt-6
            font-weight-regular
          "
        >
          Are you sure you want to delete this audience&#63;
        </div>
        <div
          class="black--text text--darken-4 text-subtitle-1 font-weight-regular"
        >
          By deleting this audience you will not be able to recover it and it
          may impact any associated engagements.
        </div>
      </template>
    </confirm-modal>
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
import ConfirmModal from "@/components/common/ConfirmModal"
import AudienceFilter from "./Configuration/Drawers/AudienceFilter"
import { formatText } from "@/utils.js"

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
    ConfirmModal,
    AudienceFilter,
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
          text: "Audience name",
          value: "name",
          width: "331px",
          fixed: true,
          divider: true,
        },
        {
          text: "Status",
          value: "status",
          width: "200px",
        },
        {
          text: "Size",
          value: "size",
          width: "112px",
          hoverTooltip:
            "Current number of customers who fit the selected attributes.",
        },
        {
          text: "Attributes",
          value: "filters",
          width: "300px",
        },
        {
          text: "Destinations",
          value: "destinations",
          width: "150px",
        },
        {
          text: "Last delivered",
          value: "last_delivered",
          width: "170",
        },
        {
          text: "Last updated",
          value: "update_time",
          width: "180",
        },
        {
          text: "Last updated by",
          value: "updated_by",
          width: "181",
        },
        {
          text: "Created",
          value: "create_time",
          width: "182",
        },
        {
          text: "Created by",
          value: "created_by",
          width: "182",
        },
      ],
      loading: false,
      selectedAudience: null,
      showLookAlikeDrawer: false,
      confirmModal: false,
      confirmSubtitle: "",
      isFilterToggled: false,
    }
  },
  computed: {
    ...mapGetters({
      rowData: "audiences/list",
      userFavorites: "users/favorites",
    }),
    audienceList() {
      let audienceValue = JSON.parse(JSON.stringify(this.rowData))
      audienceValue.forEach((audience) => {
        if (!("filters" in audience)) {
          audience["filters"] = "null"
        }
      })
      audienceValue.forEach((audience) => {
        audience.destinations.sort((a, b) => a.name.localeCompare(b.name))
      })
      return audienceValue
    },
    isDataExists() {
      if (this.rowData) return this.rowData.length > 0
      return false
    },
    filterTags() {
      let filterTagsObj = {}
      let audienceValue = JSON.parse(JSON.stringify(this.rowData))
      audienceValue.forEach((audience) => {
        if (audience.filters) {
          filterTagsObj[audience.name] = new Set()
          audience.filters.forEach((item) => {
            item.section_filters.forEach((obj) => {
              filterTagsObj[audience.name].add(obj.field)
            })
          })
        }
      })
      return filterTagsObj
    },
  },
  async mounted() {
    this.loading = true
    try {
      await this.getAllAudiences({})
    } finally {
      this.loading = false
    }
  },
  methods: {
    ...mapActions({
      getAllAudiences: "audiences/getAll",
      markFavorite: "users/markFavorite",
      clearFavorite: "users/clearFavorite",
      deleteAudience: "audiences/remove",
    }),

    isUserFavorite(entity, type) {
      return (
        this.userFavorites[type] && this.userFavorites[type].includes(entity.id)
      )
    },
    handleActionFavorite(item, type) {
      if (!this.isUserFavorite(item, type)) {
        this.markFavorite({ id: item.id, type: type })
      } else {
        this.clearFavorite({ id: item.id, type: type })
      }
    },
    openModal(audience) {
      this.selectedAudience = audience
      this.confirmSubtitle = audience.name
      this.confirmModal = true
    },
    async confirmRemoval() {
      await this.deleteAudience({ id: this.selectedAudience.id })
      this.confirmModal = false
    },
    getActionItems(audience) {
      // This assumes we cannot create a lookalike audience from a lookalike audience
      let isLookalikeableActive =
        audience.lookalikeable === "Active" && !audience.is_lookalike
      let isFavorite = this.isUserFavorite(audience, "audiences")
      let actionItems = [
        {
          title: isFavorite ? "Unfavorite" : "Favorite",
          isDisabled: false,
          onClick: () => {
            this.handleActionFavorite(audience, "audiences")
          },
        },
        { title: "Export", isDisabled: true },
        {
          title: "Edit audience",
          isDisabled: false,
          onClick: () => {
            this.editAudience(audience.id)
          },
        },
        { title: "Duplicate", isDisabled: true },
        {
          title: "Create a lookalike",
          isDisabled: !isLookalikeableActive,
          menu: {
            title: "Facebook",
            onClick: () => {
              this.$refs.lookalikeWorkflow.prefetchLookalikeDependencies()
              this.openLookAlikeDrawer(audience)
            },
            icon: "facebook",
          },
        },
        {
          title: "Delete audience",
          isDisabled: false,
          onClick: () => {
            this.openModal(audience)
          },
        },
      ]

      return actionItems
    },
    getOverallDestinations(audienceDestinations) {
      let destinations = [...audienceDestinations]
      if (destinations.length > 3) {
        return destinations
          .slice(0, 3)
          .sort((a, b) => a.name.localeCompare(b.name))
      }
      return destinations.sort((a, b) => a.name.localeCompare(b.name))
    },
    getExtraDestinations(audienceDestinations) {
      let destinations = [...audienceDestinations]
      if (destinations.length > 3) {
        return destinations
          .slice(3)
          .sort((a, b) => a.name.localeCompare(b.name))
      }
      return destinations.sort((a, b) => a.name.localeCompare(b.name))
    },
    editAudience(id) {
      this.$router.push({
        name: "AudienceUpdate",
        params: { id: id },
      })
    },

    openLookAlikeDrawer(audience) {
      this.selectedAudience = audience
      this.showLookAlikeDrawer = true
    },

    async applyFilter(params) {
      await this.getAllAudiences({
        favorites: params.selectedFavourite,
        worked_by: params.selectedAudienceWorkedWith,
        attribute: params.selectedAttributes,
      })
      this.isFilterToggled = false
    },
    formatText: formatText,
  },
}
</script>
<style lang="scss" scoped>
.audiences-wrap {
  ::v-deep .menu-cell-wrapper .action-icon {
    .fav-action {
      display: none;
    }
    .more-action {
      display: none;
    }
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
  // This CSS is to avoid conflict with Tooltip component.
  ::v-deep .destination-ico {
    span {
      display: flex;
      align-items: center;
    }
  }
  .hux-data-table {
    margin-top: 1px;
    ::v-deep table {
      .v-data-table-header {
        th:nth-child(1) {
          position: sticky;
          left: 0;
          z-index: 3;
          border-right: thin solid rgba(0, 0, 0, 0.12);
          overflow-y: visible;
          overflow-x: visible;
        }
        border-radius: 12px 12px 0px 0px;
      }
      tr {
        td:nth-child(1) {
          position: sticky;
          left: 0;
          border-right: thin solid rgba(0, 0, 0, 0.12);
        }
        &:hover {
          td:nth-child(1) {
            z-index: 1 !important;
            background: var(--v-primary-lighten2) !important;
            box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25) !important;
            .menu-cell-wrapper .action-icon {
              .fav-action {
                display: block;
              }
              .more-action {
                display: block;
              }
            }
          }
          background: var(--v-primary-lighten2) !important;
          box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25) !important;
          td.fixed-column {
            z-index: 2 !important;
            background: var(--v-primary-lighten2) !important;
            box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25) !important;
          }
        }
        td.fixed-column {
          z-index: 1 !important;
          box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25) !important;
          &:hover {
            z-index: 2 !important;
            background: var(--v-primary-lighten2) !important;
            box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25) !important;
          }
        }
      }
    }

    table {
      tr {
        td {
          font-size: 16px;
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
  .v-chip.v-size--small {
    height: 20px;
  }
}
.radio-div {
  margin-top: -11px !important;
}
.filter_col {
  height: 59px !important;
  overflow: auto;
  display: table-cell;
  vertical-align: middle;
}
</style>
