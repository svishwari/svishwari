<template>
  <v-row class="menu-cell-wrapper">
    <v-col class="d-flex pr-0">
      <router-link :to="routePath" class="text-decoration-none" append>
        <tooltip>
          <template slot="label-content">
            <span class="primary--text ellipsis"> {{ value }} </span>
          </template>
          <template slot="hover-content">
            {{ value }}
          </template>
        </tooltip>
      </router-link>
      <v-spacer></v-spacer>
      <span class="action-icon font-weight-light float-right">
        <v-menu class="menu-wrapper" bottom offset-y>
          <template #activator="{ on, attrs }">
            <v-icon
              v-bind="attrs"
              v-on="on"
              class="mr-2 more-action"
              color="primary"
              @click="takeActions($event)"
            >
              mdi-dots-vertical
            </v-icon>
          </template>
          <v-list class="list-wrapper">
            <v-list-item-group>
              <v-list-item
                v-for="(item, index) in menuOptions"
                :key="index"
                disabled
              >
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-menu>
      </span>
    </v-col>
  </v-row>
</template>
<script>
import Vue from "vue"
import Tooltip from "../Tooltip.vue"
export default Vue.extend({
  name: "MenuCell",
  components: {
    Tooltip,
  },
  props: {
    navigateTo: {
      type: Object,
      required: false,
    },
    value: {
      type: String,
      required: true,
    },
    menuOptions: {
      type: Array,
      required: false,
      default: () => [],
    },
    routeName: {
      type: String,
      required: true,
    },
    routeParam: {
      type: String,
      required: true,
    },
  },
  computed: {
    routePath() {
      return {
        name: this.routeName,
        params: { id: this.routeParam },
      }
    },
  },
  methods: {
    takeActions(evnt) {
      evnt.preventDefault()
    },
  },
})
</script>
<style lang="scss" scoped>
::v-deep.v-menu__content {
  .v-list-item {
    &.theme--light {
      min-height: 32px !important;
    }
  }
}
.menu-cell-wrapper {
  .ellipsis {
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 31ch;
    display: inline-block;
    width: 31ch;
    white-space: nowrap;
  }
  :hover {
    .action-icon {
      display: block;
    }
  }
}
</style>
