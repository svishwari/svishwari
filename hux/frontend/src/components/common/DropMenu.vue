<template>
  <div class="text-center">
    <v-menu
      v-model="menu"
      :close-on-content-click="false"
      :close-on-click="closeOnClick"
      :content-class="contentClass"
      :min-width="minWidth"
      :max-width="maxWidth"
      offset-y
    >
      <template #activator="{ on }">
        <div v-on="on">
          <slot name="menuActivator" :activatorVal="menu"></slot>
        </div>
      </template>
      <div>
        <slot name="menuHeader"></slot>
        <slot name="menuBody"></slot>
        <slot name="menuFooter"></slot>
      </div>
    </v-menu>
  </div>
</template>

<script>
export default {
  name: "DropMenu",
  props: {
    minWidth: {
      type: Number,
      required: false,
      default: 200,
    },
    maxWidth: {
      type: Number,
      required: false,
      default: 400,
    },
    closeOnClick: {
      type: Boolean,
      required: false,
      default: false,
    },
    contentClass: {
      type: String,
      required: false,
    },
  },
  data() {
    return {
      menu: false,
    }
  },
}
</script>
<style scoped>
::v-deep.v-menu__content {
  z-index: 0 !important;
}
</style>
