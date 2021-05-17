<template>
  <div>
    <page-header>
      <template slot="left">
        <breadcrumb :items="breadcrumbs" />
      </template>
    </page-header>
    <v-row class="pa-10">
      <v-col cols="6">
        <data-sources-list></data-sources-list>
      </v-col>
      <v-col cols="6">
        <destinations-list></destinations-list>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import DataSourcesList from "./DataSourcesList"
import DestinationsList from "./DestinationsList"
import PageHeader from "@/components/PageHeader"
import Breadcrumb from "@/components/common/Breadcrumb"

export default {
  name: "connections",

  components: {
    DataSourcesList,
    DestinationsList,
    PageHeader,
    Breadcrumb,
  },

  data() {
    return {
      breadcrumbs: [
        {
          text: "Connections",
          icon: "mdi-connection",
        },
      ],
    }
  },
}
</script>
