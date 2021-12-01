<template>
  <page max-width="100%">
    <div slot="header">
      <page-header header-height="110">
        <template slot="left">
          <breadcrumb :items="breadcrumbItems" />
          <div class="text-subtitle-1 font-weight-regular mt-1">
            Organize and set up your project’s assets, modules, and team.
          </div>
        </template>
      </page-header>
    </div>
  </page>
</template>

<script>
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
export default {
  name: "Configuration",
  components: { PageHeader, Breadcrumb },
  data() {
    return {
      breadcrumbItems: [
        {
          text: "Client’s configuration",
          disabled: true,
          icon: null,
        },
      ],
    }
  },
}
</script>

<style lang="scss" scoped></style>
