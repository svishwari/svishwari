<template>
  <v-switch
    v-model="localValue"
    inset
    :label="operandLabel"
    class="hux-slider"
    :disabled="isDisabled"
    :style="cssProps"
    @input="updateValue($event.target.value)"
    @change="valueChanges()"
  ></v-switch>
</template>

<script>
export default {
  name: "HuxSwitch",
  props: {
    value: {
      type: Boolean,
    },
    switchLabels: {
      type: Array,
      required: false,
      default: () => [
        {
          condition: true,
          label: "ALL",
        },
        {
          condition: false,
          label: "ANY",
        },
      ],
    },
    isDisabled: {
      type: Boolean,
      required: false,
      default: false,
    },
    isBlocked: {
      type: Boolean,
      required: false,
      default: false,
    },
    falseColor: {
      type: String,
      required: false,
      default: "var(--v-black-lighten6)",
    },
    trueColor: {
      type: String,
      required: false,
      default: "var(--v-success-darken1)",
    },
    width: {
      type: String,
      required: false,
      default: "61px",
    },
  },
  computed: {
    localValue: {
      get() {
        return this.value
      },
      set(value) {
        this.$emit("input", value)
      },
    },
    operandLabel() {
      return this.switchLabels.filter(
        (label) => label.condition == this.value
      )[0].label
    },
    cssProps() {
      return {
        "--false-color": this.isDisabled
          ? "var(--v-black-lighten3)"
          : this.isBlocked
          ? "var(--v-error-lighten1)"
          : this.falseColor,
        "--true-color": this.isDisabled
          ? "var(--v-black-lighten3)"
          : this.isBlocked
          ? "var(--v-error-lighten1)"
          : this.trueColor,
        "--button-width": this.width,
      }
    },
  },
  methods: {
    updateValue(value) {
      this.$emit("input", value)
    },
    valueChanges() {
      this.$emit("change", !this.localValue)
    },
  },
}
</script>

<style lang="scss" scoped>
.v-input {
  ::v-deep .v-input__slot {
    height: 26px;
    margin: 0;
    .v-input--selection-controls__input {
      width: var(--button-width);
      position: relative;
      .v-input--switch__track {
        @extend .new-pills;
        width: var(--button-width);
        height: 24px;
        background: var(--false-color);
        box-sizing: border-box;
        border-radius: 21px;
        opacity: inherit;
        &.primary--text {
          background: var(--true-color) !important;
        }
      }
      .v-input--switch__thumb {
        background: var(--v-white-base);
        box-sizing: border-box;
        width: 20px;
        height: 20px;
        top: 0;
        transform: translate(0, 0) !important;
      }
      .v-input--selection-controls__ripple {
        height: 0px !important;
        width: 0px !important;
      }
    }
    .v-label {
      position: absolute !important;
      font-weight: 400;
      font-size: 14px;
      line-height: 16px;
      top: 3px !important;
      left: 25px !important;
      color: var(--v-white-base);
    }
  }
  &.v-input--is-dirty {
    ::v-deep .v-input__slot {
      .v-input--selection-controls__input {
        .v-input--switch__thumb,
        .v-input--selection-controls__ripple {
          transform: translate(calc(var(--button-width) - 27px), 0) !important;
        }
      }
      .v-input--switch__thumb {
        background: var(--v-white-base);
      }
      .v-label {
        position: absolute !important;
        font-style: normal;
        font-weight: 400;
        font-size: 14px;
        line-height: 16px;
        top: 3px !important;
        left: 3px !important;
        color: var(--v-white-base);
      }
    }
  }
}
</style>
