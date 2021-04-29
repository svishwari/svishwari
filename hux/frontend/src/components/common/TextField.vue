<template>
  <div>
    <label class="ml-2">
      {{ labelText }}
      <v-icon color="primary" class="mb-2"> {{ icon }} </v-icon>
    </label>
    <v-text-field
      :label="placeholderText"
      @input="input($event)"
      @change="change($event)"
      v-model="TextFieldValue"
      :append-icon="appendIcon"
      :rules="rules"
      :type="InputType"
      @click:append="$emit('clickAppend')"
      @blur="$emit('blur', TextFieldValue)"
      single-line
      outlined
      autocomplete="off"
      :background-color="backgroundColor"
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
    labelText: {
      type: String,
      required: false,
      default: null,
    },
    placeholderText: {
      type: String,
      required: false,
      default: null,
    },
    icon: {
      type: String,
      required: false,
      default: null,
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
