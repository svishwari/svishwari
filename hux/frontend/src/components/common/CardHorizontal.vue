<template>
  <v-card
    class="d-flex justify-space-between align-center px-5 py-2 rounded"
    :class="{
      'card-horizontal-disabled': isDisabledOrDeselectable,
      'box-shadow-5': !isDisabledOrDeselectable,
    }"
    :disabled="isDisabled"
    :color="isDisabledOrDeselectable ? 'primary lighten-1' : 'white'"
    :to="to"
    height="60"
    @click="$emit('click')"
  >
    <div v-if="icon || title" class="d-flex align-center">
      <logo :type="icon" />
      <div
        class="card-horizontal-title pl-2 text-h6 black--text text--darken-4"
      >
        {{ title }}
      </div>
    </div>
    <slot></slot>
    <div v-if="isAvailable && !hideButton">
      <huxButton
        :is-outlined="!isAdded"
        :variant="isAdded ? 'primary lighten-8' : 'primary'"
        :icon="isAdded ? 'mdi-check' : null"
        size="large"
        :is-disabled="isAlreadyAdded"
        :box-shadow="false"
        icon-position="left"
        class="ma-2"
      >
        <span
          :class="[
            isAdded ? 'white--text' : 'primary--text',
            isAlreadyAdded ? 'black--text text--darken-1' : '',
          ]"
        >
          {{ isAdded ? "Added" : "Add" }}
        </span>
      </huxButton>
    </div>
  </v-card>
</template>

<script>
import huxButton from "@/components/common/huxButton"
import Logo from "@/components/common/Logo"
export default {
  name: "CardHorizontal",
  components: {
    huxButton,
    Logo,
  },

  props: {
    icon: {
      type: String,
      required: false,
    },

    title: {
      type: String,
      required: false,
    },

    isAdded: {
      type: Boolean,
      required: false,
      default: false,
    },

    isAvailable: {
      type: Boolean,
      required: false,
      default: true,
    },

    isAlreadyAdded: {
      type: Boolean,
      required: false,
      default: false,
    },

    hideButton: {
      type: Boolean,
      required: false,
      default: false,
    },

    enableBlueBackground: {
      type: Boolean,
      required: false,
      default: false,
    },

    to: {
      type: Object,
      required: false,
      default: () => {},
    },
  },

  computed: {
    isDisabled: function () {
      return this.isAlreadyAdded || !this.isAvailable
    },

    isDisabledOrDeselectable: function () {
      return this.isDisabled || this.enableBlueBackground
    },
  },
}
</script>

<style lang="scss" scoped>
.card-horizontal-disabled {
  border: 1px solid var(--v-zircon-base) !important;
  background-color: var(--v-primary-lighten1) !important;
  @extend .box-shadow-none;
  .theme--light.v-btn.v-btn--disabled.v-btn--has-bg {
    background-color: var(--v-black-lighten2) !important;
  }
  &:hover {
    @extend .box-shadow-25;
  }
}
.card-horizontal-title {
  color: var(--v-neroBlack-base);
}
</style>
