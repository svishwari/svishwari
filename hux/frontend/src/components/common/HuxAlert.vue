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
    <span v-if="type === 'Pending'" class="d-flex">
      <status
        :status="type"
        :show-label="false"
        :height="20"
        :weight="20"
        class="icon-position"
      />
      <span class="success--text">
        <span class="px-1 font-weight-bold text-h5">
          {{ title || defaultTitle }}
        </span>
        <span class="text-h5">{{ message }}</span>
      </span>
    </span>
    <span v-else>
      <div class="d-flex align-center" :class="typeClass">
        <v-icon outlined :color="type" :size="18" class="icon-position">
          {{ icon }}
        </v-icon>
        <span class="px-3 font-weight-bold text-h5">
          {{ title || defaultTitle }}
        </span>
        <span class="text-h5">{{ message }}</span>
      </div>
    </span>
  </v-snackbar>
</template>

<script>
import Status from "./Status.vue"
export default {
  name: "HuxAlert",
  components: {
    Status,
  },
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
    defaultTitle() {
      const defaultTitles = {
        success: "YAY!",
        error: "OH NO!",
      }
      return defaultTitles[this.type]
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

<style lang="scss" scoped>
.text-style {
  font-family: Open Sans;
  font-style: normal;
  font-weight: normal;
  font-size: 14px !important;
  line-height: 22px;
}
.icon-position {
  margin-top: 1.5px;
}
</style>
