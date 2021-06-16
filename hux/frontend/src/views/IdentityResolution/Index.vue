<template>
  <div>
    <v-progress-linear :active="loading" :indeterminate="loading" />
    Identity Resolution
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex"

export default {
  name: "IdentityResolution",

  data() {
    return {
      loading: false,
    }
  },

  computed: {
    ...mapGetters({
      overview: "identity/overview",
    }),
  },

  methods: {
    ...mapActions({
      getOverview: "identity/getOverview",
    }),
  },

  async mounted() {
    this.loading = true
    await this.getOverview()
    this.loading = false
  },
}
</script>

<style lang="scss" scoped></style>
