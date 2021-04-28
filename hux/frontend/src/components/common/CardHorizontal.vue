<template>
  <v-card
    class="d-flex justify-space-between align-center px-5 py-2 rounded-lg"
    @click="$emit('click')"
    :class="isDisabled ? 'card-horizontal-disabled' : ''"
    :elevation="isDisabled ? '0' : '2'"
    :disabled="isDisabled"
    :color="isDisabled ? 'background' : 'white'"
    height="60"
  >
    <div class="d-flex align-center">
      <v-icon color="primary">{{ icon }}</v-icon>
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
      ></huxButton>
    </div>
  </v-card>
</template>

<script>
import huxButton from "@/components/common/huxButton"
export default {
  name: "card-horizontal",
  components: {
    huxButton,
  },

  props: {
    icon: {
      type: String,
      required: false,
      default: "mdi-plus",
    },

    title: {
      type: String,
      required: false,
      default: "Info card title",
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

<style lang="scss" scoped>
.card-horizontal-disabled {
  border: 1px solid #e2eaec !important;
}
</style>
