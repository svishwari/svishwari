<template>
  <v-breadcrumbs :items="items" class="pl-0">
    <template v-slot:item="{ item }">
      <v-breadcrumbs-item
        :href="item.href"
        :disabled="item.disabled"
        class="font-weight-light"
      >
        <v-icon color="neroBlack" size="21" class="pr-1" v-if="item.icon">
          {{ item.icon }}
        </v-icon>
        <svg-as-component class="mr-2" :src="`assets/${item.iconPath}`" />
        <span class="neroBlack--text">{{ item.text }}</span>
      </v-breadcrumbs-item>
    </template>
    <template v-slot:divider>
      <v-icon size="21" color="primary">mdi-chevron-right</v-icon>
    </template>
  </v-breadcrumbs>
</template>

<script>
import svgAsComponent from "./SVG"
export default {
  name: "breadcrumb",
  components: {
    svgAsComponent,
  },

  props: {
    items: {
      type: Array,
      required: true,
      default: () => [],
    },
  },
}
</script>
