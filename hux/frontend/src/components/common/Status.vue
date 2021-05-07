<template>
  <div v-if="status == 'active'">
    <v-icon color="success" class="pr-2"> mdi-checkbox-blank-circle </v-icon>
    <span v-if="!hideText">Active</span>
  </div>
  <div v-else-if="status == 'pending'">
    <v-btn
      style="border-style: dashed"
      width="24"
      height="24"
      icon
      outlined
      color="success"
      class="pr-2"
    ></v-btn>
    <span v-if="!hideText">Pending</span>
  </div>
  <div v-else-if="status == 'error'">
    <v-icon color="error" class="pr-2"> mdi-alert-circle </v-icon>
    <span v-if="!hideText">Error</span>
  </div>
</template>

<script>
export default {
  name: "status",

  props: {
    status: {
      type: String,
      required: false,
      default: "success",
    },
    hideText: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
}
</script>
