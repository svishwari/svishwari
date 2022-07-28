<template>
  <v-container class="header-container">
    <v-row class="header-title" :class="description ? '' : 'pb-4'">
      <div class="title-left new-h1">
        <icon :type="iconType" :size="40" color="primary" class="mr-2"></icon>
        <span :class="maxBreadcrumbs != 'None' ? 'mr-2 blue--text' : 'mr-2'">{{
          title
        }}</span>
        <icon
          v-if="titleFavorite"
          type="Favorite"
          size="20"
          color="white-base"
          class="mt-1 mr-2 ml-1"
        ></icon>
        <icon
          v-if="maxBreadcrumbs != 'None'"
          type="Dropdown - right"
          :size="24"
          class="mr-2 mt-1"
          color="primary-lighten7"
        ></icon>
        <slot name="breadcrumbs" />
      </div>
      <v-spacer />
      <div class="title-right new-b3">
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
    titleFavorite: {
      type: Boolean,
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
    padding: 0px 32px 16px;
    line-height: 24px;
    margin-top: 8px;
  }
  .blue--text {
    color: #007cb0 !important;
  }
}
</style>
