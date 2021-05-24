<template>
  <PageHeader>
      <template slot="left">
        <Breadcrumb :items="breadcrumbItems" />
      </template>
      <template slot="right">
      </template>
  </PageHeader>
</template>

<script>
import PageHeader from "../../components/PageHeader.vue"
export default {
  name: "engagements",
  components: {
    PageHeader,
  },
  data() {
      return {
          breadcrumbItems: [
        {
          text: "Engagements",
          disabled: true,
          href: this.$route.path,
          icon: "audiences",
        },
        {
          text: "Engagements",
          disabled: true,
        },
      ],
      }
  },
}
</script>

<style lang="sass" scoped></style>
