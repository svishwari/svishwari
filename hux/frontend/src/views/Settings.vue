<template>
  <div class="client-config-wrap">
    <page-header class="py-5" :header-height="110">
      <template #left>
        <div>
          <breadcrumb :items="breadcrumbItems" />
        </div>
        <div class="text-subtitle-1 font-weight-regular pl-1">
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
  </div>
</template>

<script>
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"
import TipsMenu from "@/views/SegmentPlayground/TipsMenu.vue"
export default {
  name: "DataSources",
  components: { PageHeader, Breadcrumb, TipsMenu },
  data() {
    return {
      breadcrumbItems: [
        {
          text: "Client’s configuration",
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
}
</script>

<style lang="scss" scoped></style>
