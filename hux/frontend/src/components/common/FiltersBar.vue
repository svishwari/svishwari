<template>
  <v-expand-transition>
    <v-card
      v-show="isToggled"
      flat
      tile
      color="primary lighten-2"
      variant
      class="hux-filters-bar"
    >
      <div class="wrapper d-flex align-center">
        <slot name="default" />
      </div>
    </v-card>
  </v-expand-transition>
</template>

<script>
import { defineComponent } from "@vue/composition-api"

export default defineComponent({
  props: {
    isToggled: {
      type: Boolean,
      required: true,
      default: false,
    },
  },
})
</script>

<style lang="scss" scoped>
.hux-filters-bar {
  &.primary {
    border-bottom: 1px solid var(--v-black-lighten3) !important;
  }

  .wrapper {
    min-height: 70px;
    padding: 15px 30px;
  }
}
</style>
