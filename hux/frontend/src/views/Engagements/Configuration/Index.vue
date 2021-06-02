<template>
  <div>
    <v-progress-linear :active="loading" :indeterminate="loading" />

    <Page class="white">
      <h2 class="text-h2 mb-4">Add an engagement</h2>

      <p class="mb-10">
        Tell us a little bit about this engagement. What are its goals? When are
        you planning to run it? Who are you targeting?
      </p>

      <EngagementOverview />

      <v-divider class="divider my-4 mb-8"></v-divider>

      <EngagementForm v-model="data" />
    </Page>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
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
        delivery_schedule: "null",
      },

      loading: false,
    }
  },

  computed: {
    ...mapGetters({
      audiences: "audiences/list",
    }),
  },

  methods: {
    ...mapActions({
      getAudiences: "audiences/getAll",
    }),
  },

  async mounted() {
    this.loading = true
    await this.getAudiences()
    this.loading = false
  },
}
</script>
