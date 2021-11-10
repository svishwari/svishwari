<template>
  <div class="playground-wrap">
    <page-header :header-height-changes="'py-3'" :header-height="110">
      <template slot="left">
        <div class="mt-n3">
          <breadcrumb :items="breadcrumbItems" />
        </div>
        <div class="text-subtitle-1 font-weight-regular mt-1">
          Get immediate insights by segmenting your customer list based on
          attributes that you want to explore.
        </div>
      </template>
      <template #right> </template>
    </page-header>
    <div>
      <v-row>
        <v-col class="col-8 attribute-div"> </v-col>
        <v-col class="col-4 overview-div"></v-col>
      </v-row>
    </div>
  </div>
</template>

<script>
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"

export default {
  name: "SegmentPlayground",
  components: {
    PageHeader,
    Breadcrumb,
  },
  data() {
    return {
      breadcrumbItems: [
        {
          text: "Segment Playground",
          disabled: true,
          icon: "playground",
        },
      ],
    }
  },
}
</script>
<style lang="scss" scoped>
.playground-wrap {
  background: white;
  .attribute-div {
    border-right: 1px solid var(--v-black-lighten3);
    height: 100vh;
  }
}
</style>
