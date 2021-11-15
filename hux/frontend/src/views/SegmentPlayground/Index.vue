<template>
  <div>
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
      <template #right> <tips-menu /> </template>
    </page-header>
    <v-progress-linear :active="loading" :indeterminate="loading" />
    <page
      max-width="100%"
      padding="0 24px"
      class="white segmentation playground-wrap"
    >
      <v-row class="ma-0">
        <v-col class="col-8 pl-0 pr-6 py-6 attributes">
          <attribute-rules
            ref="filters"
            :rules="attributeRules"
            @loadingOverAllSize="(data) => updateLoad(data)"
          />
        </v-col>
        <v-col class="col-4 overviews px-6 py-6">
          <overview
            :data="overview"
            :loading="overviewLoading"
            :last-refreshed="overviewLoadingStamp"
            class="mb-3"
          />
          <geography :data="overview" :loading="overviewLoading" />
        </v-col>
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
    </page>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import Breadcrumb from "../../components/common/Breadcrumb.vue"
import HuxButton from "../../components/common/huxButton.vue"
import HuxFooter from "../../components/common/HuxFooter.vue"
import Page from "../../components/Page.vue"
import PageHeader from "../../components/PageHeader.vue"
import AttributeRules from "./AttributeRules.vue"
import TipsMenu from "./TipsMenu.vue"
import Geography from "./Geography.vue"
import Overview from "./Overview.vue"

export default {
  name: "SegmentPlayground",
  components: {
    Page,
    PageHeader,
    Breadcrumb,
    HuxFooter,
    HuxButton,
    AttributeRules,
    Overview,
    Geography,
    TipsMenu,
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
      attributeRules: [],
      overviewLoading: false,
      overviewLoadingStamp: new Date(),
    }
  },
  computed: {
    ...mapGetters({
      overview: "customers/overview",
    }),
  },
  async mounted() {
    this.loadingOverview = true
    await this.getOverview()
    this.loadingOverview = false
  },
  methods: {
    ...mapActions({
      getOverview: "customers/getOverview",
    }),
    updateLoad(data) {
      this.overviewLoading = data
      if (!data) this.overviewLoadingStamp = new Date()
    },
  },
}
</script>

<style lang="scss" scoped>
.playground-wrap {
  .attributes {
    flex: 0 0 66.639344262295082%;
    width: 66.639344262295082%;
  }
  .overviews {
    flex: 0 0 33.360655737704918%;
    width: 33.360655737704918%;
    @extend .border-start;
    border-color: var(--v-black-lighten3);
  }
}
</style>
