<template>
  <div class="steps-wrap progress-steps">
    <div v-for="(label, step) in steps" :key="step" class="steps-wrap">
      <div class="d-flex justify-center flex-column progress-step">
        <icon
          v-if="errorSteps.includes(step + 1)"
          type="negative-invert"
          :size="40"
        />
        <div
          v-else-if="currentStep <= step + 1"
          :class="
            currentStep === step + 1
              ? 'box-shadow-15-8 active step-circle'
              : 'in-active step-circle'
          "
        >
          <span class="new-b2">{{ step }}</span>
        </div>
        <icon v-else type="positive" :size="40" />
        <span class="pt-2 step-label new-b3">{{ label }}</span>
      </div>
      <div
        v-if="step != steps.length - 1"
        :class="
          currentStep > step + 1
            ? 'ruler-active ruler mb-6'
            : 'ruler-in-active ruler mb-6'
        "
      ></div>
    </div>
  </div>
</template>

<script>
import Icon from "@/components/common/Icon.vue"

export default {
  name: "ProgressIndicator",

  components: {
    Icon,
  },

  props: {
    steps: {
      type: Array,
      required: true,
    },

    currentStep: {
      type: Number,
      required: false,
      default: 1,
    },

    errorSteps: {
      type: Array,
      required: false,
      default: () => [],
    },
  },
}
</script>

<style lang="scss">
.steps-wrap {
  display: flex;
  align-items: center;
  &.progress-steps {
    padding-left: 22px;
  }
  .progress-step {
    padding-top: 10px;
    padding-bottom: 10px;
  }
  .step-circle {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    text-align: center;
    vertical-align: middle;
    line-height: 40px;
    &.active {
      border: 1px solid var(--v-success-darken1);
      color: var(--v-success-darken1);
    }
    &.in-active {
      border: 1px solid var(--v-black-lighten8);
      color: var(--v-black-lighten6);
    }
  }
  .ruler {
    width: 92px;
    &.ruler-active {
      border: 1px solid var(--v-success-darken1);
    }
    &.ruler-in-active {
      background-image: linear-gradient(
        to right,
        var(--v-black-lighten8) 50%,
        rgba(255, 255, 255, 0) 20%
      );
      background-position: bottom;
      background-size: 10px 2px;
      height: 2px;
      background-repeat: repeat-x !important;
    }
  }
  .step-label {
    color: var(--v-black-lighten6);
  }
}
</style>
