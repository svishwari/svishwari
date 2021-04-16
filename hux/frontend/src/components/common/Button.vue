<template>
  <div>
    <v-btn outlined color="#0076A8" class="ma-2 added-button">
      <v-icon left dark> mdi-check </v-icon>
      {{ AddedButtonText }}
    </v-btn>
    <v-btn outlined color="#232323" class="ma-2 add-button">
      {{ AddButtonText }}
    </v-btn>
    <v-btn tile color="primary">
      Leave configuration
    </v-btn>
    <v-btn tile class="main-button" color="#FFFFFF">
        Cancel & Return
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
    }
  },
}
</script>
<style lang="scss" scoped>
.v-btn {
  &.added-button {
    background: rgba(0, 118, 168, 0.05);
  }
  &.add-button {
    border: 1px solid #D0D0CE;
  }
  &.main-button {
    border: 1px solid #ECECEC;
    box-shadow: 0px 1px 5px rgba(0, 0, 0, 0.25);
    color: #005587;
  }
}
</style>
