<template>
  <page class="white">
    <template #header>
      <v-progress-linear :active="loading" :indeterminate="loading" />
    </template>

    <h2 class="text-h2 mb-4">Add an engagement</h2>

    <p class="mb-10">
      Tell us a little bit about this engagement. What are its goals? When are
      you planning to run it? Who are you targeting?
    </p>

    <engagement-overview v-model="data" />

    <v-divider class="divider my-4 mb-8"></v-divider>

    <engagement-form v-model="data" />
  </page>
</template>

<script>
import Page from "@/components/Page.vue"
import EngagementOverview from "./Overview.vue"
import EngagementForm from "./Form.vue"

export default {
  name: "Configuration",

  components: {
    Page,
    EngagementOverview,
    EngagementForm,
  },

  data() {
    return {
      data: {
        name: "",
        description: "",
        audiences: {},
        delivery_schedule: 0,
      },

      loading: false,
    }
  },
}
</script>
