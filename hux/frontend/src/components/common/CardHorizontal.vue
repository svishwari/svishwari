<template>
  <v-card
    class="d-flex justify-space-between align-center px-5 py-2 rounded"
    :class="{
      'card-horizontal-disabled': isDisabledOrDeselectable,
      'box-shadow-5': !isDisabledOrDeselectable,
    }"
    :disabled="isDisabled"
    :color="isDisabledOrDeselectable ? '' : 'white'"
    :to="to"
    height="60"
    @click="$emit('click')"
  >
    <div v-if="icon || title" class="d-flex align-center">
      <logo :type="icon" />
      <div class="pl-2 black--text body-1">
        {{ title }}
      </div>
    </div>
    <slot></slot>
    <div v-if="!hideButton">
      <hux-button
        :is-outlined="!isAdded"
        :variant="isAdded ? 'primary lighten-6' : 'black lighten-3'"
        :icon-color="isAdded ? 'white' : 'white'"
        :icon-variant="isAdded ? 'lighten3' : 'base'"
        :icon-size="12"
        :icon="isAdded ? 'mdi-check' : null"
        size="large"
        :is-disabled="isAlreadyAdded || isModelRequested"
        :box-shadow="false"
        icon-position="left"
        class="ma-2"
      >
        <span
          :class="[
            isAdded ? 'white--text' : 'black--text text--lighten4',
            isAlreadyAdded || isModelRequested
              ? 'black--text text--lighten-3'
              : '',
          ]"
        >
          <span v-if="requestedButton" class="text-button"
          :class="[
            isModelRequested || isAdded
              ? ''
              : 'black--text text--lighten-4',
          ]">
            {{ isModelRequested || isAdded ? "Requested" : "Request" }}
          </span>
          <span v-else class="text-button"
            >{{ isAdded ? "Added" : "Add" }}
          </span>
        </span>
      </hux-button>
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
    requestedButton: {
      type: Boolean,
      required: false,
      default: false,
    },
    isModelRequested: {
      type: Boolean,
      required: false,
      default: false,
    },
  },

  computed: {
    isDisabled: function () {
      return this.isAlreadyAdded
    },

    isDisabledOrDeselectable: function () {
      return this.isDisabled || this.enableBlueBackground
    },
  },
}
</script>

<style lang="scss" scoped>
.card-horizontal-disabled {
  border: 1px solid var(--v-black-lighten2) !important;
  background-color: var(--v-primary-lighten1) !important;
  border-radius: 4px;
  @extend .box-shadow-none;
  &:hover {
    @extend .box-shadow-25;
  }
}
</style>
