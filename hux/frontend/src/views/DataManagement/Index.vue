<template>
  <div class="datasource-wrap">
    <page-header :header-height-changes="'py-3'">
      <template slot="left">
        <breadcrumb :items="breadcrumbItems" />
      </template>
    </page-header>
  </div>
</template>

<script>
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
export default {
  name: "DataSources",
  components: { PageHeader, Breadcrumb },
  data() {
    return {
      breadcrumbItems: [
        {
          text: "Data Sources",
          disabled: true,
          icon: "datasource",
        },
      ],
    }
  },
}
</script>

<style lang="scss" scoped></style>
