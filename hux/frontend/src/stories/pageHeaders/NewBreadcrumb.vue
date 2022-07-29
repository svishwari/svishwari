<template>
  <v-breadcrumbs :items="items" class="pl-0 breadcrumb">
    <template #item="{ item }">
      <v-breadcrumbs-item
        exact
        :to="item.href"
        :disabled="item.disabled"
        class="font-weight-light"
      >
        <div v-if="item.status" class="d-flex pr-2">
          <status
            :status="item.status"
            :icon-size="item.statusSize ? item.statusSize : 21"
            collapsed
          ></status>
        </div>
        <div v-if="item.icon" class="d-flex pr-2">
          <icon
            :type="item.icon"
            :size="item.iconSize ? item.iconSize : 40"
            :color="item.iconColor ? item.iconColor : 'black-darken4'"
            :variant="item.iconColorVariant ? item.iconColorVariant : 'base'"
          />
        </div>
        <div v-if="item.logo" class="d-flex pr-2">
          <logo
            :type="item.logo"
            :size="40"
            :class="
              addBorder & reduceIcon
                ? 'addBorder br-50 pa-1 allow-overflow'
                : addBorder
                ? 'addBorder br-50'
                : reduceIcon
                ? 'padding-4'
                : ''
            "
          />
        </div>
        <div v-if="item.error" class="d-flex mr-2 mt-1">
          <icon
            type="Error & Warning"
            :size="20"
            color="white-base"
            bg-color="error-lighten1"
            class="circle"
          ></icon>
        </div>
        <span
          :class="{
            'blue--text': item.disabled,
            'pl-1 new-h1 title-up': true,
          }"
        >
          {{ item.text }}
          <sup class="title-superscript">
            {{ item.superscript }}
          </sup>
        </span>
        <div v-if="item.favorite" class="d-flex pl-2 mt-1">
          <icon type="Favorite" :size="20" color="white-base"></icon>
        </div>
      </v-breadcrumbs-item>
    </template>
    <template #divider>
      <icon
        type="Dropdown - right"
        :size="24"
        class="mr-2 ml-2 mt-1"
        color="primary-lighten7"
      />
    </template>
  </v-breadcrumbs>
</template>

<script>
import Icon from "../icons/Icon2.vue"
import Logo from "../logos/Logo.vue"
import Status from "../status/Status2.vue"

export default {
  name: "Breadcrumb",

  components: { Icon, Logo, Status },

  props: {
    items: {
      type: Array,
      required: true,
      default: () => [],
    },
    addBorder: {
      type: Boolean,
      required: false,
      default: false,
    },
    reduceIcon: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
}
</script>
<style lang="scss" scoped>
.breadcrumb {
  cursor: text;
  ::v-deep .v-breadcrumbs__divider {
    padding: 0;
  }
  ::v-deep .v-breadcrumbs__item--disabled {
    color: var(--v-black-darken4);
  }
  ::v-deep a {
    color: var(--v-primary-base) !important;
  }
  .addBorder {
    border: 1px solid var(--v-black-lighten2);
  }
  .allow-overflow {
    overflow: clip;
  }
}
.title-superscript {
  @extend .superscript;
  font-size: 8px;
  left: -8px;
  top: -18px;
}
.blue--text {
  color: #007cb0 !important;
}
.circle {
  border-radius: 50%;
}
</style>
