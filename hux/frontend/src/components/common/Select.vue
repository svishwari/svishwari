<template>
  <v-select
    v-model="selected"
    :items="items"
    :label="label"
    :menu-props="{
      contentClass: 'hux-select',
      offsetY: true,
      nudgeBottom: '5px',
    }"
    append-icon="mdi-chevron-down"
    background-color="white"
    dense
    hide-details="auto"
    outlined
    single-line
    :style="`max-width: ${width}px`"
  />
</template>

<script>
import { defineComponent, ref, watch } from "@vue/composition-api"

export default defineComponent({
  props: {
    value: {
      type: [String, Number, Boolean],
      required: false,
      default: null,
    },

    items: {
      type: Array,
      required: true,
    },

    label: {
      type: String,
      required: false,
      default: "",
    },

    width: {
      type: [String, Number],
      required: false,
      default: 141,
    },
  },

  setup(props, { emit }) {
    const selected = ref(props.value)

    watch(selected, (newSelection) => emit("input", newSelection))

    return {
      selected,
    }
  },
})
</script>

<style lang="sass" scoped>
.hux-select
  .v-select-list
    ::v-deep .v-list-item__title
      font-size: 14px
</style>
