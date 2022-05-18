<template>
  <v-card
    class="page-header--wrap d-flex justify-space-between align-center"
    :class="[headerPadding, headerHeightChanges]"
    flat
    tile
    :color="bgColor"
    :height="headerHeight"
    :min-height="headerMinHeight"
    :max-height="headerMaxHeight"
  >
    <div>
      <div class="d-flex">
        <icon
          v-if="icon"
          :type="showDemoHeader ? `${icon}_logo` : icon"
          class="pr-1"
          :size="showDemoHeader ? 40 : 20"
          color="black"
          variant="darken4"
        />
        <div v-if="title" class="text-h1 black--text" data-e2e="card-title">
          {{ title }}
        </div>
      </div>
      <div v-if="$slots.description" class="mt-2">
        <slot name="description"></slot>
      </div>
      <div v-if="$slots.left" class="black--text">
        <slot name="left"></slot>
      </div>
    </div>
    <div v-if="showDemoHeader" class="demo-header">
      <icon
        :type="`${icon}_header`"
        :custom-size="{ width: 240, height: 110 }"
        :enable-custom-size="true"
      />
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
    headerMinHeight: {
      type: String,
      required: false,
    },
    headerMaxHeight: {
      type: String,
      required: false,
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
    showDemoHeader: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
}
</script>

<style lang="scss" scoped>
.page-header--wrap {
  border-bottom: 1px solid var(--v-black-lighten3) !important;
  .demo-header {
    margin-right: -15%;
    height: inherit;
  }
}
</style>
