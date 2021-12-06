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
      <template #right>
        <tips-menu
          :panel-list-items="panelListItems"
          header="Segment Playground user guide"
        />
      </template>
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
      panelListItems: [
        {
          id: 1,
          title: "What is Segment Playground?",
          text: "<b>Segment Playground </b>allows you to explore and segment your full customer list and enables you to see real time insights.",
          textPart: "",
        },
        {
          id: 2,
          title: "What is segmenting?",
          text: "<b>Segmenting</b> is the process of filtering your full customer list based on model scores or specific characteristics.",
          textPart: "",
        },
        {
          id: 3,
          title: "How do I use Segment Playground?",
          text: "First click <b>+ Attribute,</b> then select what characteristic you would like to segment your customer list. As you add attributes, the insights on the right hand will update accordingly.",
          textPart:
            "If you want to save this segment as an audience, click on <b >Save this segment as an audience.</b> By doing so you will not only save this segment as an audience, but you will also have the ability to deliver this audience to a 3rd party platform when you are ready OR add it to an engagement.",
        },
        {
          id: 4,
          title: "+ Attribute vs + Sections",
          text: "Adding an attibute will add another line rule under an <b>All</b> vs <b>Any</b> section rule.",
          textPart:
            "Adding another section enables you to create a new <b>All</b> vs <b>Any</b> section rule in addition to your previous section(s) where you can add new attributes.",
        },
        {
          id: 5,
          title: "“All” vs “Any”",
          text: "<b>All</b> means that a customer must match every attribute within the section in order to be included in the segment.",
          textPart:
            "<b>Any</b> means that a customer must match at least 1 of the attributes within the section in order to be included in the segment.",
        },
      ],
    }
  },
  computed: {
    ...mapGetters({
      overview: "customers/overview",
    }),
  },
  async mounted() {
    this.loadingOverview = true
    try {
      await this.getOverview()
    } finally {
      this.loadingOverview = false
    }
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
