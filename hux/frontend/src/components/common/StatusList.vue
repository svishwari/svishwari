<template>
  <v-card class="rounded-sm status-card mr-2">
    <v-card-title class="d-flex justify-space-between">
      <span>{{ title }}</span>
      <v-menu class="menu-wrapper" bottom offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-icon v-bind="attrs" v-on="on" class="top-action">mdi-dots-vertical</v-icon>
        </template>
        <v-list class="menu-list-wrapper">
          <v-list-item-group>
            <v-list-item
              v-for="(item, index) in topNavItems"
              :key="index"
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
        v-for="(item, index) in destinations"
        :key="`dest-${index}`"
        @click="toggleFocus()"
      >
        <v-list-item-content class="icon-col py-1">
          <div class="d-flex align-center">
            <Logo :type="item.type" :size="18" />
            <v-spacer></v-spacer>
            <span class="action-icon font-weight-light float-right d-none">
              <v-menu class="menu-wrapper" bottom offset-y>
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                    v-bind="attrs"
                    v-on="on"
                    class="mr-2 more-action"
                    color="primary"
                    @click="takeActions($event)"
                    >mdi-dots-vertical</v-icon
                  >
                </template>
                <v-list class="menu-list-wrapper">
                  <v-list-item-group>
                    <v-list-item
                      v-for="(item, index) in items"
                      :key="index"
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
        <v-list-item-content class="status-col py-1">
          <status :status="item.status" :showLabel="false" />
        </v-list-item-content>
        <v-list-item-content class="size-col py-1">
          {{ getSize(item.size) }}
        </v-list-item-content>
        <v-list-item-content class="deliverdOn-col py-1">{{
          getTimeStamp(item.lastDeliveredOn)
        }}</v-list-item-content>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script>
import Logo from "./Logo.vue";
import Status from "./Status.vue";
import { getApproxSize } from "@/utils";
import moment from "moment";

export default {
  components: { Logo, Status },
  Statusame: "StatusList",
  data() {
    return {
      items: [
        { title: "Deliver now", active: true },
        { title: "Create lookalike", active: false },
        { title: "Edit delivery schedule", active: false },
        { title: "Pause delivery", active: false },
        { title: "Open destination", active: false },
        { title: "Remove destination", active: false },
      ],
      topNavItems: [
        { title: "Deliver now", active: true },
        { title: "Add a destination", active: true },
        { title: "Create lookalike", active: false },
        { title: "Pause all delivery", active: false },
        { title: "Remove audience", active: false },
      ],
    };
  },
  props: {
    title: {
      title: String,
      required: true,
    },
    destinations: {
      type: Array,
      default: () => [],
      required: true,
    },
  },
  methods: {
    getSize(value) {
      return getApproxSize(value);
    },
    getTimeStamp(value) {
      return moment(new Date(value)).fromNow();
    },
    takeActions(evnt) {
      evnt.preventDefault();
    },
    toggleFocus(event) {},
  },
};
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
    background: #f9fafb;
    border-radius: 12px 12px 0px 0px;
    font-size: 14px;
    line-height: 22px;
    color: #005587;
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
      }
      .status-col {
        min-width: 45px;
      }
      .size-col {
        min-width: 80px;
        font-size: 12px;
        line-height: 16px;
        color: var(--v--neroBlack-base);
      }
      .deliverdOn-col {
        font-size: 12px;
        line-height: 16px;
        color: #1e1e1e;
        min-width: 80px;
      }
      &:hover,
      &:focus {
        background: #ffffff;
        box-shadow: 0px 1px 5px rgba(0, 0, 0, 0.25);
        .action-icon {
          display: block !important;
        }
      }
    }
  }
  .menu-list-wrapper {
    background: red;
  }
}
::v-deep.v-menu__content {
  .v-list-item {
    &.theme--light {
      min-height: 32px !important;
      font-size: 14px;
      line-height: 22px;
      color: #1e1e1e;
      &.v-list-item--disabled {
        color: #d0d0ce;
      }
      &:hover {
        background: var(--v-aliceBlue-base);
      }
    }
  }
}
</style>
