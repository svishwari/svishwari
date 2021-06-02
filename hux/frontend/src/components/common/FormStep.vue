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
      <div class="form-step__label">
        <span class="text-h5">{{ label || `Step ${step}` }}</span>
        <em v-if="optional" class="text-caption grey--text"> - Optional</em>
      </div>
    </div>

    <div
      class="form-step__content pa-4 pl-8 pb-12"
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
      type: Boolean,
      required: false,
      default: false,
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
  .form-step__header {
  }

  .form-step__indicator {
    color: var(--v-secondary-base);
    border: 1px solid var(--v-secondary-base);
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
    border-left: 1px dashed var(--v-secondary-base);

    &.form-step__content--inactive {
      border-color: var(--v-lightGrey-base);
    }
  }

  &.form-step--inactive {
    color: var(--v-lightGrey-base);

    .form-step__indicator {
      color: var(--v-lightGrey-base);
      border-color: var(--v-lightGrey-base);
    }

    .form-step__content {
      border-color: var(--v-lightGrey-base);
    }
  }
}
</style>
