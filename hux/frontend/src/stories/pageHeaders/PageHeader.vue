<template>
  <v-container class="header-container">
    <v-row class="header-title" :class="description ? '' : 'pb-4'">
      <div class="title-left text-h1">
        <icon :type="iconType" :size="38" class="mr-2" color="primary"></icon>
        <span class="mr-2">{{ title }}</span>
        <icon
          v-if="$slots.breadcrumbs"
          type="arrow"
          :size="18"
          color="primary"
          class="mr-2"
        ></icon>
        <slot name="breadcrumbs" />
      </div>
      <v-spacer />
      <div class="title-right">
        <slot name="call-to-action" />
      </div>
    </v-row>
    <v-row
      v-if="description"
      class="header-description text-body-1"
      align="center"
    >
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
  },
}
</script>

<style lang="scss" scoped>
.header-container {
  background-color: lightblue;

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
    height: 32px;
    padding: 0px 32px 16px;
  }
}
</style>
