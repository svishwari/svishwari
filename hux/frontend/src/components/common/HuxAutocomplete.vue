<template>
  <v-autocomplete
    v-model="localValue"
    :items="localItems"
    item-value="value"
    item-text="text"
    solo
    :height="32"
  ></v-autocomplete>
</template>

<script>
import { defineComponent, computed } from "@vue/composition-api"

export default defineComponent({
  props: {
    value: {
      type: String,
      required: false,
      default: null,
    },
    options: {
      type: Array,
      required: true,
      default: () => [],
    },
  },
  emits: ["input", "change"],
  setup(props, { emit }) {
    const localValue = computed({
      get: () => props.value,
      set: (value) => {
        emit("input", value)
        emit("change", value)
      },
    })

    const localItems = computed({
      get() {
        return props.options.map((obj) => {
          const _key = Object.keys(obj)[0]
          return {
            value: _key,
            text: obj[_key],
          }
        })
      },
    })

    return {
      localValue,
      localItems,
    }
  },
})
</script>

<style lang="scss" scoped></style>
