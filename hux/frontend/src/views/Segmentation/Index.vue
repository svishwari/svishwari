<template>
  <page max-width="100%" padding="0 24px" class="white segmentation">
    <div slot="header">
      <page-header header-height="110" class="mt-n2" help-icon>
        <template slot="left">
          <div>
            <breadcrumb :items="breadcrumbs" />
          </div>
          <div class="text-subtitle-1 font-weight-regular mt-1">
            Get immediate insights by segmenting your customer list based on
            attributes that you want to explore.
          </div>
        </template>
      </page-header>
      <v-progress-linear :active="loading" :indeterminate="loading" />
    </div>
    <div v-if="!loading" class="playground-wrap">
      <v-row class="ma-0">
        <v-col class="col-8 attribute-div pl-0 pr-6 py-6">
          <attribute-rules :rules="[]" />
        </v-col>
        <v-col class="col-4 overview-div px-6 py-6"> Right Section </v-col>
      </v-row>
      <hux-footer
        v-if="!loading"
        slot="footer"
        data-e2e="footer"
        max-width="100%"
      >
        <template #right>
          <hux-button size="large" is-tile variant="primary base">
            Save this segment as an audience
          </hux-button>
        </template>
      </hux-footer>
    </div>
  </page>
</template>

<script>
import Breadcrumb from "../../components/common/Breadcrumb.vue"
import HuxButton from "../../components/common/huxButton.vue"
import HuxFooter from "../../components/common/HuxFooter.vue"
import Page from "../../components/Page.vue"
import PageHeader from "../../components/PageHeader.vue"
import AttributeRules from "../Audiences/AttributeRules.vue"
export default {
  name: "SegmentPlayground",
  components: {
    Page,
    PageHeader,
    Breadcrumb,
    HuxFooter,
    HuxButton,
    AttributeRules,
  },
  data() {
    return {
      breadcrumbs: [
        {
          text: "Segment Playground",
          icon: "playground",
        },
      ],
      loading: false,
    }
  },
}
</script>

<style lang="scss" scoped>
.segmentation {
  .container {
    height: 100%;
  }
  .playground-wrap {
    .attribute-div {
      @extend .border-end;
      border-color: var(--v-black-lighten3);
      height: 100vh;
    }
  }
}
</style>
