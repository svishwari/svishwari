<template>
  <v-card class="rounded-sm status-card mr-2 box-shadow-none">
    <v-card-title class="d-flex justify-space-between">
      <span class="d-flex">
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
              <span class="ellipsis">
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
        <status
          v-if="section.status"
          :status="section.status"
          :icon-size="statusIcon"
          class="ml-3"
          collapsed
          show-label
          show-icon-tooltip
          :tooltip-title="`${sectionTypePrefix} status`"
        />
      </span>
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
    <v-list v-if="section[deliveriesKey].length > 0" dense class="pa-0">
      <v-list-item
        v-for="item in section[deliveriesKey]"
        :key="item.id"
        @click="toggleFocus()"
      >
        <v-list-item-content class="icon-col py-1">
          <div class="d-flex align-center">
            <tooltip>
              <template #label-content>
                <logo :type="item.delivery_platform_type" :size="18" />
              </template>
              <template #hover-content>
                <div class="d-flex flex-column">
                  <div class="d-flex align-center">
                    <logo :type="item.delivery_platform_type" :size="18" />
                    <span class="ml-2">{{ item.name }}</span>
                  </div>
                  <span class="mb-1 mt-2">Last delivered:</span>
                  <span>{{ item.update_time | Date | Empty("-") }}</span>
                </div>
              </template>
            </tooltip>

            <v-spacer></v-spacer>

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
                      v-for="option in deliveryActionItems(item)"
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

                      <v-menu
                        v-else
                        v-model="isSubMenuOpen[item.id]"
                        offset-x
                        nudge-right="16"
                        nudge-top="4"
                      >
                        <template #activator="{ on, attrs }">
                          <v-list-item-title v-bind="attrs" v-on="on">
                            {{ option.title }}
                            <v-icon> mdi-chevron-right </v-icon>
                          </v-list-item-title>
                        </template>
                        <template #default>
                          <v-list>
                            <v-list-item
                              @click="
                                isSubMenuOpen[item.id] = false
                                openMenu[item.id] = false
                                $emit('onDestinationAction', {
                                  target: option,
                                  data: item,
                                  parent: section,
                                })
                              "
                            >
                              <v-list-item-title>
                                <logo
                                  v-if="option.menu.icon"
                                  :size="18"
                                  :type="option.menu.icon"
                                />
                                <span class="ml-1">
                                  {{ option.menu.title }}
                                </span>
                              </v-list-item-title>
                            </v-list-item>
                          </v-list>
                        </template>
                      </v-menu>
                    </v-list-item>
                  </v-list-item-group>
                </v-list>
              </v-menu>
            </span>
          </div>
        </v-list-item-content>
        <v-list-item-content v-if="item.status" class="status-col py-1 mr-2">
          <status
            :status="item.status"
            :icon-size="statusIcon"
            collapsed
            show-label
            show-icon-tooltip
            tooltip-title="Destination status"
          />
        </v-list-item-content>
        <v-list-item-content v-if="item.size" class="size-col py-1 mr-2">
          <tooltip>
            <template #label-content>
              {{ getSize(item.size) | Empty("-") }}
              <span v-if="item.match_rate">
                | {{ item.match_rate | Percentage }}
              </span>
            </template>
            <template #hover-content>
              <div class="d-flex flex-column text-caption">
                <span>Audience size</span>
                <span class="pb-3">{{ item.size | Numeric(true, false) }}</span>
                <span>Match rate</span>
                <i v-if="!item.match_rate">
                  Pending... check back in a few hours
                </i>
                <span v-else>{{ item.match_rate | Percentage }}</span>
              </div>
            </template>
          </tooltip>
        </v-list-item-content>
        <v-list-item-content v-if="!item.size" class="size-col py-1 mr-2">
          <tooltip>
            <template #label-content>
              {{ getSize(item.size) | Empty("-") }}
              <span v-if="item.match_rate">
                | {{ item.match_rate | Percentage }}
              </span>
            </template>
            <template #hover-content>
              <div class="d-flex flex-column text-caption">
                <span>Audience size</span>
                <span class="pb-3">{{ item.size | Numeric(true, false) }}</span>
                <span>Match rate</span>
                <i v-if="!item.match_rate">
                  Pending... check back in a few hours
                </i>
                <span v-else>{{ item.match_rate | Percentage }}</span>
              </div>
            </template>
          </tooltip>
        </v-list-item-content>
        <v-list-item-content
          v-if="item.update_time"
          class="deliverdOn-col py-1"
        >
          <tooltip>
            <template #label-content>
              {{ item.update_time | Date("relative") | Empty("-") }}
            </template>
            <template #hover-content>
              <div class="py-2 white d-flex flex-column">
                <span class="mb-1">Last delivered:</span>
                <span>{{ item.update_time | Date | Empty("-") }}</span>
                <span class="mt-2 mb-1">Next delivery:</span>
                <span>{{ item.next_delivery | Date | Empty("-") }}</span>
                <span class="mt-2 mb-1">Delivery schedule:</span>
                <span>{{ item.delivery_schedule_type | Empty("-") }}</span>
              </div>
            </template>
          </tooltip>
        </v-list-item-content>
      </v-list-item>
    </v-list>
    <div
      v-if="section[deliveriesKey].length == 0"
      class="py-2 px-4 empty-destinations"
    >
      <slot name="empty-destinations"></slot>
    </div>
  </v-card>
</template>

<script>
import { mapActions } from "vuex"
import Logo from "./Logo.vue"
import Status from "./Status.vue"
import { getApproxSize } from "@/utils"
import Tooltip from "./Tooltip.vue"

export default {
  name: "StatusList",
  components: {
    Logo,
    Status,
    Tooltip,
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
  },

  data() {
    return {
      openMenu: {},
      isSubMenuOpen: {},
      showDeliveryAlert: false,
      selection: null,
      lookALikeAllowedEntries: ["Facebook"],
      engagementMenuOptions: [
        { id: 1, title: "View delivery history", active: false },
        { id: 2, title: "Deliver all", active: false },
        { id: 3, title: "Add a destination", active: false },
        { id: 5, title: "Remove engagement", active: false },
      ],
      destinationMenuOptions: [
        { id: 2, title: "Create lookalike", active: false },
        { id: 1, title: "Deliver now", active: true },
        { id: 3, title: "Edit delivery schedule", active: true },
        { id: 4, title: "Pause delivery", active: false },
        { id: 5, title: "Open destination", active: false },
        { id: 6, title: "Remove destination", active: false },
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
    }),

    closeModal() {
      this.showConfirmModal = false
    },

    closeDrawer() {
      this.editDeliveryDrawer = false
    },

    onEditDeliverySchedule(destination) {
      this.showConfirmModal = true
      this.selectedDestination = destination
    },

    openEditDeliveryScheduleDrawer() {
      this.closeModal()
      this.editDeliveryDrawer = true
    },

    getSize(value) {
      return getApproxSize(value)
    },

    triggerAddDestination(engagementId, audienceId) {
      this.$emit("onAddDestination", {
        engagementId: engagementId,
        audienceId: audienceId,
      })
    },
    triggerAction(item, engagementId, audienceId) {
      switch (item.toLowerCase()) {
        case "deliver now":
          this.deliverEngagementAudience(engagementId, audienceId)
          break
        case "add a destination":
          this.triggerAddDestination(engagementId, audienceId)
          break
        case "remove audience":
          this.$emit("removeAudience", this.audience)
          break
        default:
          break
      }
    },
    async deliverEngagementAudience(engagementId, audienceId) {
      try {
        await this.deliverAudience({
          id: engagementId,
          audienceId: audienceId,
        })
        this.showDeliveryAlert = true
      } catch (error) {
        console.error(error)
      }
    },

    async deliverEngagementAudienceDestination(
      engagementId,
      audienceId,
      destinationId
    ) {
      try {
        await this.deliverAudienceDestination({
          id: engagementId,
          audienceId: audienceId,
          destinationId: destinationId,
        })
        this.showDeliveryAlert = true
      } catch (error) {
        console.error(error)
      }
    },
    sectionActionItems(section) {
      if (this.sectionType === "engagement") {
        this.engagementMenuOptions.forEach((element) => {
          switch (element.title.toLowerCase()) {
            case "view delivery history":
              element["active"] = false
              // TODO
              // element["active"] =
              //   section[this.deliveriesKey].filter(
              //     (delivery) => delivery.status === "Delivered"
              //   ).length > 0
              break
            case "deliver all":
              element["active"] = section[this.deliveriesKey].length > 0
              break
            case "add a destination":
              element["active"] = true
              break
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
  },
}
</script>

<style lang="scss" scoped>
.status-card {
  min-width: 310px;
  max-width: 310px;
  background: var(--v-white-base);
  border: 1px solid var(--v-zircon-base);
  box-sizing: border-box;
  border-radius: 12px !important;
  display: table;
  .ellipsis {
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 25ch;
    display: inline-block;
    white-space: nowrap;
  }
  .v-card__title {
    background: var(--v-background-base);
    border-radius: 12px 12px 0px 0px;
    font-size: 14px;
    line-height: 22px;
    color: var(--v-primary-base);
    height: 46px;
    flex-wrap: inherit;
    .top-action {
      color: var(--v-neroBlack-base);
    }
  }
  .empty-destinations {
    .no-destinations {
      font-size: 12px;
      line-height: 16px;
    }
  }
  .v-list {
    .v-list-item {
      .icon-col {
        min-width: 55px;
        max-width: 55px;
      }
      .status-col {
        min-width: 45px;
        max-width: 45px;
      }
      .size-col {
        min-width: 60px;
        max-width: 60px;
        font-size: 12px;
        line-height: 16px;
        color: var(--v--neroBlack-base);
      }
      .deliverdOn-col {
        font-size: 12px;
        line-height: 16px;
        color: var(--v-neroBlack-base);
        min-width: 60px;
      }
      &:hover,
      &:focus {
        background: var(--v-white-base);
        box-shadow: 0px 1px 5px rgba(0, 0, 0, 0.25);
        .action-icon {
          display: block !important;
        }
      }
    }
  }
}

::v-deep.v-menu__content {
  .v-list-item {
    &.theme--light {
      min-height: 32px !important;
      font-size: 14px;
      line-height: 22px;
      color: var(--v-neroBlack-base);
      &.v-list-item--disabled {
        color: var(--v-lightGrey-base);
      }
      &:hover {
        background: var(--v-aliceBlue-base);
      }
    }
    ::v-deep .sub-menu-class {
      display: flex;
      align-items: center;
      padding: 5px 8px;
      min-height: 32px;
      @extend .cursor-pointer;
    }
  }
}
</style>
