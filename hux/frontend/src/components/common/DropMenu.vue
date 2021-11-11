<template>
  <div class="text-center">
    <v-menu :close-on-content-click="false" :nudge-width="menuWidth" offset-y>
      <template #activator="{ on }">
        <div v-on="on">
          <slot name="menuActivator"></slot>
        </div>
      </template>
      <slot name="menuHeader"></slot>
      <slot name="menuBody"></slot>
      <slot name="menuFooter"></slot>
    </v-menu>
  </div>
</template>

<script>
export default {
  name: "DropMenu",
  props: {
    menuWidth: {
      type: Number,
      required: false,
      default: 200,
    },
  },
}
</script>
