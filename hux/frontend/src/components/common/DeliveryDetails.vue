<template>
  <v-card class="rounded-sm status-card mr-2 box-shadow-none">
    <v-card-title class="d-flex justify-space-between">
      <span class="d-flex">
        <status status="Active" :icon-size="19" collapsed class="float-left" />
        <router-link
          :to="{
            name: routeName,
            params: { id: section.id },
          }"
          class="text-decoration-none"
          append
        >
          <tooltip>
            <template #label-content>
              <span class="primary--text text-h3">
                {{ section.name }}
              </span>
            </template>
            <template #hover-content>
              <div class="py-2 white d-flex flex-column">
                <span>
                  {{ section.name }}
                </span>
                <span v-if="section.description" class="mt-3">
                  {{ section.description }}
                </span>
              </div>
            </template>
          </tooltip>
        </router-link>
      </span>
      <v-spacer> </v-spacer>
      <div
        class="d-flex mr-4 cursor-pointer deliver-icon text-body-1"
        :class="{ disabled: section.deliveries.length == 0 }"
        @click="deliverAll(section)"
      >
        <icon
          class="mr-1"
          type="deliver_2"
          :size="27"
          :color="section.deliveries.length == 0 ? 'black' : 'primary'"
          :variant="section.deliveries.length == 0 ? 'lighten3' : 'base'"
        />
        Deliver all
      </div>
      <v-menu class="menu-wrapper" bottom offset-y>
        <template #activator="{ on, attrs }">
          <v-icon v-bind="attrs" class="top-action" v-on="on">
            mdi-dots-vertical
          </v-icon>
        </template>
        <v-list class="menu-list-wrapper">
          <v-list-item-group v-model="selection" active-class="">
            <v-list-item
              v-for="item in sectionActionItems(section)"
              :key="item.id"
              :disabled="!item.active"
              @click="$emit('onSectionAction', { target: item, data: section })"
            >
              <v-list-item-title>
                {{ item.title }}
              </v-list-item-title>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-menu>
    </v-card-title>

    <v-list dense class="pa-0 delivery-table">
      <hux-data-table
        v-if="section.deliveries.length > 0"
        :columns="columnDefs"
        :sort-desc="true"
        :data-items="section.deliveries"
      >
        <template #row-item="{ item }">
          <td
            v-for="header in columnDefs"
            :key="header.value"
            class="text-body-2 column"
            :style="{ width: header.width }"
            data-e2e="map-state-list"
          >
            <div v-if="header.value == 'name'" class="text-body-1">
              <logo :type="item.delivery_platform_type" :size="24"></logo>
              <span class="ml-2 ellipsis">
                {{ item.name }}
              </span>
              <span class="action-icon font-weight-light float-right d-none">
                <v-menu
                  v-model="openMenu[item.id]"
                  class="menu-wrapper"
                  bottom
                  offset-y
                >
                  <template #activator="{ on, attrs }">
                    <v-icon
                      v-if="!section.lookalike"
                      v-bind="attrs"
                      class="mr-2 more-action"
                      color="primary"
                      v-on="on"
                      @click.prevent
                    >
                      mdi-dots-vertical
                    </v-icon>
                  </template>
                  <v-list class="menu-list-wrapper">
                    <v-list-item-group>
                      <v-list-item
                        v-for="option in destinationMenuOptions"
                        :key="option.id"
                        :disabled="!option.active"
                        @click="
                          $emit('onDestinationAction', {
                            target: option,
                            data: item,
                            parent: section,
                          })
                        "
                      >
                        <v-list-item-title v-if="!option.menu">
                          {{ option.title }}
                        </v-list-item-title>
                      </v-list-item>
                    </v-list-item-group>
                  </v-list>
                </v-menu>
              </span>
            </div>
            <div v-if="header.value == 'status'" class="text-body-1">
              <status
                :status="item['status']"
                :show-label="true"
                class="d-flex"
                :icon-size="17"
              />
            </div>
            <div v-if="header.value == 'size'" class="text-body-1">
              <size :value="item['size']" />
            </div>
            <div v-if="header.value == 'next_delivery'" class="text-body-1">
              <time-stamp :value="item['next_delivery']" />
            </div>
          </td>
        </template>
      </hux-data-table>

      <v-list dense class="add-list" :height="52">
        <v-list-item @click="$emit('onAddDestination', section)">
          <tooltip>
            <template #label-content>
              <hux-icon
                type="plus"
                :size="16"
                color="primary"
                class="mr-4 mb-1"
              />
              <hux-icon
                type="destination"
                :size="24"
                color="primary"
                class="mr-2"
              />
            </template>
            <template #hover-content>
              <div class="py-2 white d-flex flex-column">
                <span> Add a destination to this engagement </span>
              </div>
            </template>
          </tooltip>
          <v-btn
            text
            min-width="7rem"
            height="2rem"
            class="primary--text text-body-1"
          >
            Destination
          </v-btn>
        </v-list-item>
      </v-list>
    </v-list>
  </v-card>
</template>

<script>
import { mapActions } from "vuex"
import { getApproxSize } from "@/utils"
import Logo from "./Logo.vue"
import Icon from "@/components/common/Icon.vue"
import Status from "./Status.vue"
import Tooltip from "./Tooltip.vue"
import HuxDataTable from "@/components/common/dataTable/HuxDataTable.vue"
import TimeStamp from "../../components/common/huxTable/TimeStamp.vue"
import Size from "@/components/common/huxTable/Size.vue"
import HuxIcon from "@/components/common/Icon.vue"

export default {
  name: "DeliveryDetails",
  components: {
    Logo,
    Icon,
    Status,
    Tooltip,
    HuxDataTable,
    TimeStamp,
    Size,
    HuxIcon,
  },

  props: {
    section: {
      type: Object,
      required: false,
      default: () => {},
    },

    engagementId: {
      type: String,
      required: false,
    },
    statusIcon: {
      type: Number,
      required: false,
      default: 24,
    },
    menuItems: {
      type: Array,
      required: false,
    },
    deliveriesKey: {
      type: String,
      required: true,
      default: "destinations",
    },
    sectionType: {
      type: String,
      required: false,
    },
    audience: {
      type: Object,
      required: false,
    },
  },

  data() {
    return {
      openMenu: {},
      isSubMenuOpen: {},
      showDeliveryAlert: false,
      selection: null,
      matchRatePlatforms: ["facebook", "google-ads"],
      lookALikeAllowedEntries: ["Facebook"],
      engagementMenuOptions: [
        { id: 5, title: "Remove engagement", active: false },
      ],
      audienceMenuOptions: [
        {
          id: 1,
          title: "Deliver now",
          active: false,
        },
        { id: 2, title: "Add a destination", active: true },
        { id: 3, title: "Create lookalike", active: false },
        { id: 4, title: "Pause all delivery", active: false },
        { id: 5, title: "Remove audience", active: true },
      ],
      destinationMenuOptions: [
        { id: 1, title: "Deliver now", active: true },
        { id: 3, title: "Open destination", active: false },
        { id: 4, title: "Remove destination", active: true },
      ],

      stateListData: [],
      columnDefs: [
        {
          text: "Destination",
          value: "name",
          width: "35%",
        },
        {
          text: "Status",
          value: "status",
          width: "25%",
        },
        {
          text: "Target size",
          value: "size",
          width: "15%",
          hoverTooltip:
            "Average order value for all customers (known and anyonymous) for all time.",
          tooltipWidth: "201px",
        },
        {
          text: "Last delivery",
          value: "next_delivery",
          width: "25%",
        },
      ],
    }
  },

  computed: {
    sectionTypePrefix() {
      return this.$options.filters.TitleCase(this.sectionType)
    },
    routeName() {
      return this.sectionType === "engagement"
        ? "EngagementDashboard"
        : "AudienceInsight"
    },
    sectionActions() {
      return this.sectionType === "engagement"
        ? this.engagementMenuOptions
        : this.audienceMenuOptions
    },
    destinationActions() {
      return this.sectionType === "engagement"
        ? this.destinationMenuOptions
        : []
    },
    audienceId() {
      return this.$route.params.id
    },
  },

  watch: {
    // To reset the value of the openMenu
    openMenu(newValue) {
      if (!newValue) this.openMenu = {}
    },
    isSubMenuOpen(newValue) {
      if (!newValue) this.isSubMenuOpen = {}
    },
  },

  methods: {
    ...mapActions({
      deliverAudience: "engagements/deliverAudience",
      deliverAudienceDestination: "engagements/deliverAudienceDestination",
      setAlert: "alerts/setAlert",
    }),
    async deliverAll(engagement) {
      await this.deliverAudience({
        id: engagement.id,
        audienceId: this.audienceId,
      })
      this.dataPendingMesssage(engagement)
      this.$emit("refreshEntityDelivery")
    },
    addDestination() {},
    getSize(value) {
      return getApproxSize(value)
    },
    sectionActionItems(section) {
      if (this.sectionType === "engagement") {
        this.engagementMenuOptions.forEach((element) => {
          switch (element.title.toLowerCase()) {
            case "remove engagement":
              element["active"] = true
              break
            default:
              break
          }
        })
        return this.engagementMenuOptions
      } else {
        this.audienceMenuOptions.forEach((element) => {
          switch (element.title.toLowerCase()) {
            case "deliver now":
              element["active"] = section[this.deliveriesKey].length > 0
              break

            case "create lookalike":
              element["active"] = section.lookalikable === "Active"
              break

            case "Pause all delivery":
              element["active"] =
                section[this.deliveriesKey].filter(
                  (delivery) => delivery.status === "Delivering"
                ).length > 0
              break

            default:
              break
          }
        })
        return this.audienceMenuOptions
      }
    },
    deliveryActionItems(delivery) {
      const createLookaLikeOption = {
        id: 1,
        title: "Create lookalike",
        active: false,
      }
      if (delivery.name === "Facebook") {
        ;(createLookaLikeOption["active"] = true),
          (createLookaLikeOption["menu"] = {
            id: "1.1",
            title: "Facebook",
            icon: "facebook",
          })
      }
      return [
        { ...createLookaLikeOption },
        { id: 2, title: "Deliver now", active: true },
        { id: 3, title: "Edit delivery schedule", active: true },
        { id: 4, title: "Pause delivery", active: false },
        { id: 5, title: "Open destination", active: false },
        { id: 6, title: "Remove destination", active: true },
      ]
    },
    dataPendingMesssage(event) {
      const engagementName = event.name
      const audienceName = this.audience.name
      this.setAlert({
        type: "pending",
        message: `Your engagement '${engagementName}', has started delivering as part of the audience '${audienceName}'.`,
      })
    },
  },
}
</script>

<style lang="scss" scoped>
.status-card {
  width: 100%;
  background: var(--v-white-base);
  border: 1px solid var(--v-black-lighten2);
  box-sizing: border-box;
  border-radius: 12px !important;
  display: table;
  .deliver-icon {
    &.disabled {
      color: var(--v-black-lighten3);
    }
  }
  .status-list {
    min-height: 20px !important;
    max-height: 30px !important;
  }
  .ellipsis {
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 15ch;
    display: inline-block;
    white-space: nowrap;
  }
  .v-card__title {
    background: var(--v-primary-lighten1);
    border-radius: 12px 12px 0px 0px;
    font-size: 14px;
    line-height: 22px;
    color: var(--v-primary-base);
    height: 60px;
    flex-wrap: inherit;
    .top-action {
      color: var(--v-black-base);
    }
  }
  .delivery-table {
    ::v-deep .v-data-table__wrapper {
      tbody {
        tr {
          td:nth-child(1) {
            &:hover,
            &:focus {
              .action-icon {
                display: block !important;
              }
            }
          }
        }
      }
    }
  }
  .add-list {
    border-bottom-right-radius: 16px;
    border-bottom-left-radius: 16px;
  }
}
</style>
