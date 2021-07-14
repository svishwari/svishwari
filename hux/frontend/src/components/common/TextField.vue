<template>
  <div class="text-field-hux">
    <label class="d-flex align-items-center mb-2">
      <span class="neroBlack--text text-caption">
        {{ labelText }}
        <em v-if="!required"> - optional</em>
      </span>
      <v-tooltip
        v-if="helpText"
        color="transparent"
        transition="fade-transition"
        top
      >
        <template #activator="{ on, attrs }">
          <v-icon
            color="primary"
            size="small"
            class="ml-2"
            v-bind="attrs"
            v-on="on"
          >
            {{ icon }}
          </v-icon>
        </template>
        <span class="white neroBlack--text shadow pa-2 text-caption">
          {{ helpText }}
        </span>
      </v-tooltip>
    </label>
    <v-text-field
      v-model="TextFieldValue"
      :required="required"
      :height="height"
      :label="placeholderText"
      :append-icon="appendIcon"
      :rules="rules"
      :type="InputType"
      :placeholder="placeholder"
      :background-color="backgroundColor"
      single-line
      outlined
      v-bind="$attrs"
      autocomplete="off"
      @input="input($event)"
      @change="change($event)"
      @click:append="$emit('clickAppend')"
      @blur="$emit('blur', TextFieldValue)"
    >
    </v-text-field>
  </div>
</template>

<script>
export default {
  name: "text-field",
  data: function () {
    return {
      TextFieldValue: null,
    }
  },
  props: {
    required: {
      type: Boolean,
      required: false,
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
    appendIcon: {
      type: String,
      required: false,
      default: null,
    },
    InputType: {
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
  },

  methods: {
    change: function () {
      // This is a TODO
    },
    input: function () {
      this.$emit("input", this.TextFieldValue)
    },
  },
}
</script>

<style lang="scss" scoped>
.text-field-hux {
  ::v-deep .v-input {
    .v-input__control {
      .v-input__slot {
        min-height: 40px;
        .v-text-field__slot {
          .v-label {
            top: 9px;
          }
        }
        fieldset {
          color: var(--v-lightGrey-base) !important;
          border: 1px solid var(--v-lightGrey-base);
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
}
</style>
