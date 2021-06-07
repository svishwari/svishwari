<template>
  <v-menu bottom offset-y open-on-hover>
    <template v-slot:activator="{ on }">
      <span v-on="on">
        <slot name="label-content"> sample</slot>
      </span>
    </template>
    <div class="px-4 py-2 white caption">
      <slot name="hover-content"></slot>
    </div>
  </v-menu>
</template>

<script>
export default {
  name: "Tooltip",
}
</script>
