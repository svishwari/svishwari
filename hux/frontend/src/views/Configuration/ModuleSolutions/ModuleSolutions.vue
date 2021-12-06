<template>
  <div class="module-solutions-wrapper">
    <hux-empty
      class="empty-module-solutions"
      icon-type="settings"
      :icon-size="50"
      title="No modules to show"
      subtitle="Modules & solutions are being activated. Please check back in 2 hours. Thank you!"
    >
    </hux-empty>
  </div>
</template>

<script>
import HuxEmpty from "@/components/common/screens/Empty"

export default {
  name: "ModuleSolutions",
  components: { HuxEmpty },
  data() {
    return {}
  },
  computed: {},
}
</script>

<style lang="scss" scoped>
.module-solutions-wrapper {
  .empty-module-solutions {
    ::v-deep .text-center {
      width: 470px !important;
      .text-body-2 {
        line-height: 22px !important;
      }
    }
  }
}
</style>
