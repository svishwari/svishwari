<template>
  <v-breadcrumbs :items="items" class="pl-0 breadcrumb">
    <template #item="{ item }">
      <v-breadcrumbs-item
        exact
        :to="item.href"
        :disabled="item.disabled"
        class="font-weight-light"
      >
        <div v-if="item.icon" class="d-flex pr-2">
          <icon :type="item.icon" :size="24" color="neroBlack" />
        </div>
        <div v-if="item.logo" class="d-flex pr-2">
          <logo :type="item.logo" :size="24" />
        </div>
        <span :class="{ 'neroBlack--text': item.disabled, 'pl-1': true }">
          {{ item.text }}
        </span>
      </v-breadcrumbs-item>
    </template>
    <template #divider>
      <v-icon size="21" color="primary">mdi-chevron-right</v-icon>
    </template>
  </v-breadcrumbs>
</template>

<script>
import Icon from "@/components/common/Icon"
import Logo from "@/components/common/Logo"
export default {
  name: "Breadcrumb",

  components: { Icon, Logo },

  props: {
    items: {
      type: Array,
      required: true,
      default: () => [],
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
    color: var(--v-neroBlack-base);
  }
  ::v-deep a {
    color: var(--v-primary-base) !important;
  }
}
</style>
