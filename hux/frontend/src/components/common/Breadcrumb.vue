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
            :size="item.iconSize ? item.iconSize : 32"
            :color="item.iconColor ? item.iconColor : 'black-darken4'"
            :variant="item.iconColorVariant ? item.iconColorVariant : 'base'"
          />
        </div>
        <div v-if="item.logo" class="d-flex pr-2">
          <logo
            :type="item.logo"
            :size="32"
            :class="
              addBorder & reduceIcon
                ? 'addBorder br-50 pa-1'
                : addBorder
                ? 'addBorder br-50'
                : reduceIcon
                ? 'padding-4'
                : ''
            "
          />
        </div>
        <span
          :class="{
            'black--text': item.disabled,
            'pl-1 text-h1': true,
          }"
        >
          {{ item.text }}
          <sup class="superscript">
            {{ item.superscript }}
          </sup>
        </span>
      </v-breadcrumbs-item>
    </template>
    <template #divider>
      <icon type="side-arrow" :size="14" color="primary" class="mx-5 mt-1" />
    </template>
  </v-breadcrumbs>
</template>

<script>
import Icon from "@/components/common/Icon"
import Logo from "@/components/common/Logo"
import Status from "@/components/common/Status.vue"

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
  ::v-deep .v-breadcrumbs__divider {
    padding: 0;
  }
  ::v-deep .v-breadcrumbs__item--disabled {
    color: var(--v-black-darken4);
  }
  ::v-deep a {
    color: var(--v-primary-base) !important;
  }
}
.addBorder {
  border: 1px solid var(--v-black-lighten2);
}
.superscript {
  font-size: 8px;
  font-weight: bold;
  position: relative;
  left: -8px;
  top: -18px;
}
</style>
