<template>
  <div class="text-field-hux" :class="!required ? 'discription-field' : ''">
    <label
      class="d-flex align-items-center"
      :class="!required ? 'mb-0' : 'mb-1'"
    >
      <span class="new-b4 mb-1">
        {{ labelText }}
        <em v-if="!required" class="new-b4 gray--text"> - optional</em>
      </span>
      <span
        v-if="showWordCount && TextFieldValue && TextFieldValue.length > 0"
        class="new-secondary-label word-count-field"
      >
        {{ TextFieldValue.length }}
        <em v-if="!required" class="new-b4 gray--text"> - optional</em>
      </span>
      <tooltip v-if="helpText" position-top>
        <template #label-content>
          <v-icon color="primary" size="small" class="ml-1 mb-2">
            {{ icon }}
          </v-icon>
        </template>
        <template
          #hover-content
          class="white black--text text--darken-4 shadow pa-2 text-caption"
        >
          <v-sheet max-width="240px">
            {{ helpText }}
          </v-sheet>
        </template>
      </tooltip>
    </label>
    <v-text-field
      v-model="TextFieldValue"
      :required="required"
      :height="height"
      :label="placeholderText"
      :rules="rules"
      :type="inputType"
      :placeholder="placeholder"
      :background-color="backgroundColor"
      color="var(--v-black-lighten6)"
      single-line
      outlined
      v-bind="$attrs"
      autocomplete="off"
      @input="input($event)"
      @click:append="$emit('clickAppend')"
      @blur="$emit('blur', TextFieldValue)"
      @change="$emit('change', $event)"
    >
      <template #prepend> </template>
      <template #append> </template>
    </v-text-field>
  </div>
</template>

<script>
import Tooltip from "../tooltip/Tooltip2"
export default {
  name: "TextField",
  components: { Tooltip },
  props: {
    required: {
      type: Boolean,
      required: false,
    },
    showWordCount: {
      type: Boolean,
      required: false,
      default: false,
    },
    height: {
      type: String,
      required: false,
    },
    labelText: {
      type: String,
      required: false,
    },
    placeholder: {
      type: String,
      required: false,
    },
    placeholderText: {
      type: String,
      required: false,
    },
    helpText: {
      type: String,
      required: false,
    },
    icon: {
      type: String,
      required: false,
    },
    inputType: {
      type: String,
      required: false,
      default: "text",
    },
    backgroundColor: {
      type: String,
      required: false,
      default: "white",
    },
    rules: {
      type: Array,
      required: false,
      default: () => [],
    },
    value: {
      type: String,
      required: false,
    },
    appendIcon: {
      type: String,
      required: false,
    },
    prependIcon: {
      type: String,
      required: false,
    },
  },

  computed: {
    TextFieldValue: {
      get() {
        return this.value || null
      },
      set(value) {
        this.$emit("input", value)
      },
    },
  },

  methods: {
    input: function (value) {
      this.$emit("input", value)
    },
  },
}
</script>

<style lang="scss" scoped>
.text-field-hux {
  ::v-deep .v-input {
    .v-input__control {
      .v-input__slot {
        min-height: 32px;
        border-radius: 5px;
        padding: 0 8px !important;
        border: 1px solid var(--v-black-lighten8) !important;
        &:hover,
        &:active {
          border: 1px solid var(--v-black-base) !important;
        }
        .v-text-field__slot {
          .v-label {
            top: 6px;
          }
        }
        fieldset {
          color: var(--v-black-lighten3) !important;
          border: 0px !important;
        }
      }
    }

    &.error--text {
      .v-input__control {
        .v-input__slot {
          fieldset {
            color: inherit;
          }
        }
      }
    }
  }
  ::v-deep .v-text-field {
    .v-text-field__slot {
      input {
        @extend .new-b1;
        color: var(--v-black-lighten6) !important;
        &::placeholder {
          color: var(--v-black-lighten6) !important;
        }
        &:hover,
        &:active {
          color: var(--v-black-base) !important;
        }
      }
      label {
        color: var(--v-black-lighten6) !important;
      }
    }
  }
}
.discription-field {
  margin-top: -2px;
}
.word-count-field {
  margin-bottom: 2px;
}
</style>
