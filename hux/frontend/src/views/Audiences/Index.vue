<template>
  <div class="audiences-wrap white">
    <page-header class="py-5" :header-height="110">
      <template #left>
        <div>
          <breadcrumb :items="breadcrumbItems" />
        </div>
        <div class="text-subtitle-1 font-weight-regular">
          Segment your consumers into audiences based on your consumer data and
          model scores.
        </div>
      </template>
      <template #right>
        <v-btn
          icon
          data-e2e="audienceFilterToggle"
          @click.native="filterToggle()"
        >
          <icon
            type="filter"
            :size="27"
            :color="isFilterToggled > 0 ? 'primary' : 'black'"
            :variant="
              showError
                ? 'lighten3'
                : isFilterToggled > 0
                ? 'lighten6'
                : 'darken4'
            "
          />
          <v-badge
            v-if="finalFilterApplied > 0"
            :content="finalFilterApplied"
            color="white"
            offset-x="6"
            offset-y="4"
            light
            bottom
            overlap
            bordered
          />
        </v-btn>
      </template>
    </page-header>
    <div
      class="d-flex flex-nowrap align-stretch flex-grow-1 flex-shrink-0 mw-100"
    >
      <v-progress-linear
        v-if="loading"
        :active="loading"
        :indeterminate="loading"
      />
      <div
        v-if="!loading && audienceList.length > 0"
        class="flex-grow-1 flex-shrink-1 overflow-hidden mw-100"
      >
        <page-header class="top-bar" :header-height="71">
          <template slot="left">
            <v-btn disabled icon color="black">
              <icon type="search" :size="20" color="black" variant="lighten3" />
            </v-btn>
          </template>

          <template slot="right">
            <span v-if="getAccess('audience', 'create')">
              <router-link
                :to="{ name: 'SegmentPlayground' }"
                class="text-decoration-none"
                append
              >
                <huxButton
                  variant="primary base"
                  size="large"
                  is-tile
                  class="ma-2 font-weight-regular no-shadow mr-0"
                  data-e2e="add-audience"
                >
                  Create an audience
                </huxButton>
              </router-link>
            </span>
          </template>
        </page-header>
        <hux-lazy-data-table
          v-if="!loading && audienceList.length > 0"
          :columns="columnDefs"
          :data-items="audienceList"
          sort-column="update_time"
          sort-desc="false"
          data-e2e="audience-table"
          class="big-table white"
          :enable-lazy-load="enableLazyLoad"
          view-height="calc(100vh - 253px)"
          @bottomScrollEvent="intersected"
        >
          <template #row-item="{ item, index }">
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
                <menu-cell
                  :value="item[header.value]"
                  :menu-options="
                    item.is_lookalike
                      ? getLookalikeActionItems(item)
                      : getActionItems(item)
                  "
                  route-name="AudienceInsight"
                  :route-param="item['id']"
                  data-e2e="audiencename"
                  has-favorite
                  :is-favorite="isUserFavorite(item, 'audiences')"
                  class="text-body-1 name-cell"
                  :show-star="!item.is_lookalike"
                  :nudge-top="audienceList.length - 1 == index ? '70' : ''"
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
              <div v-if="header.value == 'tags' && enableDemoConfig">
                <div
                  v-if="
                    item[header.value] && item[header.value].industry.length > 0
                  "
                  class="d-flex align-center"
                >
                  <div class="d-flex align-center destination-ico">
                    <tooltip
                      v-for="tag in item[header.value].industry"
                      :key="`${item.id}-${tag}`"
                    >
                      <template #label-content>
                        <logo
                          :key="tag"
                          :size="18"
                          class="mr-1"
                          :type="`${tag}_logo`"
                        />
                      </template>
                      <template #hover-content>
                        <span>{{ formatText(tag) }}</span>
                      </template>
                    </tooltip>
                  </div>
                </div>
                <span v-else>—</span>
              </div>
              <div v-if="header.value == 'filters'" class="filter_col">
                <span
                  v-if="
                    item[header.value] == 'null' ||
                    !item[header.value] ||
                    item[header.value].length == 0
                  "
                >
                  —
                </span>
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
        </hux-lazy-data-table>

        <look-alike-audience
          ref="lookalikeWorkflow"
          :toggle="showLookAlikeDrawer"
          :selected-audience="selectedAudience"
          @onToggle="(val) => (showLookAlikeDrawer = val)"
        />
      </div>

      <div
        v-if="!showError && audienceList.length == 0 && !loading"
        class="
          flex-grow-1 flex-shrink-1
          overflow-hidden
          mw-100
          background-empty
        "
      >
        <empty-page type="no-engagement" size="50">
          <template #title>
            <div class="title-no-engagement">No audiences</div>
          </template>
          <template #subtitle>
            <div class="des-no-engagement mt-3">
              <span v-if="finalFilterApplied <= 0">
                Your list of audiences will appear here once you create them.
              </span>
              <span v-else>
                Currently there are no audiences available based on your applied
                filters.
                <br />
                Check back later or change your filters.
              </span>
            </div>
          </template>
          <template #button>
            <span
              v-if="finalFilterApplied <= 0 && getAccess('audience', 'create')"
            >
              <router-link
                :to="{ name: 'SegmentPlayground' }"
                class="text-decoration-none"
                append
                data-e2e="add-audience"
              >
                <huxButton
                  variant="primary base"
                  icon-color="white"
                  icon-variant="base"
                  size="large"
                  class="ma-2 font-weight-regular no-shadow mr-0 caption"
                  is-tile
                  height="40"
                >
                  Create an audience
                </huxButton>
              </router-link>
            </span>
            <span v-else>
              <huxButton
                button-text="Clear filters"
                variant="primary base"
                size="large"
                class="ma-2 font-weight-regular text-button"
                is-tile
                :height="'40'"
                @click="clearFilters()"
              >
                Clear filters
              </huxButton>
            </span>
          </template>
        </empty-page>
      </div>
      <div v-if="showError" class="error-wrap">
        <error
          icon-type="error-on-screens"
          :icon-size="50"
          title="Audiences are currently unavailable"
          subtitle="Our team is working hard to fix it. Please be patient and try again soon!"
        >
        </error>
      </div>

      <div class="ml-auto">
        <audience-filter
          ref="filters"
          v-model="isFilterToggled"
          view-height="calc(100vh - 180px)"
          :filter-options="attributeOptions()"
          :demo-config-selection="enableDemoConfig"
          @selected-filters="totalFiltersSelected"
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

    <confirm-modal
      v-model="confirmEditModal"
      icon="edit"
      type="error"
      title="Edit"
      :sub-title="`${confirmSubtitle}`"
      right-btn-text="Yes, edit"
      left-btn-text="Cancel"
      @onCancel="confirmEditModal = !confirmEditModal"
      @onConfirm="confirmEdit()"
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
          Are you sure you want to edit this audience&#63;
        </div>
        <div
          class="black--text text--darken-4 text-subtitle-1 font-weight-regular"
        >
          By changing this audience, all related engagements must be
          re-delivered.
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
import HuxLazyDataTable from "@/components/common/dataTable/HuxLazyDataTable.vue"
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
import Error from "@/components/common/screens/Error"
import { formatText, getAccess, getIndustryTags } from "@/utils.js"

export default {
  name: "Audiences",
  components: {
    PageHeader,
    Breadcrumb,
    huxButton,
    EmptyPage,
    HuxLazyDataTable,
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
    Error,
  },
  data() {
    return {
      showError: false,
      confirmEditModal: false,
      numFiltersSelected: 0,
      finalFilterApplied: 0,
      breadcrumbItems: [
        {
          text: "Audiences",
          disabled: true,
          icon: "audiences",
        },
      ],
      columnDefs: [
        {
          id: 1,
          text: "Audience name",
          value: "name",
          width: "331px",
          fixed: true,
          divider: true,
        },
        {
          id: 2,
          text: "Status",
          value: "status",
          width: "200px",
        },
        {
          id: 3,
          text: "Size",
          value: "size",
          width: "112px",
          hoverTooltip:
            "Current number of consumers who fit the selected attributes.",
          tooltipWidth: "231px",
        },
        {
          id: 4,
          text: "Industry",
          value: "tags",
          width: "220px",
          sortable: false,
        },
        {
          id: 5,
          text: "Attributes",
          value: "filters",
          width: "380px",
        },
        {
          id: 6,
          text: "Destinations",
          value: "destinations",
          width: "150px",
        },
        {
          id: 6,
          text: "Last delivered",
          value: "last_delivered",
          width: "170",
        },
        {
          id: 7,
          text: "Last updated",
          value: "update_time",
          width: "180",
        },
        {
          id: 8,
          text: "Last updated by",
          value: "updated_by",
          width: "181",
        },
        {
          id: 9,
          text: "Created",
          value: "create_time",
          width: "182",
        },
        {
          id: 10,
          text: "Created by",
          value: "created_by",
          width: "182",
        },
      ],
      industryTags: getIndustryTags(),
      loading: false,
      selectedAudience: null,
      showLookAlikeDrawer: false,
      confirmModal: false,
      confirmSubtitle: "",
      isFilterToggled: false,
      enableLazyLoad: false,
      enableDemoConfig: false,
      lastBatch: 0,
      batchDetails: {},
    }
  },
  computed: {
    ...mapGetters({
      rowData: "audiences/list",
      userFavorites: "users/favorites",
      ruleAttributes: "audiences/audiencesRules",
      totalAudiences: "audiences/total",
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
              let eventObj = this.getEventsOption(obj)
              let nameObj = this.attributeOptions().find((item) =>
                item.key == obj.field ? obj.field.toLowerCase() : null
              )
              if (nameObj) {
                filterTagsObj[audience.name].add(nameObj.name)
              }
              if (eventObj) {
                filterTagsObj[audience.name].add(eventObj.name)
              }
            })
          })
        }
      })
      return filterTagsObj
    },
  },
  async mounted() {
    this.loading = true
    this.enableDemoConfig = getAccess("client_config", "client_settings")
    if (!this.enableDemoConfig) {
      this.columnDefs = this.columnDefs.filter((ele) => ele.value != "tags")
    }
    try {
      this.setDefaultBatch()
      await this.fetchAudienceByBatch()
      await this.getAudiencesRules()
      this.calculateLastBatch()
    } catch (error) {
      this.showError = true
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
      getAudiencesRules: "audiences/fetchConstants",
    }),

    setDefaultBatch() {
      this.batchDetails.batch_size = 25
      this.batchDetails.batch_number = 1
      this.batchDetails.isLazyLoad = false
      this.batchDetails.lookalikeable = false
      this.batchDetails.favorites = false
      this.batchDetails.worked_by = false
      this.batchDetails.attribute = []
      this.batchDetails.events = []
      this.batchDetails.tags = []
      this.batchDetails.deliveries = 2
    },
    getEventsOption(filters) {
      let eventObj = {}
      if (filters.field == "event") {
        eventObj.name = formatText(filters.value[0].value)
        return eventObj
      } else return undefined
    },
    intersected() {
      if (this.batchDetails.batch_number <= this.lastBatch) {
        this.batchDetails.isLazyLoad = true
        this.enableLazyLoad = true
        this.fetchAudienceByBatch()
      } else {
        this.enableLazyLoad = false
      }
    },
    async fetchAudienceByBatch() {
      await this.getAllAudiences(this.batchDetails)
      this.batchDetails.batch_number++
    },
    calculateLastBatch() {
      this.lastBatch = Math.ceil(
        this.totalAudiences / this.batchDetails.batch_size
      )
    },

    async confirmEdit() {
      this.confirmEditModal = false
      this.$router.push({
        name: "AudienceUpdate",
        params: { id: this.selectedAudience.id },
      })
    },

    totalFiltersSelected(value) {
      this.numFiltersSelected = value
    },
    clearFilters() {
      this.$refs.filters.clear()
    },
    initiateClone(audienceId) {
      this.$router.push({
        name: "CloneAudience",
        params: { id: audienceId },
      })
      //CloneAudience
    },
    attributeOptions() {
      const options = []
      if (this.ruleAttributes && this.ruleAttributes.rule_attributes) {
        Object.entries(this.ruleAttributes.rule_attributes).forEach((attr) => {
          Object.keys(attr[1]).forEach((optionKey) => {
            if (
              Object.values(attr[1][optionKey])
                .map((o) => typeof o === "object" && !Array.isArray(o))
                .includes(Boolean(true))
            ) {
              Object.keys(attr[1][optionKey]).forEach((att) => {
                if (typeof attr[1][optionKey][att] === "object") {
                  options.push({
                    key: att,
                    name: attr[1][optionKey][att]["name"],
                    category: attr[0],
                    optionName: attr[1][optionKey].name,
                  })
                }
              })
            } else {
              options.push({
                key: optionKey,
                name: attr[1][optionKey]["name"],
                category: attr[0],
                optionName: attr[1][optionKey].name,
              })
            }
          })
        })

        for (let tags of this.industryTags) {
          options.push({
            key: tags,
            name: formatText(tags),
            category: "industry",
            optionName: "Tags",
          })
        }
      }
      return options
    },

    isUserFavorite(entity, type) {
      return (
        this.userFavorites &&
        this.userFavorites[type] &&
        this.userFavorites[type].includes(entity.id)
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
      let destinationMenu = []
      if (audience.destinations.length !== 0) {
        audience.destinations.forEach((element) => {
          destinationMenu.push({
            title: element.name,
            isDisabled: false,
            onClick: () => {
              window.open("https://" + element.link)
            },
            icon: element.type,
          })
        })
      }
      //In Future
      // let isLookalikeableActive =
      //   audience.lookalikeable === "Active" && !audience.is_lookalike
      let isFavorite = this.isUserFavorite(audience, "audiences")
      let actionItems = [
        {
          title: isFavorite ? "Unfavorite" : "Favorite",
          isDisabled: false,
          onClick: () => {
            this.handleActionFavorite(audience, "audiences")
          },
        },
        {
          title: "Edit audience",
          isDisabled: false,
          isHidden: !this.getAccess("audience", "update_one"),
          onClick: () => {
            this.openEditModal(audience)
          },
        },
        {
          title: "Clone audience",
          isDisabled: false,
          isHidden: !this.getAccess("audience", "create"),
          onClick: () => {
            this.initiateClone(audience.id)
          },
        },
        {
          title: "Open destination",
          isDisabled: audience.destinations.length !== 0 ? false : true,
          menu: destinationMenu,
        },
        {
          title: "Delete audience",
          isDisabled: false,
          isHidden: !this.getAccess("audience", "delete_one"),
          onClick: () => {
            this.openModal(audience)
          },
        },
      ]

      return actionItems
    },
    getLookalikeActionItems(audience) {
      let isFavorite = this.isUserFavorite(audience, "audiences")
      let actionItems = [
        {
          title: isFavorite ? "Unfavorite" : "Favorite",
          isDisabled: false,
          onClick: () => {
            this.handleActionFavorite(audience, "audiences")
          },
        },
        {
          title: "Open Facebook",
          isDisabled: false,
          onClick: () => {
            window.open("https://www.facebook.com", "_blank")
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
    openEditModal(audience) {
      this.selectedAudience = audience
      this.confirmSubtitle = audience.name
      this.confirmEditModal = true
    },
    openLookAlikeDrawer(audience) {
      this.selectedAudience = audience
      this.showLookAlikeDrawer = true
    },

    filterToggle() {
      if (!this.showError) {
        this.isFilterToggled = !this.isFilterToggled
      }
    },

    async applyFilter(params) {
      this.loading = true
      this.finalFilterApplied = params.filterApplied
      this.setDefaultBatch()
      this.batchDetails.favorites = params.selectedFavourite
      this.batchDetails.worked_by = params.selectedAudienceWorkedWith
      this.batchDetails.attribute = params.selectedAttributes
      this.batchDetails.events = params.selectedEvents
      this.batchDetails.tags = params.selectedTags
      await this.fetchAudienceByBatch()
      this.calculateLastBatch()
      this.loading = false
    },
    formatText: formatText,
    getAccess: getAccess,
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

.background-empty {
  height: 60vh !important;
  background-image: url("../../assets/images/no-alert-frame.png");
  background-position: center;
  background-size: 96% 86%;
}

//to overwrite the classes

.title-no-engagement {
  font-size: 24px !important;
  line-height: 34px !important;
  font-weight: 300 !important;
  letter-spacing: 0 !important;
  color: var(--v-black-base);
}

.des-no-engagement {
  font-size: 14px !important;
  line-height: 16px !important;
  font-weight: 400 !important;
  letter-spacing: 0 !important;
  color: var(--v-black-base);
}

::v-deep .empty-page {
  max-height: 0 !important;
  min-height: 100% !important;
  min-width: 100% !important;
}

.name-cell {
  margin-bottom: -15px !important;
}
</style>
