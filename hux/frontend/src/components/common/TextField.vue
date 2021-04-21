<template>
  <v-row>
    <v-col>
      <label>
        {{ labelText }}
        <v-icon color="primary"> {{ icon }} </v-icon>
      </label>
      <v-text-field
        :label="placeholderText"
        @input="input($event)"
        @change="change($event)"
        v-model="TextFieldValue"
        single-line
        outlined
      >
      </v-text-field>
    </v-col>
  </v-row>
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
  },

  methods: {
    change: function (value) {
    },
    input: function (value) {
      this.$emit("input", this.TextFieldValue)
    },
  },
}
</script>
<style lang="scss" scoped>
.row {
  .mdi {
    margin-bottom: 7px;
  }
}
</style>
