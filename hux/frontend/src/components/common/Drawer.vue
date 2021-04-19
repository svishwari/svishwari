<template>
  <v-navigation-drawer
    v-model="drawer"
    :right="toRight"
    :width="width"
    @input="onChange"
    temporary
    floating
    app
  >
  </v-navigation-drawer>
</template>

<script>
export default {
  name: "drawer",

  data() {
    return {
      drawer: this.isOpen,
    }
  },

  props: {
    toRight: {
      type: Boolean,
      required: false,
      default: true,
    },

    isOpen: {
      type: Boolean,
      required: false,
      default: false,
    },

    width: {
      type: String,
      required: false,
      default: "600",
    },
  },
  methods: {
    onChange(x) {
      console.log(x)
    },
    toggleDrawer() {
      this.drawer = !this.drawer
    }
  },
}
</script>
