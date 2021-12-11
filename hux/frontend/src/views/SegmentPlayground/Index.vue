<template>
  <div>
    <page-header :header-height="isEdit ? '70' : '110'" help-icon>
      <template slot="left">
        <div>
          <breadcrumb :items="breadcrumbItems" />
        </div>
        <div v-if="!isEdit" class="text-subtitle-1 font-weight-regular mt-1">
          Get immediate insights by segmenting your customer list based on
          attributes that you want to explore.
        </div>
      </template>
      <template #right>
        <tips-menu
          :panel-list-items="panelListItems"
          header="Segment Playground user guide"
          :right-position="!isEdit ? '0rem' : '5rem'"
        />
        <v-menu
          v-if="isEdit"
          v-model="openMenu"
          class="menu-wrapper"
          bottom
          offset-y
        >
          <template #activator="{ on, attrs }">
            <v-icon
              v-bind="attrs"
              class="mr-2 more-action"
              color="primary"
              :class="{ 'd-inline-block': openMenu }"
              v-on="on"
            >
              mdi-dots-vertical
            </v-icon>
          </template>
          <v-list class="list-wrapper">
            <v-list-item-group>
              <v-list-item key="delete-action" @click="initiateDelete()">
                Delete audience
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-menu>
      </template>
    </page-header>
    <v-progress-linear :active="loading" :indeterminate="loading" />
    <page
      max-width="100%"
      padding="0 24px"
      class="white segmentation playground-wrap"
    >
      <v-row class="ma-0 segment-wrap">
        <v-col class="col-8 pl-0 pr-6 py-6 attributes">
          <div v-if="isEdit" class="edit-wrap">
            <div class="text-body-1">
              You are currently editing
              <span class="text-body-2">{{ audience.originalName }}</span
              >. Please update and/or add any attributes.
            </div>
            <text-field
              v-model="audience.name"
              placeholder-text="What is the name for this audience ?"
              height="40"
              label-text="Audience name"
              background-color="white"
              required
              class="
                mt-1
                text-caption
                black--text
                text--darken-4
                pt-2
                input-placeholder
              "
              data-e2e="audience-name"
              help-text="This audience will appear in the delivered destinations as the provided Audience name. In Facebook it will appear as the provided Audience name with the timestamp of delivery."
              icon="mdi-information-outline"
            />
          </div>
          <attribute-rules
            ref="filters"
            :rules="audience.attributeRules"
            @loadingOverAllSize="(data) => updateLoad(data)"
          />
        </v-col>
        <v-col class="col-4 overviews pl-6 pr-0 py-6">
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
        <template #left>
          <hux-button
            v-if="isEdit"
            size="large"
            variant="white"
            height="40"
            is-tile
            class="btn-border box-shadow-none"
          >
            Cancel &#38; return
          </hux-button>
        </template>
        <template #right>
          <hux-button
            size="large"
            height="40"
            is-tile
            variant="primary base"
            @click="handleAction()"
          >
            {{ buttonText }}
          </hux-button>
        </template>
      </hux-footer>
    </page>
    <confirm-modal
      v-model="confirmModal"
      :icon="confirmData.icon"
      :icon-color="confirmData.iconColor"
      :icon-size="confirmData.iconSize"
      :type="confirmData.type"
      :title="confirmData.title"
      :sub-title="confirmData.subTitle"
      :right-btn-text="confirmData.rightButtonText"
      :left-btn-text="confirmData.leftButtonText"
      data-e2e="audience-confirmation"
      @onCancel="confirmModal = !confirmModal"
      @onConfirm="confirmRemoval()"
    >
      <template #body>
        <div
          v-if="isEdit"
          class="
            black--text
            text--darken-4 text-subtitle-1
            pt-6
            font-weight-regular
          "
        >
          Are you sure you want to delete this audience&#63;
        </div>
        <div
          v-if="isEdit"
          class="black--text text--darken-4 text-subtitle-1 font-weight-regular"
        >
          By deleting this audience you will not be able to recover it and it
          may impact any associated engagements.
        </div>
        <div v-if="!isEdit" class="d-flex align-center justify-center px-7">
          <text-field
            v-model="audience.name"
            placeholder-text="Audience name"
            height="40"
            background-color="white"
            required
            class="
              mt-5
              text-caption
              black--text
              text--darken-4
              input-placeholder
              w-100
            "
            data-e2e="audience-name"
          />
        </div>
      </template>
    </confirm-modal>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex"
import Breadcrumb from "../../components/common/Breadcrumb"
import HuxButton from "../../components/common/huxButton"
import HuxFooter from "../../components/common/HuxFooter"
import TextField from "@/components/common/TextField"
import Page from "../../components/Page.vue"
import PageHeader from "../../components/PageHeader.vue"
import AttributeRules from "./AttributeRules.vue"
import TipsMenu from "./TipsMenu.vue"
import Geography from "./Geography.vue"
import Overview from "./Overview.vue"
import ConfirmModal from "../../components/common/ConfirmModal.vue"

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
    TextField,
    ConfirmModal,
  },
  data() {
    return {
      breadcrumbs: [
        {
          text: "Segment Playground",
          icon: "playground",
        },
      ],
      openMenu: false,
      editBreadcrumbs: [
        {
          text: "Audiences",
          disabled: false,
          href: this.$router.resolve({ name: "Audiences" }).href,
          icon: "audiences",
        },
      ],
      audience: {
        attributeRules: [],
      },
      isEdit: false,
      loading: false,
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
      confirmData: {
        icon: "audience_icon",
        type: "primary",
        iconColor: "black",
        iconSize: "35",
        title: "",
        subTitle: "Save this segment as a new audience",
        rightButtonText: "Save",
        leftButtonText: "Cancel",
      },
      confirmModal: false,
    }
  },
  computed: {
    ...mapGetters({
      overview: "customers/overview",
      getAudience: "audiences/audience",
    }),
    breadcrumbItems() {
      const items = !this.isEdit ? this.breadcrumbs : this.editBreadcrumbs
      if (this.isEdit && this.audience && this.audience.name) {
        if (items.length === 1) {
          items.push({
            text: this.audience.name,
            disabled: false,
          })
        } else {
          items[1].text = this.audience.name
        }
      }
      return items
    },
    buttonText() {
      return this.isEdit
        ? "Apply changes & save"
        : "Save this segment as an audience"
    },
  },
  beforeRouteLeave(to, from, next) {
    if (this.flagForModal == false) {
      this.showConfirmModal = true
      this.navigateTo = to
    } else {
      next()
    }
  },
  async mounted() {
    this.loading = true
    this.loadingOverview = true
    try {
      if (this.$route.name === "AudienceUpdate") {
        this.isEdit = true
        await this.getOverview()
        this.audienceId = this.$route.params.id
        await this.getAudienceById(this.audienceId)
        const data = this.getAudience(this.audienceId)
        this.mapAudienceData(data)
      } else {
        await this.getOverview()
      }
    } finally {
      this.loadingOverview = false
      this.loading = false
    }
  },
  methods: {
    ...mapActions({
      getOverview: "customers/getOverview",
      saveAudience: "audiences/add",
      updateAudience: "audiences/update",
      getAudienceById: "audiences/getAudienceById",
      deleteAudience: "audiences/remove",
    }),
    updateLoad(data) {
      this.overviewLoading = data
      if (!data) this.overviewLoadingStamp = new Date()
    },
    async handleAction() {
      if (this.isEdit) {
        await this.updateAudience({
          id: this.audience.id,
          payload: this.preparePayload(),
        })
        this.$router.go(-1)
      } else {
        this.confirmModal = true
      }
    },
    preparePayload() {
      const filtersArray = []
      for (
        let ruleIndex = 0;
        ruleIndex < this.audience.attributeRules.length;
        ruleIndex++
      ) {
        var filter = {
          section_aggregator: this.audience.attributeRules[ruleIndex].operand
            ? "ALL"
            : "ANY",
          section_filters: [],
        }
        for (
          let conditionIndex = 0;
          conditionIndex <
          this.audience.attributeRules[ruleIndex].conditions.length;
          conditionIndex++
        ) {
          filter.section_filters.push({
            field:
              this.audience.attributeRules[ruleIndex].conditions[conditionIndex]
                .attribute.key,
            type: this.audience.attributeRules[ruleIndex].conditions[
              conditionIndex
            ].operator
              ? this.audience.attributeRules[ruleIndex].conditions[
                  conditionIndex
                ].operator.key
              : "range",
            value: this.audience.attributeRules[ruleIndex].conditions[
              conditionIndex
            ].operator
              ? this.audience.attributeRules[ruleIndex].conditions[
                  conditionIndex
                ].text
              : this.audience.attributeRules[ruleIndex].conditions[
                  conditionIndex
                ].range,
          })
        }
        filtersArray.push(filter)
      }
      return {
        filters: filtersArray,
        name: this.audience.name,
      }
    },
    initiateDelete() {
      this.confirmSubtitle = this.audience.originalName
      this.confirmData = {
        icon: "sad-face",
        type: "error",
        iconSize: 42,
        title: "You are about to delete",
        subTitle: this.audience.originalName,
        rightButtonText: "Yes, delete it",
        leftButtonText: "Nevermind!",
      }
      this.confirmModal = true
    },
    async confirmRemoval() {
      if (this.isEdit) {
        await this.deleteAudience({ id: this.audience.id })
        this.confirmModal = false
        this.$router.push({
          name: "Audiences",
        })
      } else {
        let response = await this.saveAudience(this.preparePayload())
        this.confirmModal = false
        this.$router.push({
          name: "AudienceInsight",
          params: { id: response.id },
        })
      }
    },
    getAttributeOption(attribute_key, options) {
      for (let opt of options) {
        if (opt.menu && opt.menu.length > 0) {
          return opt.menu.filter((menuOpt) => menuOpt.key === attribute_key)[0]
        } else if (opt.key === attribute_key) {
          return opt
        }
      }
    },
    mapAudienceData(data) {
      const _audienceObject = JSON.parse(JSON.stringify(data))
      _audienceObject.originalName = _audienceObject.name
      // Mapping the filters of audience.
      const attributeOptions = this.$refs.filters.attributeOptions()
      _audienceObject.attributeRules = _audienceObject.filters.map(
        (filter) => ({
          id: "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(
            /[xy]/g,
            function (c) {
              var r = (Math.random() * 16) | 0,
                v = c == "x" ? r : (r & 0x3) | 0x8
              return v.toString(16)
            }
          ),
          operand: filter.section_aggregator === "ALL",
          conditions: filter.section_filters.map((cond) => ({
            id: Math.floor(Math.random() * 1024).toString(16),
            attribute: cond.field,
            operator: cond.type === "range" ? "" : cond.type,
            text: cond.type !== "range" ? cond.value : "",
            range: cond.type === "range" ? cond.value : [],
          })),
        })
      )
      _audienceObject.attributeRules.forEach((section) => {
        section.conditions.forEach((cond) => {
          cond.attribute = this.getAttributeOption(
            cond.attribute,
            attributeOptions
          )
          let _operators = this.$refs.filters.operatorOptions(cond)
          cond.operator =
            cond.operator !== "range"
              ? _operators.filter((opt) => opt.key === cond.operator)[0]
              : cond.operator
          this.$refs.filters.triggerSizing(cond, false)
        })
      })
      this.$set(this, "audience", _audienceObject)
      this.$nextTick(function () {
        this.$refs.filters.getOverallSize()
      })
    },
  },
}
</script>

<style lang="scss" scoped>
.playground-wrap {
  .segment-wrap {
    .attributes {
      flex: 0 0 66.63934426%;
      width: 66.63934426%;
    }
    .overviews {
      flex: 0 0 33.360655737704918%;
      width: 33.360655737704918%;
      @extend .border-start;
      border-color: var(--v-black-lighten3);
    }
  }
}
</style>
