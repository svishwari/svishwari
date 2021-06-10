<template>
  <Drawer
    class="add-audience-drawer-wrapper"
    v-model="localToggle"
    :width="drawerWidth"
    :disable-transition="isOpening"
    expandable
    @iconToggle="changeOverviewListItems"
  >
    <template #header-left>
      <h3 class="text-h3">Create a new audience</h3>
    </template>

    <template #default>
      <v-progress-linear :active="loading" :indeterminate="loading" />
      <div class="pa-6">
        <h6 class="pb-6 text-h6 neroBlack--text">
          Build a target audience from the data you own.
        </h6>
        <v-form ref="newAudienceRef" v-model="newAudienceValidity">
          <TextField
            labelText="Audience name"
            placeholder="Name"
            class="audience-name-field"
            v-model="newAudience.name"
            :rules="newAudienceRules"
            required
          />
        </v-form>
        <div class="pt-4 pb-2 neroBlack--text text-caption">
          Audience overview
        </div>
        <div class="d-flex align-center pb-4">
          <MetricCard
            class="list-item ma-0 mr-3"
            v-for="(item, i) in overviewListItems"
            :key="i"
            :title="item.title"
            :subtitle="item.subtitle"
          />
        </div>
        <hr class="mb-4" />
        <div class="pt-1 pr-0">
          <attribute-rules :rules="attributeRules"></attribute-rules>
        </div>
      </div>
    </template>

    <template #footer-left>
      <v-btn tile color="white" @click="closeDrawer()">
        <span class="primary--text">Cancel &amp; back</span>
      </v-btn>
      <v-btn
        :disabled="!newAudienceValidity"
        tile
        color="primary"
        @click="add()"
      >
        Create &amp; add
      </v-btn>
    </template>
  </Drawer>
</template>

<script>
import { mapActions } from "vuex"
import Drawer from "@/components/common/Drawer.vue"
import TextField from "@/components/common/TextField"
import MetricCard from "@/components/common/MetricCard"
import AttributeRules from "@/views/Audiences/AttributeRules.vue"

export default {
  name: "AddAudienceDrawer",

  components: {
    Drawer,
    TextField,
    MetricCard,
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
      drawerWidth: 640,
      newAudienceRules: [(v) => !!v || "Audience name is required"],
      newAudienceValidity: false,
      // TODO: need to make API call and update the cards/sizes of metric cards
      newAudience: {
        name: "",
      },
      overviewListItems: [
        { title: "Target size", subtitle: "34.2M" },
        { title: "Countries", subtitle: "2" },
        { title: "US States", subtitle: "52" },
        { title: "Cities", subtitle: "-" },
        { title: "Age", subtitle: "-" },
        { title: "Women", subtitle: "52%" },
      ],
      attributeRules: [],
    }
  },

  watch: {
    toggle(value) {
      this.localToggle = value
    },

    localToggle(value) {
      this.$emit("onToggle", value)
    },
  },

  computed: {
    isOpening() {
      return this.localToggle
    },
  },

  methods: {
    ...mapActions({
      addAudience: "audiences/add",
    }),

    closeDrawer() {
      this.localToggle = false
      this.reset()
    },

    changeOverviewListItems(expanded) {
      if (expanded) {
        this.overviewListItems.push(
          { title: "Men", subtitle: "46%" },
          { title: "Other", subtitle: "2%" }
        )
      } else {
        this.overviewListItems.pop()
        this.overviewListItems.pop()
      }
    },

    reset() {
      this.$refs.newAudienceRef.reset()
      this.attributeRules = []
    },

    async add() {
      try {
        this.loading = true
        const filtersArray = []
        for (
          let ruleIndex = 0;
          ruleIndex < this.attributeRules.length;
          ruleIndex++
        ) {
          var filter = {
            section_aggregator: this.attributeRules[ruleIndex].operand
              ? "ALL"
              : "ANY",
            section_filters: [],
          }
          for (
            let conditionIndex = 0;
            conditionIndex < this.attributeRules[ruleIndex].conditions.length;
            conditionIndex++
          ) {
            filter.section_filters.push({
              field: this.attributeRules[ruleIndex].conditions[conditionIndex]
                .attribute,
              type: this.attributeRules[ruleIndex].conditions[conditionIndex]
                .operator,
              value: this.attributeRules[ruleIndex].conditions[conditionIndex]
                .text,
            })
          }
          filtersArray.push(filter)
        }

        // TODO: HUS-246 need to integrate size and other data on rules addition
        const data = {
          name: this.newAudience.name,
          filters: filtersArray,
        }

        const newAudience = await this.addAudience(data)

        this.$set(this.value, newAudience.id, {
          id: newAudience.id,
          name: newAudience.name,
          size: newAudience.size,
        })

        this.closeDrawer()
      } catch (error) {
        console.error(error)
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
<style lang="scss" scoped>
.add-audience-drawer-wrapper {
  .audience-name-field {
    max-width: 360px;
  }
  hr {
    border-style: solid;
    border-color: var(--v-zircon-base);
  }
}
</style>
