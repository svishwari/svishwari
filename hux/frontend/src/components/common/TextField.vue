<template>
  <v-row>
    <v-col cols="12" sm="6">
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
      default: "Add Account ID",
    },
    placeholderText: {
      type: String,
      required: false,
      default: "Account name",
    },
    icon: {
      type: String,
      required: false,
      default: "mdi-alert-circle-outline",
    },
  },

  methods: {
    change: function (value) {
      console.log(value)
    },
    input: function (value) {
      console.log(value)
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
