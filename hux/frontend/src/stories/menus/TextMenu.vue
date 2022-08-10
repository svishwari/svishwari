<template>
  <div class="hux-dropdown">
    <v-menu
      v-model="openMenu"
      :close-on-content-click="false"
      :offset-x="isOffsetX"
      :offset-y="isOffsetY"
      :open-on-hover="isOpenOnHover"
      :transition="transition"
      :disabled="isDisabled"
      close-on-click
      class="hux-dropdown"
    >
      <template #activator="{ on }">
        <v-list-item
          v-if="isSubMenu"
          class="d-flex justify-space-between pr-1 new-b1"
          v-on="on"
        >
          {{ label }}
          <div class="flex-grow-1"></div>
          <v-icon color="primary">mdi-chevron-right</v-icon>
        </v-list-item>
        <huxButton
          v-else-if="!isDisabled && type == 'inline'"
          :v-on="on"
          text
          width="200"
          :icon="dropDownIcon"
          icon-position="right"
          tile
          class="ma-2 main-button pr-1 new-b1"
          :style="{
            width: minWidth + 'px !important',
            borderWidth: borderWidth,
            color: dropdownColor,
          }"
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
              <span class="text-ellipsis new-h4 text-width">{{
                isSubMenu ? item.name : optionSelected["name"] || label
              }}</span>
            </template>
            <template #hover-content>
              {{ isSubMenu ? item.name : optionSelected["name"] || label }}
            </template>
          </tooltip>
          <span v-else class="text-ellipsis new-h4 text-width">{{
            isSubMenu ? item.name : optionSelected["name"] || label
          }}</span>
        </huxButton>
        <huxButton
          v-else-if="isDisabled && type == 'inline'"
          text
          width="200"
          :icon="dropDownIcon"
          icon-position="right"
          tile
          class="ma-2 main-disabled-button pr-1 new-b1"
          :style="{
            width: minWidth + 'px !important',
            borderWidth: borderWidth,
            color: 'var(--v-black-lighten5) !important',
          }"
        >
          <span class="text-ellipsis new-h4 text-width">{{ label }}</span>
        </huxButton>
        <v-icon
          v-else-if="type == 'hotdog'"
          class="hotdog-menu-button"
          :style="{
            color: dropdownColor,
          }"
          size="40"
          @click="openMenu = true"
        >
          mdi-dots-vertical
        </v-icon>
        <v-chip
          v-else
          class="pill-menu-button"
          :style="{
            background: dropdownColor,
          }"
          text-color="white"
          @click="openMenu = true"
        >
          <span class="ma-0 new-pills subtitle-2">{{ label }}</span>
          <v-icon right> {{ dropDownIcon }} </v-icon>
        </v-chip>
      </template>
      <v-list class="py-0">
        <v-list-item v-if="isHeader" class="header-class new-b2">
          <slot name="header" />
        </v-list-item>
        <template v-for="(item, index) in items">
          <div :key="index" class="dropdown-menuitems new-b1">
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
            <text-menu
              v-else-if="item.menu"
              :key="index"
              :label="item.name"
              :items="item.menu"
              :is-open-on-hover="false"
              :is-offset-x="true"
              :is-offset-y="false"
              :is-sub-menu="true"
              :is-header="false"
              :is-footer="false"
              :selected="selected"
              @on-select="onSelect"
            />
            <v-list-item v-else :key="index" @click="onSelect(item)">
              <v-list-item-title class="d-flex align-center">
                <logo
                  v-if="item.type"
                  class="mr-2"
                  :type="item.type"
                  :size="22"
                ></logo>
                <v-icon v-if="item.icon" class="mr-2">{{ item.icon }}</v-icon>
                <icon v-if="item.modelIcon" type="model" :size="22" />
                {{ item.name }}
              </v-list-item-title>
            </v-list-item>
          </div>
        </template>
      </v-list>
      <v-list-item v-if="isFooter" class="footer-class new-b3">
        <slot name="footer" />
      </v-list-item>
    </v-menu>
  </div>
</template>
<script>
import huxButton from "@/components/common/huxButton"
import Icon from "@/components/common/Icon.vue"
import Tooltip from "@/components/common/Tooltip.vue"
import Logo from "@/components/common/Logo"

export default {
  name: "TextMenu",
  components: {
    huxButton,
    Icon,
    Tooltip,
    Logo,
  },
  props: {
    type: {
      type: String,
      required: false,
      default: "inline",
    },
    selected: {
      type: [Object, String],
    },
    label: {
      type: String,
      required: false,
      default: "Select Option",
    },
    isBorder: {
      type: Boolean,
      required: false,
      default: true,
    },
    icon: String,
    items: Array,
    color: { type: String, default: "primary" },
    isOffsetX: { type: Boolean, default: false },
    isOffsetY: { type: Boolean, default: true },
    isOpenOnHover: { type: Boolean, default: false },
    isSubMenu: { type: Boolean, default: false },
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
    isDisabled: {
      type: Boolean,
      required: false,
      default: false,
    },
    isHeader: {
      type: Boolean,
      required: false,
      default: false,
    },
    isFooter: {
      type: Boolean,
      required: false,
      default: false,
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
    dropdownColor() {
      return this.isDisabled
        ? "var(--v-black-lighten5) !important"
        : this.openMenu
        ? "var(--v-primary-base) !important"
        : "var(--v-primary-lighten7) !important"
    },
    borderWidth() {
      return this.isBorder ? "1px" : "0px"
    },
    dropDownIcon() {
      return this.openMenu ? "mdi-chevron-up" : "mdi-chevron-down"
    },
  },
  methods: {
    onSelect(item) {
      this.$emit("on-select", item)
      this.openMenu = false
    },
  },
}
</script>

<style lang="scss" scoped>
.hux-dropdown {
  .main-button {
    @extend .new-h4;
    height: 32px;
    padding: 0 16px;
    border-style: solid !important;
    border-width: 1px;
    border-color: var(--v-black-lighten3) !important;
    border-radius: 4px;
    box-shadow: none !important;
    background-color: var(--v-white-base) !important;
    background: var(--v-white-base) !important;
    width: auto !important;
    min-width: 200px;
    color: var(--v-primary-lighten7) !important;
    &:hover {
      color: var(--v-primary-base) !important;
    }
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
.main-disabled-button {
  color: var(--v-black-lighten5) !important;
  &:hover {
    color: var(--v-black-lighten5) !important;
  }
  @extend .main-button;
  ::v-deep .v-btn__content {
    .text-width {
      position: relative;
      bottom: 2px !important;
    }
    .v-icon {
      color: var(--v-black-lighten5) !important;
    }
  }
}
.hotdog-menu-button {
  color: var(--v-primary-lighten7) !important;
  &:hover {
    color: var(--v-primary-base) !important;
  }
  &::after {
    background: var(--v-black-base) !important;
    transform: scale(1) !important;
  }
}
.pill-menu-button {
  background: var(--v-primary-lighten7) !important;
  &:hover {
    background: var(--v-primary-base) !important;
  }
  ::v-deep .v-chip__content {
    .v-icon {
      color: var(--v-white-base);
    }
  }
}
.dropdown-menuitems {
  min-width: 230px;
  font-size: 16px;
  line-height: 24px !important;

  color: var(--v-black-darken4);
  .v-list-item {
    min-height: 40px;
    &:hover::before {
      opacity: 0.03 !important;
    }
    .v-list-item__title {
      line-height: 24px !important;
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
::v-deep .header-class {
  color: var(--v-black-base);
}
::v-deep .footer-class {
  border-top: 1px solid var(--v-black-lighten1);
  background-color: var(--v-black-lighten7);
  color: var(--v-primary-lighten7) !important;
}
</style>
