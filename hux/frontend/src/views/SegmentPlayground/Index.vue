<template>
  <div class="playground-outermost-wrap">
    <page-header :header-height="isEdit ? '70' : '110'" help-icon>
      <template slot="left">
        <div>
          <breadcrumb :items="breadcrumbItems" />
        </div>
        <div v-if="!isEdit" class="text-subtitle-1 font-weight-regular mt-1">
          Get immediate insights by segmenting your consumer list based on
          attributes that you want to explore.
        </div>
      </template>
      <template #right>
        <tips-menu
          v-if="hasOverview"
          :panel-list-items="panelListItems"
          header="Segment Playground user guide"
          :right-position="!isEdit ? '0rem' : '5rem'"
          max-height="calc(100vh - 363px)"
        />
        <v-menu
          v-if="isEdit"
          v-model="openMenu"
          class="menu-wrapper zi-100"
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
              <v-list-item
                key="delete-action"
                class="body-1 delete-tooltip"
                @click="initiateDelete()"
              >
                Delete audience
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-menu>
      </template>
    </page-header>
    <v-progress-linear :active="loading" :indeterminate="loading" />
    <page
      v-if="!loading && hasOverview && !errorState"
      max-width="100%"
      class="
        white
        segmentation
        playground-wrap
        flex-grow-1 flex-shrink-1
        mw-100
        content-section
      "
    >
      <v-row class="ma-0 segment-wrap">
        <v-col
          class="col-8 pl-0 pr-6 attributes"
          :class="isEdit ? 'py-7' : 'py-6'"
        >
          <div v-if="isEdit" class="edit-wrap">
            <div class="body-1">
              You are currently editing the current audience, "{{
                audience.originalName
              }}". Please update and/or add any attributes.
            </div>
            <text-field
              v-model="audience.name"
              placeholder-text="What is the name for this audience ?"
              height="40"
              label-text="Edit name"
              background-color="white"
              required
              class="
                mt-2
                text-caption
                black--text
                text--darken-4
                input-placeholder
                pt-3
                audience-form
              "
              data-e2e="edit-audience-name"
            />

            <div class="black--text text--darken-4 text-h5 text-label mb-1">
              Industry
            </div>
            <div class="tag-section">
              <hux-drop-down-search
                v-model="selectedTags"
                :min-width="360"
                :min-selection="0"
                :items="mapIndustryTags"
                :is-search-enabled="false"
              >
                <template #activator>
                  <div class="mb-8" :min-width="360">
                    <v-select
                      dense
                      readonly
                      :placeholder="
                        selectedTags.length > 0
                          ? `Client industry (${selectedTags.length})`
                          : 'Select client industry'
                      "
                      class="dropdown-select-placeholder"
                      outlined
                      background-color="white"
                      append-icon="mdi-chevron-down"
                    />
                  </div>
                </template>
              </hux-drop-down-search>
            </div>
          </div>
          <attribute-rules
            ref="filters"
            :rules="audience.attributeRules"
            @loadingOverAllSize="(data) => updateLoad(data)"
            @attribute-options="(data) => attributeOptions(data)"
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
            v-if="isEdit || isClone"
            size="large"
            variant="white"
            height="40"
            is-tile
            class="btn-border box-shadow-none cancel-color"
            @click.native="$router.go(-1)"
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
            data-e2e="action-audience"
            @click="handleAction()"
          >
            {{ buttonText }}
          </hux-button>
        </template>
      </hux-footer>
    </page>
    <v-row v-else-if="!loading && !errorState" class="ma-0 empty-row">
      <empty-page type="no-customer-data" :size="50">
        <template #title>
          <div class="h2">No consumer data to show</div>
        </template>
        <template #subtitle>
          <div class="body-2 mt-3">
            Please be patient while our team connects your data.
          </div>
        </template>
      </empty-page>
    </v-row>
    <div v-else-if="!loading && errorState" class="error-wrap">
      <error
        icon-type="error-on-screens"
        :icon-size="50"
        title="Segment playground is currently unavailable"
        subtitle="Our team is working hard to fix it. Please be patient and try again soon!"
      >
      </error>
    </div>
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
      @onCancel="
        audience.name = ''
        confirmModal = !confirmModal
      "
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
        <div
          v-if="!isEdit"
          class="d-flex flex-column align-center justify-center px-7 mt-5"
        >
          <div class="add-modal" style="width: 496px">
            <div
              class="
                black--text
                text--darken-4 text-h5 text-left text-label
                mb-n1
              "
            >
              Audience name
            </div>
            <text-field
              v-model="audience.name"
              placeholder-text="Enter audience name"
              height="40"
              background-color="white"
              required
              class="
                text-caption
                black--text
                text--darken-4
                input-placeholder
                w-100
              "
              data-e2e="audience-name"
            />
          </div>
          <div
            class="tag-section add-modal mt-n2"
            style="width: 496px; height: 40px"
          >
            <div
              class="black--text text--darken-4 text-left text-h5 text-label"
            >
              Industry
            </div>
            <hux-drop-down-search
              v-model="selectedTags"
              class="wow"
              :min-width="360"
              :min-selection="0"
              :items="mapIndustryTags"
              :is-search-enabled="false"
            >
              <template #activator>
                <div :min-width="360" style="height: 44px">
                  <v-select
                    dense
                    readonly
                    :placeholder="
                      selectedTags.length > 0
                        ? `Client industry (${selectedTags.length})`
                        : 'Select client industry'
                    "
                    class="dropdown-select-placeholder"
                    outlined
                    background-color="white"
                    append-icon="mdi-chevron-down"
                  />
                </div>
              </template>
            </hux-drop-down-search>
          </div>
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
import TipsMenu from "@/components/common/TipsMenu.vue"
import Geography from "./Geography.vue"
import Overview from "./Overview.vue"
import ConfirmModal from "../../components/common/ConfirmModal.vue"
import HuxDropDownSearch from "@/components/common/HuxDropDownSearch"
import EmptyPage from "@/components/common/EmptyPage.vue"
import Error from "@/components/common/screens/Error"
import { v4 as uuidv4 } from "uuid"
import { formatText, getIndustryTags } from "@/utils.js"

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
    HuxDropDownSearch,
    ConfirmModal,
    EmptyPage,
    Error,
  },
  data() {
    return {
      breadcrumbs: [
        {
          text: "Segment Playground",
          icon: "playground",
        },
      ],
      industry_tags: getIndustryTags(),
      selectedTags: [],
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
      isClone: false,
      loading: false,
      overviewLoading: false,
      overviewLoadingStamp: new Date(),
      panelListItems: [
        {
          id: 1,
          title: "What is Segment Playground?",
          text: "<b>Segment Playground </b>allows you to explore and segment your full consumer list and enables you to see real time insights.",
          textPart: "",
        },
        {
          id: 2,
          title: "What is segmenting?",
          text: "<b>Segmenting</b> is the process of filtering your full consumer list based on model scores or specific characteristics.",
          textPart: "",
        },
        {
          id: 3,
          title: "How do I use Segment Playground?",
          text: "First click <b>+ Attribute,</b> then select what characteristic you would like to segment your consumer list. As you add attributes, the insights on the right hand will update accordingly.",
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
          text: "<b>All</b> means that a consumer must match every attribute within the section in order to be included in the segment.",
          textPart:
            "<b>Any</b> means that a consumer must match at least 1 of the attributes within the section in order to be included in the segment.",
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
      errorState: false,
      audienceId: "",
    }
  },
  computed: {
    ...mapGetters({
      overview: "customers/overview",
      getAudience: "audiences/audience",
    }),
    hasOverview() {
      return this.overview && Object.keys(this.overview).length > 0
    },
    mapIndustryTags() {
      return this.industry_tags.map((element) =>
        this.formatTagsOptions(element)
      )
    },
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
        : "Save segmentation as an audience"
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
      switch (this.$route.name) {
        case "AudienceUpdate":
          await this.getAudienceData(true, this.$route.params.id)
          break

        case "CloneAudience":
          await this.getAudienceData(false, this.$route.params.id)
          break

        default:
          await this.getOverview()
      }
    } catch (error) {
      this.errorState = true
    } finally {
      this.loadingOverview = false
      this.loading = false
    }
    // if (this.audienceId !== "") {
    //   const data = this.getAudience(this.audienceId)
    //   this.mapAudienceData(data)
    // }
  },
  methods: {
    ...mapActions({
      getOverview: "customers/getOverview",
      saveAudience: "audiences/add",
      updateAudience: "audiences/update",
      getAudienceById: "audiences/getAudienceById",
      deleteAudience: "audiences/remove",
    }),
    async getAudienceData(isEdit, audienceId) {
      this.isEdit = isEdit
      this.isClone = !isEdit
      this.audienceId = audienceId
      await this.getOverview()
      await this.getAudienceById(audienceId)
      this.mapAudienceTags()
    },
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
        tags: {
          industry:
            this.selectedTags.length > 0
              ? this.selectedTags.map((item) => item?.name.toLowerCase())
              : [],
        },
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

    attributeOptions(data) {
      this.$refs.filters = data
      this.mapAudienceData(this.getAudience(this.audienceId))
    },

    mapAudienceTags() {
      let audienceData = JSON.parse(
        JSON.stringify(this.getAudience(this.audienceId))
      )
      let tagsData = audienceData.tags?.industry
      if (tagsData.length > 0) {
        tagsData.forEach((item) =>
          this.selectedTags.push(this.formatTagsOptions(item))
        )
      }
    },

    formatTagsOptions(item) {
      return {
        name: formatText(item),
      }
    },

    mapAudienceData(data) {
      const _audienceObject = JSON.parse(JSON.stringify(data))
      _audienceObject.originalName = _audienceObject.name
      // Mapping the filters of audience.
      const attributeOptions = this.$refs?.filters.attributeOptions()
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
            id: uuidv4(),
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
          let _operators = this.$refs?.filters.operatorOptions(cond)
          cond.operator =
            cond.operator !== "range"
              ? _operators.filter((opt) => opt.key === cond.operator)[0]
              : cond.operator
          this.$refs?.filters.triggerSizing(cond, false)
        })
      })
      this.$set(this, "audience", _audienceObject)
      if (this.isClone) {
        this.audience.name = ""
      }
      this.$nextTick(function () {
        this.$refs?.filters.getOverallSize()
      })
    },
    formatText: formatText,
  },
}
</script>

<style lang="scss" scoped>
.dropdown-select-placeholder {
  ::v-deep .v-input__control {
    .v-input__slot {
      fieldset {
        border-color: var(--v-black-lighten3);
      }
      input::placeholder {
        color: var(--v-black-base);
      }
    }
    .v-text-field__details {
      display: none;
    }
  }
}
.playground-outermost-wrap {
  height: calc(100vh - 150px) !important;
  .playground-wrap {
    ::v-deep .container {
      padding: 0px 24px !important;
    }
    .segment-wrap {
      .attributes {
        max-height: calc(100vh - 260px) !important;
        overflow-y: auto;
        flex: 0 0 66.64%;
        width: 66.64%;
      }
      .overviews {
        @extend .attributes;
        flex: 0 0 33.36%;
        width: 33.36%;
        @extend .border-start;
        border-color: var(--v-black-lighten3);
      }
    }
  }
  ::v-deep {
    .error-row {
      padding-top: 105px !important;
    }
    .empty-row {
      padding-top: 150px !important;
    }
    .error-wrap {
      padding-right: 60px;
    }
  }

  .audience-form {
    height: 86px;
    width: 360px;
  }

  .delete-tooltip {
    width: 191px;
    height: 32px;
    margin: -5px 0px -5px 0px;
  }

  .cancel-color {
    color: var(--v-primary-base);
  }

  .menuable__content__active {
    z-index: 100 !important;
  }

  ::v-deep .confirm-modal-body {
    .add-modal {
      width: 496px !important;
    }
  }

  .tag-section {
    max-width: 360px !important;
  }
}

::-webkit-scrollbar {
  width: 5px;
}
::-webkit-scrollbar-track {
  box-shadow: inset 0 0 5px var(--v-white-base);
  border-radius: 10px;
}
::-webkit-scrollbar-thumb {
  background: var(--v-black-lighten3);
  border-radius: 5px;
}
::-webkit-scrollbar-thumb:hover {
  background: var(--v-black-lighten3);
}
.content-section {
  overflow-y: hidden !important;
  overflow-x: hidden !important;
  .container {
    height: calc(100vh - 260px);
  }
}
.zi-100 {
  z-index: 100;
}
</style>
