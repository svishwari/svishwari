<template>
  <hux-drop-down-search
    v-model="value"
    :items="items"
    :is-search-enabled="false"
    @onValueChange="$emit('onValueChange')"
  >
    <template #activator>
      <v-card class="filter-card-wrapper" rounded="0">
        <span class="primary--text mr-2">{{ name }}</span>
        <v-icon color="primary" class="filter-chevron-icon">
          mdi-chevron-down
        </v-icon>
      </v-card>
    </template>
  </hux-drop-down-search>
</template>

<script>
import HuxDropDownSearch from "@/components/common/HuxDropDownSearch"

export default {
  name: "HuxFilter",

  components: {
    HuxDropDownSearch,
  },

  props: {
    name: {
      type: String,
      required: true,
    },
    items: {
      type: Array,
      required: false,
      default: () => [],
    },
    value: {
      type: Array,
      required: false,
      default: () => [],
    },
    onSelect: {
      type: Function,
      required: false,
      default: () => {},
    },
  },
}
</script>

<style lang="scss" scoped>
.filter-card-wrapper {
  @extend .cursor-pointer;
  @extend .box-shadow-25;
  padding: 3px 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-right: 16px;
  margin-bottom: 2px;
  .filter-chevron-icon {
    padding-top: 2px;
  }
}
</style>
