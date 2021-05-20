<template>
  <v-breadcrumbs :items="items" class="pl-0">
    <template v-slot:item="{ item }">
      <v-breadcrumbs-item
        :href="item.href"
        :disabled="item.disabled"
        class="font-weight-light"
      >
        <div v-if="item.icon" class="d-flex">
          <Icon :type="item.icon" :size="24" color="neroBlack" />
        </div>
        <span class="neroBlack--text pl-2">{{ item.text }}</span>
      </v-breadcrumbs-item>
    </template>
    <template v-slot:divider>
      <v-icon size="21" color="primary">mdi-chevron-right</v-icon>
    </template>
  </v-breadcrumbs>
</template>

<script>
import Icon from "@/components/common/Icon"
export default {
  name: "breadcrumb",
  components: {
    svgAsComponent,
  },

  components: { Icon },

  props: {
    items: {
      type: Array,
      required: true,
      default: () => [],
    },
  },
}
</script>
