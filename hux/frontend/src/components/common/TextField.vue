<template>
  <div class="text-field-hux" :class="!required ? 'discription-field' : ''">
    <label
      class="d-flex align-items-center"
      :class="!required ? 'mb-0' : 'mb-1'"
    >
      <span class="black--text text--darken-4 text-h5">
        {{ labelText }}
        <em v-if="!required" class="text-h6 gray--text"> - optional</em>
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
      :append-icon="appendIcon"
      :rules="rules"
      :type="inputType"
      :placeholder="placeholder"
      :background-color="backgroundColor"
      color="var(--v-black-lighten4)"
      single-line
      outlined
      v-bind="$attrs"
      autocomplete="off"
      @input="input($event)"
      @click:append="$emit('clickAppend')"
      @blur="$emit('blur', TextFieldValue)"
      @change="$emit('change', $event)"
    >
    </v-text-field>
  </div>
</template>

<script>
import Tooltip from "@/components/common/Tooltip"
export default {
  name: "TextField",
  components: { Tooltip },
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
        min-height: 40px;
        .v-text-field__slot {
          .v-label {
            top: 9px;
          }
        }
        fieldset {
          color: var(--v-black-lighten3) !important;
          border: 1px solid var(--v-black-lighten3);
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
        &::placeholder {
          color: var(--v-black-lighten4) !important;
        }
      }
    }
  }
}
.discription-field {
  margin-top: -2px;
}
</style>
