<template>
  <div
    :style="{ 'background-color': bgColor }"
    class="page-header--wrap d-flex justify-space-between align-center"
  >
    <div class="page-header--left">
      <div class="page-header-container d-flex">
        <v-icon size="20" color="black">
          {{ icon }}
        </v-icon>
        <div class="page-header-title pl-1">
          {{ title }}
        </div>
      </div>
      <div class="page-header-description">
        <slot name="description"></slot>
      </div>
      <slot name="left"></slot>
    </div>
    <div class="page-header--right">
      <slot name="right"></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: "PageHeader",

  props: {
    icon: {
      type: String,
      required: false,
    },

    title: {
      type: String,
      required: false,
    },

    bgColor: {
      type: String,
      required: false,
      default: "white",
    },
  },
}
</script>

<style lang="scss" scoped>
.page-header--wrap {
  padding: 20px 30px;
  .page-header--left {
    .page-header-title {
      font-size: 24px;
      font-weight: 600;
      line-height: 40px;
    }
    .page-header-description {
      font-size: 14px;
      line-height: 22px;
    }
  }
}
</style>
