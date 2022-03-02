<template>
  <page-header class="background-border" :header-height-changes="'py-3'">
    <template #left>
      <span class="d-flex flex-row">
        <breadcrumb :items="breadcrumbItems" />
        <icon
          v-if="engagementData.favorite"
          class="ml-3 mt-2"
          type="fav_filled"
          :size="24"
        />
      </span>
    </template>
    <template #right>
      <div class="d-flex align-center">
        <tooltip position-bottom>
          <template #label-content>
            <icon
              type="pencil"
              :size="18"
              class="cursor-pointer mr-7"
              color="black-darken4"
              @click.native="editEngagement()"
            />
          </template>
          <template #hover-content>
            <div class="text--body-1 pb-2">Click to edit this engagement</div>
          </template>
        </tooltip>
        <v-menu v-model="openMenu" class="menu-wrapper" bottom offset-y>
          <template #activator="{ on, attrs }">
            <v-icon
              v-bind="attrs"
              class="cursor-pointer mr-7"
              color="black-darken4"
              :class="{ 'd-inline-block': openMenu }"
              v-on="on"
            >
              mdi-dots-vertical
            </v-icon>
          </template>
          <v-list class="list-wrapper">
            <v-list-item-group>
              <v-list-item @click="favoriteAudience()">
                {{ engagementData.favorite ? "Unfavorite" : "Favorite" }}
              </v-list-item>
              <v-list-item @click="openDownloadDrawer()">
                <tooltip>
                  <template #label-content> Download KPIs as .csv </template>
                  <template #hover-content>
                    Download Email Marketing and Digital Advertising performance
                    metrics as CSVs.
                  </template>
                </tooltip>
              </v-list-item>
              <v-list-item
                :disabled="engagementData.status == 'Inactive'"
                @click="inactiveEngagement()"
              >
                Make inactive
              </v-list-item>
              <v-list-item @click="initiateDelete()">
                Delete engagement
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </v-menu>
      </div>
    </template>
  </page-header>
</template>

<script>
import PageHeader from "@/components/PageHeader.vue"
import Breadcrumb from "@/components/common/Breadcrumb.vue"
import Icon from "@/components/common/Icon.vue"
import Tooltip from "@/components/common/Tooltip.vue"

export default {
  name: "DashboardHeader",
  components: { PageHeader, Breadcrumb, Icon, Tooltip },
  props: {
    breadcrumbItems: {
      type: Array,
      required: false,
      default: () => [],
    },
    engagementData: {
      type: Object,
      required: false,
      default: () => {},
    },
  },
  data() {
    return {
      openMenu: false,
    }
  },
  computed: {
    engagementId() {
      return this.$route.params.id
    },
  },
  methods: {
    initiateDelete() {
      this.$emit("removeEngagement", this.engagementData)
    },
    favoriteAudience() {
      this.$emit("favoriteEngagement", this.engagementData)
    },
    openDownloadDrawer() {
      this.$emit("openDownloadDrawer")
    },
    inactiveEngagement() {
      this.$emit("inactiveEngagement", this.engagementData)
    },
    editLookalike() {
      this.$emit("editLookalike")
    },
    editEngagement() {
      this.$emit("editEngagement")
    },
  },
}
</script>

<style lang="scss" scoped></style>
