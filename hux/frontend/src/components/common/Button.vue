<template>
  <div>
    <v-btn outlined color="primary" class="ma-2 added-button">
      <v-icon left dark> mdi-check </v-icon>
      {{ AddedButtonText }}
    </v-btn>
    <v-btn outlined color="darkGrey" class="ma-2 add-button">
      {{ AddButtonText }}
    </v-btn>
    <v-btn tile color="primary"> Leave configuration </v-btn>
    <v-btn tile class="main-button" color="tertiary">
      Cancel &amp; Return
    </v-btn>
  </div>
</template>

<script>
export default {
  name: "button",

  props: {
    AddedButtonText: {
      type: String,
      required: false,
      default: "Added",
    },
    AddButtonText: {
      type: String,
      required: false,
      default: "Add",
    },
  },
}
</script>
