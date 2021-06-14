<template>
  <div>
    <v-progress-linear :active="loading" :indeterminate="loading" />
    Customer Profiles
    <!--
    <pre>{{ overview }}</pre>
    <pre>{{ customers }}</pre>
    -->
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex"

export default {
  name: "CustomerProfiles",

  data() {
    return {
      loading: false,
    }
  },

  computed: {
    ...mapGetters({
      customers: "customers/list",
      overview: "customers/overview",
    }),
  },

  methods: {
    ...mapActions({
      getCustomers: "customers/getAll",
      getOverview: "customers/getOverview",
    }),
  },

  async mounted() {
    this.loading = true
    await this.getOverview()
    await this.getCustomers()
    this.loading = false
  },
}
</script>

<style lang="scss" scoped></style>
