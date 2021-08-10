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
        <span v-else class="text-h5">{{ label || `Step ${step}` }}</span>
        <v-menu :max-width="tooltipWidth" open-on-hover offset-y v-if="tooltip">
          <template #activator="{ on }">
            <v-icon color="primary" :size="12" class="ml-1" v-on="on">
              mdi-information-outline
            </v-icon>
          </template>
          <template #default>
            <div class="px-4 py-2 white">
              <div class="neroBlack--text text-caption">
                {{tooltipHeading}}
              </div>
              <div class="neroBlack--text text-caption mt-1">
                {{tooltipText}}
              </div>
            </div>
          </template>
        </v-menu>
        <span
          v-if="optional"
          class="text-caption pl-1"
          :class="disabled ? 'lightGrey--text' : 'grey--text'"
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

    tooltip: {
      type: Boolean,
      required: false,
      default: false,
    },

    tooltipWidth: {
      type: String,
      required: false,
      default: false,
    },

    tooltipHeading: {
      type: String,
      required: false,
    },

    tooltipText: {
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
