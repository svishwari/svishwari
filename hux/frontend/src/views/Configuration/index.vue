<template>
  <page max-width="100%" class="config-wrapper">
    <div slot="header">
      <page-header header-height="110">
        <template slot="left">
          <breadcrumb :items="breadcrumbItems" />
          <div class="text-subtitle-1 font-weight-regular mt-1">
            Organize and set up your project’s assets, modules, and team.
          </div>
        </template>
        <template #right>
          <tips-menu
            :panel-list-items="panelListItems"
            header="Configuration user guide"
          />
        </template>
      </page-header>
      <v-progress-linear :active="loading" :indeterminate="loading" />
    </div>
    <div v-if="!loading" class="config-content">
      <v-row v-if="false" class="">
        <v-col>
          <!-- UI to show when configuration is activated -->
          <config-tabs />
        </v-col>
      </v-row>
      <hux-empty
        v-else-if="!isConfigActivated"
        class="config-activating"
        icon-type="settings"
        :icon-size="50"
        title="Nothing to show"
        subtitle="Configuration is currently being activated. Please check back later. Thank you!"
      >
      </hux-empty>
      <error
        v-else
        icon-type="error-on-screens"
        :icon-size="50"
        title="Client settings is currently unavailable"
        subtitle="Our team is working hard to fix it. Please be patient and try again soon!"
        class="my-8"
      >
      </error>
    </div>
  </page>
</template>

<script>
import { mapGetters } from "vuex"

import Breadcrumb from "@/components/common/Breadcrumb"
import ConfigTabs from "./tabs"
import Error from "@/components/common/screens/Error"
import HuxEmpty from "@/components/common/screens/Empty"
import PageHeader from "@/components/PageHeader"
import Page from "@/components/Page"
import TipsMenu from "@/views/SegmentPlayground/TipsMenu.vue"

export default {
  name: "Configuration",
  components: { Breadcrumb, ConfigTabs, Error, HuxEmpty, PageHeader, Page, TipsMenu },
  data() {
    return {
      loading: false,
      breadcrumbItems: [
        {
          text: "Client’s configuration",
          disabled: true,
          icon: null,
        },
      ],
      panelListItems: [
        {
          id: 1,
          title: "What is a module?",
          text: "A module is a core capability of Hux. This screen showcases what capabilties have been enabled for this client as well as what capabilities they are missing out on.",
          textPart:
            "When activated the module appears as a section in the left side navigation with its related assets. ",
        },
        {
          id: 2,
          title: "What are business solutions?",
          text: "Our business solutions are end-to-end solutions that leverage one or more modules to target specific business objectives and meet the needs of our clients.",
          textPart:
            "When activated, a busines solution can provide you with additional dashboards, supplement current dashboards or enable additional features in the Hux platform.",
        },
        {
          id: 3,
          title: "Team member access level",
          text: "On the <b>Team member</b> tab you will see a list of individuals who have access to this client and what they have access to do.<br/><br/><b>Admin</b> access grants the ability to select who has access to view PII data and have the ability to remove and add different items (such as destinations and audiences) across Hux.",
          textPart:
            "<b>Edit</b> access allows the same removal and addition functionality as an admin BUT they do not have access to designate who can and cannot view PII data.<br/><br/><b>View-only</b> access does not have any addition and removal access across Hux.",
        },
        {
          id: 4,
          title: "Controlling who has PII access",
          text: "Only admins have the ability to designate who does and does not have access to PII data. If you are an individual who does not have PII data then you will not be able to download or view that data.",
          textPart:
            "If you wish to view PII data, reach out to an an individual who has admin access.",
        },
      ],
    }
  },
  computed: {
    ...mapGetters({}),

    isConfigActivated() {
      return true
    },
  },
}
</script>

<style lang="scss" scoped>
.config-wrapper {
  ::v-deep .container {
    padding-top: 0px;
  }
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
