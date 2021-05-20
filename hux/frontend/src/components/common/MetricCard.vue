<template>
  <v-card
    class="metric-card-wrapper mb-2"
    :class="{ 'no-click': !interactable }"
    @click="$emit('click')"
    :disabled="!active"
    :width="width"
    :min-width="minWidth"
    :height="height"
    elevation="0"
    :ripple="interactable"
  >
    <v-list-item three-line>
      <v-list-item-content>
        <v-list-item-title
          class="item-headline mt-1"
          v-bind:class="interactable ? 'primary--text ' : 'gray--text '"
        >
          {{ title }}
        </v-list-item-title>
        <slot name="extra-item"></slot>
        <v-list-item-subtitle
          class="item-subtitle mb-3 text-h6 neroBlack--text"
          v-if="subtitle"
        >
          {{ subtitle }}
        </v-list-item-subtitle>
      </v-list-item-content>
      <v-icon color="zircon" x-large> {{ icon }} </v-icon>
      <slot name="short-name"></slot>
    </v-list-item>
  </v-card>
</template>

<script>
export default {
  name: "metric-card",

  props: {
    icon: {
      type: String,
      required: false,
    },

    title: {
      type: String,
      required: false,
      default: "Info card title",
    },

    subtitle: {
      type: String,
      required: false,
    },

    active: {
      type: Boolean,
      required: false,
      default: true,
    },

    interactable: {
      type: Boolean,
      required: false,
      default: true,
    },

    width: {
      type: [String, Number],
      required: false,
      default: 135,
    },
    minWidth: {
      type: [String, Number],
      required: false,
    },

    height: {
      type: Number,
      required: false,
      default: 80,
    },
  },
}
</script>

<style lang="scss" scoped>
.metric-card-wrapper {
  border: 1px solid var(--v-zircon-base);
  &.no-click {
    background-color: transparent;
  }
  .item-headline {
    font-size: 12px;
    color: var(--v-gray-base) !important;
  }
  .v-list-item__title {
    font-weight: 400;
  }
  .v-list-item__subtitle {
    font-weight: 600;
  }
  &.v-card--disabled {
    background-color: transparent;
    .v-list-item__title {
      color: var(--v-gray-base);
    }
  }
}
</style>
