<template>
  <page max-width="100%"  class="config-wrapper">
    <div slot="header">
      <page-header header-height="110">
        <template slot="left">
          <breadcrumb :items="breadcrumbItems" />
          <div class="text-subtitle-1 font-weight-regular mt-1">
            Organize and set up your project’s assets, modules, and team.
          </div>
        </template>
      </page-header>
      <v-progress-linear :active="loading" :indeterminate="loading" />
    </div>
    <div class="config-content" v-if="!loading">
      <v-row v-if="false" class="ma-0 pa-2">
        <v-col>
          <!-- UI to show when configuration is activated -->
        </v-col>
      </v-row>
      <hux-empty
        v-if="isConfigActivated"
        class="config-activating"
        icon-type="settings"
        :icon-size="50"
        title="Nothing to show"
        subtitle="Configuration is currently being activated. Please check back later. Thank you!"
      >
      </hux-empty>
    </div>
  </page>
</template>

<script>
import { mapGetters } from "vuex"

import PageHeader from "@/components/PageHeader"
import Page from "@/components/Page"
import Breadcrumb from "@/components/common/Breadcrumb"
import HuxEmpty from "@/components/common/screens/Empty"

export default {
  name: "Configuration",
  components: { PageHeader, Page, Breadcrumb, HuxEmpty },
  data() {
    return {
      breadcrumbItems: [
        {
          text: "Client’s configuration",
          disabled: true,
          icon: null,
        },
      ],
      loading: false,
    }
  },
  computed: {
    ...mapGetters({ }),

    isConfigActivated() {
      return true
    },
  },
}
</script>

<style lang="scss" scoped>
.config-wrapper {
  .config-content {
    .config-activating {
     ::v-deep .text-center {
        width: 470px !important;
        .text-body-2 {
          line-height: 22px !important;
        }
      }
    }
  }
}
</style>
