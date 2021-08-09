<template>
  <v-card
    class="metric-card-wrapper rounded-lg"
    :class="{ 'no-click': !interactable }"
    :style="{ 'flex-grow': grow }"
    :max-width="maxWidth"
    height="78"
    :disabled="!active"
    elevation="0"
    :ripple="interactable"
    @click="$emit('click')"
  >
    <div class="d-flex align-center justify-space-between">
      <div class="flex-grow-1">
        <span
          v-if="!titleTooltip"
          class="text-caption"
          :class="interactable ? 'primary--text ' : 'gray--text '"
        >
          {{ title }}
        </span>
        <tooltip v-else>
          <template #label-content>
            <span
              class="text-caption"
              :class="interactable ? 'primary--text ' : 'gray--text '"
            >
              {{ title }}
            </span>
          </template>
          <template #hover-content>
            {{ titleTooltip }}
          </template>
        </tooltip>

        <slot name="extra-item"></slot>

        <div class="pt-1">
          <span class="font-weight-semi-bold">{{ subtitle }}</span>
          <slot name="subtitle-extended"></slot>
        </div>
      </div>

      <v-icon v-if="icon" color="zircon" x-large> {{ icon }} </v-icon>

      <slot name="short-name"></slot>
    </div>
  </v-card>
</template>

<script>
import Tooltip from "./Tooltip.vue"
export default {
  name: "MetricCard",
  components: { Tooltip },

  props: {
    icon: {
      type: String,
      required: false,
    },

    title: {
      type: [String, Number],
      required: false,
      default: "Info card title",
    },

    subtitle: {
      type: [String, Number],
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
      default: false,
    },
    titleTooltip: {
      type: String,
      required: false,
    },

    grow: {
      type: Number,
      required: false,
      default: 1,
    },

    maxWidth: {
      type: [String, Number],
      required: false,
    },
  },
}
</script>

<style lang="scss" scoped>
.metric-card-wrapper {
  border: 1px solid var(--v-zircon-base);
  padding: 20px 15px;
  &.no-click {
    cursor: default;
    background-color: transparent;
    cursor: default;
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
    overflow: unset;
  }
  &.v-card--disabled {
    background-color: transparent;
    .v-list-item__title {
      color: var(--v-gray-base);
    }
  }
}
</style>
