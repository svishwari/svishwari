<template>
  <v-snackbar
    v-model="isOpen"
    height="56"
    :timeout="timeout"
    app
    top
    :type="type"
    color="white rounded-0"
    elevation="3"
  >
    <div class="d-flex align-center" :class="typeClass">
      <v-icon outlined :color="type">{{ icon }}</v-icon>
      <span class="px-4 font-weight-bold">{{ title }}</span>
      <span>{{ message }}</span>
    </div>
  </v-snackbar>
</template>

<script>
export default {
  name: "HuxAlert",

  props: {
    type: {
      type: String,
      required: false,
      default: "success",
    },

    value: {
      type: Boolean,
      required: true,
      default: false,
    },

    message: {
      type: String,
      required: false,
      default: null,
    },

    title: {
      type: String,
      required: false,
      default: null,
    },

    autoHide: {
      type: Boolean,
      required: false,
      default: true,
    },
  },

  data() {
    return {
      isOpen: false,
    }
  },

  computed: {
    icon() {
      if (this.type == "success") {
        return "mdi-check-circle"
      } else if (this.type == "error") {
        return "mdi-alert-circle"
      } else if (this.type == "secondary") {
        return "mdi-message-alert"
      }
      return "mdi-information"
    },
    typeClass() {
      return `${this.type}--text`
    },
    timeout() {
      return this.autoHide ? 5000 : 0
    },
  },

  watch: {
    value: function () {
      this.isOpen = this.value
    },
    isOpen: function () {
      this.$emit("input", this.isOpen)
    },
  },
}
</script>
