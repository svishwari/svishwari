<template>
  <v-card
    :class="{
      'border-image': borderImage,
    }"
    class="rhombus-card-wrapper"
    :style="style"
    shaped
    outlined
  >
    <v-card-text :class="`text-subtitle-2 text-style ${textColor}`">
      {{ value }}
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "RhombusNumber",
  props: {
    value: {
      type: Number,
      required: true,
    },
    color: {
      type: String,
      required: false,
      default: "primary",
    },
    variant: {
      type: String,
      required: false,
      default: "darken1",
    },
    textColor: {
      type: String,
      required: false,
      default: "black--text",
    },
    borderImage: {
      type: Boolean,
      required: false,
      default: false,
    },
    borderWidth: {
      type: Number,
      required: false,
    },
  },
  computed: {
    style() {
      return {
        "border-color": "var(--v-" + this.color + "-" + this.variant + ")",
        "border-width": this.borderWidth + "px",
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.rhombus-card-wrapper {
  transform: rotate(45deg);
  width: 30px;
  height: 30px;
  border-radius: 0 !important;
}
.text-style {
  // num style
  line-height: 18px;
  transform: translate(0%, 25%) rotate(-45deg);
  padding: 0px;
  display: block;
  text-align: center;
}

.border-image {
  border-image-source: linear-gradient(
    122deg,
    #e3e34d 2.41%,
    #0e7b7e 38.12%,
    #3a88b8 51.2%,
    #add1d6 98.98%
  );
  border-image-slice: 1;
}
</style>
