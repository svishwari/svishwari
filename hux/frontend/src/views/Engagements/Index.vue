<template>
  <div class="engagements-wrap white">
    <page-header class="py-5" :header-height="110">
      <template #left>
        <div>
          <breadcrumb :items="breadcrumbItems" />
        </div>
        <div class="text-subtitle-1 font-weight-regular">
          Start making meaningful connections with current and future consumers
          by targeting intelligent audiences while staying organized.
        </div>
      </template>
      <template #right>
        <v-btn icon @click.native="filterToggle()">
          <icon
            type="filter"
            :size="27"
            :color="
              isEmptyError ? 'black' : isFilterToggled ? 'primary' : 'black'
            "
            :variant="
              isEmptyError
                ? 'lighten3'
                : isFilterToggled
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
        v-if="!loading && rowData.length > 0"
        class="flex-grow-1 flex-shrink-1 overflow-hidden mw-100"
      >
        <page-header class="top-bar" :header-height="71">
          <template #left>
            <v-btn disabled icon color="black">
              <icon type="search" :size="20" color="black" variant="lighten3" />
            </v-btn>
          </template>

          <template #right>
            <router-link
              v-if="getAccess('engagements', 'create_one')"
              :disabled="isEmptyError"
              :event="!isEmptyError ? 'click' : ''"
              :to="{ name: 'EngagementConfiguration' }"
              class="text-decoration-none"
              append
              data-e2e="add-engagement"
            >
              <huxButton
                variant="primary base"
                size="large"
                is-custom-icon
                class="ma-2 font-weight-regular no-shadow mr-0 caption"
                is-tile
                :is-disabled="isEmptyError"
                height="40"
              >
                Create engagement
              </huxButton>
            </router-link>
          </template>
        </page-header>
        <hux-lazy-data-table
          v-if="!loading && rowData.length > 0"
          :columns="columnDefs"
          :data-items="rowData"
          view-height="calc(100vh - 253px)"
          sort-column="update_time"
          sort-desc="false"
          nested
          data-e2e="engagement-table"
          class="big-table"
          :enable-lazy-load="enableLazyLoad"
          @bottomScrollEvent="intersected"
        >
          <template #item-row="{ item, expandFunc, isExpanded }">
            <tr :class="{ 'expanded-row': isExpanded }">
              <td
                v-for="header in columnDefs"
                :key="header.value"
                :class="{
                  'fixed-column': header.fixed,
                  'v-data-table__divider': header.fixed,
                  'primary--text': header.fixed,
                  'expanded-row': isExpanded,
                  'pl-3': header.value == 'audiences',
                }"
                :style="{ width: header.width }"
              >
                <div v-if="header.value == 'name'" class="w-80">
                  <menu-cell
                    :value="item[header.value]"
                    :menu-options="getActionItems(item)"
                    route-name="EngagementDashboard"
                    :route-param="item['id']"
                    :data="item"
                    :data-e2e="setEngagementSelector(item)"
                    has-favorite
                    :is-favorite="isUserFavorite(item, 'engagements')"
                    class="text-body-1"
                    @actionFavorite="handleActionFavorite(item, 'engagements')"
                  >
                    <template #expand-icon>
                      <span
                        v-if="item.audiences.length > 0"
                        data-e2e="expand-engagement"
                        @click="expandFunc(!isExpanded)"
                      >
                        <icon
                          type="expand-arrow"
                          :size="14"
                          color="primary"
                          class="
                            cursor-pointer
                            mdi-chevron-right
                            mx-2
                            d-inline-block
                          "
                          :class="{ 'normal-icon': isExpanded }"
                        />
                      </span>
                    </template>
                  </menu-cell>
                </div>
                <div v-if="header.value == 'audiences'">
                  {{ item[header.value].length }}
                </div>
                <div
                  v-if="header.value == 'destinations'"
                  class="d-flex align-center"
                >
                  <div class="d-flex align-center destination-ico">
                    <tooltip
                      v-for="destination in getOverallDestinations(
                        item[header.value]
                      )"
                      :key="destination.id"
                    >
                      <template #label-content>
                        <logo
                          class="mr-1"
                          :type="destination.delivery_platform_type"
                          :size="24"
                        />
                      </template>
                      <template #hover-content>
                        <span>{{ destination.name }}</span>
                      </template>
                    </tooltip>
                  </div>
                  <span v-if="item[header.value].length > 3" class="ml-1">
                    <tooltip>
                      <template #label-content>
                        + {{ item[header.value].length - 3 }}
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
                              :type="extraDestination.delivery_platform_type"
                              :size="18"
                            />
                            <span>{{ extraDestination.name }}</span>
                          </div>
                        </div>
                      </template>
                    </tooltip>
                  </span>
                  <span v-else-if="item[header.value].length == 0">—</span>
                </div>
                <div v-if="header.value == 'status'">
                  <status
                    :status="item[header.value]"
                    :show-label="true"
                    class="d-flex"
                    :icon-size="17"
                  />
                </div>
                <div v-if="header.value == 'last_delivered'">
                  <tooltip>
                    <template #label-content>
                      {{ item[header.value] | Date("relative") | Empty }}
                    </template>
                    <template #hover-content>
                      <div v-if="item[header.value] !== ''">
                        <div class="neroBlack--text text-body-2 mb-2">
                          Delivered to:
                        </div>
                        <div
                          v-for="destination in item['destinations']"
                          :key="destination.id"
                          class="mb-2"
                        >
                          <div class="d-flex align-center mb-1">
                            <logo
                              :type="destination.delivery_platform_type"
                              :size="18"
                            />
                            <span class="ml-1 neroBlack--text text-body-2">
                              {{ destination.name }}
                            </span>
                          </div>
                          <div class="neroBlack--text text-body-2">
                            {{
                              destination.latest_delivery
                                ? destination.latest_delivery.update_time
                                : "" | Date | Empty
                            }}
                          </div>
                        </div>
                      </div>
                      <div v-else>—</div>
                    </template>
                  </tooltip>
                </div>
                <div v-if="header.value == 'delivery_schedule'">
                  <tooltip :max-width="280">
                    <template #label-content>
                      {{ item[header.value] | DeliverySchedule }}
                    </template>
                    <template #hover-content>
                      <span
                        v-if="!item[header.value] || item[header.value] === {}"
                      >
                        This engagement was delivered manually on
                        {{
                          item["last_delivered"]
                            | Date("MMMM D, YYYY [at] h:mm A")
                            | Empty
                        }}
                      </span>
                      <hux-delivery-text
                        v-else
                        class="text-body-2"
                        :schedule="
                          item[header.value] ? item[header.value].schedule : {}
                        "
                        :start-date="
                          item[header.value]
                            ? item[header.value].start_date
                            : ''
                        "
                        :end-date="
                          item[header.value] ? item[header.value].end_date : ''
                        "
                      />
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
            </tr>
          </template>
          <template #expanded-row="{ expandedHeaders, parentItem }">
            <td
              v-if="parentItem.audiences.length > 0"
              :colspan="expandedHeaders.length"
              class="pa-0 child"
            >
              <hux-data-table
                v-if="parentItem.audiences.length > 0"
                :columns="expandedHeaders"
                :data-items="parentItem.audiences"
                :show-header="false"
                class="expanded-table big-table"
                view-height="auto"
                nested
                data-e2e="audience-table"
              >
                <template #item-row="{ item, expandFunc, isExpanded }">
                  <tr :class="{ 'expanded-row': isExpanded }">
                    <td
                      :style="{ width: expandedHeaders[0].width }"
                      class="expanded-row-cover"
                    ></td>
                    <td
                      v-for="header in getAudienceHeaders(subHeaders)"
                      :key="header.value"
                      :class="{
                        'child-row pl-1': header.value == 'name',
                      }"
                      :style="{ width: header.width }"
                    >
                      <div v-if="header.value == 'name'">
                        <menu-cell
                          :value="item[header.value]"
                          route-name="AudienceInsight"
                          :route-param="item['id']"
                          :data="item"
                          :label-class="{
                            'no-expand': item.destinations.length == 0,
                          }"
                          class="text-body-1"
                        >
                          <template #expand-icon>
                            <span
                              v-if="item.destinations.length > 0"
                              data-e2e="expand-audience"
                              @click="expandFunc(!isExpanded)"
                            >
                              <icon
                                type="expand-arrow"
                                :size="14"
                                color="primary"
                                class="
                                  cursor-pointer
                                  mdi-chevron-right
                                  mx-2
                                  d-inline-block
                                "
                                :class="{ 'normal-icon': isExpanded }"
                              />
                            </span>
                          </template>
                        </menu-cell>
                      </div>
                      <div v-if="header.value == 'status'">
                        <div>
                          <status
                            :status="item[header.value]"
                            :show-label="true"
                            class="d-flex"
                            :icon-size="17"
                          />
                        </div>
                      </div>
                      <div
                        v-if="header.value == 'destinations'"
                        class="d-flex align-center"
                      >
                        <div class="d-flex align-center destination-ico">
                          <tooltip
                            v-for="destination in getOverallDestinations(
                              item[header.value]
                            )"
                            :key="destination.id"
                          >
                            <template #label-content>
                              <logo
                                class="mr-1"
                                :type="destination.delivery_platform_type"
                                :size="18"
                              />
                            </template>
                            <template #hover-content>
                              <span>{{ destination.name }}</span>
                            </template>
                          </tooltip>
                        </div>
                        <span v-if="item[header.value].length > 3" class="ml-1">
                          <tooltip>
                            <template #label-content>
                              + {{ item[header.value].length - 3 }}
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
                                    :type="
                                      extraDestination.delivery_platform_type
                                    "
                                    :size="18"
                                  />
                                  <span>{{ extraDestination.name }}</span>
                                </div>
                              </div>
                            </template>
                          </tooltip>
                        </span>
                        <span v-else-if="item[header.value].length == 0"
                          >—</span
                        >
                      </div>
                      <div v-if="header.value == 'last_delivered'">
                        <tooltip>
                          <template #label-content>
                            <span data-e2e="last-delivered">
                              {{
                                item[header.value] | Date("relative") | Empty
                              }}
                            </span>
                          </template>
                          <template #hover-content>
                            <div>
                              <div class="neroBlack--text text-body-2 mb-2">
                                Delivered to:
                              </div>
                              <div
                                v-for="destination in item['destinations']"
                                :key="destination.id"
                                class="mb-2"
                              >
                                <div class="d-flex align-center mb-1">
                                  <logo
                                    :type="destination.delivery_platform_type"
                                    :size="18"
                                  />
                                  <span
                                    class="ml-1 neroBlack--text text-body-2"
                                  >
                                    {{ destination.name }}
                                  </span>
                                </div>
                                <div class="neroBlack--text text-body-2">
                                  {{
                                    destination.latest_delivery.update_time
                                      | Date
                                      | Empty
                                  }}
                                </div>
                              </div>
                            </div>
                          </template>
                        </tooltip>
                      </div>
                      <div v-if="header.value == 'delivery_schedule'">
                        <tooltip :max-width="280">
                          <template #label-content>
                            {{ item[header.value] | DeliverySchedule }}
                          </template>
                          <template #hover-content>
                            <span
                              v-if="
                                deliveryScheduleNullCheck(item[header.value])
                              "
                            >
                              This audience was delivered manually on
                              {{
                                item["last_delivered"]
                                  | Date("MMMM D, YYYY [at] h:mm A")
                                  | Empty
                              }}
                            </span>
                            <hux-delivery-text
                              v-else
                              class="text-body-2"
                              :schedule="
                                item[header.value]
                                  ? item[header.value].schedule
                                  : {}
                              "
                              :start-date="
                                item[header.value]
                                  ? item[header.value].start_date
                                  : ''
                              "
                              :end-date="
                                item[header.value]
                                  ? item[header.value].end_date
                                  : ''
                              "
                            />
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
                          header.value == 'updated_by' ||
                          header.value == 'created_by'
                        "
                      >
                        <avatar :name="item[header.value]" />
                      </div>
                    </td>
                  </tr>
                </template>
                <!-- eslint-disable vue/no-template-shadow -->
                <template #expanded-row="{ expandedHeaders, parentItem }">
                  <td
                    v-if="parentItem.destinations.length > 0"
                    :colspan="expandedHeaders.length"
                    class="pa-0 child"
                  >
                    <hux-data-table
                      v-if="parentItem"
                      :columns="expandedHeaders"
                      :data-items="getDestinations(parentItem)"
                      :show-header="false"
                      view-height="auto"
                      class="big-table"
                    >
                      <template #row-item="{ item }">
                        <td
                          v-for="header in columnDefs"
                          :key="header.value"
                          :style="{ width: header.width }"
                        >
                          <div v-if="header.value == 'status'">
                            <div>
                              <status
                                :status="item[header.value]"
                                :show-label="true"
                                class="d-flex"
                                :icon-size="17"
                              />
                            </div>
                          </div>
                          <div v-if="header.value == 'destinations'">
                            <tooltip>
                              <template #label-content>
                                <logo
                                  :key="item[header.value].id"
                                  :type="
                                    item[header.value].delivery_platform_type
                                  "
                                  :size="18"
                                  class="mr-1"
                                />
                              </template>
                              <template #hover-content>
                                {{ item[header.value].name }}
                              </template>
                            </tooltip>
                          </div>
                          <div v-if="header.value == 'last_delivered'">
                            <time-stamp :value="item[header.value]" />
                          </div>
                          <div v-if="header.value == 'delivery_schedule'">
                            <tooltip>
                              <template #label-content>
                                {{
                                  item[header.value]
                                    ? item[header.value].periodicity
                                    : "-"
                                }}
                              </template>
                              <template #hover-content>
                                <hux-delivery-text
                                  v-if="item[header.value]"
                                  :schedule="item[header.value]"
                                  type="destination"
                                />
                                <span v-else>-</span>
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
                              header.value == 'updated_by' ||
                              header.value == 'created_by'
                            "
                          >
                            <avatar :name="item[header.value]" />
                          </div>
                        </td>
                      </template>
                    </hux-data-table>
                  </td>
                </template>
                <!-- eslint-enable -->
              </hux-data-table>
            </td>
          </template>
        </hux-lazy-data-table>

        <look-alike-audience
          ref="lookalikeWorkflow"
          :toggle="showLookAlikeDrawer"
          :selected-audience="selectedAudience"
          @onBack="reloadAudienceData()"
          @onCreate="onCreated()"
        />
      </div>

      <div
        v-if="!loading && rowData.length == 0 && !isEmptyError"
        class="
          flex-grow-1 flex-shrink-1
          overflow-hidden
          mw-100
          background-empty
        "
      >
        <empty-page type="no-engagement" size="50">
          <template #title>
            <div class="title-no-engagement">No engagements</div>
          </template>
          <template #subtitle>
            <div class="des-no-engagement mt-3">
              <span v-if="finalFilterApplied <= 0">
                Engagements will appear here once you start creating them.
              </span>
              <span v-else>
                Currently there are no engagements available based on your
                applied filters. <br />
                Check back later or change your filters.
              </span>
            </div>
          </template>
          <template #button>
            <span v-if="finalFilterApplied <= 0">
              <router-link
                v-if="getAccess('engagements', 'create_one')"
                :to="{ name: 'EngagementConfiguration' }"
                class="text-decoration-none"
                append
                data-e2e="add-engagement"
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
                  Create an engagement
                </huxButton>
              </router-link>
            </span>
            <span v-if="finalFilterApplied > 0 && rowData.length <= 0">
              <huxButton
                button-text="Clear filters"
                variant="primary base"
                size="large"
                class="ma-2 font-weight-regular text-button"
                is-tile
                :height="'40'"
                @click="clearFilter()"
              >
                Clear filters
              </huxButton>
            </span>
          </template>
        </empty-page>
      </div>

      <div
        v-if="!loading && rowData.length == 0 && isEmptyError"
        class="error-wrap"
      >
        <error
          icon-type="error-on-screens"
          :icon-size="50"
          title="Engagements are currently unavailable"
          subtitle="Our team is working hard to fix it. Please be patient and try again soon!"
        >
        </error>
      </div>

      <div class="ml-auto">
        <engagement-filter
          ref="filters"
          v-model="isFilterToggled"
          view-height="calc(100vh - 180px)"
          @selected-filters="totalFiltersSelected"
          @onSectionAction="applyFilter"
        />
      </div>
    </div>
    <confirm-modal
      v-model="showAudienceRemoveConfirmation"
      icon="modal-remove"
      title="You are about to remove"
      :sub-title="`${confirmSubtitle}`"
      right-btn-text="Yes, remove audience"
      @onCancel="showAudienceRemoveConfirmation = false"
      @onConfirm="
        showAudienceRemoveConfirmation = false
        removeAudience()
      "
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
          Are you sure you want to remove this audience from this engagement?
        </div>
        <div
          class="black--text text--darken-4 text-subtitle-1 font-weight-regular"
        >
          By removing this audience, it will not be deleted, but it will become
          unattached from this engagement.
        </div>
      </template>
    </confirm-modal>

    <confirm-modal
      v-model="confirmModal"
      icon="sad-face"
      type="error"
      title="You are about to delete"
      :sub-title="`${confirmSubtitle}`"
      right-btn-text="Yes, delete engagement"
      left-btn-text="Nevermind!"
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
          Are you sure you want to delete this Engagement&#63;
        </div>
        <div
          class="black--text text--darken-4 text-subtitle-1 font-weight-regular"
        >
          By deleting this engagement you will not be able to recover it and it
          may impact any associated destinations.
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
          Are you sure you want to edit this engagement&#63;
        </div>
        <div
          class="black--text text--darken-4 text-subtitle-1 font-weight-regular"
        >
          By changing the engagement, you may need to reschedule the delivery
          time and it will impact all associated audiences and destinations.
        </div>
      </template>
    </confirm-modal>

    <confirm-modal
      v-model="confirmInactiveModal"
      icon="alert-inactive"
      :title="`Make ${confirmSubtitle}`"
      sub-title="inactive?"
      right-btn-text="Yes, make engagement inactive"
      left-btn-text="Nevermind!"
      @onCancel="confirmInactiveModal = !confirmInactiveModal"
      @onConfirm="confirmInactive()"
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
          Are you sure you want to make this Engagement inactive&#63;
        </div>
        <div
          class="black--text text--darken-4 text-subtitle-1 font-weight-regular"
        >
          By making it inactive all audiences that are part of this engagement
          will have their delivery paused.
        </div>
      </template>
    </confirm-modal>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import { isEmpty } from "lodash"
import PageHeader from "@/components/PageHeader"
import Error from "@/components/common/screens/Error"
import Breadcrumb from "@/components/common/Breadcrumb"
import Icon from "@/components/common/Icon"
import huxButton from "@/components/common/huxButton"
import HuxLazyDataTable from "@/components/common/dataTable/HuxLazyDataTable.vue"
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import Avatar from "../../components/common/Avatar.vue"
import TimeStamp from "../../components/common/huxTable/TimeStamp.vue"
import Status from "../../components/common/Status.vue"
import MenuCell from "../../components/common/huxTable/MenuCell.vue"
import LookAlikeAudience from "@/views/Audiences/Configuration/Drawers/LookAlikeAudience.vue"
import Logo from "../../components/common/Logo.vue"
import Tooltip from "../../components/common/Tooltip.vue"
import ConfirmModal from "../../components/common/ConfirmModal.vue"
import HuxDeliveryText from "../../components/common/DatePicker/HuxDeliveryText.vue"
import EngagementFilter from "./Configuration/Drawers/EngagementFilter.vue"
import EmptyPage from "@/components/common/EmptyPage"
import { getAccess } from "@/utils"

export default {
  name: "Engagements",
  components: {
    PageHeader,
    Breadcrumb,
    Icon,
    huxButton,
    Error,
    HuxLazyDataTable,
    HuxDataTable,
    Avatar,
    TimeStamp,
    Status,
    MenuCell,
    LookAlikeAudience,
    Logo,
    Tooltip,
    ConfirmModal,
    HuxDeliveryText,
    EngagementFilter,
    EmptyPage,
  },
  data() {
    return {
      isFilterToggled: false,
      confirmModal: false,
      confirmEditModal: false,
      confirmInactiveModal: false,
      confirmSubtitle: "",
      selectedEngagement: null,
      selectedAudience: null,
      showLookAlikeDrawer: false,
      showAudienceRemoveConfirmation: false,
      selectedEngagementId: "",
      selectedAudienceId: "",
      isEmptyError: false,
      breadcrumbItems: [
        {
          text: "Engagements",
          disabled: true,
          icon: "speaker_down",
        },
      ],
      loading: true,
      manualDeliverySchedule: "Manual",
      numFiltersSelected: 0,
      finalFilterApplied: 0,
      enableLazyLoad: false,
      lastBatch: 0,
      batchDetails: {},
      columnDefs: [
        {
          text: "Engagement name",
          value: "name",
          width: "17%",
          class: "sticky-header",
        },
        {
          text: "Audiences",
          value: "audiences",
          width: "10%",
          class: "sticky-header",
        },
        {
          text: "Destinations",
          value: "destinations",
          width: "10%",
          class: "sticky-header",
        },
        {
          text: "Status",
          value: "status",
          width: "15%",
          class: "sticky-header",
        },
        {
          text: "Last delivered",
          value: "last_delivered",
          width: "8%",
          class: "sticky-header",
        },
        {
          text: "Delivery schedule",
          value: "delivery_schedule",
          width: "11%",
          class: "sticky-header",
        },
        {
          text: "Last updated",
          value: "update_time",
          width: "11%",
          class: "sticky-header",
        },
        {
          text: "Last updated by",
          value: "updated_by",
          width: "8%",
          class: "sticky-header",
        },
        {
          text: "Created",
          value: "create_time",
          width: "11%",
          class: "sticky-header",
        },
        {
          text: "Created by",
          value: "created_by",
          width: "8%",
          class: "sticky-header",
        },
      ],
    }
  },
  computed: {
    ...mapGetters({
      engagementData: "engagements/list",
      audiencesData: "audiences/audience",
      userFavorites: "users/favorites",
      totalEngagements: "engagements/total",
    }),
    audience(id) {
      return this.audiencesData(id)
    },
    subHeaders() {
      const _headers = JSON.parse(JSON.stringify(this.columnDefs))
      _headers.splice(1, 1)
      return _headers
    },
    rowData() {
      let engagementList = JSON.parse(JSON.stringify(this.engagementData))
      engagementList = engagementList.map((eng) => {
        let last_delivered_eng = ""
        let engDestinationList = []
        let eng_audiences = eng.audiences.map((audience) => {
          let last_delivered_aud = ""
          audience.destinations.map((destination) => {
            let dest_latest_delivery_time = destination.latest_delivery
              ? destination.latest_delivery.update_time || ""
              : ""
            let engDestIndex = engDestinationList.findIndex(
              (each) => destination.id === each.id
            )
            if (last_delivered_aud < dest_latest_delivery_time) {
              last_delivered_aud = dest_latest_delivery_time
            }
            if (engDestIndex !== -1) {
              if (
                engDestinationList[engDestIndex].latest_delivery.update_time ||
                "" < dest_latest_delivery_time
              ) {
                engDestinationList[engDestIndex] = destination
              }
            } else {
              engDestinationList.push(destination)
            }
          })
          if (last_delivered_eng < last_delivered_aud) {
            last_delivered_eng = last_delivered_aud
          }
          audience.destinations = audience.destinations.sort((a, b) =>
            a.name > b.name ? 1 : -1
          )
          return {
            ...audience,
            last_delivered: last_delivered_aud,
          }
        })
        engDestinationList = engDestinationList.sort((a, b) =>
          a.name > b.name ? 1 : -1
        )
        return {
          ...eng,
          audiences: eng_audiences,
          destinations: engDestinationList,
          last_delivered: last_delivered_eng,
        }
      })
      return engagementList.sort((a, b) => (a.name > b.name ? 1 : -1))
    },
  },

  async mounted() {
    this.loading = true
    try {
      this.setDefaultBatch()
      await this.fetchEngagementsByBatch()
      this.calculateLastBatch()
    } catch (error) {
      this.isEmptyError = true
    } finally {
      this.loading = false
    }
  },

  methods: {
    ...mapActions({
      getAllEngagements: "engagements/getAll",
      updateAudienceList: "engagements/updateAudienceList",
      updateEngagement: "engagements/updateEngagement",
      detachAudience: "engagements/detachAudience",
      setAlert: "alerts/setAlert",
      markFavorite: "users/markFavorite",
      clearFavorite: "users/clearFavorite",
      deleteEngagement: "engagements/remove",
    }),

    deliveryScheduleNullCheck(deliveryObject) {
      return !deliveryObject && isEmpty(deliveryObject)
    },

    setDefaultBatch() {
      this.batchDetails.batch_size = 25
      this.batchDetails.batch_number = 1
      this.batchDetails.favorites = false
      this.batchDetails.my_engagements = false
    },

    intersected() {
      if (this.batchDetails.batch_number <= this.lastBatch) {
        this.batchDetails.isLazyLoad = true
        this.enableLazyLoad = true
        this.fetchEngagementsByBatch()
      } else {
        this.enableLazyLoad = false
      }
    },
    async fetchEngagementsByBatch() {
      await this.getAllEngagements(this.batchDetails)
      this.batchDetails.batch_number++
    },
    calculateLastBatch() {
      this.lastBatch = Math.ceil(
        this.totalEngagements / this.batchDetails.batch_size
      )
    },

    clearFilter() {
      this.$refs.filters.clearAndReload()
    },

    totalFiltersSelected(value) {
      this.numFiltersSelected = value
    },

    async applyFilter(params) {
      this.loading = true
      this.finalFilterApplied = params.filterApplied
      this.setDefaultBatch()
      this.batchDetails.favorites = params.selectedFavourite
      this.batchDetails.my_engagements = params.selectedEngagementsWorkedWith
      try {
        await this.fetchEngagementsByBatch()
        this.calculateLastBatch()
      } catch (error) {
        this.isEmptyError = true
        this.clearFilter()
      } finally {
        this.loading = false
      }
    },

    openModal(engagement) {
      this.selectedEngagement = engagement
      this.confirmSubtitle = engagement.name
      this.confirmModal = true
    },

    async confirmRemoval() {
      await this.deleteEngagement({ id: this.selectedEngagement.id })
      this.confirmModal = false
    },

    openEditModal(engagement) {
      this.selectedEngagement = engagement
      this.confirmSubtitle = engagement.name
      this.confirmEditModal = true
    },

    async confirmEdit() {
      await this.editEngagement(this.selectedEngagement.id)
      this.confirmEditModal = false
    },

    filterToggle() {
      if (!this.isEmptyError) {
        this.isFilterToggled = !this.isFilterToggled
      }
    },

    openInactiveModal(engagement) {
      this.selectedEngagement = engagement
      this.confirmSubtitle = engagement.name
      this.confirmInactiveModal = true
    },

    async confirmInactive() {
      const inactiveEngagementPayload = {
        status: "Inactive",
      }
      const payload = {
        id: this.selectedEngagement.id,
        data: inactiveEngagementPayload,
      }
      await this.updateEngagement(payload)
      this.loading = true
      try {
        this.setDefaultBatch()
        await this.fetchEngagementsByBatch()
      } catch (error) {
        this.isEmptyError = true
      } finally {
        this.rowData = this.engagementData.sort((a, b) =>
          a.name > b.name ? 1 : -1
        )
        this.loading = false
      }
      this.confirmInactiveModal = false
    },

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
    getAudienceHeaders(headers) {
      headers[0].width = "10%"
      return headers
    },
    async removeAudience() {
      this.loading = true
      const removePayload = { audience_ids: [] }
      removePayload.audience_ids.push(this.selectedAudienceId)
      try {
        await this.detachAudience({
          engagementId: this.selectedEngagementId,
          data: removePayload,
        })
        this.setDefaultBatch()
        await this.fetchEngagementsByBatch()
      } catch (error) {
        this.isEmptyError = true
      } finally {
        this.loading = false
      }
    },
    getOverallDestinations(engagementDestinations) {
      let destinations = [...engagementDestinations]
      if (destinations.length > 3) {
        return destinations.slice(0, 3)
      }
      return destinations
    },
    getExtraDestinations(engagementDestinations) {
      let destinations = [...engagementDestinations]
      if (destinations.length > 3) {
        return destinations.slice(3)
      }
      return destinations
    },
    getDestinations(parent) {
      return parent.destinations.map((dest) => {
        const _destinationObj = {
          destinations: {
            delivery_platform_type: dest["delivery_platform_type"],
            name: dest["name"],
            id: dest.id,
          },
          status: dest.latest_delivery["status"],
          create_time: dest.create_time,
          created_by: dest.create_by,
          update_time: dest.update_time,
          updated_by: dest.updated_by,
          last_delivered: dest.latest_delivery["update_time"],
          delivery_schedule: dest.delivery_schedule,
        }
        return _destinationObj
      })
    },
    openLookAlikeDrawer(value) {
      this.selectedAudience = value
      this.$refs.lookalikeWorkflow.prefetchLookalikeDependencies()
      this.lookalikeCreated = false
      this.showLookAlikeDrawer = true
    },

    reloadAudienceData() {
      this.showLookAlikeDrawer = false
    },
    async onCreated() {
      this.setAlert({
        type: "success",
        message: `Your lookalike audience, ${name}, has been created successfully.`,
      })
    },
    getActionItems(engagement) {
      let isFavorite = this.isUserFavorite(engagement, "audiences")
      let actionItems = [
        {
          title: isFavorite ? "Unfavorite" : "Favorite",
          isDisabled: false,
          onClick: () => {
            this.handleActionFavorite(engagement, "engagements")
          },
        },
        // TODO: enable once features are available
        // { title: "Export", isDisabled: true },
        {
          title: "Edit engagement",
          isDisabled: false,
          isHidden: !this.getAccess("engagements", "update_one"),
          onClick: () => {
            this.openEditModal(engagement)
          },
        },
        // TODO: enable once features are available
        // { title: "Duplicate", isDisabled: true },
        {
          title: "Make inactive",
          isDisabled: false,
          isHidden: !this.getAccess("engagements", "update_one"),
          onClick: (value) => {
            this.openInactiveModal(value)
          },
        },
        {
          title: "Delete engagement",
          isDisabled: false,
          isHidden: !this.getAccess("engagements", "delete_one"),
          onClick: () => {
            this.openModal(engagement)
          },
        },
      ]

      return actionItems
    },
    editEngagement(id) {
      this.$router.push({
        name: "EngagementUpdate",
        params: { id: id },
      })
    },
    setEngagementSelector(engagement) {
      if (
        engagement["status"] == "Active" &&
        engagement["audiences"].length > 0
      ) {
        return "enagement-active"
      } else return "enagement-inactive"
    },
    getAudienceActionItems(audience, engagementId) {
      let audienceActionItems = [
        // TODO: enable once features are available
        // { title: "Favorite", isDisabled: true },
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
          isDisabled: false,
          menu: {
            icon: "facebook",
            title: "Facebook",
            isDisabled: true,
            onClick: (value) => {
              this.openLookAlikeDrawer(value)
            },
          },
        },
        {
          title: "Remove audience",
          isDisabled: false,
          onClick: (value) => {
            this.showAudienceRemoveConfirmation = true
            this.confirmSubtitle = value.name
            this.selectedEngagementId = engagementId
            this.selectedAudienceId = value.id
          },
        },
      ]
      return audienceActionItems
    },
    editAudience(id) {
      this.$router.push({
        name: "AudienceUpdate",
        params: { id: id },
      })
    },
    getAccess: getAccess,
  },
}
</script>

<style lang="scss" scoped>
.engagements-wrap {
  background: var(--v-primary-lighten1);
  ::v-deep .menu-cell-wrapper {
    .action-icon {
      .fav-action {
        display: none;
      }
      .more-action {
        display: none;
      }
    }
    .mdi-chevron-right,
    .mdi-dots-vertical {
      background: transparent !important;
    }
    .no-expand {
      padding-left: 8px;
    }
  }
  // This CSS is to avoid conflict with Tooltip component.
  ::v-deep .destination-ico {
    span {
      display: flex;
      align-items: center;
    }
  }
  .ellipsis-21 {
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 21ch;
    display: inline-block;
    width: 21ch;
    white-space: nowrap;
  }
  .mdi-chevron-right {
    transition: 0.3s cubic-bezier(0.25, 0.8, 0.5, 1), visibility 0s;
    &.normal-icon {
      transform: rotate(90deg);
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
  .hux-data-table {
    .mdi-chevron-right {
      &::after {
        opacity: 0;
      }
    }
    ::v-deep table {
      tr {
        &:hover {
          background: var(--v-primary-lighten2) !important;
        }
        td {
          font-size: 14px !important;
          color: var(--v-black-darken4);
        }
        td:nth-child(1) {
          font-size: 16px !important;
        }
      }
      .expanded-row {
        background-color: var(--v-primary-lighten2) !important;
      }
      .v-data-table-header {
        th:nth-child(1) {
          left: 0;
          z-index: 3;
          border-right: thin solid rgba(0, 0, 0, 0.12);
          overflow-y: visible;
          overflow-x: visible;
        }
        border-radius: 12px 12px 0px 0px;
      }
      tr {
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
          .menu-cell-wrapper {
            .action-icon {
              .fav-action {
                display: block;
              }
              .more-action {
                display: block;
              }
            }
          }
        }
        td {
          font-size: 16px !important;
          line-height: 22px;
          color: var(--v-black-darken4);
        }
        td:nth-child(1) {
          position: sticky;
          left: 0;
          border-right: thin solid rgba(0, 0, 0, 0.12);
          background-color: white;
          .menu-cell-wrapper > div {
            a.text-decoration-none {
              .ellipsis {
                width: auto !important;
              }
            }
          }
        }
      }
      tbody {
        tr {
          td:first-child {
            z-index: 1;
          }
        }
        tr:last-child {
          td {
            border-bottom: 1px solid var(--v-black-lighten3) !important;
          }
        }
      }
    }
    .child {
      ::v-deep .theme--light {
        background: var(--v-primary-lighten1);
        .v-icon {
          background: transparent;
        }
        .v-data-table__wrapper {
          box-shadow: inset 0px 10px 10px -4px var(--v-black-lighten3);
          border-bottom: thin solid rgba(0, 0, 0, 0.12);
        }
      }
      ::v-deep .v-data-table {
        .v-data-table__wrapper {
          tr {
            td:first-child {
              width: 100% !important;
              position: relative;
              margin-left: 0px;
              display: block;
              background-color: var(--v-primary-lighten1);
            }
          }
        }
      }
    }
  }
  ::v-deep .hux-data-table.expanded-table {
    .v-data-table__wrapper {
      box-shadow: inset 0px 10px 10px -4px #d0d0ce !important;
      .child-row {
        border-right: none;
      }
      .expanded-row-cover {
        width: 100% !important;
        position: fixed;
        margin-left: 220px;
        display: block;
        background-color: var(--v-primary-lighten1);
      }
      td:nth-child(2) {
        width: 9.2% !important;
      }
      td:nth-child(3) {
        width: 9.2% !important;
      }
      td:nth-child(4) {
        width: 13.7% !important;
      }
      td:nth-child(5) {
        width: 7.3% !important;
      }
      td:nth-child(6) {
        width: 10.1% !important;
      }
      td:nth-child(7) {
        width: 10.1% !important;
      }
      td:nth-child(8) {
        width: 7.3% !important;
      }
      td:nth-child(9) {
        width: 10.2% !important;
      }
      td:nth-child(10) {
        width: 7.3% !important;
      }
    }
    td:nth-child(1) {
      background: none;
    }
    .ellipsis {
      width: 13ch;
      max-width: 13ch;
    }
  }
  ::v-deep .menu-cell-wrapper :hover .action-icon {
    display: initial;
  }

  .unavailable-engagement {
    margin-top: 180px !important;
  }
}
.icon-border {
  cursor: default !important;
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
</style>
