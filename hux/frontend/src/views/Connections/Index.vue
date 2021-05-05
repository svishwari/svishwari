<template>
  <div class="connections-wrap grey lighten-5">
    <PageHeader>
      <template slot="left">
        <Breadcrumb :items="breadcrumbItems" />
      </template>
    </PageHeader>
    <v-row class="pa-10">
      <v-col cols="6">
        <data-sources></data-sources>
      </v-col>
      <v-col cols="6">
        <destinations></destinations>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import DataSources from "./DataSources"
import Destinations from "./Destinations"
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"

export default {
  name: "connections",

  components: {
    DataSources,
    Destinations,
    PageHeader,
    Breadcrumb,
  },

  data() {
    return {
      breadcrumbItems: [
        {
          text: "Connections",
          disabled: false,
          href: this.$route.path,
          icon: "mdi-connection",
        },
      ],
    }
  },
}
</script>
