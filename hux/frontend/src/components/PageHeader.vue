<template>
  <v-card
    class="page-header--wrap d-flex justify-space-between align-center"
    :class="[headerPadding, headerHeightChanges]"
    flat
    tile
    :color="bgColor"
    :height="headerHeight"
  >
    <div>
      <div class="d-flex">
        <icon
          v-if="icon"
          :type="icon"
          class="pr-1"
          :size="20"
          color="black"
          variant="darken4"
        />
        <div class="text-h2" data-e2e="card-title">
          {{ title }}
        </div>
      </div>
      <div v-if="$slots.description" class="mt-2">
        <slot name="description"></slot>
      </div>
      <slot name="left"></slot>
    </div>
    <div class="page-header--right">
      <slot name="right"></slot>
    </div>
  </v-card>
</template>

<script>
import Icon from "./common/Icon"
export default {
  name: "PageHeader",
  components: {
    Icon,
  },
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
      required: false,
      default: "white",
    },

    headerHeight: {
      type: [Number, String],
      required: false,
      default: 72,
    },

    headerPadding: {
      type: String,
      required: false,
      default: "px-8",
    },

    headerHeightChanges: {
      type: String,
      required: false,
      default: "py-5",
    },
  },
}
</script>

<style lang="scss" scoped>
.page-header--wrap {
  border-bottom: 1px solid var(--v-black-lighten3) !important;
}
</style>
