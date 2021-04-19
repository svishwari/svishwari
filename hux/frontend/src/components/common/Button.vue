<template>
  <div>
    <v-btn outlined color="primary v-btn--active" class="ma-2">
      <v-icon left dark> mdi-check </v-icon>
      {{ AddedButtonText }}
    </v-btn>
    <v-btn outlined color="darkGrey" class="ma-2">
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
