<template>
  <v-card
    class="d-flex justify-space-between align-center px-5 py-2 rounded list-shadow"
    @click="$emit('click')"
    :class="isDisabledOrDeselectable ? 'card-horizontal-disabled' : ''"
    :elevation="isDisabledOrDeselectable ? '0' : '2'"
    :disabled="isDisabled"
    :color="isDisabledOrDeselectable ? 'background' : 'white'"
    height="60"
  >
    <div v-if="icon || title" class="d-flex align-center">
      <Logo :type="icon" />
      <div class="pl-2 font-weight-regular">{{ title }}</div>
    </div>
    <slot></slot>
    <div v-if="isAvailable && !hideButton">
      <huxButton
        :ButtonText="isAdded ? 'Added' : 'Add'"
        :isOutlined="!isAdded"
        :variant="isAdded ? 'secondary' : 'gray'"
        :icon="isAdded ? 'mdi-check' : null"
        size="large"
        :isDisabled="isAlreadyAdded"
        iconPosition="left"
        class="ma-2"
        :ButtonTextColor="!isAdded ? 'gray--text' : ''"
      ></huxButton>
    </div>
  </v-card>
</template>

<script>
import huxButton from "@/components/common/huxButton"
import Logo from "@/components/common/Logo"
export default {
  name: "card-horizontal",
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
.horizontal-card {
  box-shadow: 0px 0px 10px 2px rgba(0, 0, 0, 0.05);
  .card-horizontal-disabled {
    border: 1px solid var(--v-zircon-base) !important;
  }
  &:hover {
    box-shadow: 0px 1px 5px rgba(0, 0, 0, 0.25) !important;
  }
}
</style>
