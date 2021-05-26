<template>
  <div>
    <label class="d-flex align-items-center mb-2">
      <span v-html="labelText"></span>
      <v-tooltip top v-if="helpText">
        <template v-slot:activator="{ on, attrs }">
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
        <span>
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
