<template>
  <page-header class="background-border" :header-height-changes="'py-3'">
    <template #left>
      <span class="d-flex flex-row">
        <breadcrumb :items="breadcrumbItems" />
        <icon
          v-if="audienceData.favorite"
          class="ml-3 mt-2"
          type="fav_filled"
          :size="24"
        />
      </span>
    </template>
    <template #right>
      <div class="d-flex align-center">
        <icon
          type="refresh-2"
          :size="18"
          class="cursor-pointer mr-7"
          color="black-darken4"
          @click.native="$emit('onRefresh')"
        />
        <tooltip position-bottom>
          <template #label-content>
            <icon
              type="pencil"
              :size="18"
              class="cursor-pointer mr-7"
              color="black-darken4"
              @click.native="
                $router.push({
                  name: 'AudienceUpdate',
                  params: { id: audienceId },
                })
              "
            />
          </template>
          <template #hover-content>
            <div class="text--body-1 pb-2">Click to edit this audience</div>
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
              <v-list-item @click="favoriteAudience()"> Favorite </v-list-item>
              <v-list-item @click="initiateDelete()">
                Delete audience
              </v-list-item>
              <v-list-item @click="openDownloadDrawer()">
                Download as
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
    audienceData: {
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
    audienceId() {
      return this.$route.params.id
    },
  },
  methods: {
    initiateDelete() {
      this.$emit("removeAudience", this.audienceData)
    },
    favoriteAudience() {
      this.$emit("favoriteAudience", this.audienceData)
    },
    openDownloadDrawer() {
      this.$emit("openDownloadDrawer")
    },
  },
}
</script>

<style lang="scss" scoped></style>