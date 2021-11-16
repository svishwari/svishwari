<template>
  <v-switch
    v-model="localValue"
    inset
    :label="operandLabel"
    class="hux-slider"
    @input="updateValue($event.target.value)"
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
        (label) => label.condition === this.value
      )[0].label
    },
  },
  methods: {
    updateValue(value) {
      this.$emit("input", value)
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
      width: 61px;
      position: relative;
      .v-input--switch__track {
        width: 61px;
        height: 24px;
        background: var(--v-white-base);
        border: 1px solid var(--v-primary-lighten6);
        box-sizing: border-box;
        border-radius: 21px;
        opacity: inherit;
      }
      .v-input--switch__thumb {
        background: var(--v-primary-lighten6);
        border: 1px solid var(--v-white-base);
        box-sizing: border-box;
        width: 20px;
        height: 20px;
        top: 0;
        transform: translate(0, 0) !important;
      }
    }
    .v-label {
      position: absolute !important;
      font-weight: 400;
      font-size: 14px;
      line-height: 16px;
      top: 3px !important;
      left: 25px !important;
      color: var(--v-primary-lighten6);
    }
  }
  &.v-input--is-dirty {
    ::v-deep .v-input__slot {
      .v-input--selection-controls__input {
        .v-input--switch__thumb,
        .v-input--selection-controls__ripple {
          transform: translate(34px, 0) !important;
        }
      }
      .v-input--switch__track {
        border: 1px solid var(--v-success-base);
      }
      .v-input--switch__thumb {
        background: var(--v-success-base);
      }
      .v-label {
        position: absolute !important;
        font-style: normal;
        font-weight: 400;
        font-size: 14px;
        line-height: 16px;
        top: 3px !important;
        left: 3px !important;
        color: var(--v-success-base);
      }
    }
  }
}
</style>
