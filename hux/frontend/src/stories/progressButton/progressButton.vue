<template>
  <div class="progress-button d-flex flex-wrap">
    <hux-button v-if="variant == 'validate'" @click="validate()">
      Validate
    </hux-button>
    <hux-button
      v-else-if="variant == 'success'"
      icon="Checkmark"
      background-color="success darken-1"
      :icon-size="16"
      class="success-button"
    >
      Success
    </hux-button>
    <hux-button v-else-if="variant == 'progressing'" class="processing-button">
      Progressing...
    </hux-button>
    <hux-button
      v-else
      icon="Error &amp; Warning"
      :icon-size="16"
      background-color="error lighten-1"
      class="error-button"
    >
      Error!
    </hux-button>
  </div>
</template>

<script>
import HuxButton from "../huxButton/huxButton2.vue"
export default {
  name: "ProgressButton",
  components: {
    HuxButton,
  },
  props: {
    variant: {
      type: String,
      required: true,
    },
  },
  watch: {
    loader() {
      if (this.enableLoading) {
        const l = this.loader
        this[l] = !this[l]
        setTimeout(() => (this[l] = false), 3000)
        this.loader = null
      }
    },
  },
  methods: {
    onClick: function () {
      this.$emit("click")
      this.loader = "loading"
    },
  },
}
</script>
<style lang="scss" scoped>
@mixin background-icon-color($value) {
  background-color: var($value) !important;
  ::v-deep .v-btn__content {
    svg {
      background-color: var($value) !important;
      fill: var(--v-white-base) !important;
    }
  }
}
.progress-button {
  .success-button {
    @include background-icon-color(--v-success-darken1);
  }
  .error-button {
    @include background-icon-color(--v-error-lighten1);
  }
}
</style>
