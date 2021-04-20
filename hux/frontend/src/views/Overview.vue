<template>
  <PageHeader
    :title="'Welcome back, ' + firstName + '!'"
    icon="mdi-bullhorn-outline"
  >
    <template slot="description">
      <div>
        Hux is here to help you make better, faster decisions to improve your
        Customer Experiences.
        <a>Learn More ></a>
      </div>
    </template>
  </PageHeader>
</template>

<script>
import PageHeader from "@/components/PageHeader"

export default {
  name: "overview",
  components: {
    PageHeader,
  },
  computed: {
    firstName() {
      return this.$store.getters.getFirstname
    },
  },
}
</script>

<style lang="scss" scoped></style>
