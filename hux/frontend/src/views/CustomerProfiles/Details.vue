<template>
  <div>
    <v-progress-linear :active="loading" :indeterminate="loading" />
    Customer Profile Details

    <!-- <pre>{{ customer(id) }}</pre> -->
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex"

export default {
  name: "CustomerDetails",

  data() {
    return {
      loading: false,
    }
  },

  computed: {
    ...mapGetters({
      customer: "customers/single",
    }),

    id() {
      return this.$route.params.id
    },
  },

  methods: {
    ...mapActions({
      getCustomer: "customers/get",
    }),
  },

  async mounted() {
    this.loading = true
    await this.getCustomer(this.id)
    this.loading = false
  },
}
</script>

<style lang="scss" scoped></style>
