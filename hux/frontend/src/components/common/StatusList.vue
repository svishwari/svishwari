<template>
  <v-card class="rounded-sm status-card mr-2 box-shadow-none">
    <v-card-title class="d-flex justify-space-between">
      <span
        ><router-link
          :to="{
            name: 'AudienceInsight',
            params: { id: audience.audienceId },
          }"
          class="text-decoration-none"
          append
          >{{ audience.name }}</router-link
        ></span
      >
      <v-menu class="menu-wrapper" bottom offset-y>
        <template #activator="{ on, attrs }">
          <v-icon v-bind="attrs" v-on="on" class="top-action"
            >mdi-dots-vertical</v-icon
          >
        </template>
        <v-list class="menu-list-wrapper">
          <v-list-item-group>
            <v-list-item
              v-for="item in topNavItems"
              :key="item.id"
              :disabled="!item.active"
            >
              <v-list-item-title>{{ item.title }}</v-list-item-title>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-menu>
    </v-card-title>
    <v-list dense class="pa-0">
      <v-list-item
        v-for="item in audience.destinations"
        :key="item.id"
        @click="toggleFocus()"
      >
        <v-list-item-content class="icon-col py-1">
          <div class="d-flex align-center">
            <tooltip>
              <template slot="label-content">
                <Logo :type="item.type" :size="18" />
              </template>
              <template slot="hover-content">
                <div class="d-flex align-center">
                  <Logo :type="item.type" :size="18" />
                  <span class="ml-2">{{ item.type | TitleCase }}</span>
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
                    >mdi-dots-vertical</v-icon
                  >
                </template>
                <v-list class="menu-list-wrapper">
                  <v-list-item-group>
                    <v-list-item
                      v-for="item in items"
                      :key="item.id"
                      :disabled="!item.active"
                    >
                      <v-list-item-title>{{ item.title }}</v-list-item-title>
                    </v-list-item>
                  </v-list-item-group>
                </v-list>
              </v-menu>
            </span>
          </div>
        </v-list-item-content>
        <v-list-item-content class="status-col py-1" v-if="item.status">
          <status :status="item.status" collapsed showLabel />
        </v-list-item-content>
        <v-list-item-content class="size-col py-1" v-if="item.size">
          <tooltip>
            <template slot="label-content">
              {{ getSize(item.size) }}
            </template>
            <template slot="hover-content">
              {{ item.size | FormatSize }}
            </template>
          </tooltip>
        </v-list-item-content>
        <v-list-item-content
          class="deliverdOn-col py-1"
          v-if="item.lastDeliveredOn"
        >
          <tooltip>
            <template slot="label-content">
              {{ getTimeStamp(item.lastDeliveredOn) }}
            </template>
            <template slot="hover-content">
              {{ item.lastDeliveredOn | Date | Empty }}
            </template>
          </tooltip>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script>
import Logo from "./Logo.vue"
import Status from "./Status.vue"
import { getApproxSize } from "@/utils"
import moment from "moment"
import Tooltip from "./Tooltip.vue"

export default {
  components: { Logo, Status, Tooltip },
  name: "StatusList",
  data() {
    return {
      items: [
        { id: 1, title: "Deliver now", active: true },
        { id: 2, title: "Create lookalike", active: false },
        { id: 3, title: "Edit delivery schedule", active: false },
        { id: 4, title: "Pause delivery", active: false },
        { id: 5, title: "Open destination", active: false },
        { id: 6, title: "Remove destination", active: false },
      ],
      topNavItems: [
        { id: 1, title: "Deliver now", active: true },
        { id: 2, title: "Add a destination", active: true },
        { id: 3, title: "Create lookalike", active: false },
        { id: 4, title: "Pause all delivery", active: false },
        { id: 5, title: "Remove audience", active: false },
      ],
    }
  },
  props: {
    audience: {
      title: Object,
      required: true,
    },
  },
  methods: {
    getSize(value) {
      return getApproxSize(value)
    },
    getTimeStamp(value) {
      return moment(new Date(value)).fromNow()
    },
    toggleFocus() {},
  },
}
</script>

<style lang="scss" scoped>
.status-card {
  min-width: 310px;
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
