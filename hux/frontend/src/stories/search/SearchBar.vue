<template>
  <v-text-field
    :label="placeholderText"
    solo
    background-color="#F9FAFB"
    height="32px"
    outlined
    clearable
  >
    <template #prepend-inner>
      <icon type="help" size="40" color="primary" class="pa-2" />
    </template>
  </v-text-field>
</template>

<script>
import Icon from "../icons/Icon2.vue"
export default {
  name: "Search",
  components: { Icon },
  props: {
    placeholderText: {
      type: String,
      required: false,
      default: "Search...",
    },
  },
}
</script>

<style lang="scss" scoped>
::v-deep .v-input__control {
  max-height: 60px;
  .v-input__slot {
    margin-bottom: 0px;
  }
  .v-text-field__details {
    margin-bottom: 0px;
  }
}
</style>
