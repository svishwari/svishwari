<template>
  <v-card
    class="score-card-wrapper rounded-lg no-click"
    :width="width"
    :height="height"
    :disabled="active"
    elevation="0"
  >
    <div class="score-card-info">
      <icon
        class="model-icon"
        :type="icon"
        size="24"
        :stroke="stroke"
        :variant="variant"
      />
      <span class="model-name text-body-2">{{ title }}</span>
      <span class="text-subtitle-1" :class="{ 'model-value ': hasSlot }">
        {{ value }}
      </span>
      <slot name="progress-bar"></slot>
    </div>
  </v-card>
</template>

<script>
import Icon from "@/components/common/Icon"

export default {
  name: "ScoreCard",
  components: { Icon },
  props: {
    width: {
      type: [String, Number],
      required: false,
      default: 150,
    },
    height: {
      type: [String, Number],
      required: false,
      default: 90,
    },
    active: {
      type: Boolean,
      required: false,
      default: true,
    },
    icon: {
      type: String,
      required: false,
      default: "hx-trustid-colored",
    },
    title: {
      type: [String, Number],
      required: true,
      default: "Transparency",
    },
    value: {
      type: [String, Number],
      required: true,
      default: 75,
    },
    stroke: {
      type: String,
      required: false,
      default: "primary",
    },
    variant: {
      type: String,
      required: false,
      default: "base",
    },
  },
  computed: {
    hasSlot() {
      return (
        !!this.$slots["progress-bar"] || !!this.$scopedSlots["progress-bar"]
      )
    },
  },
}
</script>

<style lang="scss" scoped>
.score-card-wrapper {
  border: 1px solid var(--v-black-lighten2);
  padding: 15px;
  &::before {
    border-radius: 12px;
  }
  &.no-click {
    cursor: default;
    background-color: transparent;
    cursor: default;
    &::before {
      background: var(--v-primary-lighten1) !important;
      border-radius: 10px;
    }
  }
  .score-card-info {
    text-align: center;
    .model-icon {
      display: block;
      margin-left: calc(100% - 70px);
      border: 1px solid var(--v-black-lighten2) !important;
      box-sizing: border-box;
      border-radius: 50%;
      padding: 2px;
    }
    .model-name {
      display: block;
    }
    .model-value {
      float: left;
    }
    ::v-deep .chart-container {
      .chart {
        svg {
          margin-left: -16px !important;
        }
      }
    }
  }
}
</style>
