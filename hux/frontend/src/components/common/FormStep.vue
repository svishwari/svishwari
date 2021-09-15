<template>
  <div
    class="form-step d-flex flex-column"
    :class="{
      'form-step--inactive': disabled,
      'form-step--active': !disabled,
    }"
  >
    <div class="form-step__header d-flex flex-row">
      <span class="form-step__indicator rounded-circle">
        {{ step }}
      </span>
      <div class="form-step__label d-flex align-center">
        <slot v-if="$slots.label" name="label"></slot>
        <span
          v-else
          class="text-h5"
          :class="
            disabled
              ? 'black--text text--lighten-3'
              : 'black--text text--darken-4'
          "
        >
          {{ label || `Step ${step}` }}
        </span>
        <span
          v-if="optional"
          class="text-caption pl-1"
          :class="
            disabled
              ? 'black--text text--lighten-3'
              : 'black--text text--darken-4'
          "
        >
          <em>{{ optional }}</em>
        </span>
      </div>
    </div>

    <div
      class="form-step__content pa-3 pl-8 pb-12"
      :class="{
        'form-step__content--inactive': border === 'inactive',
      }"
    >
      <slot name="default" />
    </div>
  </div>
</template>

<script>
export default {
  name: "FormStep",

  props: {
    step: {
      type: Number,
      required: true,
    },

    label: {
      type: String,
      required: false,
    },

    optional: {
      type: String,
      required: false,
    },

    disabled: {
      type: Boolean,
      required: false,
      default: false,
    },

    border: {
      type: String,
      required: false,
    },
  },
}
</script>

<style lang="scss" scoped>
$form-step-spacing: 16px;

.form-step {
  .form-step__indicator {
    color: var(--v-primary-lighten8);
    border: 1px solid var(--v-primary-lighten8);
    width: $form-step-spacing * 2;
    height: $form-step-spacing * 2;
    line-height: $form-step-spacing * 2;
    margin-right: $form-step-spacing;
    text-align: center;
  }

  .form-step__label {
    line-height: $form-step-spacing * 2;
  }

  .form-step__content {
    margin-left: $form-step-spacing;
    border-left: 1px dashed var(--v-primary-lighten8);

    &.form-step__content--inactive {
      border-color: var(--v-black-lighten3);
    }
  }

  &.form-step--inactive {
    color: var(--v-black-lighten3);

    .form-step__indicator {
      color: var(--v-black-lighten3);
      border-color: var(--v-black-lighten3);
    }

    .form-step__content {
      border-color: var(--v-black-lighten3);
    }
  }
}
</style>
