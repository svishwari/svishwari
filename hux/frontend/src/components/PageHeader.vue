<template>
  <v-card
    class="page-header--wrap d-flex justify-space-between align-center px-8 py-5"
    elevation="1"
    tile
    :color="bgColor"
    :height="headerHeight"
  >
    <div>
      <div class="d-flex">
        <v-icon v-if="icon" class="pr-1" size="20" color="black">
          {{ icon }}
        </v-icon>
        <div class="text-h2">
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
      required: false,
      default: "white",
    },

    headerHeight: {
      type: Number,
      required: false,
      default: undefined,
    },
  },
}
</script>
