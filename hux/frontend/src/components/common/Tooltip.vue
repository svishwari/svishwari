<template>
  <v-menu
    :top="positionTop"
    offset-y
    open-on-hover
    :content-class="contentClass"
    :max-width="maxWidth"
    :min-width="minWidth"
    :nudge-right="nudgeRight"
  >
    <template #activator="{ on }">
      <span v-on="on">
        <slot name="label-content"></slot>
        <slot name="default"></slot>
      </span>
    </template>
    <div class="px-4 py-2 white text-h5">
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
    contentClass: {
      type: String,
      required: false,
      default: "",
    },
    maxWidth: {
      type: [String, Number],
      required: false,
      default: "auto",
    },
    minWidth: {
      type: [String, Number],
      required: false,
      default: undefined,
    },
    nudgeRight: {
      type: [String, Number],
      required: false,
      default: 0,
    },
  },
}
</script>
