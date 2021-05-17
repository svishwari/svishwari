<template>
  <v-card
    class="d-flex justify-space-between align-center px-5 py-2 rounded"
    @click="$emit('click')"
    :class="isDisabled ? 'card-horizontal-disabled' : ''"
    :elevation="isDisabled ? '0' : '2'"
    :disabled="isDisabled"
    :color="isDisabled ? 'background' : 'white'"
    height="60"
    :style="
      isDisabled ? 'border: 1px solid var(--v-zircon-base)!important;' : ''
    "
  >
    <div class="d-flex align-center">
      <Logo :type="icon" />
      <div class="pl-2 font-weight-regular">{{ title }}</div>
    </div>
    <slot></slot>
    <div v-if="isAvailable && !hideButton">
      <huxButton
        :ButtonText="isAdded ? 'Added' : 'Add'"
        :isOutlined="!isAdded"
        :variant="isAdded ? 'secondary' : 'lightGrey'"
        :icon="isAdded ? 'mdi-check' : null"
        size="large"
        :isDisabled="isAlreadyAdded"
        iconPosition="left"
        class="ma-2"
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
  },

  computed: {
    isDisabled: function () {
      return this.isAlreadyAdded || !this.isAvailable
    },
  },
}
</script>
