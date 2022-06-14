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
      <div class="d-flex align-center insight-height">
        <icon
          type="refresh-2"
          :size="18"
          class="cursor-pointer mr-7"
          color="black-darken4"
          @click.native="$emit('onRefresh')"
        />
        <tooltip position-bottom>
          <template #label-content>
            <span
              v-if="
                audienceData.is_lookalike === true &&
                getAccess('audience', 'edit_lookalike')
              "
              @click="openLookalikeEditModal()"
            >
              <icon
                type="pencil"
                :size="18"
                class="cursor-pointer mr-7"
                color="black-darken4"
              />
            </span>
            <span
              v-else-if="getAccess('audience', 'update_one')"
              @click="initiateEdit()"
            >
              <icon
                type="pencil"
                :size="18"
                class="cursor-pointer mr-7"
                color="black-darken4"
              />
            </span>
          </template>
          <template #hover-content>
            <div class="text--body-1">
              <span v-if="audienceData.is_lookalike === true">
                Edit {{ audienceData.name }}
              </span>
              <span v-else>Edit Audience</span>
            </div>
          </template>
        </tooltip>
        <v-menu v-model="openMenu" class="menu-wrapper" bottom offset-y>
          <template #activator="{ on, attrs }">
            <v-icon
              v-bind="attrs"
              class="cursor-pointer mr-7"
              color="black base"
              :class="{ 'd-inline-block': openMenu }"
              v-on="on"
            >
              mdi-dots-vertical
            </v-icon>
          </template>
          <v-list class="text-body-1 pa-0">
            <v-list-item-group>
              <v-list-item @click="favoriteAudience()">
                {{ audienceData.favorite ? "Unfavorite" : "Favorite" }}
              </v-list-item>
              <v-list-item
                v-if="getAccess('audience', 'delete_one')"
                @click="initiateDelete()"
              >
                Delete audience
              </v-list-item>
              <v-list-item
                v-if="
                  !audienceData.is_lookalike &&
                  getAccess('audience', 'download')
                "
                @click="openDownloadDrawer()"
              >
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
import { getAccess } from "../../../utils"

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
    openLookalikeEditModal() {
      this.$emit("openLookalikeEditModal")
    },
    initiateEdit() {
      this.$emit("editAudience", this.audienceData)
    },
    getAccess: getAccess,
  },
}
</script>

<style lang="scss" scoped>
.v-list-item {
  min-height: 32px;
}
.insight-height {
  height: 30px !important;
}
::v-deep .mdi-dots-vertical::before {
  height: 28px !important;
}
</style>
