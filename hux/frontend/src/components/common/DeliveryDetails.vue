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
        v-if="getAccess('delivery', 'deliver')"
        class="d-flex mr-4 cursor-pointer deliver-icon text-body-1 mt-2"
        :class="{ disabled: section.deliveries.length == 0 }"
        data-e2e="deliver-all"
        @click="deliverAll(section)"
      >
        <icon
          class="mr-1 mt-n1"
          :type="section.deliveries.length == 0 ? 'deliver' : 'deliver_2'"
          :size="37"
          :color="section.deliveries.length == 0 ? 'black' : 'primary'"
          :variant="section.deliveries.length == 0 ? 'lighten3' : 'base'"
        />
        <span class="deliverAll"> Deliver all </span>
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
            data-e2e="destination-list-audience"
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
                        v-for="option in destinationActions"
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
            <div v-if="header.value == 'replace'" class="text-body-1">
              <hux-switch
                v-if="item['is_ad_platform']"
                v-model="item['replace_audience']"
                :switch-labels="switchLabels"
                false-color="var(--v-black-lighten4)"
                @change="handleChange(section.id, item.id, $event)"
              />
            </div>
          </td>
        </template>
      </hux-data-table>

      <v-list
        v-if="getAccess('engagements', 'add_destination_to_engagement')"
        dense
        class="add-list"
        :height="52"
      >
        <v-list-item @click="$emit('onAddDestination', section)">
          <tooltip>
            <template #label-content>
              <hux-icon
                type="plus"
                :size="16"
                color="primary"
                class="mr-2 plus-icon"
              />
              <hux-icon
                type="destination_button"
                :size="34"
                color="primary"
                class="mr-0 mb-n1"
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
            data-e2e="add-audience-destination"
            class="primary--text text-body-1"
          >
            <span class="destination_text">Destination</span>
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
import HuxSwitch from "@/components/common/Switch.vue"
import { getAccess } from "@/utils"

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
    HuxSwitch,
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
        {
          id: 5,
          title: "Remove engagement",
          active: false,
          isHidden: !this.getAccess("engagements", "delete_one"),
        },
      ],
      audienceMenuOptions: [
        {
          id: 1,
          title: "Deliver now",
          isHidden: !this.getAccess("delivery", "deliver"),
          active: false,
        },
        {
          id: 2,
          title: "Add a destination",
          active: true,
          isHidden: !this.getAccess(
            "engagements",
            "add_destination_to_engagement"
          ),
        },
        {
          id: 3,
          title: "Create lookalike",
          active: false,
          isHidden: !this.getAccess("audience", "create_lookalike"),
        },
        { id: 4, title: "Pause all delivery", active: false },
        {
          id: 5,
          title: "Remove audience",
          active: true,
          isHidden: !this.getAccess(
            "engagements",
            "remove_audience_from_engagement"
          ),
        },
      ],
      destinationMenuOptions: [
        {
          id: 1,
          title: "Deliver now",
          active: true,
          isHidden: !this.getAccess("delivery", "deliver"),
        },
        { id: 3, title: "Open destination", active: false },
        {
          id: 4,
          title: "Remove destination",
          active: true,
          isHidden: !this.getAccess(
            "engagements",
            "remove_destination_from_engagement"
          ),
        },
      ],

      stateListData: [],
      columnDefs: [
        {
          text: "Destination",
          value: "name",
          width: "25%",
        },
        {
          text: "Status",
          value: "status",
          width: "15%",
        },
        {
          text: "Target size",
          value: "size",
          width: "15%",
          hoverTooltip:
            "Average order value for all consumers (known and anyonymous) for all time.",
          tooltipWidth: "201px",
        },
        {
          text: "Last delivery",
          value: "next_delivery",
          width: "25%",
        },
        {
          text: "Replace",
          value: "replace",
          width: "20%",
        },
      ],
      switchLabels: [
        {
          condition: true,
          label: "ON",
        },
        {
          condition: false,
          label: "OFF",
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
        ? this.engagementMenuOptions.filter((x) => !x.isHidden)
        : this.audienceMenuOptions.filter((x) => !x.isHidden)
    },
    destinationActions() {
      return this.sectionType === "engagement"
        ? this.destinationMenuOptions.filter((x) => !x.isHidden)
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
      updateReplace: "engagements/updateReplace",
      replaceAudience: "audiences/replaceAudienceToggle",
      updateAudience: "audiences/update",
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
        isHidden: !this.getAccess("audience", "create_lookalike"),
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
        {
          id: 2,
          title: "Deliver now",
          active: true,
          isHidden: !this.getAccess("delivery", "deliver"),
        },
        {
          id: 3,
          title: "Edit delivery schedule",
          active: true,
          isHidden: !this.getAccess("delivery", "schedule_delivery"),
        },
        { id: 4, title: "Pause delivery", active: false },
        { id: 5, title: "Open destination", active: false },
        {
          id: 6,
          title: "Remove destination",
          active: true,
          isHidden: !this.getAccess(
            "engagements",
            "remove_destination_from_engagement"
          ),
        },
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
    getAccess: getAccess,
    handleChange(...args) {
      const data = {
        engagement_id: args[0],
        audience_id: this.audienceId,
        destination_id: args[1],
        value: args[2],
      }
      let updatedEngagements = []
      if (this.audience.engagements) {
        updatedEngagements = this.audience.engagements.map((obj) => {
          if (obj && obj.id == args[0]) {
            return {
              ...obj,
              deliveries: obj.deliveries
                ? obj.deliveries.map((del) => {
                    if (del.delivery_platform_id == args[1]) {
                      return { ...del, replace_audience: args[2] }
                    }
                    return del
                  })
                : [],
            }
          }
          return obj
        })
      }
      this.updateAudience({
        id: this.audienceId,
        payload: {
          engagements: updatedEngagements,
        },
      })
      this.replaceAudience(data)
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
      pointer-events: none;
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
.deliverAll {
  margin-top: 2px;
}
.destination_text {
  margin-top: -2px;
}
.plus-icon {
  margin-bottom: 7px;
}
</style>
