<template>
  <v-select
    v-model="localValue"
    :items="localItems"
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
  >
    <template slot="item" slot-scope="data">
      <icon
        type="check-icon"
        size="12"
        class="mr-2"
        :color="data.attrs.inputValue ? 'primary' : ''"
      />
      {{ data.item }}
    </template>
  </v-select>
</template>

<script>
import { defineComponent, computed } from "@vue/composition-api"
import Icon from "@/components/common/Icon.vue"

export default defineComponent({
  components: {
    Icon,
  },

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
      get: () => props.items,
    })

    return {
      localValue,
      localItems,
    }
  },
})
</script>

<style lang="scss" scoped>
.hux-select {
  .v-select-list {
    ::v-deep .v-list-item__title {
      font-size: 14px;
    }
  }
}
</style>
