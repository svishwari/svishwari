<template>
  <v-card class="rounded-sm status-card mr-2 box-shadow-none">
    <v-card-title v-if="showTitle" class="d-flex justify-space-between">
      <span class="d-flex">
        <logo :type="section.type" :size="24" class="mr-2" />
        <tooltip>
          <template #label-content>
            <span class="text-h3 black--text">
              {{ section.name }}
            </span>
          </template>
          <template #hover-content>
            <div class="py-2 white d-flex flex-column">
              <span>
                {{ section.name }}
              </span>
            </div>
          </template>
        </tooltip>
      </span>
      <v-spacer> </v-spacer>
      <div
        class="d-flex mr-4 cursor-pointer deliver-icon text-body-1 mt-2"
        :class="{ disabled: section.destination_audiences.length == 0 }"
        @click="deliverAll(section)"
      >
        <icon
          class="mr-1 mt-n1"
          type="deliver_2"
          :size="37"
          :color="
            section.destination_audiences.length == 0 ? 'black' : 'primary'
          "
          :variant="
            section.destination_audiences.length == 0 ? 'lighten3' : 'base'
          "
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
              v-for="item in sectionActions"
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

    <delivery-table
      :section="updateSection()"
      audience-key="destination_audiences"
      table-data="latest_delivery"
      :headers="headers"
      :audience-menu-options="audienceMenuOptions"
      @triggerSelectAudience="$emit('triggerSelectAudience', section.id)"
      @onSectionAction="$emit('triggerOverviewAction', $event)"
    />
  </v-card>
</template>

<script>
import { mapActions } from "vuex"
import { getApproxSize } from "@/utils"
import DeliveryTable from "./DeliveryTable.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import Icon from "@/components/common/Icon.vue"
import Logo from "@/components/common/Logo"

export default {
  name: "DeliveryDetails",
  components: {
    DeliveryTable,
    Tooltip,
    Icon,
    Logo,
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
    showTitle: {
      type: Boolean,
      required: false,
      default: true,
    },
    headers: {
      type: Array,
      required: true,
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
        { id: 1, title: "Deliver now", active: true },
        { id: 2, title: "Create lookalike", active: true },
        { id: 3, title: "Remove audience", active: true },
      ],
      destinationMenuOptions: [
        { id: 1, title: "Open destination", active: true },
        { id: 2, title: "Edit delivery schedule", active: true },
        { id: 3, title: "Remove destination", active: true },
      ],

      stateListData: [],
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
        : this.destinationMenuOptions
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
      await this.deliverAudienceDestination({
        id: this.engagementId,
        audienceId: "000000000000000000000000",
        destinationId: engagement.id,
      })
      this.dataPendingMessage(engagement)
      this.$emit("refreshEntityDelivery")
    },
    addDestination() {},
    getSize(value) {
      return getApproxSize(value)
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
    dataPendingMessage(event) {
      const destinationName = event.name
      this.setAlert({
        type: "pending",
        message: `Your destination '${destinationName}', has started delivering as part of the engagement '${this.engagementId}'.`,
      })
    },
    updateSection() {
      this.section.destination_audiences.forEach((element) => {
        element["latest_delivery"].name = element.name
      })
      return this.section
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
  overflow: hidden;
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
  .hux-data-table {
    ::v-deep table {
      .v-data-table-header {
        tr {
          th {
            background: var(--v-primary-lighten2);
            height: 40px !important;
          }
        }
      }
      tbody {
        tr {
          td {
            height: 40px !important;
          }
        }
      }
      border-radius: 12px 12px 0px 0px;
      overflow: hidden;
    }
  }
}
.deliverAll {
  margin-top: 2px;
}
</style>
