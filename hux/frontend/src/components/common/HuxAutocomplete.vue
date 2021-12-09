<template>
  <v-autocomplete
    v-model="localValue"
    :items="localItems"
    item-value="value"
    item-text="text"
    append-icon="mdi-chevron-down"
    solo
    :height="40"
    :search-input.sync="search"
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
    search: {
      type: Function,
      required: false,
      default: () => [],
    },
  },
  data() {
    return {
      search: null,
    }
  },
  watch: {
    search: {
      handler: function (val, oldVal) {
        console.log("value", val)
      },
      deep: true,
    },
  },
  // methods: {
  //   inputchange() {
  //     console.log("heloooooooooooooooo", this.value)
  //   },
  // },
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

<style lang="scss" scoped>
::v-deep .v-input__control {
  min-height: auto !important;
}
</style>
