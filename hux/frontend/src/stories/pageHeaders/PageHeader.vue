<template>
  <v-container class="header-container">
    <v-row class="header-title" :class="description ? '' : 'pb-4'">
      <div class="title-left text-h2">
        <icon :type="iconType" :size="40" color="primary" class="mr-2"></icon>
        <span class="mr-2">{{ title }}</span>
        <icon
          v-if="titleIcon"
          :type="titleIconSel"
          :size="40"
          color="primary"
          class="mr-2"
        ></icon>
        <icon
          v-if="maxBreadcrumbs != 'None'"
          type="Dropdown - right"
          :size="24"
          color="black"
          class="mr-2 mt-1"
        ></icon>
        <slot name="breadcrumbs" />
      </div>
      <v-spacer />
      <div class="title-right text-h3">
        <slot name="call-to-action" />
      </div>
    </v-row>
    <v-row v-if="description" class="header-description new-b1" align="center">
      {{ description }}
    </v-row>
  </v-container>
</template>

<script>
import Icon from "../icons/Icon2.vue"
export default {
  name: "PageHeader",
  components: { Icon },
  props: {
    iconType: {
      type: String,
      required: true,
    },
    title: {
      type: String,
      required: true,
      default: "Title",
    },
    description: {
      type: String,
      required: false,
    },
    titleIconSel: {
      type: String,
      required: false,
    },
    titleIcon: {
      type: Boolean,
      required: true,
    },
    maxBreadcrumbs: {
      type: String,
      required: true,
    },
  },
}
</script>

<style lang="scss" scoped>
.header-container {
  border-bottom: 1px solid #dddddd;
  color: #1e1e1e;

  .header-title {
    height: 72px;
    padding: 16px 32px 8px;
  }

  .title-left {
    display: flex;
    align-items: center;
  }

  .title-right {
    display: flex;
    align-items: center;
  }

  .header-description {
    min-height: 32px;
    padding: 0px 32px 16px;
    line-height: 24px;
    margin-top: 8px;
  }
}
</style>
