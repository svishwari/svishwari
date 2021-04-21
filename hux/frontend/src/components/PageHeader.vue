<template>
  <v-card
    class="page-header--wrap d-flex justify-space-between align-center px-8 py-5"
    elevation="1"
    tile
    :color="bgColor"
  >
    <div>
      <div class="page-header-container d-flex">
        <v-icon size="20" color="black">
          {{ icon }}
        </v-icon>
        <div class="text-h5 pl-1">
          {{ title }}
        </div>
      </div>
      <div>
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
  },
}
</script>
