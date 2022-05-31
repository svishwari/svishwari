<template>
  <v-card
    class="options-wrap d-flex align-center"
    :class="[padding, heightChanges]"
    flat
    tile
    :color="bgColor"
    :height="height"
  >
    <hux-button v-if="buttonText">{{ buttonText }}</hux-button>
    <template v-if="icons">
      <div class="ml-1 mr-3 icon-wrap">
        <icon
          v-for="i in icons"
          :key="i"
          :type="i"
          :size="iconSize"
          class="ml-1 mr-1"
        />
      </div>
    </template>
    <search v-if="searchBar" />
  </v-card>
</template>

<script>
import huxButton from "./huxButton.vue"
import icon from "./Icon.vue"
import search from "./Search.vue"
export default {
  name: "OptionsBar",
  components: { huxButton, icon, search },
  props: {
    bgColor: {
      required: false,
      default: "white",
    },
    height: {
      type: [Number, String],
      required: false,
      default: 72,
    },
    padding: {
      type: String,
      required: false,
      default: "px-8",
    },
    heightChanges: {
      type: String,
      required: false,
      default: "py-5",
    },
    buttonText: {
      type: String,
      required: false,
    },
    icons: {
      type: Array,
      required: false,
      default: () => [],
    },
    iconSize: {
      type: Number,
      required: false,
      default: 38,
    },
    searchBar: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
}
</script>

<style lang="scss" scoped>
.options-wrap {
  border-top: 1px solid var(--v-black-lighten3) !important;
  border-bottom: 1px solid var(--v-black-lighten3) !important;

  .icon-wrap {
    display: flex;
    align-items: center;
  }
}
</style>
