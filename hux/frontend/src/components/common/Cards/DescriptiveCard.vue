<template>
  <v-card
    class="descriptive-card align-center text-center rounded-lg mr-10 mb-10"
    :disabled="disabled"
  >
    <div v-if="$slots.top" class="pa-3 pb-0">
      <slot name="top" />
    </div>

    <div v-if="icon" class="d-flex justify-center pb-4">
      <Icon :type="icon" :size="60" color="primary" class="d-block" />
    </div>

    <div class="text-h4 pb-2">
      {{ title }}
    </div>

    <div class="text-caption">
      {{ description }}
    </div>

    <div class="pt-2" v-if="$slots.default">
      <slot />
    </div>
  </v-card>
</template>

<script>
import Icon from "@/components/common/Icon"

export default {
  name: "descriptive-card",

  components: {
    Icon,
  },

  props: {
    icon: {
      type: String,
      required: false,
    },

    title: {
      type: String,
      required: false,
      default: "Model Name",
    },

    description: {
      type: String,
      required: false,
      default: "Descriptive text for the model item chosen above",
    },

    disabled: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
}
</script>

<style lang="scss" scoped>
.descriptive-card {
  box-shadow: 0px 0px 10px 2px rgba(0, 0, 0, 0.05) !important;
  color: var(--v-neroblack-base);
  cursor: default;
  font-weight: normal;
  min-height: 255px;
  transition: box-shadow 0.2s;
  width: 255px;

  &:hover {
    box-shadow: 0px 0px 10px 2px rgba(117, 123, 123, 0.3) !important;
  }
}
</style>
