<template>
  <drawer
    v-model="localToggle"
    class="audience-detail-drawer-wrapper"
    :width="drawerWidth"
    :loading="loading"
    @onClose="closeDrawer()"
  >
    <template #header-left>
      <h3 class="text-h2">{{ audienceData && audienceData.name }}</h3>
    </template>

    <template #default>
      <div class="pa-6">
        <overview :insights="audienceData" />
        <v-divider class="my-4 mb-6 mr-4"></v-divider>
        <attribute-rules
          ref="filters"
          class="rules"
          :rules="audience.attributeRules"
          :read-mode="true"
          @loadingOverAllSize="(data) => updateLoad(data)"
        />
      </div>
    </template>

    <template #footer-left> </template>
  </drawer>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import Drawer from "@/components/common/Drawer.vue"
import Overview from "@/views/Engagements/Configuration/Overview/Overview.vue"
import AttributeRules from "@/views/SegmentPlayground/AttributeRules.vue"

export default {
  name: "AudienceDetailDrawer",
  /**
   * Dependency injection for component
   */
  components: {
    Drawer,
    Overview,
    AttributeRules,
  },

  props: {
    value: {
      type: Object,
      required: true,
    },
    /**
     * A toggle indicating whether the drawer is open or not.
     */
    toggle: {
      type: Boolean,
      required: false,
      default: false,
    },
  },

  data() {
    return {
      loading: false,
      localToggle: false,
      drawerWidth: 950,
      audienceData: null,
      overviewLoading: false,
      overviewLoadingStamp: new Date(),
      audience: {
        attributeRules: [],
      },
    }
  },

  computed: {
    ...mapGetters({
      getAudience: "audiences/audience",
    }),
  },
  /**
   * Keeping an eye on toggle indicating whether the drawer is open or not.
   */
  watch: {
    toggle(value) {
      this.localToggle = value
    },
    localToggle(value) {
      this.$emit("onToggle", value)
    },
  },

  methods: {
    ...mapActions({
      getAudienceById: "audiences/getAudienceById",
    }),
    reset() {
      this.attributeRules = []
    },
    updateLoad(data) {
      this.overviewLoading = data
      if (!data) this.overviewLoadingStamp = new Date()
    },
    /**
     * Method to close the drawer & reset drawer boolean flag.
     */
    closeDrawer() {
      this.localToggle = false
      this.reset()
    },
    /**
     * Method to close the drawer by clicking on cancel button.
     */
    onCancelAndBack() {
      this.$emit("onCancelAndBack")
      this.reset()
    },
    /**
     * Method to fecth audience details by ID.
     *
     * @param {string} id audience id
     */
    async fetchAudienceDetails(id) {
      try {
        this.loading = true
        await this.getAudienceById(id)
        const _getAudience = this.getAudience(id)
        this.audienceData = JSON.parse(JSON.stringify(_getAudience))
        this.mapAudienceData(this.audienceData)
        this.loading = false
      } finally {
        this.loading = false
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
      if (this.isClone) {
        this.audience.name = ""
      }
      this.$nextTick(function () {
        this.$refs.filters.getOverallSize()
      })
    },
  },
}
</script>
<style lang="scss" scoped>
.audience-detail-drawer-wrapper {
  .rules {
    .condition-card {
    }
  }
  ::v-deep .add-wrap {
    .new-attribute {
      visibility: hidden !important;
    }
  }
}
</style>
