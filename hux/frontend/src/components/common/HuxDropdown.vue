<template>
  <div class="hux-dropdown">
    <v-menu
      v-model="openMenu"
      :close-on-content-click="false"
      :offset-x="isOffsetX"
      :offset-y="isOffsetY"
      :open-on-hover="isOpenOnHover"
      :transition="transition"
      close-on-click
      class="hux-dropdown"
    >
      <template #activator="{ on }">
        <v-list-item
          v-if="isSubMenu"
          class="d-flex justify-space-between pr-1 text-body-1"
          v-on="on"
        >
          <icon v-if="modelIcon" :type="modelIcon" :size="21" class="ml-n1" />
          {{ label }}
          <div class="flex-grow-1"></div>
          <v-icon color="primary">mdi-chevron-right</v-icon>
        </v-list-item>
        <huxButton
          v-else
          :v-on="on"
          text
          width="200"
          icon=" mdi-chevron-down"
          icon-position="right"
          tile
          class="ma-2 main-button pr-1 text-body-1"
          :style="{ width: minWidth + 'px !important' }"
          @click="openMenu = true"
        >
          <tooltip v-if="showHover">
            <template #label-content>
              <logo
                v-if="dropIcon"
                :type="dropIcon"
                class="mr-2 mt-1"
                :size="20"
              ></logo>
              <span class="text-ellipsis text-width">{{
                isSubMenu ? item.name : optionSelected["name"] || label
              }}</span>
            </template>
            <template #hover-content>
              {{ isSubMenu ? item.name : optionSelected["name"] || label }}
            </template>
          </tooltip>
          <span v-else class="text-ellipsis text-width">{{
            isSubMenu ? item.name : optionSelected["name"] || label
          }}</span>
        </huxButton>
      </template>
      <v-list>
        <template v-for="(item, index) in items">
          <div :key="index" class="dropdown-menuitems">
            <v-divider v-if="item.isDivider" :key="index" />
            <div
              v-if="item.isGroup"
              :key="item.name"
              :class="{
                'group_title px-4 d-flex align-center': true,
                'mt-2': index != 0,
              }"
            >
              {{ item.name }}
            </div>
            <hux-dropdown
              v-else-if="item.menu || item.metricOptions"
              :key="index"
              :label="item.name"
              :items="item.menu || item.metricOptions"
              :is-open-on-hover="false"
              :is-offset-x="true"
              :is-offset-y="false"
              :is-sub-menu="true"
              :model-icon="item.modelIcon"
              :selected="selected"
              @on-select="onSelect"
            />
            <v-list-item v-else :key="index" @click="onSelect(item)">
              <v-list-item-title class="d-flex align-center">
                <v-icon
                  v-if="optionSelected.name == item.name"
                  :color="color"
                  size="16"
                  >mdi-check</v-icon
                >
                <logo v-if="item.type" :type="item.type" :size="20"></logo>
                <v-icon v-if="item.icon">{{ item.icon }}</v-icon>
                <icon
                  v-if="item.modelIcon"
                  type="model"
                  :size="21"
                  class="ml-n1"
                />
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
import Tooltip from "@/components/common/Tooltip.vue"
import Logo from "@/components/common/Logo"

export default {
  name: "HuxDropdown",
  components: {
    huxButton,
    Icon,
    Tooltip,
    Logo,
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
    modelIcon: { type: String, required: false, default: "" },
    transition: { type: String, default: "scale-transition" },
    minWidth: {
      type: String,
      required: false,
      default: "200",
    },
    dropIcon: {
      type: String,
      required: false,
      default: "",
    },
    showHover: {
      type: Boolean,
      required: false,
      default: true,
    },
  },
  data: function () {
    return {
      openMenu: this.value,
    }
  },
  computed: {
    optionSelected() {
      return this.selected || this.label
    },
  },
  methods: {
    onSelect(item) {
      if (item.model) {
        item.model.selected = item.key
      }
      this.$emit("on-select", item)
      this.openMenu = false
    },
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
    border-color: var(--v-black-lighten3) !important;
    border-radius: 4px;
    box-shadow: none !important;
    background-color: var(--v-white-base) !important;
    background: var(--v-white-base) !important;
    font-size: 16px !important;
    line-height: 22px !important;
    font-weight: 400 !important;
    width: auto !important;
    min-width: 200px;
    color: var(--v-black-darken4);
    ::v-deep .v-btn__content {
      top: 1px;
      .spacer {
        &:nth-child(2) {
          display: none;
        }
      }
      .v-icon {
        top: -1px;
        color: var(--v-primary-base);
      }
    }
  }
}
.dropdown-menuitems {
  min-width: 230px;
  font-size: 14px;
  line-height: 22px !important;

  color: var(--v-black-darken4);
  .v-list-item {
    min-height: 32px;
    .v-list-item__title {
      line-height: 22px !important;
    }
  }
  .group_title {
    text-transform: uppercase;
    color: var(--v-black-lighten4);
  }
}
.text-width {
  width: 150px;
  text-align: left;
}
</style>
