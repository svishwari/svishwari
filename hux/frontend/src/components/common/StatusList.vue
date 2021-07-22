<template>
  <v-card class="rounded-sm status-card mr-2 box-shadow-none">
    <v-card-title class="d-flex justify-space-between">
      <span class="d-flex">
        <router-link
          :to="{
            name: 'AudienceInsight',
            params: { id: section.id },
          }"
          class="text-decoration-none"
          append
        >
          <tooltip>
            <template #label-content>
              {{ section.name }}
            </template>
            <template #hover-content>
              <div class="py-2 white d-flex flex-column">
                <span>
                  {{ section.name }}
                </span>
                <span class="mt-3" v-if="section.description">
                  {{ section.description }}
                </span>
              </div>
            </template>
          </tooltip>
        </router-link>
        <status
          v-if="section.status"
          :status="section.status"
          :iconSize="statusIcon"
          class="ml-2"
          collapsed
          showLabel
          tooltipTitle="Engagement status"
        />
      </span>
      <v-menu class="menu-wrapper" bottom offset-y>
        <template #activator="{ on, attrs }">
          <v-icon v-bind="attrs" v-on="on" class="top-action">
            mdi-dots-vertical
          </v-icon>
        </template>
        <v-list class="menu-list-wrapper">
          <v-list-item-group>
            <v-list-item
              v-for="item in menuItems"
              :key="item.id"
              :disabled="!item.active"
            >
              <v-list-item-title
                @click="
                  $emit('onSectionAction', { target: item, item: section })
                "
              >
                {{ item.title }}
              </v-list-item-title>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-menu>
    </v-card-title>
    <v-list dense class="pa-0" v-if="section.destinations.length > 0">
      <v-list-item
        v-for="item in section.destinations"
        :key="item.id"
        @click="toggleFocus()"
      >
        <v-list-item-content class="icon-col py-1">
          <div class="d-flex align-center">
            <tooltip>
              <template #label-content>
                <Logo :type="item.type" :size="18" />
              </template>
              <template #hover-content>
                <div class="d-flex flex-column">
                  <div class="d-flex align-center">
                    <Logo :type="item.type" :size="18" />
                    <span class="ml-2">{{ item.name }}</span>
                  </div>
                  <span class="mb-1 mt-2">Last delivered:</span>
                  <span>{{ item.update_time | Date | Empty("-") }}</span>
                </div>
              </template>
            </tooltip>

            <v-spacer></v-spacer>

            <span class="action-icon font-weight-light float-right d-none">
              <v-menu class="menu-wrapper" bottom offset-y>
                <template #activator="{ on, attrs }">
                  <v-icon
                    v-bind="attrs"
                    v-on="on"
                    class="mr-2 more-action"
                    color="primary"
                    @click.prevent
                    v-if="!section.lookalike"
                  >
                    mdi-dots-vertical
                  </v-icon>
                </template>
                <v-list class="menu-list-wrapper">
                  <v-list-item-group>
                    <v-list-item
                      v-for="option in destinationMenuItems"
                      :key="option.id"
                      :disabled="!option.active"
                    >
                      <v-list-item-title
                        v-if="option.title === 'Deliver now'"
                        @click="
                          $emit('onDestinationAction', {
                            target: option,
                            item: item,
                          })
                        "
                      >
                        {{ option.title }}
                      </v-list-item-title>
                      <v-list-item-title v-else>
                        {{ option.title }}
                      </v-list-item-title>
                    </v-list-item>
                  </v-list-item-group>
                </v-list>
              </v-menu>
            </span>
          </div>
        </v-list-item-content>
        <v-list-item-content v-if="item.status" class="status-col py-1">
          <status
            :status="item.status"
            :iconSize="statusIcon"
            collapsed
            showLabel
            tooltipTitle="Destination status"
          />
        </v-list-item-content>
        <v-list-item-content v-if="item.size" class="size-col py-1">
          <tooltip>
            <template #label-content>
              {{ getSize(item.size) }}
            </template>
            <template #hover-content>
              {{ item.size | Numeric(true, false) }}
            </template>
          </tooltip>
        </v-list-item-content>
        <v-list-item-content v-if="!item.size" class="deliverdOn-col py-1">
          <tooltip>
            <template #label-content>
              {{ getSize(item.size) | Empty("-") }}
            </template>
            <template #hover-content>
              {{ item.size | Numeric(true, false) | Empty("-") }}
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
      v-if="section.destinations.length == 0"
      class="py-2 px-4 empty-destinations"
    >
      <slot name="empty-destinations"></slot>
    </div>

    <hux-alert
      v-model="showDeliveryAlert"
      type="success"
      title="YAY!"
      message="Successfully delivered your audience."
    />
  </v-card>
</template>

<script>
import { mapActions } from "vuex"
import Logo from "./Logo.vue"
import Status from "./Status.vue"
import { getApproxSize } from "@/utils"
import Tooltip from "./Tooltip.vue"
import HuxAlert from "@/components/common/HuxAlert.vue"

export default {
  components: { Logo, Status, Tooltip, HuxAlert },

  name: "StatusList",

  data() {
    return {
      showDeliveryAlert: false,
    }
  },

  props: {
    section: {
      type: Object,
      required: false,
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
    destinationMenuItems: {
      type: Array,
      required: false,
    },
  },

  methods: {
    ...mapActions({
      deliverAudience: "engagements/deliverAudience",
      deliverAudienceDestination: "engagements/deliverAudienceDestination",
    }),

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
        min-width: 69px;
        max-width: 69px;
      }
      .status-col {
        min-width: 45px;
        max-width: 45px;
      }
      .size-col {
        min-width: 80px;
        max-width: 80px;
        font-size: 12px;
        line-height: 16px;
        color: var(--v--neroBlack-base);
      }
      .deliverdOn-col {
        font-size: 12px;
        line-height: 16px;
        color: var(--v-neroBlack-base);
        min-width: 80px;
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
  }
}
</style>
