<template>
  <div class="connections-wrap grey lighten-5 pt-10 pr-7 pb-7 pl-7">
    <v-row>
      <v-col cols="6" class="d-flex align-end">
        <v-icon> mdi-cloud-download-outline </v-icon>
        <span class="font-weight-light ml-2 mt-1">Data Sources</span>
        <v-icon class="ml-2 add-icon" color="primary"> mdi-plus-circle </v-icon>
      </v-col>

      <v-col cols="6" class="align-end">
        <v-icon> mdi-map-marker-circle </v-icon>
        <span class="font-weight-light ml-2 mt-1">Destinations</span>
        <v-icon class="ml-2 add-icon" color="primary"> mdi-plus-circle </v-icon>
        <span class="font-weight-light ml-2 mt-1 float-right">
          View Destinations Details
          <v-icon class="mr-2" color="primary"> mdi-chevron-right </v-icon>
        </span>
      </v-col>

      <v-col cols="6 pt-0">
        <EmptyDataSource />
      </v-col>

      <v-col cols="6 pt-0">
        <DestinationListCard v-for="item in destinationLists" :key="item.title">
          <template v-slot:logo>
            <v-img
              class="elevation-6"
              alt=""
              :src="getImgUrl(item)"
            ></v-img>
          </template>
          <template v-slot:title>
            {{ item.title }}
          </template>
        </DestinationListCard>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import DestinationListCard from "@/components/DestinationListCard"
import EmptyDataSource from "@/components/EmptyDataSource"

export default {
  name: "connections",
  components: { DestinationListCard, EmptyDataSource },
  data() {
    return {
      destinationLists: [
        { logoUrl: "../assets/images/adobe-icon.png", title: "Adobe Experience" },
        { logoUrl: "../assets/images/adobe-icon.png", title: "Facebook" },
        { logoUrl: "../assets/images/adobe-icon.png", title: "Google" },
        { logoUrl: "../assets/images/adobe-icon.png", title: "Twilio" },
        { logoUrl: "../assets/images/adobe-icon.png", title: "Amazon" },
      ],
    }
  },
  methods: {
    getImgUrl(item) {
      return item.logoUrl;
    },
  },
}
</script>

<style lang="scss" scoped>
.connections-wrap {
  .add-icon {
    cursor: pointer;
  }
}
</style>
