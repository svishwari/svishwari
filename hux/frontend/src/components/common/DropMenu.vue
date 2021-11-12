<template>
  <div class="text-center">
    <v-menu
      v-model="menu"
      :close-on-content-click="false"
      :min-width="200"
      :max-width="365"
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
  },
  data() {
    return {
      menu: false,
    }
  },
}
</script>
