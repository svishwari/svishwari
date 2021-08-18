<template>
  <v-menu :top="positionTop" offset-y open-on-hover>
    <template #activator="{ on }">
      <span class="d-inline-flex align-center" v-on="on">
        <slot name="label-content"></slot>
        <slot name="default"></slot>
      </span>
    </template>
    <div class="px-4 py-2 white caption">
      <slot name="hover-content"></slot>
      <slot name="tooltip"></slot>
    </div>
  </v-menu>
</template>

<script>
export default {
  name: "Tooltip",
  props: {
    positionTop: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
}
</script>
