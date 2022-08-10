<template>
  <div>
    <slot name="header" />
    <div
      class="container no-shadow"
      :style="{ 'max-width': maxWidth, padding: padding }"
    >
      <empty-page v-if="errorState" class="mt-n3" type="sad-face-2" :size="40">
        <template #title>
          <div class="text-h4 mt-4 error-text-color">Unavailable</div>
        </template>
        <template #subtitle>
          <div class="text-body-1 mt-4 error-text-color">
            Our team is working hard to fix it. <br />Please be patient and try
            again soon!
          </div>
        </template>
      </empty-page>
      <empty-page
        v-else-if="emptyState"
        type="trash_can"
        class="mt-n3"
        :size="40"
      >
        <template #title>
          <div class="text-h4 mt-4 empty-text-color">Welcome to the void</div>
        </template>
        <template #subtitle>
          <div class="text-body-1 mt-4 empty-text-color">
            You currently have no data.
          </div>
        </template>
      </empty-page>
      <slot />
    </div>
    <slot name="footer" />
  </div>
</template>

<script>
import EmptyPage from "@/components/common/EmptyPage.vue"

export default {
  name: "Page2",

  components: {
    EmptyPage,
  },

  props: {
    maxWidth: {
      type: String,
      required: false,
      default: "auto",
    },
    padding: {
      type: String,
      required: false,
      default: "auto",
    },
    emptyState: {
      type: Boolean,
      required: false,
      default: false,
    },
    errorState: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
}
</script>

<style lang="scss" scoped>
.container {
  max-width: 1220px;
  padding: 30px;
  height: calc(100vh - 180px);
  overflow-y: auto !important;
  overflow-x: hidden !important;
  box-shadow: -100px 0px 200px rgba(30, 30, 30, 0.03),
    -8px 0px 16px rgba(0, 85, 135, 0.15);
}
.empty-text-color {
  color: var(--v-black-lighten6) !important;
  font-weight: 400 !important;
}
.error-text-color {
  color: var(--v-black-base) !important;
  font-weight: 400 !important;
}
</style>
