<template>
  <v-card
    class="metric-card-wrapper rounded-lg align-center"
    :class="{ 'no-click': !interactable }"
    :style="{ 'flex-grow': grow }"
    :max-width="maxWidth"
    :height="height"
    :disabled="!active"
    elevation="0"
    :ripple="interactable"
    @click="$emit('click')"
  >
    <div class="d-flex align-center justify-space-between w-100">
      <div
        class="flex-grow-1"
        :class="{ 'align-center text-center': highLevel }"
      >
        <span
          v-if="!titleTooltip"
          class="text-body-2"
          :class="[
            interactable ? 'primary--text ' : 'black--text text--darken-1 ',
            highLevel ? 'highlevel-title' : '',
          ]"
        >
          {{ title }}
        </span>
        <tooltip v-else>
          <template #label-content>
            <span
              class="text-h5"
              :class="
                interactable ? 'primary--text ' : 'black--text text--darken-1 '
              "
            >
              {{ title }}
            </span>
          </template>
          <template #hover-content>
            {{ titleTooltip }}
          </template>
        </tooltip>

        <slot name="extra-item"></slot>

        <div class="subtitle-slot">
          <span
            class="text-body-1"
            :class="{
              'no-click': !interactable,
              'flex-grow-1 align-center text-center highlevel-subtitle':
                highLevel,
            }"
          >
            {{ subtitle }}
          </span>
          <slot name="subtitle-extended"></slot>
        </div>
      </div>

      <v-icon v-if="icon" color="black lighten-2" x-large> {{ icon }} </v-icon>

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
    height: {
      type: [String, Number],
      required: false,
      default: 75,
    },
    highLevel: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
}
</script>

<style lang="scss" scoped>
.metric-card-wrapper {
  border: 1px solid var(--v-black-lighten2);
  padding: 20px 15px;
  display: -webkit-box;
  display: -webkit-flex;
  display: -ms-flexbox;
  display: flex;
  &.no-click {
    cursor: default;
    background-color: transparent;
    cursor: default;
  }
  .item-headline {
    color: var(--v-black-darken1) !important;
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
      color: var(--v-black-darken1);
    }
  }
  div.d-flex.align-center.justify-space-between {
    .subtitle-slot {
      display: flex;
    }
  }
  .highlevel-title {
    font-weight: 300;
    font-size: 28px !important;
    line-height: 40px;
    color: var(--v-black-darken4) !important;
  }
  .highlevel-subtitle {
    font-size: 14px !important;
    line-height: 16px;
    color: #4f4f4f;
    color: var(--v-black-darken1) !important;
  }
}
</style>
