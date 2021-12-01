<template>
  <page-header class="background-border" :header-height-changes="'py-3'">
    <template #left>
      <breadcrumb :items="breadcrumbItems" />
    </template>
    <template #right>
      <div class="d-flex align-center">
        <icon
          type="refresh-2"
          :size="18"
          class="cursor-pointer mr-7"
          color="black-darken4"
          @click.native="$emit('onRefresh')"
        />
        <icon
          type="pencil"
          :size="18"
          class="cursor-pointer mr-7"
          color="black-darken4"
          @click.native="
            $router.push({
              name: 'AudienceUpdate',
              params: { id: audienceId },
            })
          "
        />
        <icon
          type="dots-vertical"
          :size="18"
          class="cursor-pointer mr-7"
          color="black-darken4"
        />
      </div>
    </template>
  </page-header>
</template>

<script>
import PageHeader from "@/components/PageHeader.vue"
import Breadcrumb from "@/components/common/Breadcrumb.vue"
import Icon from "@/components/common/Icon.vue"

export default {
  name: "DashboardHeader",
  components: { PageHeader, Breadcrumb, Icon },
  props: {
    breadcrumbItems: {
      type: Array,
      required: false,
      default: () => [],
    },
  },
  data() {
    return {}
  },
  computed: {
    audienceId() {
      return this.$route.params.id
    },
  },
}
</script>

<style lang="scss" scoped></style>
