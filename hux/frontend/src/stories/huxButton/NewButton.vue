<template>
  <v-btn :text="textOnly" class="px-6" :color="getClass(color)" :outlined="outlined" @click="onClick">
    <div class="button-content text-button">
      <icon v-if="icon" :type="icon" size="15" :color="iconColor" class="mr-2"/>
      <slot name="default" />
    </div>
  </v-btn>  
</template>

<script>
import Icon from "../icons/Icon2.vue"

export default {
  name: "NewButton",
  components: { Icon },
  props: {
    textOnly: {
      type: Boolean,
      required: false,
      default: false,
    },
    icon: {
      type: String,
      required: false,
      default: null,
    },
    color: {
      type: String,
      required: false,
      default: "secondary",
    },
    iconColor: {
      type: String,
      required: false,
      default: "primary",
    },
    outlined: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  methods: {
    onClick: function () {
      this.$emit("click")
    },
    getClass(color) {
      return `var(--v-${color})`
    },
  },
}
</script>

<style lang="scss" scoped>
.button-content {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
