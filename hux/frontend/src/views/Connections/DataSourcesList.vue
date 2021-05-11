<template>
  <div>
    <div class="d-flex align-end mb-4">
      <v-icon> mdi-cloud-download-outline </v-icon>
      <h5 class="font-weight-light text-h5 ml-2 mt-1">Data Sources</h5>
      <v-icon class="ml-2 add-icon" color="primary" disabled>
        mdi-plus-circle
      </v-icon>
    </div>

    <EmptyStateData>
      <template v-slot:icon> mdi-alert-circle-outline </template>
      <template v-slot:title> Oops! There’s nothing here yet </template>
      <template v-slot:subtitle>
        To create a connection, a data source must be imported!
        <br />
        Begin by selecting the plus button above.
      </template>
    </EmptyStateData>
  </div>
</template>

<script>
import EmptyStateData from "@/components/common/EmptyStateData"

export default {
  name: "data-sources-list",

  components: { EmptyStateData },
}
</script>
