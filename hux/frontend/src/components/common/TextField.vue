<template>
    <v-row>
        <v-col cols="12" sm="6">
            <label>{{ labelText }}</label>
            <v-text-field :label="placeholderText" single-line outlined> </v-text-field>
        </v-col>
    </v-row>
</template>

<script>
export default {
  name: "text-field",

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
  },
}
</script>
