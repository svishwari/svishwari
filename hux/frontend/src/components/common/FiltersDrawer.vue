<template>
  <v-expand-x-transition>
    <v-card
      v-show="isToggled"
      :width="width"
      :height="height"
      flat
      tile
      color="white"
      class="hux-filters-drawer"
    >
      <div class="pa-6">
        <slot name="default" />
      </div>
    </v-card>
  </v-expand-x-transition>
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

    width: {
      type: String,
      required: false,
      default: "300px",
    },

    height: {
      type: String,
      required: false,
      default: "100%",
    },
  },
})
</script>

<style lang="scss" scoped>
.hux-filters-drawer {
  border-left: 1px solid var(--v-black-lighten3) !important;
}
</style>
