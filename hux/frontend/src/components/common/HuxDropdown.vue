<template>
  <div class="hux-dropdown">
    <v-menu
      :close-on-content-click="false"
      :offset-x="isOffsetX"
      :offset-y="isOffsetY"
      :open-on-hover="isOpenOnHover"
      :transition="transition"
      close-on-click
      v-model="openMenu"
      class="hux-dropdown"
    >
      <template #activator="{ on }">
        <v-list-item
          v-if="isSubMenu"
          class="d-flex justify-space-between pr-1"
          v-on="on"
        >
          {{ label }}
          <div class="flex-grow-1"></div>
          <v-icon color="primary">mdi-chevron-right</v-icon>
        </v-list-item>
        <huxButton
          v-else
          :v-on="on"
          @click="openMenu = true"
          text
          width="200"
          icon=" mdi-chevron-down"
          iconPosition="right"
          tile
          class="ma-2 main-button pr-1"
        >
          {{ isSubMenu ? item.name : optionSelected["name"] || label }}
        </huxButton>
      </template>
      <v-list>
        <template v-for="(item, index) in items">
          <div class="dropdown-menuitems" :key="index">
            <v-divider v-if="item.isDivider" :key="index" />
            <div
              v-if="item.isGroup"
              :key="item.name"
              class="group_title px-4 d-flex align-center"
            >
              {{ item.name }}
            </div>
            <hux-dropdown
              v-else-if="item.menu"
              :key="index"
              :label="item.name"
              :items="item.menu"
              @on-select="onSelect"
              :is-open-on-hover="false"
              :is-offset-x="true"
              :is-offset-y="false"
              :is-sub-menu="true"
              :selected="selected"
            />
            <v-list-item v-else :key="index" @click="onSelect(item)">
              <v-list-item-title class="d-flex align-center">
                <v-icon
                  :color="color"
                  size="16"
                  v-if="optionSelected.name == item.name"
                  >mdi-check</v-icon
                >
                <v-icon v-if="item.icon">{{ item.icon }}</v-icon>
                <icon type="model" :size="21" v-if="item.modelIcon" />
                {{ item.name }}
              </v-list-item-title>
            </v-list-item>
          </div>
        </template>
      </v-list>
    </v-menu>
  </div>
</template>
<script>
import huxButton from "@/components/common/huxButton"
import Icon from "./Icon.vue"
export default {
  name: "hux-dropdown",
  components: {
    huxButton,
    Icon,
  },
  computed: {
    optionSelected() {
      return this.selected || this.label
    },
  },
  props: {
    selected: {
      type: [Object, String],
    },
    label: {
      type: String,
      required: false,
      default: "Select Option",
    },
    icon: String,
    items: Array,
    color: { type: String, default: "primary" },
    isOffsetX: { type: Boolean, default: false },
    isOffsetY: { type: Boolean, default: true },
    isOpenOnHover: { type: Boolean, default: false },
    isSubMenu: { type: Boolean, default: false },
    transition: { type: String, default: "scale-transition" },
  },
  methods: {
    onSelect(item) {
      this.$emit("on-select", item)
      this.openMenu = false
    },
  },
  data: function () {
    return {
      openMenu: this.value,
    }
  },
}
</script>

<style lang="scss" scoped>
.hux-dropdown {
  .main-button {
    height: 32px;
    min-width: 64px;
    padding: 0 16px;
    border-style: solid !important;
    border-width: 1px;
    border-color: var(--v-lightGrey-base) !important;
    border-radius: 0;
    box-shadow: none !important;
    background-color: var(--v-white-base) !important;
    background: var(--v-white-base) !important;
    font-size: 14px;
    line-height: 22px;
    width: auto !important;
    min-width: 200px;
    color: var(--v-neroBlack-base);
    ::v-deep .v-btn__content {
      .spacer {
        &:nth-child(2) {
          display: none;
        }
      }
      .v-icon {
        color: var(--v-primary-base);
      }
    }
  }
}
.dropdown-menuitems {
  min-width: 230px;
  font-size: 14px;
  line-height: 22px !important;

  color: var(--v-neroBlack-base);
  .v-list-item {
    min-height: 32px;
    .v-list-item__title {
      line-height: 22px !important;
    }
  }
  .group_title {
    text-transform: uppercase;
    color: var(--v-gray-base);
  }
}
</style>
